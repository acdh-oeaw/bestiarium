# Create your tests here.
from unittest.mock import PropertyMock, patch
from xml.etree import ElementTree as ET

from django.test import TestCase

from .workbook import Workbook


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
