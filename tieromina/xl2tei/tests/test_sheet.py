from django.test import TestCase
from unittest.mock import MagicMock, patch, call, ANY

import xlrd
from ..sheet  import Sheet


class SheetTestCase(TestCase):
    def setUp(self):
        wb = xlrd.open_workbook('xl2tei/tests/Snake_23_1_11.xls',formatting_info=True)
        self.wb_sheet = wb.sheet_by_index(0)      
        return

    
    @patch('xl2tei.comments.Comments.append')   
    def test_comment_lines(self, mock_append):
        sheet = Sheet(self.wb_sheet)
        self.assertEqual(mock_append.call_count, 2)
        expected_calls = [call(self.wb_sheet.row(21)), call(self.wb_sheet.row(22))]
        # Cannt match because the objects can't be compared on eqality
        actual_calls = mock_append.call_args_list
        self.assertEqual(str(actual_calls[0][0][0]), "[text:'Philological commentary' (XF:39), empty:'' (XF:21), text:'According to KAL 1, p. 3, SU 51/49+ cannot be considered “canonical, but are merely very close to the canonical series (cf. ibd, p. 6, fn. 57).' (XF:39), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21)]")
        self.assertEqual(str(actual_calls[1][0][0]),"[empty:'' (XF:21), empty:'' (XF:21), text:'gerû “to be hostile, to start a lawsuit”, “to bring suit and complain against” (CAD G: 61-62). The translation “who is litigating” is borrowed from CCP 3.5.22.A.b.' (XF:40), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21), empty:'' (XF:21)]")       
        return
