# Create your tests here.
from unittest.mock import PropertyMock, patch
from xml.etree import ElementTree as ET

from django.test import TestCase

from .omensworkbook import OmensWorkbook
from .sheet import Sheet
from .workbook import Style, Workbook


class WorkbookTestCase(TestCase):

    test_file = 'xlsx/test_data/Snakes 23.1-11.xlsx'

    @patch('xlsx.workbook.Style')
    @patch('xml.etree.ElementTree.XML')
    def test_wbinit(self, MockXML, MockStyle):
        wb = Workbook(self.test_file)
        MockStyle.assert_called_once()
        MockXML.assert_called_once()
        self.assertIsNotNone(wb.shared_strings)

    @patch('xlsx.workbook.Style')
    @patch('xlsx.workbook.Sheet')
    def test_get_sheet(self, MockSheet, MockStyle):
        wb = Workbook(self.test_file)
        for sheet in wb.get_sheets():
            MockSheet.assert_called_once()
            MockSheet.reset_mock()


class StyleTestCase(TestCase):
    pass


class SheetTestCase(TestCase):
    def setUp(self):
        sheet_xml = ET.parse('xlsx/test_data/sheet1.xml').getroot()
        with open('xlsx/test_data/styles.xml', 'r') as f:
            style_xml = f.read()

        style = Style(style_xml)
        shared_strings_xml = ET.parse(
            'xlsx/test_data/sharedStrings.xml').getroot()
        self.sheet = Sheet(sheet_xml=sheet_xml,
                           style=style,
                           shared_strings=shared_strings_xml)

    def test_bold_cell(self):
        cell = self.sheet.get_cell_at('A1')
        for i, token in enumerate(self.sheet.get_tokens_in_cell(cell)):
            assert token.format.bold == True
            assert token.complete
            assert i == 0

    def test_italics_cell(self):
        cell = self.sheet.get_cell_at('D13')
        for i, token in enumerate(self.sheet.get_tokens_in_cell(cell)):
            assert token.format.bold == True
            assert token.format.italics == True
            assert token.complete
            assert i == 0

    def test_font_color(self):
        cell = self.sheet.get_cell_at('C3')
        for token in self.sheet.get_tokens_in_cell(cell):
            assert token.format.color == 'FFFF0000'
            assert token.complete
            assert token.text == '1'

        cell = self.sheet.get_cell_at('B6')
        for token in self.sheet.get_tokens_in_cell(cell):
            assert token.format.color == 'FF808080'

    def test_multiple_tokens(self):
        cell = self.sheet.get_cell_at('L4')
        for i, token in enumerate(self.sheet.get_tokens_in_cell(cell)):
            if i == 0:
                assert token.text == 'ŠUB-'
                assert not token.format.italics
            elif i == 1:
                assert token.text == 'ut'
                assert token.format.italics
        assert i == 1

    def test_background_color(self):
        cell = self.sheet.get_cell_at('P12')
        for i, token in enumerate(self.sheet.get_tokens_in_cell(cell)):
            assert token.format.bgcolor == 'FF00B0F0'
            if i == 0:
                assert token.text == 'GÍD.DA'
                assert not token.format.italics
            elif i == 1:
                assert token.text == '-ik'
                assert token.format.italics
        assert i == 1


class OmensWorkbookTestCase(TestCase):
    test_file = 'xlsx/test_data/Snakes 23.1-11.xlsx'

    def test_tei(self):
        omens_workbook = OmensWorkbook(self.test_file)
        tei = omens_workbook.export_to_tei()
        print(tei)
