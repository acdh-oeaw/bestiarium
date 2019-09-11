from pprint import pprint
from unittest.mock import PropertyMock, patch
from xml.etree import ElementTree as ET

from django.test import TestCase

from ..cell import Cell

NS = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


class CellTestCase(TestCase):
    def setUp(self):
        ss_xml = ET.parse('xlsx2tei/tests/sharedStrings.xml').getroot()
        self.shared_strings = ss_xml.findall('ns:si', NS)

    def test_multiple_tokens_in_cell(self):
        cell = Cell(self.shared_strings[13])
        self.assertEqual(str(cell.tokens[0]), 'ŠUB-')
        self.assertEqual(str(cell.tokens[1]), 'ut')
        self.assertTrue(cell.tokens[1].italics)
        self.assertFalse(cell.tokens[0].italics)
