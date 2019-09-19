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
ROWTYPE_READING = 'READING'
ROWTYPE_COMMENT = 'COMMENT'


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
            cells = list(self.sheet.get_cells(row))
            row_type = self.get_row_type(cells[0], row_type)
            print(row_num, row_type)
            if row_type == ROWTYPE_SCORE:
                # self.add_scoreline(row)
                pass
            elif row_type == ROWTYPE_READING:
                pass
            elif row_type == ROWTYPE_COMMENT:
                self._add_comment(row)

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

    def get_row_type(self, cell, prev_row_type):
        '''
        Returns the row type based on the contents of cell_text
        Expects the cell in the first column but does not validate
        '''
        if not cell or cell.column_name != 'A': return prev_row_type

        if (not cell.full_text and prev_row_type == ROWTYPE_COMMENT
            ) or 'comment' in cell.full_text.lower():
            if not prev_row_type == ROWTYPE_COMMENT:
                self.commentary = Commentary(cell.full_text)
            return ROWTYPE_COMMENT

        if any(
                rdg for rdg in ('(en)', '(de)', '(trl)', '(trs)')
                if rdg in cell.full_text.lower()):
            return ROWTYPE_READING

        return ROWTYPE_SCORE

    def _add_scoreline(self, row):
        '''
        Adds the score line to the score attribute
        '''
        # Create a score object
        pass

    def _add_comment(self, row):
        '''
        Adds philological commentary to the commentary attribute
        '''
        for cell in self.sheet.get_cells(row):
            if cell.column_name == 'A' or not cell.full_text:
                continue

            self.commentary.append(cell)
