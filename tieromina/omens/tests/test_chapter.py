from unittest.mock import patch

from django.test import TestCase

from ..chapter import Chapter

NS = {'ns': 'http://www.tei-c.org/ns/1.0'}


class WorkbookTestCase(TestCase):

    test_file = 'omens/tests/test_data/Snakes 23.1-11.xlsx'

    def test_chapter(self):
        wb = Chapter()
        tei = wb.export_to_tei(self.test_file)
        print(tei)
