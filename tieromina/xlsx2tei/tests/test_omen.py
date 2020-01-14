from unittest import TestCase
from unittest.mock import patch
from xml.etree import ElementTree as ET

from ..namespaces import NS
from ..omen import Omen

ss_xml = ET.parse('test_data/sharedStrings.xml')
shared_strings = ss_xml.findall('spreadsheetml:si', NS)


class OmenTestCase(TestCase):
    @patch('xlsx2tei.workbook.Style')
    def setUp(self, MockStyle):
        sheet_xml = ET.parse('test_data/sheet1.xml').getroot()

        shared_strings_xml = ET.parse('test_data/sharedStrings.xml').getroot()
        self.omen = Omen(
            sheet_name='1',
            xml=sheet_xml,
            style=MockStyle(),
            shared_strings=shared_strings_xml)

    def test_score(self):
        self.omen.score
