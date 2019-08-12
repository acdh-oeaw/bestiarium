from django.test import TestCase

import xlrd
from ..workbook import Workbook

class WorkbookTestCase(TestCase):
    def setUp(self):
        self.wb = Workbook('xl2tei/tests/Snake_23_1_11.xls')
        return

    def test_line_num_format(self):
        self.assertEqual(self.wb.line_num_format, 2)
        return
