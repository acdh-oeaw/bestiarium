from unittest.mock import MagicMock, patch
from xml.etree import ElementTree as ET

from django.test import TestCase

from ..omen import Omen
from ..sheet import Sheet
from ..util import pretty_print
from ..workbook import Style

NS = {'tei': 'http://www.tei-c.org/ns/1.0'}


class OmenTestCase(TestCase):
    def setUp(self):
        pass

    def test_omen_div(self):
        with open('omens/tests/test_data/styles.xml', 'r') as f:
            style_xml = f.read()

        self.style = Style(style_xml)
        self.shared_strings_xml = ET.parse(
            'omens/tests/test_data/sharedStrings.xml').getroot()

        sheet = Sheet(
            name='test',
            sheet_xml=ET.parse('omens/tests/test_data/sheet1.xml').getroot(),
            style=self.style,
            shared_strings=self.shared_strings_xml)
        omen = Omen(sheet)

        with patch(
                'omens.models.Witness.objects.get_or_create',
                MagicMock(return_value=(None, False))):
            with patch(
                    'omens.models.Omen.objects.get_or_create',
                    MagicMock(return_value=(None, False))):
                score = omen.export_to_tei(chapter='Whatever').find(
                    'div[@type="score"]', NS)

        pretty_print(score)
