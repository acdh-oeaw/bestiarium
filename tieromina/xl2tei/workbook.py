import logging
from xml.dom import minidom
from xml.etree import ElementTree as ET
import xlrd
from .wbformat import WBFormat

from .sheet import Sheet


def pretty_print(root):
    '''
    pretty prints xml elements
    '''
    dom = minidom.parseString(ET.tostring(root))
    pretty_root = dom.toprettyxml(indent="  ", newl="\n")
    return pretty_root


NAMESPACES = {
    'tei': 'http://www.tei-c.org/ns/1.0',
    'xml': 'http://www.w3.org/XML/1998/namespace'
}

for namespace, uri in NAMESPACES.items():
    ET.register_namespace(namespace, uri)


class Workbook:
    '''
    Represents an Excel workbook
    containing one or more omens
    from a chapter
    '''
    def __init__(self, wbfile):
        self.wbfile = wbfile
        try:
            self.book = xlrd.open_workbook(wbfile, formatting_info=True)
        except Exception as e:
            raise e

        self.wbformat = WBFormat(self.book)
        self.omens = {}
        self.witnesses = {}
        self.chapter = None
        for sheet in self.book.sheets():
            omen = Sheet(sheet, self.wbformat)
            self.omens[omen.omen_name] = omen
            if not self.chapter:
                self.chapter = omen.omen_name.chapter

        self.convert_to_tei()

    def convert_to_tei(self):
        '''
        generates TEI representation
        by creating from scratch or
        editing to the existing TEI representation
        of this chapter
        '''
        self.tei = ''
        return

    def save_to_db(self, spreadsheet):
        logging.debug('Saving {} to the model'.format(spreadsheet))
        return
