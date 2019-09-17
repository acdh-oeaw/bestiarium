'''
A subclass of Workbook for reading omens as defined in
https://oeawcloud.oeaw.ac.at/index.php/f/11933088
'''

from xml.dom import minidom
from xml.etree import ElementTree as ET

from .omensheet import OmenSheet
from .workbook import Workbook

# Start creating TEI for the set of omens
NS = {'tei': 'http://www.tei-c.org/ns/1.0'}


def pretty_print(root):
    '''
    pretty prints xml elements
    '''
    dom = minidom.parseString(ET.tostring(root))
    pretty_root = dom.toprettyxml(indent="  ", newl="\n")
    # print(pretty_root)
    return pretty_root


class OmensWorkbook(Workbook):
    '''
    An XLSX workbook containing omens in different sheets
    Exportable as TEI
    '''

    def __init__(self, wbfile):
        super().__init__(wbfile)

    @staticmethod
    def get_omen_name(sheet):
        omen_name = sheet.get_text_at('A1')
        return omen_name

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

    def export_to_tei(self):
        '''
        Updates the TEI representation of a chapter with the omens in the workbook
        '''

        # TODO: extract existing representation and update

        root = self._get_tei_outline()  # TEI skeleton
        body = root.find('./text/body')

        for sheet in self.get_sheets():
            # Read omen
            omen_sheet = OmenSheet(sheet)

            # Add witnesses from the omen to TEI
            for witness in omen_sheet.score.keys():
                pass

            # Add omen div to TEI
            omen_div = omen_sheet.omen_div
            body.append(omen_div)

        return pretty_print(root)
