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

    def __init__(self, contents, fmt=None):
        self.catchall = contents  # just a holder for what comes in
        if isinstance(contents, ET.Element):
            # ET.dump(contents)
            pass
        self.fmt = fmt
        self.tokens = []
        self.read()

    def read(self):
        '''
        Converts different parts of the formatted cell into a list of Token objects
        '''
        self.tokens = []
        if isinstance(self.catchall, str):
            # number or something else, didn't come from SharedStrings
            self.tokens.append(Token(text=self.catchall, fmt=self.fmt))
        elif isinstance(self.catchall, ET.Element):
            # si contains only one t tag
            if len(self.catchall) == 1 and self.catchall[0].tag.endswith('}t'):
                self.tokens.append(Token(text=self.catchall[0].text))
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
                            subscript=subscript,
                            superscript=superscript,
                            italics=italics)
                        self.tokens.append(Token(text=text, fmt=fmt))

    @property
    def italics(self) -> bool:
        return self.fmt.italics if self.fmt else False

    @property
    def bold(self):
        return self.fmt.bold if self.fmt else False

    @property
    def font_color(self):
        return self.fmt.color if self.fmt else None

    @property
    def bgcolor(self):
        return self.fmt.bgcolor if self.fmt else None

    def __str__(self):
        return str(self.tokens)


class Fmt(NamedTuple):
    '''
    Holds text format properties
    '''
    bold: bool = False
    italics: bool = False
    subscript: bool = False
    superscript: bool = False
    color: str = None
    bgcolor: str = None


class Token(NamedTuple):
    '''
    Holds a few formatting properties
    '''
    text: str
    fmt: 'Fmt' = Fmt()

    def __str__(self):
        return self.text

    @property
    def italics(self):
        return self.fmt.italics

    @property
    def bold(self):
        return self.fmt.bold

    @property
    def color(self):
        return self.fmt.color

    @property
    def bgcolor(self):
        return self.fmt.color

    @property
    def subscript(self):
        return self.fmt.subscript

    @property
    def superscript(self):
        return self.fmt.superscript
