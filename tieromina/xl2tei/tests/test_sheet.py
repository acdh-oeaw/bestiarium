from django.test import TestCase
from unittest.mock import patch, call, ANY, PropertyMock

import xlrd
from ..sheet  import Sheet


@patch('xl2tei.comments.Comments.append')
class SheetTestCase(TestCase):
    def setUp(self):
        wb = xlrd.open_workbook('xl2tei/tests/Snake_23_1_11.xls',formatting_info=True)
        self.wb_sheet = wb.sheet_by_index(2)      
        return

    @patch('xl2tei.wbformat.WBFormat')
    @patch('xl2tei.wbformat.WBFormat.is_line_num')
    def test_comment_lines(self, MockFormat, mock_line_num, mock_comment):
        sheet = Sheet(self.wb_sheet, wbformat=MockFormat())
        self.assertEqual(mock_comment.call_count, 6)
        expected_calls_comments = [call(self.wb_sheet.row(21)), call(self.wb_sheet.row(22))]
        # Cannt match because the objects can't be compared on eqality
        actual_calls = mock_comment.call_args_list
        self.assertEqual(str(actual_calls[0][0][0]), str(self.wb_sheet.row(19)))
        self.assertEqual(str(actual_calls[1][0][0]), str(self.wb_sheet.row(20)))
        self.assertEqual(str(actual_calls[2][0][0]), str(self.wb_sheet.row(21)))
        self.assertEqual(str(actual_calls[3][0][0]), str(self.wb_sheet.row(22)))
        self.assertEqual(str(actual_calls[4][0][0]), str(self.wb_sheet.row(23)))
        self.assertEqual(str(actual_calls[5][0][0]), str(self.wb_sheet.row(24)))
        return

    @patch('xl2tei.sheet.Sheet.read_score')   
    def test_score_lines(self, mock_score, mock_comment):
        sheet = Sheet(self.wb_sheet)
        self.assertEqual(mock_score.call_count, 8)
        expected_calls_comments = [call(self.wb_sheet.row(21)), call(self.wb_sheet.row(22))]
        # Cannt match because the objects can't be compared on eqality
        actual_calls = mock_score.call_args_list
        self.assertEqual(str(actual_calls[0][0][0]), str(self.wb_sheet.row(2)))
        self.assertEqual(str(actual_calls[1][0][0]), str(self.wb_sheet.row(3)))
        self.assertEqual(str(actual_calls[2][0][0]), str(self.wb_sheet.row(4)))
        self.assertEqual(str(actual_calls[3][0][0]), str(self.wb_sheet.row(5)))
        self.assertEqual(str(actual_calls[4][0][0]), str(self.wb_sheet.row(6)))
        self.assertEqual(str(actual_calls[5][0][0]), str(self.wb_sheet.row(7)))
        self.assertEqual(str(actual_calls[6][0][0]), str(self.wb_sheet.row(8)))
        self.assertEqual(str(actual_calls[7][0][0]), str(self.wb_sheet.row(9)))
        return


    @patch('xlrd.sheet.Sheet.name', new_callable=PropertyMock, return_value='23.11')
    def test_simple_omen_name_with_tradition(self, mock_sheet_name, mock_comment):
        sheet = Sheet(self.wb_sheet)
        self.assertEqual(sheet.omen_num, '11')
        self.assertEqual(sheet.tradition, '')
        self.assertEqual(sheet.chapter, '23')        
        self.assertEqual(sheet.omen_name, 'Omen 23.11')
        self.assertEqual(sheet.siglum, '')                        
        return

    @patch('xlrd.sheet.Sheet.name', new_callable=PropertyMock, return_value='32.N.1')
    def test_omen_name_with_tradition(self, mock_sheet_name, mock_comment):
        sheet = Sheet(self.wb_sheet)
        self.assertEqual(sheet.omen_num, '1')
        self.assertEqual(sheet.tradition, 'N')
        self.assertEqual(sheet.chapter, '32')        
        self.assertEqual(sheet.omen_name, 'Omen 32.N.1')
        self.assertEqual(sheet.siglum, '')        
        return


    @patch('xlrd.sheet.Sheet.name', new_callable=PropertyMock, return_value='32.N.K09507(2).4')
    def test_omen_name_with_tradition_and_siglum(self, mock_sheet_name, mock_comment):
        sheet = Sheet(self.wb_sheet)
        self.assertEqual(sheet.omen_num, '4')
        self.assertEqual(sheet.tradition, 'N')
        self.assertEqual(sheet.chapter, '32')        
        self.assertEqual(sheet.siglum, 'K09507(2)')
        self.assertEqual(sheet.omen_name, 'Omen 32.N.K09507(2).4')
        return

