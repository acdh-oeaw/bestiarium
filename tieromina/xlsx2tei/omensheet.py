import logging
from xml.etree import ElementTree as ET

from .sheet import Sheet

NS = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


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
                # print(cell)
                pass
