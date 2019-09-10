from pprint import pprint
from unittest.mock import PropertyMock, patch
from xml.etree import ElementTree as ET

from django.test import TestCase

from ..omensheet import OmenSheet
from ..omensworkbook import OmensWorkbook
from ..sheet import Sheet
from ..workbook import Workbook


class WorkbookTestCase(TestCase):

    test_file = 'xlsx2tei/tests/Snakes 23.1-11.xlsx'

    def test_wbfile(self):
        wb = Workbook(self.test_file)
        self.assertEqual(wb.wbfile, self.test_file)
        self.assertIsNotNone(wb.z)
        self.assertEqual(len(wb.sheets), 11)
        self.assertEqual(len(wb.shared_strings), 570)
        self.assertEqual(len(wb.cell_formats), 102)
        self.assertEqual(len(wb.fonts), 29)
        self.assertEqual(len(wb.background), 3)
        return

    def test_get_sheet(self):
        wb = Workbook(self.test_file)
        sheet = wb.get_sheet(1)
        self.assertIsNotNone(sheet)
        sheet = wb.get_sheet(100)
        self.assertIsNone(sheet)
        # TODO: Test the printed warning somehow


class OmensWorkbookTestCase(TestCase):
    test_file = 'xlsx2tei/tests/Snakes 23.1-11.xlsx'

    def test_wb_file(self):
        wb = OmensWorkbook(self.test_file)
        sheet = wb.get_sheet(1)
        cell = sheet.contents[3].get('C')
        print(sheet.contents[6].get('P'))
        # print('Sheet')
        # pprint(sheet.contents)
