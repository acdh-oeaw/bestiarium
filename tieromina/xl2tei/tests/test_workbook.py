from unittest.mock import PropertyMock, patch

from django.test import TestCase

from ..workbook import Workbook


@patch('xl2tei.workbook.WBFormat')
@patch('xl2tei.workbook.Sheet')
class WorkbookTestCase(TestCase):
    test_file = 'xl2tei/tests/Snake_23_1_11.xls'

    def test_wbfile(self, MockSheet, MockWBFormat):
        wb = Workbook(self.test_file)
        self.assertEqual(wb.wbfile, self.test_file)
        return

    def test_number_of_sheets(self, MockSheet, MockWBFormat):
        _ = Workbook(self.test_file)
        self.assertEqual(MockSheet.call_count, 11)
        self.assertEqual(MockWBFormat.call_count, 1)
        return
