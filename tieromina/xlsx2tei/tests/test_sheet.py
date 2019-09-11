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
        mock_workbook = MagicMock()
        with open('xlsx2tei/tests/sheet1.xml', 'r') as f:
            sheet_xml = f.read()
        styles_xml = ET.parse('xlsx2tei/tests/styles.xml').getroot()
        ss_xml = ET.parse('xlsx2tei/tests/sharedStrings.xml').getroot()
        mock_workbook.shared_strings = ss_xml.findall('ns:si', NS)
        mock_workbook.cell_formats = styles_xml.findall('ns:cellXfs/ns:xf', NS)
        mock_workbook.fonts = styles_xml.findall('ns:fonts/ns:font', NS)
        mock_workbook.background = styles_xml.findall('ns:fills/ns:fill', NS)
        self.sheet = Sheet(sheet_xml=sheet_xml, workbook=mock_workbook)

    def test_number_of_rows(self):
        self.assertEqual(len(self.sheet.contents), 17)

    def test_cell_values(self):
        self.assertEqual(str(self.sheet.get_cell(1, 'A').text[0]), 'Omen 23.1')
        self.assertEqual(str(self.sheet.get_cell(3, 'A').text[0]), 'K 02925+')
        self.assertEqual(str(self.sheet.get_cell(3, 'C').text[0]), '1')
        self.assertEqual(str(self.sheet.get_cell(9, 'D').text[0]), '˹DIŠ˺')

    def test_italics_whole_cell(self):
        self.assertFalse(self.sheet.get_cell(1, 'A').italics)
        self.assertFalse(self.sheet.get_cell(3, 'A').italics)
        self.assertTrue(self.sheet.get_cell(3, 'C').italics)

    def test_multiple_tokens_in_cell(self):
        self.assertEqual(str(self.sheet.get_cell(4, 'L').text[0]), 'ŠUB-')
        self.assertEqual(str(self.sheet.get_cell(4, 'L').text[1]), 'ut')

    def test_italics_partial(self):
        self.assertTrue(self.sheet.get_cell(4, 'L').text[1].italics)
        self.assertFalse(self.sheet.get_cell(4, 'L').text[0].italics)

    def test_background_color(self):
        # 12: M, N, O, P
        # self.assertEqual(
        #     self.sheet.get_cell(12, 'M').text[0].color, 'FF00B0F0')
        self.assertEqual(
            self.sheet.get_cell(12, 'P').text[0].bgcolor, 'FF00B0F0')
