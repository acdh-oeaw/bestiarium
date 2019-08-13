from django.test import TestCase
import xlrd

from ..comments import Comments


class CommentsTestCase(TestCase):
    def setUp(self):
        wb = xlrd.open_workbook('xl2tei/tests/Snake_23_1_11.xls',formatting_info=True)
        self.sheet = wb.sheet_by_index(0)
        return
  
    def test_empty_comment(self):
        comments = Comments()
        self.assertEqual(comments.label, 'Philological Commentary')
        self.assertEqual(comments.reference, '')
        self.assertEqual(comments.text, [])
        return
    
    def test_one_line(self):
        comments = Comments()
        comments.append(self.sheet.row(21))
        self.assertEqual(comments.text, ['According to KAL 1, p. 3, SU 51/49+ cannot be considered “canonical, but are merely very close to the canonical series (cf. ibd, p. 6, fn. 57).'])
        self.assertEqual(len(comments.text), 1)
        return

    def test_multiple_lines(self):
        comments = Comments()
        comments.append(self.sheet.row(21))
        comments.append(self.sheet.row(22))
        self.assertEqual(comments.text[0], 'According to KAL 1, p. 3, SU 51/49+ cannot be considered “canonical, but are merely very close to the canonical series (cf. ibd, p. 6, fn. 57).')
        return
