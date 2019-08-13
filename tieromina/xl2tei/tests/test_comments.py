from django.test import TestCase
import xlrd

from ..comments import Comments


class TabletTestCase(TestCase):
    def setUp(self):        
        wb = xlrd.open_workbook('xl2tei/tests/Snake_23_1_11.xls',formatting_info=True)
        self.sheet = wb.sheet_by_index(0)
        self.comment = Comments()
        return


    def test_empty_comment(self):
        self.assertEqual(self.comment.label, 'Philological Commentary')
        self.assertEqual(self.comment.reference, '')
        self.assertEqual(self.comment.text, [])
        return
        
