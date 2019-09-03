'''
A single sheet from a workbook
'''
from collections import defaultdict
from xml.etree import ElementTree as ET

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
                    row_contents[cell.attrib.get('r').rstrip(
                        row_name)] = cell_contents

            if row_contents:
                self.contents[int(row_name)] = row_contents

        # print(self.contents)

    @classmethod
    def col_name2num(cls, letter: str):
        """ A -> 0, B -> 1, Z -> 25, AA -> 26, BA -> 52 """
        base26digits = [1 + ord(x) - ord("A") for x in letter]
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


class OmenSheet(Sheet):
    '''
    A single sheet from the omens workbook
    Represents one omen,
    and its relation to other omens
    '''

    def __init__(self, *, workbook, sheet_xml):
        super().__init__(workbook=workbook, sheet_xml=sheet_xml)
        self.read_omen()

    def read_omen(self):
        for row_name, row in self.contents.items():
            first_col_val = row.get('A')
            for col_name, cell in row.items():
                texts = cell.findall('.//ns:t', NS)
                print(col_name, row_name, [t.text for t in texts])
