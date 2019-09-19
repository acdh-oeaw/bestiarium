from unittest.mock import patch
from xml.etree import ElementTree as ET

from django.test import TestCase

from ..chapter import pretty_print
from ..omen import Omen
from ..sheet import Sheet
from ..workbook import Style

NS = {'ns': 'http://www.tei-c.org/ns/1.0'}


class OmenTestCase(TestCase):
    def setUp(self):
        sheet_xml = ET.parse('omens/tests/test_data/sheet1.xml').getroot()
        with open('omens/tests/test_data/styles.xml', 'r') as f:
            style_xml = f.read()

        style = Style(style_xml)
        shared_strings_xml = ET.parse(
            'omens/tests/test_data/sharedStrings.xml').getroot()
        sheet = Sheet(
            sheet_xml=sheet_xml,
            style=style,
            shared_strings=shared_strings_xml)
        self.omen = Omen(sheet)

    def test_omen_div(self):
        omen_div = pretty_print(self.omen.tei_div)
        print(omen_div)
