from unittest import TestCase
from unittest.mock import patch
from xml.etree import ElementTree as ET

from ..comment import Comment
from ..namespaces import NS

ss_xml = ET.parse('test_data/sharedStrings.xml')
shared_strings = ss_xml.findall('spreadsheetml:si', NS)


class CommentTestCase(TestCase):
    @patch('xlsx2tei.cell.Cell.shared_strings', shared_strings)
    def test_is_comment(self):
        pass
