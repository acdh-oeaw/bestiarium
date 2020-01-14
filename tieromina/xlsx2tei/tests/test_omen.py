from unittest import TestCase
from unittest.mock import patch
from xml.etree import ElementTree as ET

from ..namespaces import NS
from ..omen import Omen

ss_xml = ET.parse('xlsx2tei/test_data/sharedStrings.xml')
shared_strings = ss_xml.findall('spreadsheetml:si', NS)


class OmenTestCase(TestCase):
    @patch('xlsx2tei.workbook.Style')
    def setUp(self, MockStyle):
        sheet_xml = ET.parse('xlsx2tei/test_data/sheet1.xml').getroot()

        shared_strings_xml = ET.parse(
            'xlsx2tei/test_data/sharedStrings.xml').getroot()
        self.omen = Omen(
            sheet_name='1',
            xml=sheet_xml,
            style=MockStyle(),
            shared_strings=shared_strings_xml)

    def test_score(self):
        score = self.omen.score
        self.assertEqual(len(score), 7)

    def test_readings(self):
        readings = list(self.omen.readings(11))
        print(readings)
        self.assertEqual(len(readings), 2)

    def test_comment(self):
        comments = self.omen.comments(20)
        self.assertEqual(len(comments), 2)
