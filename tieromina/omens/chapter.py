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

    def export_to_tei(self, wbfile):
        '''
        Updates the TEI representation of a chapter
        with the omens in the workbook
        '''
        wb = Workbook(wbfile)
        # TODO: extract existing representation and update

        body = None
        for sheet in wb.get_sheets():
            # Read omen
            try:
                omen = Omen(sheet)
            except Exception as e:
                logging.error('Error processing omen from sheet %s', sheet)
                continue

            db, created = DB.objects.get_or_create(
                chapter_name=omen.chapter_name)
            if body is None:
                if created or not chapter_db.tei:
                    logger.debug("Creating new chapter: %s", omen.chapter_name)
                    root = Chapter._get_tei_outline()  # TEI skeleton

                else:
                    root = ET.fromstring(chapter_db.tei)

                body = root.find('.//tei:body', NS)

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
            omen_div = omen.tei
            body.append(omen_div)

        tei_str = element2string(root)
        db.tei = tei_str
        db.save()
        return db
