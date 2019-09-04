from xml.etree import ElementTree as ET

NS = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


class Cell:
    '''
    At the moment holds the XML for font, background and border properties of the cell
    '''

    ADDRESS, CONTENTS, FONT, BACKGROUND = 'address', 'contents', 'font', 'background'
    formats = None

    def __init__(self, **kwargs):
        self.contents = kwargs.get(Cell.CONTENTS)
        self.font = kwargs.get(Cell.FONT)
        self.background = kwargs.get(Cell.BACKGROUND)

    @property
    def text(self) -> str:
        if isinstance(self.contents, str):
            return str(self.contents)

        return str([t.text for t in self.contents.findall('.//ns:t', NS)])

    @property
    def font_color(self):
        if self.font:
            color = self.font.find('ns:color', NS)
            if color:
                return color.attrib.get('rgb')

    @property
    def bg_color(self):
        if self.background:
            color = self.background.find('ns:PatternFill/ns:fgColor', NS)
            if color:
                return color.attrib.get('rgb')

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text
