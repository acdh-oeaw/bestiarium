'''
A single sheet from a workbook
'''
from collections import defaultdict
from xml.etree import ElementTree as ET

from .cell import Cell

NS = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


class Sheet:
    '''
    A spreadsheet from a workbook
    '''
    contents = defaultdict(dict)

    def __init__(self, *, workbook, sheet_xml: ET.ElementTree):
        self.sheet = ET.ElementTree(ET.XML(sheet_xml)).getroot()
        self.workbook = workbook
        self.read()

    def read(self):
        '''
        Reads the contents of the sheet
        '''
        rows = self.sheet.findall('ns:sheetData/ns:row', NS)
        for r, row in enumerate(rows):
            row_name = row.attrib.get('r')
            cells = row.findall('ns:c', NS)
            row_contents = {}
            for c, cell in enumerate(cells):
                cell_contents = self.get_cell_contents(cell)
                if cell_contents:
                    cell_format = self.workbook.cell_formats[int(
                        cell.attrib.get('s'))]
                    background = self.workbook.background[int(
                        cell_format.attrib.get('fillId')
                    )] if 'fillId' in cell_format.attrib else None
                    font = self.workbook.fonts[int(
                        cell_format.attrib.get('fontId')
                    )] if 'fontId' in cell_format.attrib else None
                    row_contents[cell.attrib.get('r').rstrip(row_name)] = Cell(
                        **{
                            Cell.CONTENTS: cell_contents,
                            Cell.FONT: font,
                            Cell.BACKGROUND: background
                        })

            if row_contents:
                self.contents[int(row_name)] = row_contents

        # print(self.contents)

    def get_cell(self, row_name: str, col_name: str) -> Cell:
        return self.contents[int(row_name)].get(col_name)

    @classmethod
    def col_name2num(cls, letter: str):
        """ A -> 0, B -> 1, Z -> 25, AA -> 26, BA -> 52 """
        base26digits = [1 + ord(x) - ord('A') for x in letter]
        return sum([
            x * 26**(len(base26digits) - k - 1)
            for k, x in enumerate(base26digits)
        ]) - 1

    def get_cell_contents(self, cell: ET.Element) -> ET.Element:
        '''
        Returns the cell contents
        in the form of an XML element
        given the row and column
        '''

        if len(cell) and 't' in cell.attrib and cell.attrib['t'] == 's':
            # shared string
            idx = int(cell.find('ns:v', NS).text)
            si = self.workbook.shared_strings[idx]
            return si
