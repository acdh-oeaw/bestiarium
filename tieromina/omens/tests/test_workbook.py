from unittest.mock import patch

from django.test import TestCase

from ..workbook import Workbook

NS = {'ns': 'http://www.tei-c.org/ns/1.0'}


class WorkbookTestCase(TestCase):

    test_file = 'omens/tests/test_data/Snakes 23.1-11.xlsx'

    @patch('omens.workbook.Style')
    @patch('xml.etree.ElementTree.XML')
    def test_wbinit(self, MockXML, MockStyle):
        wb = Workbook(self.test_file)
        MockStyle.assert_called_once()
        MockXML.assert_called_once()
        self.assertIsNotNone(wb.shared_strings)

    @patch('omens.workbook.Style')
    @patch('omens.workbook.Sheet')
    def test_get_sheet(self, MockSheet, MockStyle):
        wb = Workbook(self.test_file)
        for sheet in wb.get_sheets():
            MockSheet.assert_called_once()
            MockSheet.reset_mock()
