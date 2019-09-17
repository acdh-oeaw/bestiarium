'''
Deconstructs omen encoded in a spreadsheet to an object
Exports the omen object into a div element for TEI
'''
import logging
import re
from collections import UserList, defaultdict, namedtuple
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


class ReadingId(namedtuple('ReadingId', 'label, siglum, reference')):
    def __new__(cls, col1: str, col2: str = None):
        reference = col2 if col2 else ''

        m = re.match(
            r'^(?P<label>[a-zA-Z\s]*)\s(?P<siglum>.*)\((?P<rdg_type>[a-zA-Z]*)\)$',
            col1)
        if m:
            label = m.group('label')
            siglum = m.group('siglum')
        else:
            logging.warning(
                'Unexpected format in "%s" - unable to match regular expression',
                col1)
            label = col1
            siglum = ''
        return super().__new__(
            cls, label=label, siglum=siglum, reference=reference)


class Witness(namedtuple('Witness', 'siglum, joins, reference')):
    '''
    A witness - siglum, joins and if applicable, reference
    '''

    def __new__(cls, col1: str, reference: str):
        '''
        Converts the first two column values for a score line into an immutable namedtuple,
        so it can be used as a key in the score dict
        '''
        witness_parts = col1.split('+.')
        siglum = witness_parts[0].rstrip('+')
        joins = tuple(witness_parts[1:])
        return super().__new__(
            cls, siglum=siglum, joins=joins, reference=reference)

    @property
    def witness_id(self):
        '''
        returns a string  representation of the witness that can be legally used in an XML attribute
        '''
        return "wit_" + re.sub("[^A-Za-z0-9\-_:\.]+", "_", self.siglum)


class ScoreLine:
    '''
    Line containing score from a particular witness
    '''
    lemmas: List  # list of cells
    witness: Witness


class Commentary(UserList):
    '''
    List of comments from the omen sheet; each cell in an item in the cell
    '''
    title: str = 'Philological commentary'

    def __init__(self, title=None):
        super().__init__()
        if title: self.title = title


class Reading:
    '''
    Contains the translations, transliterations and transcriptions of the omen
    '''

    translation: Dict = defaultdict(list)
    transcription: Dict = defaultdict(list)
    transliteration: Dict = defaultdict(list)


class ReadingLine(UserList):
    '''
    A line - translation/transcription or transliteration
    Reading-id: 
    '''
    reading_id: ReadingId


class Position:
    '''
    Line, column, obverse and reverse information about the position of the omen in the tablet
    '''

    def __init__(self, cell_value):
        self.cell_value = cell_value

        self.reverse = 'Reverse' if 'r.' in cell_value else 'Obverse'

        if cell_value and not cell_value.startswith(
                'r') and not cell_value[0].isnumeric():
            self.column_break = cell_value.split()[0]
            self.line_break = ' '.join(cell_value.split()[1:])
        else:
            self.line_break = cell_value
            self.column_break = None

        return


class OmenSheet(Sheet):
    '''
    A subclasss of Sheet, reads a spreadsheet containing an Omen
    '''
    score: Dict = {}
    protasis: List[str] = []
    apodosis: List[str] = []
    commentary: Commentary = None
    reading: Reading = Reading()

    def __init__(self, sheet):
        super().__init__(
            sheet_xml=sheet.sheet,
            style=sheet.style,
            shared_strings=sheet.shared_strings)

        self.read()

    def get_row_type(self, row, prev_row_type):
        '''
        Returns the row type based on the contents of cell_text
        Expects the cell in the first column but does not validate
        '''
        first_cell = self.find_cell_in_row(row, 'A')
        if not first_cell: return prev_row_type
        cell_text = self.get_text_from_cell(first_cell)

        if (not cell_text and prev_row_type == ROWTYPE_COMMENT
            ) or 'comment' in cell_text.lower():
            self.commentary = Commentary(cell_text)
            return ROWTYPE_COMMENT
        if '(trl)' in cell_text.lower():
            return ROWTYPE_TRANSLITERATION
        if '(trs)' in cell_text.lower():
            return ROWTYPE_TRANSCRIPTION
        if any(lang for lang in ('(en)', '(de)') if lang in cell_text.lower()):
            return ROWTYPE_TRANSLATION
        if '(' not in cell_text:
            return ROWTYPE_SCORE

        raise ('Unknown row type')

    def add_comment(self, row):
        '''
        Adds philological commentary to the commentary attribute in the class
        '''
        for col_num, cell in enumerate(self.get_cells_in_row(row)):
            if self.get_column_name(
                    cell) == 'A' or not self.get_text_from_cell(cell):
                continue

            self.commentary.append(cell)

    def add_scoreline(self, row):
        '''
        Adds the scoreline to the score attribute
        '''
        witness = self.get_witness(row)
        if witness.__hash__ in self.score.keys():
            raise ValueError(f'Duplicate witness+reference {row}')
        self.score[witness] = []
        for col_num, cell in enumerate(self.get_cells_in_row(row)):
            cell_text = self.get_text_from_cell(cell)
            if (self.get_column_name(cell) in 'AB' or not cell_text):
                continue
            self.score[witness].append(cell_text)

    def add_transliteration(self, row):
        '''
        Add transliteration to readings
        '''
        col1, ref = self.find_cell_in_row(row, 'A'), self.find_cell_in_row(
            row, 'B')
        reading_id = ReadingId(
            col1=self.get_text_from_cell(col1) if col1 else '',
            col2=self.get_text_from_cell(ref) if ref else '')

        for col_num, cell in enumerate(self.get_cells_in_row(row)):
            cell_text = self.get_text_from_cell(cell)
            if (self.get_column_name(cell) in 'AB' or not cell_text):
                continue
            self.reading.transliteration[reading_id].append(cell_text)

    def add_transcription(self, row):
        '''
        Add transcription to readings
        '''
        pass

    def add_translation(self, row):
        '''
        Add translation to omen
        '''
        pass

    def read(self):
        '''
        Reads the spreadsheet into an OmenSheet representation
        '''
        row_type = None  # initial guess can also be omen name?
        # TODO:  omen connections
        self.omen_name = self.get_text_from_cell(self.get_cell_at('A1'))
        for row_num, row in enumerate(self.get_rows()):
            if self.is_empty_row(row) or row_num == 0:
                continue
            # Find row type
            row_type = self.get_row_type(row, row_type)
            if row_type == ROWTYPE_SCORE:
                self.add_scoreline(row)
            elif row_type == ROWTYPE_COMMENT:
                self.add_comment(row)
            elif row_type == ROWTYPE_TRANSLITERATION:
                self.add_transliteration(row)
            elif row_type == ROWTYPE_TRANSCRIPTION:
                self.add_transcription(row)
            elif row_type == ROWTYPE_TRANSLATION:
                self.add_translation(row)

    def get_witness(self, row):
        '''
        Creates a hashable representation of the siglum+reference
        '''
        col1, ref = self.find_cell_in_row(row, 'A'), self.find_cell_in_row(
            row, 'B')
        witness = Witness(
            col1=self.get_text_from_cell(col1),
            reference=self.get_text_from_cell(ref))
        return witness

    def get_reading_id(self, row):
        '''
        Creates a hashable representation of the reading group - CopyText or Var or ...
        '''
        col1, ref = self.find_cell_in_row(row, 'A'), self.find_cell_in_row(
            row, 'B')
        witness = Witness(
            col1=self.get_text_from_cell(col1),
            reference=self.get_text_from_cell(ref))
        return witness

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
