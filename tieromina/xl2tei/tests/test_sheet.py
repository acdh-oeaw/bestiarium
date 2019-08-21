from django.test import TestCase
from unittest.mock import patch, call, ANY, PropertyMock

import xlrd
from ..sheet  import Sheet
from pprint import pprint


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


    @patch('xlrd.sheet.Sheet.name', new_callable=PropertyMock, return_value='23.11')
    def test_simple_omen_name_with_tradition(self, mock_sheet_name):
        sheet = Sheet(self.wb_sheet)
        self.assertEqual(sheet.omen_num, '11')
        self.assertEqual(sheet.tradition, '')
        self.assertEqual(sheet.chapter, '23')        
        self.assertEqual(sheet.omen_name, 'Omen 23.11')
        self.assertEqual(sheet.siglum, '')                        
        return

    @patch('xlrd.sheet.Sheet.name', new_callable=PropertyMock, return_value='32.N.1')
    def test_omen_name_with_tradition(self, mock_sheet_name):
        sheet = Sheet(self.wb_sheet)
        self.assertEqual(sheet.omen_num, '1')
        self.assertEqual(sheet.tradition, 'N')
        self.assertEqual(sheet.chapter, '32')        
        self.assertEqual(sheet.omen_name, 'Omen 32.N.1')
        self.assertEqual(sheet.siglum, '')        
        return


    @patch('xlrd.sheet.Sheet.name', new_callable=PropertyMock, return_value='32.N.K09507(2).4')
    def test_omen_name_with_tradition_and_siglum(self, mock_sheet_name):
        sheet = Sheet(self.wb_sheet)
        self.assertEqual(sheet.omen_num, '4')
        self.assertEqual(sheet.tradition, 'N')
        self.assertEqual(sheet.chapter, '32')        
        self.assertEqual(sheet.siglum, 'K09507(2)')
        self.assertEqual(sheet.omen_name, 'Omen 32.N.K09507(2).4')
        return

