from unittest import TestCase
from unittest.mock import patch

from ..workbook import Workbook


class WorkbookTestCase(TestCase):

    test_file = 'xlsx2tei/test_data/Snakes 23.1-11.xlsx'

    @patch('xlsx2tei.workbook.Style')
    @patch('xml.etree.ElementTree.XML')
    def test_wbinit(self, MockXML, MockStyle):
        wb = Workbook(self.test_file)
        MockStyle.assert_called_once()
        MockXML.assert_called()
        self.assertIsNotNone(wb.shared_strings)

    @patch('xlsx2tei.workbook.Style')
    @patch('xlsx2tei.workbook.Sheet')
    def test_get_sheet(self, MockSheet, MockStyle):
        wb = Workbook(self.test_file)
        for sheet in wb.sheets:
            MockSheet.assert_called_once()
            MockSheet.reset_mock()
