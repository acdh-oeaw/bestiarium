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

    def test_cell_values(self):
        self.assertEqual(len(self.sheet.contents), 17)

        self.assertEqual(str(self.sheet.get_cell(1, 'A').text[0]), 'Omen 23.1')
        self.assertFalse(self.sheet.get_cell(1, 'A').text[0].italics)

        self.assertEqual(str(self.sheet.get_cell(3, 'A').text[0]), 'K 02925+')
        self.assertFalse(self.sheet.get_cell(3, 'A').text[0].italics)

        self.assertEqual(str(self.sheet.get_cell(3, 'C').text[0]), '1')
        self.assertTrue(self.sheet.get_cell(3, 'C').text[0].italics)

    def test_in_cell_formatting(self):
        print(self.sheet.get_cell(4, 'L').text)
        self.assertTrue(self.sheet.get_cell(4, 'L').text[1].italics)
        self.assertEqual(str(self.sheet.get_cell(4, 'L').text[1]), 'ut')
        self.assertEqual(str(self.sheet.get_cell(4, 'L').text[0]), 'ŠUB-')

        # self.assertEqual(str(self.sheet.contents[3]['C'].text[0]), '1')
