import logging
from xml.etree import ElementTree as ET

from .namespaces import NS, TEI_NS, XML_ID, get_attribute

for ns, uri in NS.items():
    ET.register_namespace(ns, uri)


from typing import NamedTuple

from django.db import DatabaseError, transaction
from django.db.utils import IntegrityError
from xlsx.workbook import Workbook

from .importer import Importer
from .models import Chapter, Omen, Segment, Witness
from .reconstruction import Reconstruction
from .score import Score
from .util import clean_id, element2string

logger = logging.getLogger(__name__)


class OmenImporter:
    """
    Imports omen work book into the database, and updates the TEI
    """

    expected_columns = []
    root = None  # tei root

    @staticmethod
    def tei_root():
        """
        adds the TEI skeleton
        """
        root = ET.Element(get_attribute("TEI", TEI_NS))
        header = ET.SubElement(root, get_attribute("teiHeader", TEI_NS))
        fileDesc = ET.SubElement(header, get_attribute("fileDesc", TEI_NS))
        titleStmt = ET.SubElement(fileDesc, get_attribute("titleStmt", TEI_NS))
        title = ET.SubElement(titleStmt, get_attribute("title", TEI_NS))
        editor = ET.SubElement(titleStmt, get_attribute("editor", TEI_NS))
        respStmt = ET.SubElement(titleStmt, get_attribute("respStmt", TEI_NS))
        publicationStmt = ET.SubElement(
            fileDesc, get_attribute("publicationStmt", TEI_NS)
        )
        p = ET.SubElement(publicationStmt, "p")
        p.text = "Working copy, for internal use only"
        sourceDesc = ET.SubElement(header, get_attribute("sourceDesc", TEI_NS))
        ET.SubElement(sourceDesc, get_attribute("listWit", TEI_NS))
        text = ET.SubElement(root, get_attribute("text", TEI_NS))
        body = ET.SubElement(text, get_attribute("body", TEI_NS))
        ET.SubElement(body, "head")
        return root

    def __init__(self, file_to_import, upload):
        self.wb = Workbook(file_to_import)
        ## Extract chapter name from the first sheet name
        self.sheets = list(self.wb.get_sheets())
        self.upload = upload

    def save(self):
        """
        imports omens from workbook, updates TEI for chapter in the database
        """
        report = []
        chapter_name = self.sheets[0].name.split(".")[0]

        if not chapter_name.isnumeric():
            logger.error("Unexpected chapter name %s", chapter_name)
            report.append(f"Unexpected chapter name {chapter_name}")
            return report

        self.chapter, created = Chapter.objects.update_or_create(
            chapter_name=chapter_name
        )
        self.chapter.upload.add(self.upload)
        self.chapter.save()

        body, self.root = None, None
        # build TEI
        if self.chapter.tei and not self.root:
            # load existing TEI
            self.root = ET.fromstring(self.chapter.tei)
        elif not self.root:
            self.root = OmenImporter.tei_root()  # TEI skeleton

        body = self.root.find(".//tei:body", NS)
        title = self.root.find(".//tei:title", NS)
        title.text = f"Chapter {chapter_name}"

        for sheet in self.sheets:  # Read sheet by sheet
            # extract omen data
            try:
                with transaction.atomic():
                    omen_data = self.extract_omen_data(sheet)
            except ValueError as ve:
                report.append(str(ve))
                continue

            logger.debug("Found %s witnesses", omen_data.witnesses)
            for witness in omen_data.witnesses:
                witness_elem = self.root.find(
                    f'.//tei:witness[@xml:id="{witness.xml_id}"]',
                    NS,
                )

                if witness_elem is None:
                    self.root.find(".//tei:listWit", NS).append(witness.tei)

            # Check and remove if omen already exists in the TEI
            omen_div_old = body.find(f'.//tei:div[@n="{omen_data.label}"]', NS)
            if omen_div_old is not None:
                logger.warning("Overwriting existing omen div: %s", omen_data.label)
                body.remove(omen_div_old)

            # Add omen div to TEI
            body.append(omen_data.tei)
        self.chapter.tei = element2string(self.root)
        self.chapter.save()
        return report

    def extract_omen_data(self, sheet):
        """
        imports omen from sheet, returns TEI for the omen
        """

        def get_row_type(cell, prev_row_type=None):
            """
            Returns the row type based on the contents of cell_text
            Expects the cell in the first column but does not validate
            """
            if (
                not cell.is_empty
                and cell.column_name != "A"
                and prev_row_type == ROWTYPE.COMMENT
            ):
                return ROWTYPE.COMMENT

            if (
                not cell.full_text and prev_row_type == ROWTYPE.COMMENT
            ) or "comment" in cell.full_text.lower():
                return ROWTYPE.COMMENT

            if any(
                rdg
                for rdg in ("(en)", "(de)", "(dt)", "(trl)", "(trs)")
                if rdg in cell.full_text.lower()
            ):
                return ROWTYPE.RECONSTRUCTION

            if prev_row_type not in (ROWTYPE.RECONSTRUCTION, ROWTYPE.COMMENT):
                return ROWTYPE.SCORE

            raise ValueError(
                f"Row {cell.row_name} does not appear to be score, reading or commentary."
            )

        label = sheet.get_cell_at("A1").full_text
        xml_id = clean_id(label)
        witnesses = []

        try:
            omen, created = Omen.objects.update_or_create(
                xml_id=xml_id,
                omen_name=label,
                omen_num=sheet.name,
                chapter=self.chapter,
            )
            omen.save()
            if created:  # create records for protasis and apodosis
                protasis = Segment(
                    xml_id=xml_id + "_P", omen=omen, segment_type="PROTASIS"
                )
                protasis.save()
                apodosis = Segment(
                    xml_id=xml_id + "_A", omen=omen, segment_type="APODOSIS"
                )
                apodosis.save()
        except IntegrityError as ie:
            raise ValueError(f"Error creating omen {label} from {sheet.name}")

        score = Score(omen)
        recon = Reconstruction(omen)
        tei = ET.Element("tei:div", {"n": label, XML_ID: xml_id})

        row_type = None
        for row_num, row in sheet.get_rows():
            if sheet.is_empty_row(row) or row_num == "1":
                continue

            cells = list(sheet.get_cells(row))
            row_type = get_row_type(cells[0], row_type)

            # Score data
            if row_type == ROWTYPE.SCORE:

                # Get the witness for score line
                search_str = cells[0].full_text.split("+")[0]
                wit = Witness.objects.filter(
                    witness_id__icontains=search_str
                ) | Witness.objects.filter(museum_numbers__icontains=search_str)
                if not wit:
                    raise ValueError(
                        f'Unknown siglum - "{cells[0].full_text}". Unable to find any siglum starting with {search_str} for {label} in sheet {sheet.name}'
                    )

                if len(wit) != 1:
                    raise ValueError(
                        f'Ambiguous siglum - "{cells[0].full_text}". Found {len(wit)} matches.'
                    )

                witnesses.extend(wit)
                omen.witness.add(wit[0])

                # build score
                score.add_row(cells, wit[0])
            elif row_type == ROWTYPE.RECONSTRUCTION:
                recon.add_to_reconstruction(cells)

            # Readings
            ## Transliteration
            ## Transcription
            ## Translation
            # Philologocal commentary?

        # append score div to omen
        tei.append(score.tei)
        for recon_grp in recon.tei:
            tei.append(recon_grp)

        return OmenData(
            name=sheet.name, label=label, tei=tei, witnesses=list(set(witnesses))
        )

    def add_score_line(self):
        pass


class OmenData(NamedTuple):
    name: str
    label: str
    tei: any
    witnesses: any


class ROWTYPE:
    SCORE = "score"
    RECONSTRUCTION = "reconstruction"
    COMMENT = "comment"