'''
A chapter containing one of more omens, derived from one of more workbooks
'''

import logging
from xml.etree import ElementTree as ET

from .models import Chapter as DB
from .namespaces import NS, TEI_NS, XML_NS, get_attribute
from .omen import Omen
from .util import element2string
from .workbook import Workbook

logger = logging.getLogger(__name__)

for ns, uri in NS.items():
    ET.register_namespace(ns, uri)


class Chapter:
    def __init__(self):
        self.name = ''

    @staticmethod
    def _get_tei_outline():
        '''
        adds the TEI skeleton
        '''
        root = ET.Element('TEI', {'xmlns': NS['tei']})
        header = ET.SubElement(root, 'teiHeader')
        fileDesc = ET.SubElement(header, 'fileDesc')
        titleStmt = ET.SubElement(fileDesc, 'titleStmt')
        title = ET.SubElement(titleStmt, 'title')
        editor = ET.SubElement(titleStmt, 'editor')
        respStmt = ET.SubElement(titleStmt, 'respStmt')
        publicationStmt = ET.SubElement(fileDesc, 'publicationStmt')
        p = ET.SubElement(publicationStmt, 'p')
        p.text = 'Working copy, for internal use only'
        sourceDesc = ET.SubElement(header, 'sourceDesc')
        ET.SubElement(sourceDesc, get_attribute('listWit', TEI_NS))
        text = ET.SubElement(root, get_attribute('text', TEI_NS))
        body = ET.SubElement(text, get_attribute('body', TEI_NS))
        ET.SubElement(body, 'head')

        return root

    def add_workbook(self, wbfile):
        '''
        Updates the TEI using the workbok information
        '''
        self.export_to_tei(wbfile)

    def export_to_tei(self, wbfile):
        '''
        Updates the TEI representation of a chapter
        with the omens in the workbook
        '''
        wb = Workbook(wbfile)
        # TODO: extract existing representation and update

        body = None
        db, created = None, None
        for sheet in wb.get_sheets():
            try:
                omen = Omen(sheet)  # Read omen
            except Exception as e:
                logging.error('Error "%s" processing omen from sheet %s',
                              repr(e), sheet)
                continue

            if self.name and self.name != omen.chapter_name:
                logging.error(
                    'Expecting omens from chapter %s. Found chapter %s',
                    self.name, omen.chapter_name)
                continue

            # Create a chapter record if it doesn't already exist
            if db is None:
                db, created = DB.objects.get_or_create(
                    chapter_name=omen.chapter_name)

            # Extract body from the database TEI or generate TEI
            if body is None:
                if created or not chapter_db.tei:
                    logger.debug("Creating new chapter: %s", omen.chapter_name)
                    root = Chapter._get_tei_outline()  # TEI skeleton
                else:
                    root = ET.fromstring(chapter_db.tei)

                body = root.find('.//tei:body', NS)

                # HACK  - when body is unsearchable within the "tei" namespace
                if body is None:
                    body = root.find('.//*body', NS)
                    if body is None:
                        ET.dump(root)
                        raise ValueError('Cannot find BODY')

            # Add witnesses from the omen to TEI
            for witness in omen.score.witnesses:
                logger.debug('Witness %s in Omen %s', witness.xml_id,
                             omen.omen_name)
                witness_elem = root.find(
                    # f'.//witness[@{get_attribute("id",XML_NS)}="{witness.xml_id}"]',
                    f'.//tei:witness[@xml:id="{witness.xml_id}"]',
                    NS)
                if witness_elem is None:
                    listwit = root.find('.//tei:listWit', NS)
                    listwit.append(
                        ET.Element(
                            get_attribute('witness', TEI_NS), {
                                get_attribute('id', XML_NS): witness.xml_id
                            }))

            # Check and remove if omen already exists in the TEI
            omen_div_old = body.find(f'.//tei:div[@n="{omen.omen_name}"]', NS)
            if omen_div_old is not None:
                logger.warning('Overwriting existing omen div: %s',
                               ET.tostring(omen_div_old))
                body.remove(omen_div_old)

            # Add omen div to TEI
            omen_div = omen.export_to_tei(db)
            body.append(omen_div)

        self.tei = element2string(root)
        db.tei = self.tei
        db.save()
