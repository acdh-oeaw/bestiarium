from unittest.mock import ANY, MagicMock, PropertyMock, call, patch

import xlrd
from django.test import TestCase

from ..wbformat import WBFormat
from ..workbook import Workbook


class WorkbookTestCase(TestCase):
    test_file = 'xl2tei/tests/Snake_23_1_11.xls'

    def test_wbfile(self):
        wb = Workbook(self.test_file)
        self.assertEqual(wb.wbfile, self.test_file)
        return
    
    @patch('xl2tei.workbook.WBFormat')
    @patch('xl2tei.workbook.Sheet')
    def test_number_of_sheets(self, MockSheet, MockWBFormat):
        wb = Workbook(self.test_file)
        self.assertEqual(MockSheet.call_count, 11)
        self.assertEqual(MockWBFormat.call_count, 1)
        return

    @patch('xl2tei.workbook.Sheet.chapter', new_callable=PropertyMock, return_value='100')
    def test_chapter_set_from_omen(self, mock_chapter):
        wb = Workbook(self.test_file)
        self.assertEqual(wb.chapter, '100')
        return
