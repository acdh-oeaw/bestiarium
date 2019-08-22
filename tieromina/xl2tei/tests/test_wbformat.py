from unittest.mock import ANY, MagicMock, PropertyMock, call, patch

import xlrd
from django.test import TestCase

from ..wbformat import WBFormat


class WorkbookFormatTestCase(TestCase):
    def setUp(self):
        self.wb = xlrd.open_workbook('xl2tei/tests/Snake_23_1_11.xls',formatting_info=True)
        self.wb_format = WBFormat(self.wb)
        return
    
    def test_init(self):
        self.assertEqual(self.wb_format.xf_list, self.wb.xf_list)
        self.assertEqual(self.wb_format.font_list, self.wb.font_list)
        self.assertEqual(self.wb_format.colour_map, self.wb.colour_map)
        return

    def test_line_num(self):
        self.assertFalse(self.wb_format.is_line_num(self.wb.sheet_by_index(0).row(1)[0]))
        self.assertFalse(self.wb_format.is_line_num(self.wb.sheet_by_index(0).row(1)[2]))
        self.assertTrue(self.wb_format.is_line_num(self.wb.sheet_by_index(1).row(2)[2]))
        self.assertTrue(self.wb_format.is_line_num(self.wb.sheet_by_index(1).row(3)[16]))                
        return
