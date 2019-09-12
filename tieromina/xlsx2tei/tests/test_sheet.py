from pprint import pprint
from unittest.mock import MagicMock, PropertyMock, patch
from xml.etree import ElementTree as ET

from django.test import TestCase

from ..omensheet import OmenSheet
from ..sheet import Sheet

NS = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


class SheetTestCase(TestCase):
    test_file = 'xlsx2tei/tests/sheet1.xml'
    sheet_num = 0

    def setUp(self):
        self.mock_workbook = MagicMock()
        with open('xlsx2tei/tests/sheet1.xml', 'r') as f:
            sheet_xml = f.read()

        self.sheet_root = ET.fromstring(sheet_xml)
        styles_xml = ET.parse('xlsx2tei/tests/styles.xml').getroot()
        self.ss_xml = ET.parse('xlsx2tei/tests/sharedStrings.xml').getroot()
        self.mock_workbook.shared_strings = self.ss_xml.findall('ns:si', NS)
        self.mock_workbook.cell_formats = styles_xml.findall(
            'ns:cellXfs/ns:xf', NS)
        self.mock_workbook.fonts = styles_xml.findall('ns:fonts/ns:font', NS)
        self.mock_workbook.background = styles_xml.findall(
            'ns:fills/ns:fill', NS)
        self.sheet = Sheet(sheet_xml=sheet_xml, workbook=self.mock_workbook)

    def get_cell(self, address):
        return self.sheet_root.find(f'.//*[@r="{address}"]')

    def test_number_of_rows(self):
        self.assertEqual(len(self.sheet.contents), 17)

    def test_extacted_format_none(self):
        cell = self.get_cell('A1')
        with patch('xlsx2tei.sheet.Fmt') as MockFmt:
            self.sheet.extract_format(cell)
            MockFmt.assert_called_once_with(
                color=None, bgcolor=None, bold=True, italics=False)

    def test_extracted_format_color(self):
        with patch('xlsx2tei.sheet.Fmt') as MockFmt:
            cell = self.get_cell('C3')
            self.sheet.extract_format(cell)
            MockFmt.assert_called_once_with(
                color='FFFF0000', bgcolor=None, bold=False, italics=True)
        with patch('xlsx2tei.sheet.Fmt') as MockFmt:
            cell = self.get_cell('C8')
            self.sheet.extract_format(cell)
            MockFmt.assert_called_once_with(
                color='FFFF0000', bgcolor=None, bold=False, italics=True)
        with patch('xlsx2tei.sheet.Fmt') as MockFmt:
            cell = self.get_cell('A6')
            self.sheet.extract_format(cell)
            MockFmt.assert_called_once_with(
                color='FF808080', bgcolor=None, bold=False, italics=False)
        with patch('xlsx2tei.sheet.Fmt') as MockFmt:
            cell = self.get_cell('B6')
            self.sheet.extract_format(cell)
            MockFmt.assert_called_once_with(
                color='FF808080', bgcolor=None, bold=False, italics=False)

    def test_extracted_format_bgcolor(self):
        with patch('xlsx2tei.sheet.Fmt') as MockFmt:
            cell = self.get_cell('M12')
            self.sheet.extract_format(cell)
            MockFmt.assert_called_once_with(
                bgcolor='FF00B0F0', color=None, bold=False, italics=True)

        with patch('xlsx2tei.sheet.Fmt') as MockFmt:
            cell = self.get_cell('P12')
            self.sheet.extract_format(cell)
            MockFmt.assert_called_once_with(
                bgcolor='FF00B0F0', color=None, bold=False, italics=False)
