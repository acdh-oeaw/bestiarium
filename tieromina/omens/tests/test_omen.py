from unittest.mock import MagicMock, patch
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

    @patch('omens.models.Reconstruction.save', return_value=None)
    @patch('omens.models.Chapter', autospec=True)
    @patch(
        'omens.models.Omen.objects.get_or_create', return_value=(None, False))
    @patch('omens.models.Witness.objects.get_or_create', autospec=True)
    def test_omen_div(self, MockWit, MockOmen, MockChap, MockRecon):
        sheet = Sheet(
            sheet_xml=ET.parse('omens/tests/test_data/sheet1.xml').getroot(),
            name='test',
            style=self.style,
            shared_strings=self.shared_strings_xml)
        omen = Omen(sheet)
        print(omen.omen_name)
        tei = omen.export_to_tei(chapter_db=None)
        pretty_print(tei)
