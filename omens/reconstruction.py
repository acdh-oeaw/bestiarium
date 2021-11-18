"""
Represents the reconstructions of an omen
"""
import logging
import re
from collections import UserDict, defaultdict, namedtuple
from xml.etree import ElementTree as ET

from .lemma import Lemma
from .line import Line
from .models import Lemma as LemmaDB
from .models import Reconstruction as ReconstructionDB
from .models import Translation as TranslationDB
from .namespaces import XML_ID
from .util import clean_id

logger = logging.getLogger(__name__)


class ReconstructionId(namedtuple("ReconstructionId", "omen_prefix,label,witness")):
    @classmethod
    def idno_parts(cls, idno):
        m = re.match(
            r"^(?P<label>[a-zA-Z.\s]*)\s(?P<siglum>.*)\((?P<rdg_type>[a-zA-Z]*)\)$", idno
        )
        if not m:
            raise ValueError(f"Unrecognised row header; idno: {idno}", )
        return namedtuple("idno", "label,witness,rdg_type")(
            label=m.group("label"),
            witness=m.group("siglum")[1:-2],
            rdg_type=m.group("rdg_type"),
        )

    def __new__(cls, omen_prefix, idno):
        """
        Converts the first two column values for a score line into an immutable namedtuple,
        so it can be used as a key in the score dict
        """
        ip = ReconstructionId.idno_parts(idno)
        return super().__new__(
            cls, omen_prefix=omen_prefix, label=ip.label, witness=ip.witness
        )

    @property
    def xml_id(self):
        return (
            self.omen_prefix
            + "."  # noqa: W503
            + clean_id(self.label)  # noqa: W503
            + ("." + clean_id(self.witness) if self.witness else "")  # noqa: W503
        )


class ReconstructionLine(Line):
    """
    A list of lemmas that make a reconstruction line
    The information about Apodosis is obtained in one of these lines - and updated
    """

    reconstruction_type: str

    def __init__(self, row: list, omen):
        super().__init__(omen.xml_id)
        # Create a database record for this reconstruction

        self.reconstruction_id = ReconstructionId(
            omen_prefix=omen.xml_id,
            idno=row[0].full_text,
        )

        ip = ReconstructionId.idno_parts(idno=row[0].full_text)
        self.rdg_type = ip.rdg_type
        self.reference = row[1].full_text if row[1].column_name == "B" else ""
        recon_db = ReconstructionDB(
            xml_id=clean_id(self.xml_id),
            label=self.reconstruction_id.label,
            omen=omen,
        )
        recon_db.save()
        for cell in row:
            if not cell.full_text or cell.column_name in "AB":
                continue
            if self.rdg_type in ("trl", "trs"):
                self.data.append(Lemma(cell, omen=omen))
            else:
                self.data.append(cell)

        if self.rdg_type in ("trl", "trs"):
            self.connect_damaged_ends()
            for word in self.data:
                if word.apodosis:
                    try:

                        lemma_db = LemmaDB.objects.get(xml_id=word.xml_id)
                        lemma_db.set_segment_type_to_apodosis()

                    except Exception:
                        logging.warning("Could not change %s to APODOSIS", word.xml_id)
                else:
                    pass
        else:  # No W tag in translations - but it contains text, might contain anchor elements for breaks
            full_translation = ""
            for i, word in enumerate(self.data):
                full_translation += " " + word.full_text
                if i > 0:
                    logger.warning(
                        "Unexpected values in translation row; expecting only one cell, \n%s",
                        word,
                    )
            translation_parts = full_translation.split("–")
            if len(translation_parts) == 1:
                translation_parts.append("")
            elif len(translation_parts) > 2:
                raise ValueError(
                    f"More than one apodosis found in row {row[0].row_name}."
                )

            protasis_translation_db = TranslationDB(
                xml_id=self.xml_id + "_protasis",
                reconstruction=recon_db,
                segment=recon_db.omen.protasis,
                translation_txt=translation_parts[0],
                lang=self.rdg_type,
            )
            protasis_translation_db.save()

            apodosis_translation_db = TranslationDB(
                xml_id=self.xml_id + "_apodosis",
                reconstruction=recon_db,
                segment=recon_db.omen.apodosis,
                translation_txt=translation_parts[1],
                lang=self.rdg_type,
            )

            apodosis_translation_db.save()

    @property
    def xml_id(self):
        return f'{self.rdg_type}.{self.reconstruction_id.xml_id}{"_"+clean_id(self.reference) if self.reference else ""}'  # noqa: E501

    @property
    def tei(self):
        ab = ET.Element("ab", {XML_ID: self.xml_id})
        if self.reference:
            ab.attrib["source"] = self.reference

        if self.rdg_type == "trl":
            ab.attrib["type"] = "transliteration"
        elif self.rdg_type == "trs":
            ab.attrib["type"] = "transcription"
        else:
            ab.attrib["type"] = "translation"
            ab.attrib["lang"] = self.rdg_type

        if self.rdg_type in ("trl", "trs"):
            self.connect_damaged_ends()
            for word in self.data:
                w = word.reconstruction_tei(self.omen_prefix)
                ab.append(w)

        else:  # No W tag in translations - but it contains text, might contain anchor elements for breaks
            full_translation = ""
            for i, word in enumerate(self.data):
                full_translation += " " + word.full_text
                if i > 0:
                    logger.warning(
                        "Unexpected values in translation row; expecting only one cell, \n%s",
                        word,
                    )

            logger.debug("BEFORE removing breaks %s", full_translation)
            translation_parts = full_translation.split("–")
            if len(translation_parts) == 1:
                translation_parts.append("")
            elif len(translation_parts) > 2:
                translation_parts[1] = "-".join(translation_parts[1:])

            logger.debug("PARTS: %s", translation_parts)

            protasis_element = ET.Element(
                "div",
                {
                    XML_ID: self.xml_id + "_protasis",
                    "type": "protasis",
                },
            )

            protasis_element.text = translation_parts[0].strip()

            apodosis_element = ET.Element(
                "div", {XML_ID: self.xml_id + "_apodosis", "type": "apodosis"}
            )
            apodosis_element.text = translation_parts[1].strip()

            ab.append(apodosis_element)
            ab.append(protasis_element)

        return ab


class Reconstruction(UserDict):
    """
    Keys are ReconstructionIdb
    Comprises of reconstructions which could be one or more of the following:
     - transliteration,
     - transcription,
     - translation
    """

    def __init__(self, omen):
        super().__init__()
        self.omen = omen
        self.omen_prefix = omen.xml_id
        self.data = defaultdict(list)

    def add_to_reconstruction(self, row: list):
        """
        Identifies the score line and adds it to the score
        """
        logger.debug("Adding to reconstruction")
        reconstruction_line = ReconstructionLine(row, self.omen)
        self.data[reconstruction_line.reconstruction_id].append(reconstruction_line)

    @property
    def tei(self):
        for rdg_grp, lines in self.data.items():
            elem = ET.Element(
                "div",
                {
                    "n": f"{rdg_grp.label} ({rdg_grp.witness})"
                    if rdg_grp.witness
                    else rdg_grp.label,
                    XML_ID: clean_id(rdg_grp.xml_id),
                },
            )

            for line in lines:
                elem.append(line.tei)

            yield elem
