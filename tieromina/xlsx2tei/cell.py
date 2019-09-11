'''
Represents information within a cell in an Omens workbook
'''
from typing import NamedTuple
from xml.etree import ElementTree as ET

NS = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


class Cell:
    '''
    At the moment holds the XML for font, background and border properties of the cell
    '''

    ADDRESS, CONTENTS, FONT, BACKGROUND = 'address', 'contents', 'font', 'background'

    def __init__(self, contents, font=None, background=None):
        self.catchall = contents  # just a holder for what comes in
        if isinstance(contents, ET.Element):
            # ET.dump(contents)
            pass
        self.font = font
        self.background = background
        self.text = []
        self.read()

    def read(self):
        '''
        Converts different parts of the formatted cell into a list of FormattedText objects
        '''
        self.text = []
        if isinstance(self.catchall, str):
            # number or something else, didn't come from SharedStrings
            self.text.append(
                FormattedText(
                    text=self.catchall,
                    fmt=Fmt(
                        color=self.font_color,
                        bgcolor=self.bgcolor,
                        italics=self.italics)))
        elif isinstance(self.catchall, ET.Element):
            # si contains only one t tag
            if len(self.catchall) == 1 and self.catchall[0].tag.endswith('}t'):
                self.text.append(FormattedText(text=self.catchall[0].text))
            else:
                # si -> r -> rPr (format), t (text)
                for elem in self.catchall:  # r
                    fmt = Fmt()
                    if elem.tag.endswith('}r'):
                        color_tag = elem.find('ns:rPr/ns:color', NS)
                        color = color_tag.attrib.get(
                            'rgb') if color_tag is not None else None
                        italics = True if elem.find('./ns:rPr/ns:i',
                                                    NS) is not None else False
                        subscript = True if elem.find(
                            'ns:rPr/ns:vertAlign[@val="subscript"]',
                            NS) is not None else False
                        superscript = True if elem.find(
                            'ns:rPr/ns:vertAlign[@val="superscript"]',
                            NS) is not None else False

                        text = elem.find('./ns:t', NS).text
                        fmt = Fmt(
                            color=color,
                            italics=italics,
                            subscript=subscript,
                            superscript=superscript)
                        self.text.append(FormattedText(text=text, fmt=fmt))

    @property
    def italics(self):
        if self.font:
            return self.font.find('ns:i', NS) is not None
        return False

    @property
    def font_color(self):
        if self.font:
            color = self.font.find('ns:color', NS)
            if color is not None:
                return color.attrib.get('rgb')

    @property
    def bgcolor(self):
        if self.background:
            color = self.background.find('ns:PatternFill/ns:fgColor', NS)
            if color is not None:
                return color.attrib.get('rgb')

    def __str__(self):
        return str(self.text)


class Fmt(NamedTuple):
    '''
    Holds text format properties
    '''
    color: str = None
    bgcolor: str = None
    italics: bool = False
    subscript: bool = False
    superscript: bool = False


class FormattedText(NamedTuple):
    '''
    Holds a few formatting properties
    '''
    text: str
    fmt: 'Fmt' = Fmt()

    def __str__(self):
        return self.text

    @property
    def color(self):
        return self.fmt.color

    @property
    def bgcolor(self):
        return self.fmt.bgcolor

    @property
    def italics(self):
        return self.fmt.italics

    @property
    def subscript(self):
        return self.fmt.subscript

    @property
    def superscript(self):
        return self.fmt.superscript
