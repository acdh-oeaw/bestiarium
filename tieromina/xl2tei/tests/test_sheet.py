from pprint import pprint
from unittest.mock import ANY, PropertyMock, call, patch

import xlrd
from django.test import TestCase

from ..sheet import Sheet


class SheetTestCase(TestCase):
    def setUp(self):
        wb = xlrd.open_workbook('xl2tei/tests/Snake_23_1_11.xls',formatting_info=True)
        self.wb_sheet = wb.sheet_by_index(2)      
        return

    @patch('xl2tei.wbformat.WBFormat')
    @patch('xl2tei.wbformat.WBFormat.is_line_num')
    @patch('xl2tei.comments.Comments')
    def test_comment_lines(self, mock_line_num, MockFormat, MockComment):
        sheet = Sheet(self.wb_sheet, wbformat=MockFormat())
        
        return

    @patch('xl2tei.sheet.Sheet.read_score')   
    def test_score_lines(self, mock_score):
        sheet = Sheet(self.wb_sheet)
        self.assertEqual(mock_score.call_count, 1)
        # Cannt match because the objects can't be compared on eqality
        actual_calls = mock_score.call_args_list[0][0][0]
        self.assertEqual(str(actual_calls[0]), str(self.wb_sheet.row(2)))
        self.assertEqual(str(actual_calls[1]), str(self.wb_sheet.row(3)))
        self.assertEqual(str(actual_calls[2]), str(self.wb_sheet.row(4)))
        self.assertEqual(str(actual_calls[3]), str(self.wb_sheet.row(5)))
        self.assertEqual(str(actual_calls[4]), str(self.wb_sheet.row(6)))
        self.assertEqual(str(actual_calls[5]), str(self.wb_sheet.row(7)))
        self.assertEqual(str(actual_calls[6]), str(self.wb_sheet.row(8)))
        self.assertEqual(str(actual_calls[7]), str(self.wb_sheet.row(9)))
        return
