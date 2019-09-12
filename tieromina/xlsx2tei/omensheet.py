'''
Omen specific reading of a sheet from a workbook
'''
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

    def __init__(self, *, workbook, sheet_xml: ET.ElementTree):
        super().__init__(workbook=workbook, sheet_xml=sheet_xml)

        self.title = self.contents[1]['A'].text
        self.read_omen()

    def read_omen(self):
        for row_num, cells in self.contents.items():
            if row_num == 1:  # Omen name, skip
                continue
            for col_name, cell in cells:
                pass

    def get_val_at_column(col_name: str):
        pass
