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
        workbook = MagicMock()
        with open('xlsx2tei/tests/sheet1.xml', 'r') as f:
            sheet_xml = f.read()
        styles_xml = ET.parse('xlsx2tei/tests/styles.xml').getroot()
        ss_xml = ET.parse('xlsx2tei/tests/sharedStrings.xml').getroot()
        workbook.shared_strings = ss_xml.findall('ns:si', NS)
        workbook.cell_formats = styles_xml.findall('ns:cellXfs/ns:xf', NS)
        workbook.fonts = styles_xml.findall('ns:fonts/ns:font', NS)
        workbook.background = styles_xml.findall('ns:fills/ns:fill', NS)
        self.sheet = Sheet(sheet_xml=sheet_xml, workbook=workbook)

    def test_init(self):
        self.assertEqual(len(self.sheet.contents), 17)

        self.assertEqual(str(self.sheet.contents[1]['A'].text[0]), 'Omen 23.1')
