'''
An xlsx Workbook
Thanks to https://gist.github.com/brendano/22764
'''
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from .sheet import Sheet

NS = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


class Workbook:
    '''
    Represents a workbook of Omens
    '''

    def __init__(self, wbfile):
        self.wbfile = wbfile
        self.z = ZipFile(wbfile)
        self.style = Style(self.z.read('xl/styles.xml'))
        ss_xml = ET.XML(self.z.read('xl/sharedStrings.xml'))
        self.shared_strings = ss_xml.findall('ns:si', NS)

    def get_sheets(self):
        '''
        yields the sheets present in the workbook
        '''
        wb_xml = ET.ElementTree(ET.fromstring(
            self.z.read("xl/workbook.xml"))).getroot()
        sheets = wb_xml.find('ns:sheets', NS)

        for sheet_num, elem in enumerate(sheets):
            sheet_xml = ET.XML(
                self.z.read(f'xl/worksheets/sheet{sheet_num+1}.xml'))
            yield Sheet(
                sheet_xml=sheet_xml,
                style=self.style,
                shared_strings=self.shared_strings)


class Style:
    '''
    Formatting information of a workbook
    '''

    def __init__(self, styles: bytes):
        styles_xml = ET.XML(styles)
        self.xfs = styles_xml.findall('ns:cellXfs/ns:xf', NS)
        self.fonts = styles_xml.findall('ns:fonts/ns:font', NS)
        self.fills = styles_xml.findall('ns:fills/ns:fill', NS)
