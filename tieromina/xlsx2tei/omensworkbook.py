import logging

from .omensheet import OmenSheet
from .workbook import Workbook


class OmensWorkbook(Workbook):
    '''
    '''

    def __init__(self, wbfile):
        super().__init__(wbfile)

    def get_sheet(self, sheet_num: int) -> OmenSheet:
        sheet_xml = self.get_sheet_xml(sheet_num)
        if sheet_xml:
            return OmenSheet(sheet_xml=sheet_xml, workbook=self)

    def get_tei(self):
        '''
        Returns the TEI of the sheet
        '''
        # Form header
        for sheet_id, sheet_name in self.sheets.items():
            sheet = self.get_sheet(sheet_id)

        return
