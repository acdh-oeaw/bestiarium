from unittest import TestCase
from unittest.mock import patch
from xml.etree import ElementTree as ET

from ..namespaces import NS
from ..row import Row

ss_xml = ET.parse('test_data/sharedStrings.xml')
shared_strings = ss_xml.findall('spreadsheetml:si', NS)


class RowTestCase(TestCase):
    @patch('xlsx2tei.sheet.Sheet')
    def setUp(self, MockSheet):
        sheet_xml = ET.parse('test_data/sheet1.xml').getroot()
        row_xml = sheet_xml.find(
            'spreadsheetml:sheetData/spreadsheetml:row[@r="1"]', NS)

        self.row = Row(sheet=MockSheet(), xml=row_xml)
        self.empty_row = Row(
            sheet=MockSheet(),
            xml=sheet_xml.find(
                'spreadsheetml:sheetData/spreadsheetml:row[@r="2"]', NS))

    def test_num_cells_in_row(self):
        self.assertEqual(len(list(self.row.cells)), 17)

    @patch('xlsx2tei.cell.Cell.shared_strings', shared_strings)
    def test_empty_row(self):
        self.assertTrue(self.empty_row.is_empty)
        self.assertFalse(self.row.is_empty)

    @patch('xlsx2tei.cell.Cell.shared_strings', shared_strings)
    def test_cell_at(self):
        cell = self.row.cell_at_column('A')
        self.assertEqual(cell.address, 'A1')
