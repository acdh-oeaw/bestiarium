from unittest.mock import MagicMock, patch
from xml.etree import ElementTree as ET

from django.test import TestCase

from ..omensheet import OmenSheet

NS = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


class OmenSheetTestCase(TestCase):
    def setUp(self):
        self.mock_workbook = MagicMock()
        with open('xlsx2tei/tests/sheet1.xml', 'r') as f:
            self.sheet_xml = f.read()

        self.sheet_root = ET.fromstring(self.sheet_xml)
        styles_xml = ET.parse('xlsx2tei/tests/styles.xml').getroot()
        self.ss_xml = ET.parse('xlsx2tei/tests/sharedStrings.xml').getroot()
        self.mock_workbook.shared_strings = self.ss_xml.findall('ns:si', NS)
        self.mock_workbook.cell_formats = styles_xml.findall(
            'ns:cellXfs/ns:xf', NS)
        self.mock_workbook.fonts = styles_xml.findall('ns:fonts/ns:font', NS)
        self.mock_workbook.background = styles_xml.findall(
            'ns:fills/ns:fill', NS)

    def test_omen_title(self):
        with patch('xlsx2tei.omensheet.Omen.set_title') as mock_set_title:
            sheet = OmenSheet(
                sheet_xml=self.sheet_xml, workbook=self.mock_workbook)

            mock_set_title.assert_called_once_with('Omen 23.1')
