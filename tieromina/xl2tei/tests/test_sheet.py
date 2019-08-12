from django.test import TestCase

import xlrd
from ..sheet import Sheet

class SheetTestCase(TestCase):
    def setUp(self):
        wb = xlrd.open_workbook('xl2tei/tests/Snake_23_1_11.xls',formatting_info=True)
        self.sheet = Sheet(wb.sheet_by_index(0), line_num_format=2)
        return

    def test_line_num_format(self):
        self.assertEqual(self.sheet.line_num_format, 2)
        return

