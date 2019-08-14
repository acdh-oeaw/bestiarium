from django.test import TestCase

import xlrd
from ..sheet  import Sheet
from ..comments import Comments

class SheetTestCase(TestCase):
    def setUp(self):
        wb = xlrd.open_workbook('xl2tei/tests/Snake_23_1_11.xls',formatting_info=True)
        self.wb_sheet = wb.sheet_by_index(0)      
        self.sheet = Sheet(self.wb_sheet)
        return

    def test_comment_lines(self):
        self.assertEqual(self.sheet.comments.text[0], 'According to KAL 1, p. 3, SU 51/49+ cannot be considered “canonical, but are merely very close to the canonical series (cf. ibd, p. 6, fn. 57).')
        self.assertEqual(self.sheet.comments.text[1],'gerû “to be hostile, to start a lawsuit”, “to bring suit and complain against” (CAD G: 61-62). The translation “who is litigating” is borrowed from CCP 3.5.22.A.b.')
        return

