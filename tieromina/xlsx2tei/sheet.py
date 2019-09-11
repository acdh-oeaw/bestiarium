'''
A single sheet from a workbook
'''
from collections import defaultdict
from xml.etree import ElementTree as ET

from .cell import Cell, Fmt

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
        Parses the XML structure
        extracts cell contents and
        formating information for all cells
        Updates the contents attribute
        self.contents [int: row_name] = row_contents
        row_contents[str: colname] = Cell
        '''

        def get_cell_contents() -> ET.Element:
            '''
            Returns the cell contents
            in the form of an XML element
            given the row and column
            '''

            if cell is not None and 't' in cell.attrib and cell.attrib['t'] == 's':
                # shared string
                idx = int(cell.find('ns:v', NS).text)
                si = self.workbook.shared_strings[idx]
                return si

            if cell is not None:
                raw_text_elem = cell.find('ns:v', NS)
                if raw_text_elem is not None:
                    return raw_text_elem.text

        rows = self.sheet.findall('ns:sheetData/ns:row', NS)
        for r, row in enumerate(rows):
            row_name = row.attrib.get('r')
            cells = row.findall('ns:c', NS)
            row_contents = {}
            for c, cell in enumerate(cells):
                cell_contents = get_cell_contents()
                if cell_contents:
                    fmt = self.extract_format(cell)
                    row_contents[cell.attrib.get('r').rstrip(row_name)] = Cell(
                        contents=cell_contents, fmt=fmt)

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

    def extract_format(self, cell):
        '''
        returns a Fmt tuple
        '''
        xf_idx = int(cell.attrib.get('s'))
        xf = self.workbook.cell_formats[xf_idx]
        font_idx = int(xf.attrib.get('fontId'))
        font = self.workbook.fonts[font_idx]
        italics = font.find('ns:i', NS) is not None
        boldface = font.find('ns:b', NS) is not None
        if font.find('ns:color', NS) is not None:
            color = font.find('ns:color', NS).attrib.get('rgb')
        else:
            color = None

        fill_idx = int(xf.attrib.get('fillId'))
        fill = self.workbook.background[fill_idx]
        if fill.find('ns:patternFill/ns:fgColor', NS) is not None:
            bgcolor = fill.find('ns:patternFill/ns:fgColor',
                                NS).attrib.get('rgb')
        else:
            bgcolor = None
        return Fmt(
            bold=boldface, italics=italics, color=color, bgcolor=bgcolor)
