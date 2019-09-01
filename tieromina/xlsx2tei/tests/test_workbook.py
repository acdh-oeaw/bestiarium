from unittest.mock import PropertyMock, patch

from django.test import TestCase

from ..workbook import Workbook


class WorkbookTestCase(TestCase):
    test_file = 'xl2tei/tests/Snake_23_1_11.xls'

    def test_wbfile(self):
        wb = Workbook(self.test_file)
        self.assertEqual(wb.wbfile, self.test_file)
        return
