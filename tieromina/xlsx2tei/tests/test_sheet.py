from unittest import TestCase
from xml.etree import ElementTree as ET

from ..sheet import Sheet
from ..workbook import Style


class SheetTestCase(TestCase):
    def setUp(self):
        sheet_xml = ET.parse('test_data/sheet1.xml').getroot()
        style_xml = ET.parse('test_data/styles.xml')

        style = Style(style_xml)
        shared_strings_xml = ET.parse('test_data/sharedStrings.xml').getroot()
        self.sheet = Sheet(
            sheet_name='1',
            xml=sheet_xml,
            style=style,
            shared_strings=shared_strings_xml)

    def test_rows(self):
        for row in self.sheet.rows:
            pass

    def test_bold_cell(self):
        cell = self.sheet.cell_at('A1')
        self.assertEqual(cell.cell_format.bold, True)
        # for i, chunk in enumerate(cell.chunks):
        #     assert chunk.cell_format.bold == True
        #     assert chunk.complete
