'''
Reads an xlsx Workbook
Thanks to https://gist.github.com/brendano/22764
'''
import itertools
import logging
import os
import re
import sys
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from .sheet import OmenSheet

NS = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


class Workbook:
    '''
    Represents a workbook of Omens
    '''

    def __init__(self, wbfile):
        self.wbfile = wbfile
        self.z = ZipFile(wbfile)
        wb_xml = ET.ElementTree(ET.fromstring(
            self.z.read("xl/workbook.xml"))).getroot()
        _sheets = wb_xml.find('ns:sheets', NS)
        self.sheets = {
            elem.attrib.get('sheetId'): elem.attrib.get('name')
            for elem in _sheets
        }
        ss_xml = ET.XML(self.z.read('xl/sharedStrings.xml'))
        self.shared_strings = ss_xml.findall('ns:si', NS)
        styles_xml = ET.XML(self.z.read('xl/styles.xml'))
        self.cell_formats = styles_xml.findall('ns:cellXfs/ns:xf', NS)
        self.fonts = styles_xml.findall('ns:fonts/ns:font', NS)
        self.background = styles_xml.findall('ns:fills/ns:fill', NS)

    # self.ss_list = ET.XML(ss_xml).findall(n('si'))
    def get_sheet(self, sheet_num: int):
        '''
        Returns the sheet XML given the sheet number
        '''
        try:
            sheet_xml = self.z.read(f'xl/worksheets/sheet{sheet_num}.xml')
            return Sheet(workbook=self, sheet_xml=sheet_xml)
        except KeyError:
            logging.warning('Sheet "%s" not found!', sheet_num)

    def get_tei(self):
        '''
        Returns the TEI of the sheet
        '''
        # Form header
        for sheet_id, sheet_name in self.sheets.items():
            sheet = self.get_sheet(sheet_id)

        return
