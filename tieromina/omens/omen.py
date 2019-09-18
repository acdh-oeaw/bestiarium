'''
Collection of classes used to describe various parts of an omen
'''
import logging
import re
from collections import UserList, namedtuple
from typing import Dict, List
from xml.etree import ElementTree as ET

from .cell import Cell

LINENUM_COLOR = 'FFFF0000'

ROWTYPE_BLANK = 'BLANK'
ROWTYPE_SCORE = 'SCORE'
ROWTYPE_TRANSLITERATION = 'TRANSLITERATION'
ROWTYPE_TRANSCRIPTION = 'TRANSCRIPTION'
ROWTYPE_TRANSLATION = 'TRANSLATION'
ROWTYPE_COMMENT = 'COMMENT'


class ReadingId(namedtuple('ReadingId', 'label, siglum, reference')):
    '''
    A hashable representation of a reading label
    '''

    def __new__(cls, col1: Cell, col2: Cell):
        reference = col2.full_text

        m = re.match(
            r'^(?P<label>[a-zA-Z\s]*)\s(?P<siglum>.*)\((?P<rdg_type>[a-zA-Z]*)\)$',
            col1.full_text)
        if m:
            label = m.group('label')
            siglum = m.group('siglum')
        else:
            logging.warning(
                'Unexpected format in "%s" - unable to match regular expression',
                col1)
            label = col1.full_text
            siglum = ''
        return super().__new__(
            cls, label=label, siglum=siglum, reference=reference)


class Witness(namedtuple('Witness', 'siglum, joins, reference')):
    '''
    A witness - siglum, joins and if applicable, reference
    '''

    def __new__(cls, col1: Cell, reference: Cell):
        '''
        Converts the first two column values for a score line into an immutable namedtuple,
        so it can be used as a key in the score dict
        '''
        witness_parts = col1.split('+.')
        siglum = witness_parts[0].rstrip('+')
        joins = tuple(witness_parts[1:])
        return super().__new__(
            cls, siglum=siglum, joins=joins, reference=reference)


class Commentary(UserList):
    '''
    List of comments from the omen sheet; each cell in an item in the cell
    '''
    title: str = 'Philological commentary'

    def __init__(self, title=None):
        super().__init__()
        if title: self.title = title


class Omen:
    '''
    An omen - described by its score, transliteration transcription, translation and commentary
    '''
    omen_name: str = ''
    score: Dict = {}
    protasis: List[str] = []
    apodosis: List[str] = []

    commentary: Commentary = None

    # reading: Reading = Reading()

    def __init__(self, sheet):
        self.sheet = sheet
        self.read()

    def read(self):
        A1 = self.sheet.get_cell_at('A1')
        self.omen_name = A1.full_text
        row_type = None
        for row_num, row in self.sheet.get_rows():
            if self.sheet.is_empty_row(row) or row_num == 1:
                continue
            # Find row type
            first_cell = self.sheet.get_cell_at(f'A{row_num}')
            row_type = self.get_row_type(first_cell, row_type)
            print(row_num, row_type)
            if row_type == ROWTYPE_SCORE:
                # self.add_scoreline(row)
                pass
            elif row_type == ROWTYPE_COMMENT:
                self._add_comment(row)
            elif row_type == ROWTYPE_TRANSLITERATION:
                # self.add_transliteration(row)
                pass
            elif row_type == ROWTYPE_TRANSCRIPTION:
                # self.add_transcription(row)
                pass
            elif row_type == ROWTYPE_TRANSLATION:
                # self.add_translation(row)
                pass

    @property
    def omen_div(self):
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
            p.text = comment.address + '\n'
            for token in comment.tokens:
                p.text += token.text

        return omen_div

    def get_row_type(self, first_cell, prev_row_type):
        '''
        Returns the row type based on the contents of cell_text
        Expects the cell in the first column but does not validate
        '''
        if not first_cell: return prev_row_type
        cell_text = first_cell.full_text

        if (not cell_text and prev_row_type == ROWTYPE_COMMENT
            ) or 'comment' in cell_text.lower():
            if not prev_row_type == ROWTYPE_COMMENT:
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

    def _add_comment(self, row):
        '''
        Adds philological commentary to the commentary attribute in the class
        '''
        for cell in self.sheet.get_cells(row):
            if cell.column_name == 'A' or not cell.full_text:
                continue

            self.commentary.append(cell)
