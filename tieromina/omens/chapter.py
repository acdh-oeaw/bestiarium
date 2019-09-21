'''
A chapter containing one of more omens, derived from one of more workbooks
'''

from xml.etree import ElementTree as ET

from .namespaces import NS
from .omen import Omen
from .util import element2string
from .workbook import Workbook


class Chapter:
    def __init__(self):
        self.name = ''

    def _get_tei_outline(self):
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
        ET.SubElement(sourceDesc, 'listWit')

        text = ET.SubElement(root, 'text')
        body = ET.SubElement(text, 'body')
        ET.SubElement(body, 'head')

        return root

    def export_to_tei(self, wbfile):
        '''
        Updates the TEI representation of a chapter with the omens in the workbook
        '''
        wb = Workbook(wbfile)

        # TODO: extract existing representation and update

        root = self._get_tei_outline()  # TEI skeleton
        body = root.find('./text/body')

        for sheet in wb.get_sheets():
            # Read omen
            omen = Omen(sheet)

            # Add witnesses from the omen to TEI
            for witness in omen.score.witnesses:
                pass

            # Add omen div to TEI
            omen_div = omen.tei
            body.append(omen_div)

        return element2string(root)
