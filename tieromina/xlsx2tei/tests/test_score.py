from unittest import TestCase
from unittest.mock import patch
from xml.etree import ElementTree as ET

from ..namespaces import NS
from ..score import Score, ScoreRow
from ..workbook import Style

ss_xml = ET.parse('xlsx2tei/test_data/sharedStrings.xml')
shared_strings = ss_xml.findall('spreadsheetml:si', NS)
style = Style(ET.parse('xlsx2tei/test_data/styles.xml'))


class ScoreRowTestCase(TestCase):
    @patch('xlsx2tei.sheet.Sheet')
    def setUp(self, MockSheet):
        sheet_xml = ET.parse('xlsx2tei/test_data/sheet1.xml').getroot()
        sheet4_xml = ET.parse('xlsx2tei/test_data/sheet4.xml').getroot()
        row_xml = sheet_xml.find(
            'spreadsheetml:sheetData/spreadsheetml:row[@r="6"]', NS)
        shared_strings_xml = ET.parse(
            'xlsx2tei/test_data/sharedStrings.xml').getroot()
        self.score_row = ScoreRow(sheet=MockSheet(), xml=row_xml)
        self.multiline_score_row = ScoreRow(
            sheet=MockSheet(),
            xml=sheet4_xml.find(
                'spreadsheetml:sheetData/spreadsheetml:row[@r="5"]', NS))

    def test_witness(self):
        wit = self.score_row.witness
        self.assertEqual(wit.address, 'A6')

    def test_witness(self):
        wit = self.score_row.reference
        self.assertEqual(wit.address, 'B6')

    @patch('xlsx2tei.row.Cell.style', style)
    @patch('xlsx2tei.cell.Cell.shared_strings', shared_strings)
    def test_lines(self):
        lines = list(self.score_row.lines)
        self.assertEqual(len(lines), 1)
        self.assertEqual(len(lines[0]), 2)
        multiple_lines = list(self.multiline_score_row.lines)
        self.assertEqual(len(multiple_lines), 2)
        self.assertEqual(len(multiple_lines[0]), 6)
        self.assertEqual(len(multiple_lines[1]), 2)
