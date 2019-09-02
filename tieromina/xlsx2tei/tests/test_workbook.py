from unittest.mock import PropertyMock, patch

from django.test import TestCase

from ..workbook import Workbook


class WorkbookTestCase(TestCase):
    test_file = 'xlsx2tei/tests/Snakes 23.1-11.xlsx'

    def test_wbfile(self):
        wb = Workbook(self.test_file)
        self.assertEqual(wb.wbfile, self.test_file)
        self.assertIsNotNone(wb.z)
        self.assertEqual(len(wb.sheets), 11)
        self.assertEqual(len(wb.shared_strings), 570)
        return

    def test_get_sheet(self):
        wb = Workbook(self.test_file)
        sheet = wb.get_sheet(1)
        self.assertIsNotNone(sheet)
        sheet = wb.get_sheet(100)
        self.assertIsNone(sheet)
        # TODO: Test the printed warning somehow
