'''
Omen specific reading of a sheet from a workbook
'''
import logging
from xml.etree import ElementTree as ET

from .omen import Omen
from .sheet import Sheet

NS = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


class OmenSheet(Sheet):
    '''
    A single sheet from the omens workbook
    Represents one omen,
    and its relation to other omens
    '''
    omen = Omen()

    def __init__(self, *, workbook, sheet_xml: ET.ElementTree):
        super().__init__(workbook=workbook, sheet_xml=sheet_xml)
        self.omen.set_title(self.contents[1]['A'].text)
        self.read_omen()

    def read_omen(self):
        prev_row_type = None
        comment = False
        for row_num, cells in self.contents.items():
            if row_num == 1:  # Omen name, skip
                continue

            for col_name, cell in cells.items():
                if col_name == 'A':
                    if not cell.text:  # empty first column
                        pass

    def get_val_at_column(col_name: str):
        pass
