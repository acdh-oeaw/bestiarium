from unittest import TestCase
from unittest.mock import patch
from xml.etree import ElementTree as ET

from ..cell import Cell
from ..namespaces import NS
from ..workbook import Style  # TODO: Not ideal but WTH

ss_xml = ET.parse('test_data/sharedStrings.xml')
shared_strings = ss_xml.findall('spreadsheetml:si', NS)
style_xml = ET.parse('test_data/styles.xml')
style = Style(style_xml)


class CellTestCase(TestCase):
    @patch('xlsx2tei.cell.Cell.style', style)
    @patch('xlsx2tei.sheet.Sheet')
    def setUp(self, MockSheet):
        sheet_xml = ET.parse('test_data/sheet1.xml').getroot()
        self.cell = Cell(MockSheet(), sheet_xml.find('.//*[@r="A1"]', NS))
        self.red_cell = Cell(MockSheet(), sheet_xml.find('.//*[@r="C3"]', NS))
        self.multipart_cell = Cell(MockSheet(),
                                   sheet_xml.find('.//*[@r="F9"]', NS))
        self.empty_cell = Cell(MockSheet(), sheet_xml.find(
            './/*[@r="A2"]', NS))

    @patch('xlsx2tei.cell.Cell.shared_strings', shared_strings)
    def test_cells_basic(self):
        self.assertEqual(len(list(self.cell.cell_contents)), 1)
        self.assertEqual(self.cell.cell_format.bold, True)
        print(self.empty_cell.cell_format, self.cell.plain_text)

    def test_format(self):
        print("Color", self.red_cell.cell_format.color)
        self.assertEqual(self.cell.cell_format.bold, True)
        self.assertEqual(self.empty_cell.cell_format.bold, False)
        self.assertEqual(self.multipart_cell.cell_format.bold, False)

    @patch('xlsx2tei.cell.Cell.shared_strings', shared_strings)
    def test_cells_multipart(self):
        self.assertGreater(len(list(self.multipart_cell.cell_contents)), 1)
        pass
