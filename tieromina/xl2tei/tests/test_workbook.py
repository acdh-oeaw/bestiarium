from django.test import TestCase
from unittest.mock import patch, call, ANY

from ..workbook import Workbook

class WorkbookTestCase(TestCase):
    test_file = 'xl2tei/tests/Snake_23_1_11.xls'

    @patch('xl2tei.workbook.WBFormat')
    @patch('xl2tei.workbook.Sheet')
    def test_wb_format(self, MockSheet, MockWBFormat):
        wb = Workbook(self.test_file)
        self.assertEqual(MockSheet.call_count, 11)
        self.assertEqual(MockWBFormat.call_count, 1)
        self.assertNotEqual(wb.wbformat, None)
        return
