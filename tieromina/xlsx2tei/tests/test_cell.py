from pprint import pprint
from unittest.mock import PropertyMock, patch
from xml.etree import ElementTree as ET

from django.test import TestCase

from ..cell import Cell, FormattedText


class CellTestCase(TestCase):
    def test_simple_cell(self):
        cell = Cell('1')
        # self.assertEqual(cell.text[0]._asdict(), FormattedText(1)._asdict())
        self.assertIsNone(cell.font)
        self.assertIsNone(cell.background)
        pass
