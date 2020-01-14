from typing import NamedTuple
from xml.etree import ElementTree as ET

from .namespaces import NS


class CellFormat(NamedTuple):
    '''
    Holds text cell_format properties
    at a cell level or within a cell
    '''
    bold: bool = False
    italics: bool = False
    subscript: bool = False
    superscript: bool = False
    color: str = None
    bgcolor: str = None


class Chunk(NamedTuple):
    '''
    Smallest unit of information in a cell with the same formatting
    '''
    text: str
    cell_format: CellFormat
    complete: bool = False  # whether this is the only chunk in the cell


class Cell:
    def __init__(self, sheet, cell_element):
        '''
        Returns a standalone cell object representation of the cell data
        '''
        self.sheet = sheet
        self.xml = cell_element
        self.address = cell_element.attrib.get('r')
        self.cell_format = self.extract_cell_format(cell_element)

    def __str__(self):
        return f'{self.sheet}, {self.address}'

    def __repr__(self):
        return f'{self.sheet}, {self.address}'

    @property
    def plain_text(self):
        '''
        Returns full text from the cell without formatting
        '''
        text = ''
        for chunk in self.cell_contents:
            text += chunk.text

        return text.strip()

    @property
    def is_not_empty(self):
        return len(self.plain_text) != 0

    @property
    def cell_contents(self) -> Chunk:
        if 't' in self.xml.attrib and self.xml.attrib['t'] == 's':
            for segment in self.formatted_cell_contents():
                yield segment
        else:
            # raw text element
            raw_text_elem = self.xml.find('spreadsheetml:v', NS)
            if raw_text_elem is not None:
                yield Chunk(
                    text=raw_text_elem.text,
                    cell_format=self.cell_format,
                    complete=True)

    @property
    def shared_strings(self):
        return self.sheet.shared_strings

    def formatted_cell_contents(self) -> Chunk:
        # shared string
        idx = int(self.xml.find('spreadsheetml:v', NS).text)
        si = self.shared_strings[idx]
        # Read si and related formatting
        if len(si) == 1 and si[0].tag.endswith('}t'):
            # only one "chunk" in the shared string
            # No extra formatting
            yield Chunk(
                text=si[0].text, cell_format=self.cell_format, complete=True)
        else:
            # multiple chunks and in-cell formatting
            for elem in si:  # r elements
                color_tag = elem.find('spreadsheetml:rPr/spreadsheetml:color',
                                      NS)
                color = color_tag.attrib.get(
                    'rgb') if color_tag is not None else None
                italics = True if elem.find(
                    './spreadsheetml:rPr/spreadsheetml:i',
                    NS) is not None else False
                boldface = True if elem.find(
                    './spreadsheetml:rPr/spreadsheetml:b',
                    NS) is not None else False

                subscript = True if elem.find(
                    'spreadsheetml:rPr/spreadsheetml:vertAlign[@val="subscript"]',
                    NS) is not None else False
                superscript = True if elem.find(
                    'spreadsheetml:rPr/spreadsheetml:vertAlign[@val="superscript"]',
                    NS) is not None else False
                fmt = CellFormat(
                    subscript=subscript,
                    superscript=superscript,
                    italics=italics,
                    bold=boldface,
                    color=color,
                    bgcolor=self.cell_format.bgcolor)

                yield Chunk(
                    text=elem.find('./spreadsheetml:t', NS).text,
                    cell_format=fmt)

    @property
    def style(self):
        return self.sheet.style

    def extract_cell_format(self, cell) -> CellFormat:
        '''
        returns a CellFormat tuple
        '''
        xf_idx = int(cell.attrib.get('s'))
        xf = self.style.xfs[xf_idx]
        font_idx = int(xf.attrib.get('fontId'))
        font = self.style.fonts[font_idx]
        italics = len(font.findall('spreadsheetml:i', NS)) == 1
        boldface = len(font.findall('spreadsheetml:b', NS)) == 1
        if font.find('spreadsheetml:color', NS) is not None:
            color = font.find('spreadsheetml:color', NS).attrib.get('rgb')
        else:

            color = None

        fill_idx = int(xf.attrib.get('fillId'))
        fill = self.style.fills[fill_idx]
        if fill.find('spreadsheetml:patternFill/spreadsheetml:fgColor',
                     NS) is not None:
            bgcolor = fill.find(
                'spreadsheetml:patternFill/spreadsheetml:fgColor',
                NS).attrib.get('rgb')
        else:
            bgcolor = None
        return CellFormat(
            bold=boldface, italics=italics, color=color, bgcolor=bgcolor)
