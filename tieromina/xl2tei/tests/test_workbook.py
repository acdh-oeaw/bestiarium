from django.test import TestCase

import xlrd
from ..workbook import Workbook

class WorkbookTestCase(TestCase):
    def setUp(self):
        self.wb = Workbook('xl2tei/tests/Snake_23_1_11.xls')
        return

    def test_wb_format(self):
        self.assertNotEqual(self.wb.wbformat, None)
        return
