from django.test import TestCase

import xlrd
from ..sheet  import Sheet
from ..comments import Comments

class SheetTestCase(TestCase):
    def setUp(self):
        wb = xlrd.open_workbook('xl2tei/tests/Snake_23_1_11.xls',formatting_info=True)
        self.wb_sheet = wb.sheet_by_index(0)
        self.sheet = Sheet(self.wb_sheet, line_num_format=2)
        return

    def test_line_num_format(self):
        self.assertEqual(self.sheet .line_num_format, 2)
        return

    def test_comment_lines(self):
        expected_comment = Comments()
        expected_comment.append(self.wb_sheet.row(21))
        expected_comment.append(self.wb_sheet.row(22))
        self.assertEqual(self.sheet .comments.__dict__, expected_comment.__dict__)
        return
