from unittest.mock import patch
from xml.etree import ElementTree as ET

from django.test import TestCase

from ..chapter import Chapter
from ..models import Chapter as DB
from ..namespaces import get_attribute
from ..util import pretty_print

NS = {
    'ns': 'http://www.tei-c.org/ns/1.0',
    'xml': 'http://www.w3.org/XML/1998/namespace'
}

ET.register_namespace('ns', NS['ns'])
ET.register_namespace('xml', NS['xml'])


class WorkbookTestCase(TestCase):

    test_file = 'omens/tests/test_data/Snakes 23.1-11.xlsx'

    def test_chapter(self):
        wb = Chapter()
        tei = wb.add_workbook(self.test_file)
        db_object = DB.objects.get(chapter_name='23')
        assert str(db_object) == 'Chapter 23'

    def test_witnesses(self):
        ch = Chapter()
        ch.add_workbook(self.test_file)
        tei = ET.fromstring(ch.tei)
        listwit = tei.find('.//ns:listWit', NS)
        assert (listwit is not None)
        witness_list = []
        for elem in listwit:
            wit_id = elem.get(get_attribute('id', NS['xml']))
            assert wit_id not in witness_list
            witness_list.append(wit_id)

        # pretty_print(tei)
