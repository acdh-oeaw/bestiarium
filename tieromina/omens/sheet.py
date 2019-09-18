'''
A single sheet from a workbook
'''
from collections import defaultdict
from xml.etree import ElementTree as ET

from .cell import Cell, Format, Token

NS = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


class Sheet:
    '''
    A single sheet from a workbook
    Initialised with shared styles and strings
    '''

    def __init__(self, *, sheet_xml, style, shared_strings):
        self.sheet = sheet_xml
        self.style = style
        self.shared_strings = shared_strings

    def get_cell_at(self, address: str) -> Cell:
        '''
        Returns cell at a given location (like A23)
        '''
        c = self.sheet.find(f'.//*[@r="{address}"]')
        if not c:
            return Cell(address)
        return self._get_cell_from_element(c)

    def get_rows(self):
        '''
        Yields the row name and the row
        '''
        rows = self.sheet.findall('ns:sheetData/ns:row', NS)
        for row in rows:
            row_name = row.attrib.get('r')
            yield row_name, row

    def get_cells(self, row) -> Cell:
        '''
        Yields standalone cell instances representing the contents of a cell
        '''
        elems = row.findall('ns:c', NS)
        for c in elems:
            cell = self._get_cell_from_element(c)
            yield cell

    def is_empty_row(self, row) -> bool:
        '''
        Returns True if the row is empty
        '''
        for cell in self.get_cells(row):
            if cell.full_text:
                return False

        return True

    def _get_cell_from_element(self, cell_element):
        '''
        Returns a standalone cell object representation of the cell data
        '''
        cell = Cell(cell_element.attrib.get('r'))
        for token in self._get_tokens(cell_element):
            cell.add_token(token)

        return cell

    def _get_tokens(self, cell_element):
        '''
        Yields units of text along with their formatting (Token instance)
        TODO: preserve space tag in shared strings
        '''
        if not cell_element:
            return
        cell_format = self._extract_cell_format(cell_element)

        if 't' in cell_element.attrib and cell_element.attrib['t'] == 's':
            # shared string
            idx = int(cell_element.find('ns:v', NS).text)
            si = self.shared_strings[idx]
            # Read si and related formatting
            if len(si) == 1 and si[0].tag.endswith('}t'):
                # only one "token" in the shared string
                # No extra formatting
                yield Token(text=si[0].text, format=cell_format, complete=True)
            else:
                # multiple tokens and in-cell formatting
                for elem in si:  # r elements
                    color_tag = elem.find('ns:rPr/ns:color', NS)
                    color = color_tag.attrib.get(
                        'rgb') if color_tag is not None else None
                    italics = True if elem.find('./ns:rPr/ns:i',
                                                NS) is not None else False
                    boldface = True if elem.find('./ns:rPr/ns:b',
                                                 NS) is not None else False

                    subscript = True if elem.find(
                        'ns:rPr/ns:vertAlign[@val="subscript"]',
                        NS) is not None else False
                    superscript = True if elem.find(
                        'ns:rPr/ns:vertAlign[@val="superscript"]',
                        NS) is not None else False
                    fmt = Format(
                        subscript=subscript,
                        superscript=superscript,
                        italics=italics,
                        bold=boldface,
                        color=color,
                        bgcolor=cell_format.bgcolor)

                    yield Token(text=elem.find('./ns:t', NS).text, format=fmt)

        else:
            # raw text element
            raw_text_elem = cell_element.find('ns:v', NS)
            if raw_text_elem is not None:
                yield Token(
                    text=raw_text_elem.text, format=cell_format, complete=True)

    def _extract_cell_format(self, cell) -> Format:
        '''
        returns a Format tuple
        '''
        xf_idx = int(cell.attrib.get('s'))
        xf = self.style.xfs[xf_idx]
        font_idx = int(xf.attrib.get('fontId'))
        font = self.style.fonts[font_idx]
        italics = font.find('ns:i', NS) is not None
        boldface = font.find('ns:b', NS) is not None
        if font.find('ns:color', NS) is not None:
            color = font.find('ns:color', NS).attrib.get('rgb')
        else:
            color = None

        fill_idx = int(xf.attrib.get('fillId'))
        fill = self.style.fills[fill_idx]
        if fill.find('ns:patternFill/ns:fgColor', NS) is not None:
            bgcolor = fill.find('ns:patternFill/ns:fgColor',
                                NS).attrib.get('rgb')
        else:
            bgcolor = None
        return Format(
            bold=boldface, italics=italics, color=color, bgcolor=bgcolor)
