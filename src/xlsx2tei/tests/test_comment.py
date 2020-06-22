from unittest import TestCase
from unittest.mock import patch
from xml.etree import ElementTree as ET

from ..comment import Comment, CommentRow
from ..namespaces import NS

ss_xml = ET.parse('xlsx2tei/test_data/sharedStrings.xml')
shared_strings = ss_xml.findall('spreadsheetml:si', NS)


class CommentRowTestCase(TestCase):
    @patch('xlsx2tei.sheet.Sheet')
    def setUp(self, MockSheet):
        sheet_xml = ET.parse('xlsx2tei/test_data/sheet1.xml').getroot()
        self.row1 = CommentRow(
            sheet=MockSheet(),
            xml=sheet_xml.find(
                'spreadsheetml:sheetData/spreadsheetml:row[@r="22"]', NS))
        self.row2 = CommentRow(
            sheet=MockSheet(),
            xml=sheet_xml.find(
                'spreadsheetml:sheetData/spreadsheetml:row[@r="23"]', NS))

    @patch('xlsx2tei.cell.Cell.shared_strings', shared_strings)
    def test_is_comment(self):
        self.assertIs(Comment.is_comment(self.row1), True)
        self.assertIs(Comment.is_comment(self.row2), False)

    @patch('xlsx2tei.cell.Cell.shared_strings', shared_strings)
    def test_marked_up_text(self):
        self.row1.marked_up_text
        self.row2.marked_up_text
