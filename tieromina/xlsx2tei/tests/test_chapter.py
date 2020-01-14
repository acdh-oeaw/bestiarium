from unittest import TestCase
from unittest.mock import patch
from xml.etree import ElementTree as ET

from ..chapter import Chapter
from ..namespaces import NS
from ..workbook import Workbook

ss_xml = ET.parse('xlsx2tei/test_data/sharedStrings.xml')
shared_strings = ss_xml.findall('spreadsheetml:si', NS)


class ChapterTestCase(TestCase):
    def setUp(self):
        self.chapter = Chapter()

    def test_add_from_workbook(self):
        test_file = 'xlsx2tei/test_data/Snakes 23.1-11.xlsx'
        self.chapter.add_from_workbook(Workbook(test_file))
