'''
An xlsx Workbook
Thanks to https://gist.github.com/brendano/22764
'''
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from .namespaces import NS
from .sheet import Sheet


class Workbook:
    '''
    Represents a workbook of Omens
    '''
    def __init__(self, wbfile):
        self.wbfile = wbfile
        self.z = ZipFile(wbfile)
        self.style = Style(self.z.read('xl/styles.xml'))
        ss_xml = ET.XML(self.z.read('xl/sharedStrings.xml'))
        self.shared_strings = ss_xml.findall('spreadsheetml:si', NS)

    def get_sheets(self):
        '''
        yields the sheets present in the workbook
        '''
        wb_xml = ET.ElementTree(ET.fromstring(
            self.z.read("xl/workbook.xml"))).getroot()
        sheets = wb_xml.find('spreadsheetml:sheets', NS)

        for sheet_num, elem in enumerate(sheets):
            sheet_name = elem.attrib.get('name')
            sheet_xml = ET.XML(
                self.z.read(f'xl/worksheets/sheet{sheet_num+1}.xml'))
            yield Sheet(name=sheet_name,
                        sheet_xml=sheet_xml,
                        style=self.style,
                        shared_strings=self.shared_strings)


class Style:
    '''
    Formatting information of a workbook
    '''
    def __init__(self, styles: bytes):
        styles_xml = ET.XML(styles)
        self.xfs = styles_xml.findall('spreadsheetml:cellXfs/spreadsheetml:xf',
                                      NS)
        self.fonts = styles_xml.findall(
            'spreadsheetml:fonts/spreadsheetml:font', NS)
        self.fills = styles_xml.findall(
            'spreadsheetml:fills/spreadsheetml:fill', NS)
