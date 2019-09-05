from typing import Any, NamedTuple
from xml.etree import ElementTree as ET

NS = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


class Cell:
    '''
    At the moment holds the XML for font, background and border properties of the cell
    '''

    ADDRESS, CONTENTS, FONT, BACKGROUND = 'address', 'contents', 'font', 'background'

    def __init__(self, contents, font=None, background=None):
        self.catchall = contents  # just a holder for what comes in
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
                    fmt=Fmt(color=self.font_color, bgcolor=self.bgcolor)))
        elif isinstance(self.catchall, ET.Element):
            # si contains only one t tag
            if len(self.catchall) == 1 and self.catchall[0].tag.endswith('}t'):
                self.text.append(
                    FormattedText(text=self.catchall[0].text, fmt=Fmt()))
            else:
                # si -> r -> rPr (format), t (text)
                for elem in self.catchall:  # r
                    fmt = Fmt()
                    if elem.tag.endswith('}r'):
                        color_tag = elem.find('ns:rPr/ns:color', NS)
                        color = color_tag.attrib.get(
                            'rgb') if color_tag is not None else None
                        italics = True if elem.find('./ns:rPr/ns:i',
                                                    NS) else False
                        subscript = True if elem.find(
                            'ns:rPr/ns:vertAlign[@val="subscript"]',
                            NS) else False
                        superscript = True if elem.find(
                            'ns:rPr/ns:vertAlign[@val="superscript"]',
                            NS) else False

                        text = elem.find('./ns:t', NS).text
                        fmt = Fmt(
                            color=color,
                            italics=italics,
                            subscript=subscript,
                            superscript=superscript)
                        self.text.append(FormattedText(text=text, fmt=fmt))

    @property
    def font_color(self):
        if self.font:
            color = self.font.find('ns:color', NS)
            if color:
                return color.attrib.get('rgb')

    @property
    def bgcolor(self):
        if self.background:
            color = self.background.find('ns:PatternFill/ns:fgColor', NS)
            if color:
                return color.attrib.get('rgb')

    def __str__(self):
        return str(self.text)

    def __repr__(self):
        return str(len(self.text))


class Fmt(NamedTuple):
    '''
    Holds text format properties
    '''
    color: str = None
    bgcolor: str = None
    italics: bool = None
    subscript: bool = None
    superscript: bool = None


class FormattedText(NamedTuple):
    '''
    Holds a few formatting properties
    '''
    text: str
    fmt: 'Fmt' = Fmt()
