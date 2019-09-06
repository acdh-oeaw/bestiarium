from pprint import pprint
from unittest.mock import PropertyMock, patch
from xml.etree import ElementTree as ET

from django.test import TestCase

from ..cell import Cell, FormattedText

ET.register_namespace(
    'ns', 'http://schemas.openxmlformats.org/spreadsheetml/2006/main')
ET.register_namespace('nss', 'http://ns')


class CellTestCase(TestCase):
    def test_simple_cell(self):
        cell = Cell('1')
        # self.assertEqual(cell.text[0]._asdict(), FormattedText(1)._asdict())
        self.assertIsNone(cell.font)
        self.assertIsNone(cell.background)
        self.assertEqual(cell.text, [FormattedText('1')])
        pass

    def test_shared_string_single(self):
        # cell_content = ET.fromstring(
        #     '''{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si>
        #     <{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t>Omen 23.2</{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t>
        #     </{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si>'''
        # )
        cell_content = ET.XML('<si><t>Omen 23.2</t></si>')
        cell = Cell(cell_content)
        self.assertIsNone(cell.font)
        self.assertIsNone(cell.background)
        # self.assertEqual(cell.text, [FormattedText('Omen 23.2')])
