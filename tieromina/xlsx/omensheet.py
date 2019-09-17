'''
Deconstructs omen encoded in a spreadsheet to an object
Exports the omen object into a div element for TEI
'''
from xml.etree import ElementTree as ET

from .sheet import Sheet

LINENUM_COLOR = 'FFFF0000'

ROWTYPE_BLANK = 'BLANK'
ROWTYPE_SCORE = 'SCORE'
ROWTYPE_TRANSLITERATION = 'TRANSLITERATION'
ROWTYPE_TRANSCRIPTION = 'TRANSCRIPTION'
ROWTYPE_TRANSLATION = 'TRANSLATION'
ROWTYPE_COMMENT = 'COMMENT'


class OmenSheet(Sheet):
    def __init__(self, sheet):
        super().__init__(
            sheet_xml=sheet.sheet,
            style=sheet.style,
            shared_strings=sheet.shared_strings)
        self.read()

    def read(self):
        A1 = self.get_cell_at('A1')
        self.omen_name = self.get_text_from_cell(A1)
        self.witnesses = []

    def get_omen_div(self):
        omen_div = ET.Element('div', {'n': self.omen_name})
        omen_head = ET.SubElement(omen_div, 'head')
        score = ET.SubElement(omen_div, 'div', {'type': 'score'})
        ab = ET.SubElement(score, 'ab')
        row_type = None
        return omen_div
        # for row_num, row in enumerate(sheet.get_rows()):
        #     for col_num, cell in enumerate(sheet.get_cells_in_row(row)):
        #         if row_num == 0 and col_num == 0:
        #             omen_name = sheet.get_text_from_cell(cell)
        #             omen_div.attrib['n'] = omen_name
        #             omen_head.text = omen_name

        #             continue

        #         if col_num == 0:  # FIRST CELL in the row
        #             cell_text = sheet.get_text_from_cell(cell)

        #         for token in sheet.get_tokens_in_cell(cell):
        #             if (row_type == ROWTYPE_SCORE
        #                     and token.format.color == LINENUM_COLOR):
        #                 position = Position(token.text)
        #                 # Read the line/column information and move to next cell
        #                 if position.line_break:
        #                     lb = ET.SubElement(ab, 'lb', {
        #                         'n': position.line_break
        #                     })

        #                 if position.column_break:
        #                     cb = ET.SubElement(ab, 'cb', {
        #                         'n': position.line_break
        #                     })

        #                 break
