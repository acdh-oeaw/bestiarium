from unittest.mock import patch
from xml.etree import ElementTree as ET

from django.test import TestCase

from ..omen import Omen
from ..sheet import Sheet
from ..util import pretty_print
from ..workbook import Style

NS = {'ns': 'http://www.tei-c.org/ns/1.0'}


class OmenTestCase(TestCase):
    def setUp(self):

        with open('omens/tests/test_data/styles.xml', 'r') as f:
            style_xml = f.read()

        self.style = Style(style_xml)
        self.shared_strings_xml = ET.parse(
            'omens/tests/test_data/sharedStrings.xml').getroot()

    def test_omen_div(self):
        sheet = Sheet(
            sheet_xml=ET.parse('omens/tests/test_data/sheet1.xml').getroot(),
            name='test',
            style=self.style,
            shared_strings=self.shared_strings_xml)
        omen = Omen(sheet)
        print(omen.omen_name)
        with patch('omens.models.Omen.objects') as MockDB:
            tei = omen.export_to_tei(chapter='Whatever')
