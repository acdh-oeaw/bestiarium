from django.test import TestCase
from unittest.mock import patch, call, ANY, PropertyMock

import xlrd
from ..sheet  import Sheet


class SheetTestCase(TestCase):
    def setUp(self):
        wb = xlrd.open_workbook('xl2tei/tests/Snake_23_1_11.xls',formatting_info=True)
        self.wb_sheet = wb.sheet_by_index(2)      
        return

    
    @patch('xl2tei.comments.Comments.append')   
    def test_comment_lines(self, mock_append):
        sheet = Sheet(self.wb_sheet)
        self.assertEqual(mock_append.call_count, 6)
        expected_calls = [call(self.wb_sheet.row(21)), call(self.wb_sheet.row(22))]
        # Cannt match because the objects can't be compared on eqality
        actual_calls = mock_append.call_args_list
        self.assertEqual(str(actual_calls[0][0][0]), str(self.wb_sheet.row(19)))
        self.assertEqual(str(actual_calls[1][0][0]), str(self.wb_sheet.row(20)))
        self.assertEqual(str(actual_calls[2][0][0]), str(self.wb_sheet.row(21)))
        self.assertEqual(str(actual_calls[3][0][0]), str(self.wb_sheet.row(22)))
        self.assertEqual(str(actual_calls[4][0][0]), str(self.wb_sheet.row(23)))
        self.assertEqual(str(actual_calls[5][0][0]), str(self.wb_sheet.row(24)))
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

