from xml.etree import ElementTree as ET

from django.test import TestCase

from ..sheet import Sheet
from ..workbook import Style

NS = {'ns': 'http://www.tei-c.org/ns/1.0'}


class SheetTestCase(TestCase):
    # TODO: Rewite tests by mocking token
    def setUp(self):
        sheet_xml = ET.parse('omens/tests/test_data/sheet1.xml').getroot()
        with open('omens/tests/test_data/styles.xml', 'r') as f:
            style_xml = f.read()

        style = Style(style_xml)
        shared_strings_xml = ET.parse(
            'omens/tests/test_data/sharedStrings.xml').getroot()
        self.sheet = Sheet(
            sheet_xml=sheet_xml,
            style=style,
            shared_strings=shared_strings_xml)

    def test_bold_cell(self):
        cell = self.sheet.get_cell_at('A1')
        for i, token in enumerate(cell.tokens):
            assert token.format.bold == True
            assert token.complete
