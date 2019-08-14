from ..wbformat import WBFormat
from unittest.mock import patch, call, ANY, PropertyMock, MagicMock
from django.test import TestCase
import xlrd

class WorkbookFormatTestCase(TestCase):
    
    def setUp(self):
        self.wbfmt = WBFormat(xf_list=[1,2,3],
                              font_list=['a', 'b', 'c'])
        
    @patch('xlrd.sheet.Cell.xf_index', new_callable=PropertyMock, return_value=0)
    @patch('xlrd.formatting.XF.font_index', new_callable=PropertyMock, return_value=0)
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
