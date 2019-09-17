'''
Deconstructs omen encoded in a spreadsheet to an object
Exports the omen object into a div element for TEI
'''
from collections import UserList, namedtuple
from typing import Dict, List
from xml.etree import ElementTree as ET

from .sheet import Sheet

LINENUM_COLOR = 'FFFF0000'

ROWTYPE_BLANK = 'BLANK'
ROWTYPE_SCORE = 'SCORE'
ROWTYPE_TRANSLITERATION = 'TRANSLITERATION'
ROWTYPE_TRANSCRIPTION = 'TRANSCRIPTION'
ROWTYPE_TRANSLATION = 'TRANSLATION'
ROWTYPE_COMMENT = 'COMMENT'


class Witness(namedtuple('Witness', 'siglum, joins, reference')):
    '''
    A witness - siglum, joins and if applicable, reference
    '''
    siglum: str
    joins: list = None
    reference: str = None

    def __new__(cls, col1: str, reference: str):
        '''
        Converts the first two column values for a score line into an immutable namedtuple,
        so it can be used as a key in the score dict
        '''
        witness_parts = col1.split('+.')
        siglum = witness_parts[0].rstrip('+')
        joins = witness_parts[1:]
        return super().__new__(
            cls, siglum=siglum, joins=joins, reference=reference)

    @property
    def witness_id(self):
        return "wit_" + re.sub("[^A-Za-z0-9\-_:\.]+", "_", self.siglum)


class ScoreLine:
    lemmas: List  # list of cells
    witness: Witness


class Commentary(UserList):
    '''
    List of comments from the omen sheet; each cell in an item in the cell
    '''
    title: str = 'Philological commentary'

    def set_title(self, title):
        self.title = title


class OmenSheet(Sheet):
    witnesses: List[Witness] = []
    score: Dict[Witness, ScoreLine]
    protasis: List[str]
    apodosis: List[str]
    commentary: Commentary = Commentary()

    def __init__(self, sheet):
        super().__init__(
            sheet_xml=sheet.sheet,
            style=sheet.style,
            shared_strings=sheet.shared_strings)

        self.read()

    def get_row_type(self, cell_text, prev_row_type):
        '''
        Returns the row type based on the contents of cell_text
        Expects the cell in the first column but does not validate
        '''
        if (not cell_text and prev_row_type == ROWTYPE_COMMENT
            ) or 'comment' in cell_text.lower():
            return ROWTYPE_COMMENT
        if 'trl' in cell_text.lower():
            return ROWTYPE_TRANSLITERATION
        if 'trs' in cell_text.lower():
            return ROWTYPE_TRANSCRIPTION
        if 'en' or 'de' in cell_text.lower():
            return ROWTYPE_TRANSLATION
        if '(' or ')' not in cell_text:
            return ROWTYPE_SCORE

        raise ('Unknown row type')

    def read(self):
        '''
        Reads the spreadsheet into an OmenSheet representation
        '''
        row_type = None  # initial guess can also be omen name?
        for row_num, row in enumerate(self.get_rows()):
            if self.is_empty_row(row):
                continue

            for col_num, cell in enumerate(self.get_cells_in_row(row)):
                cell_text = self.get_text_from_cell(cell)

                if not cell_text:  # SKIP empty cells
                    continue

                if row_num == 0 and col_num == 0:  # Omen name
                    self.omen_name = cell_text
                elif col_num == 0:  # first cell in the row
                    row_type = self.get_row_type(cell_text, row_type)
                    continue

                if row_type == ROWTYPE_COMMENT:
                    self.commentary.append(cell)

    def is_position_cell(self, cell):
        '''
        Returns True if the cell contains line number formatting
        '''
        for token in self.get_tokens_in_cell(cell):
            if token.format.color == LINENUM_COLOR and token.text:
                return True

    @property
    def omen_div(self):
        '''
        Constructs a TEI markup representation for the omen sheet and returns it
        '''
        omen_div = ET.Element('div', {'n': self.omen_name})
        omen_head = ET.SubElement(omen_div, 'head')
        score = ET.SubElement(omen_div, 'div', {'type': 'score'})
        ab = ET.SubElement(score, 'ab')
        row_type = None
        comments_div = ET.SubElement(omen_div, 'div', {'type': 'commentary'})
        comments_head = ET.SubElement(comments_div, 'head')
        comments_head.text = self.commentary.title
        for comment in self.commentary:
            p = ET.SubElement(comments_div, 'p')
            p.text = ''
            for token in self.get_tokens_in_cell(comment):
                p.text += token.text

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
