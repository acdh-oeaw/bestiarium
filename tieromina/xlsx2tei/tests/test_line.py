from unittest import TestCase
from unittest.mock import patch
from xml.etree import ElementTree as ET

from ..line import Line, LineInfo
from ..namespaces import NS
from ..workbook import Style

ss_xml = ET.parse('test_data/sharedStrings.xml')
style = Style(ET.parse('test_data/styles.xml'))
shared_strings = ss_xml.findall('spreadsheetml:si', NS)


class LineInfoTestCase(TestCase):
    @patch('xlsx2tei.cell.Cell.style', style)
    @patch('xlsx2tei.sheet.Sheet')
    def setUp(self, MockSheet):
        sheet_xml = ET.parse('test_data/sheet1.xml').getroot()
        sheet4_xml = ET.parse('test_data/sheet4.xml').getroot()
        self.not_new_line = LineInfo(MockSheet(),
                                     sheet_xml.find('.//*[@r="A1"]', NS))

        self.line_num = LineInfo(MockSheet(),
                                 sheet_xml.find('.//*[@r="C3"]', NS))
        self.reverse_line = LineInfo(MockSheet(),
                                     sheet_xml.find('.//*[@r="C4"]', NS))
        self.broken_line = LineInfo(MockSheet(),
                                    sheet_xml.find('.//*[@r="C6"]', NS))
        self.column_and_line = LineInfo(MockSheet(),
                                        sheet_xml.find('.//*[@r="C8"]', NS))

        self.extra_info = LineInfo(MockSheet(),
                                   sheet4_xml.find('.//*[@r="W6"]', NS))

        self.column_and_broken_line = LineInfo(MockSheet(),
                                               sheet4_xml.find(
                                                   './/*[@r="O7"]', NS))

    @patch('xlsx2tei.cell.Cell.shared_strings', shared_strings)
    def test_label(self):
        self.assertEqual(self.line_num.label, '1')
        self.assertEqual(self.reverse_line.label, 'r. 13')
        self.assertEqual(self.broken_line.label, "18'")
        self.assertEqual(self.column_and_line.label, 'ii 17')
        self.assertEqual(self.extra_info.label, 'ii 21 (23.5*)')
        self.assertEqual(self.column_and_broken_line.label, 'ii 4\'')

    @patch('xlsx2tei.cell.Cell.shared_strings', shared_strings)
    def test_column(self):
        self.assertEqual(self.line_num.column, '')
        self.assertEqual(self.reverse_line.column, '')
        self.assertEqual(self.broken_line.column, "")
        self.assertEqual(self.column_and_line.column, 'ii')
        self.assertEqual(self.extra_info.column, 'ii')
        self.assertEqual(self.column_and_broken_line.column, 'ii')

    @patch('xlsx2tei.cell.Cell.shared_strings', shared_strings)
    def test_line_num(self):
        self.assertEqual(self.line_num.line_num, '1')
        self.assertEqual(self.reverse_line.line_num, '13')
        self.assertEqual(self.broken_line.line_num, '18')
        self.assertEqual(self.column_and_line.line_num, '17')
        self.assertEqual(self.extra_info.line_num, '21')
        self.assertEqual(self.column_and_broken_line.line_num, '4')

    @patch('xlsx2tei.cell.Cell.shared_strings', shared_strings)
    def test_reverse(self):
        self.assertEqual(self.line_num.reverse, False)
        self.assertEqual(self.reverse_line.reverse, True)
        self.assertEqual(self.broken_line.reverse, False)
        self.assertEqual(self.column_and_line.reverse, False)
        self.assertEqual(self.extra_info.reverse, False)
        self.assertEqual(self.column_and_broken_line.reverse, False)

    @patch('xlsx2tei.cell.Cell.shared_strings', shared_strings)
    def test_broken(self):
        self.assertEqual(self.line_num.broken, False)
        self.assertEqual(self.reverse_line.broken, False)
        self.assertEqual(self.broken_line.broken, True)
        self.assertEqual(self.column_and_line.broken, False)
        self.assertEqual(self.extra_info.broken, False)
        self.assertEqual(self.column_and_broken_line.broken, True)

    @patch('xlsx2tei.cell.Cell.shared_strings', shared_strings)
    def test_extra_info(self):
        self.assertEqual(self.line_num.extra_info, '')
        self.assertEqual(self.reverse_line.extra_info, '')
        self.assertEqual(self.broken_line.extra_info, '')
        self.assertEqual(self.column_and_line.extra_info, '')
        self.assertEqual(self.extra_info.extra_info, '(23.5*)')
        self.assertEqual(self.column_and_broken_line.extra_info, '')

    def test_is_new_line(self):
        self.assertTrue(LineInfo.is_new_line(self.line_num))
        self.assertTrue(LineInfo.is_new_line(self.reverse_line))
        self.assertTrue(LineInfo.is_new_line(self.broken_line))
        self.assertTrue(LineInfo.is_new_line(self.column_and_line))
        self.assertTrue(LineInfo.is_new_line(self.extra_info))
        self.assertTrue(LineInfo.is_new_line(self.column_and_broken_line))
        self.assertFalse(LineInfo.is_new_line(self.not_new_line))
