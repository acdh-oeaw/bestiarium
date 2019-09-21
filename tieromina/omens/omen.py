'''
Collection of classes used to describe various parts of an omen
'''
import logging
import re
from collections import UserList, namedtuple
from typing import Dict, List
from xml.etree import ElementTree as ET

from .cell import Cell
from .commentary import Commentary
from .readings import Readings
from .score import Score

ROWTYPE_BLANK = 'BLANK'
ROWTYPE_SCORE = 'SCORE'
ROWTYPE_READING = 'READING'
ROWTYPE_COMMENT = 'COMMENT'


class Omen:
    '''
    An omen - described by its score, transliteration transcription, translation and commentary
    '''
    omen_name: str

    def __init__(self, sheet):
        self.omen_name: str = sheet
        self.commentary: Commentary = Commentary()
        self.score: Score = Score(self.omen_prefix)
        self._read(sheet)

    @property
    def omen_prefix(self):
        return self.omen_name.lower().replace(' ', '')

    @property
    def omen_name(self):
        return self.__omen_name

    @omen_name.setter
    def omen_name(self, sheet):
        val = sheet.get_cell_at('A1').full_text
        if '=' in val:
            parts = val.split('=')
            self.__omen_name = parts[0]
        else:
            self.__omen_name = val

    def _read(self, sheet):
        '''
        Reads the spreadsheet and constructs the omen object
        '''
        row_type = None
        for row_num, row in sheet.get_rows():
            if sheet.is_empty_row(row) or row_num == 1:
                continue
            # Find row type
            cells = list(sheet.get_cells(row))
            row_type = Omen.get_row_type(cells[0], row_type)
            # logging.debug('ROW: %s - %s ', row_num, row_type)
            if row_type == ROWTYPE_SCORE:
                self.score.add_row(cells)
            elif row_type == ROWTYPE_READING:
                pass
            elif row_type == ROWTYPE_COMMENT:
                self.commentary.add_row(cells)

    @property
    def tei(self):
        omen_div = ET.Element('div', {'n': self.omen_name})
        omen_head = ET.SubElement(omen_div, 'head')
        score_div = self.score.tei
        omen_div.append(score_div)
        row_type = None
        comments_div = self.commentary.tei
        omen_div.append(comments_div)
        return omen_div

    @staticmethod
    def get_row_type(cell, prev_row_type):
        '''
        Returns the row type based on the contents of cell_text
        Expects the cell in the first column but does not validate
        '''
        if not cell or cell.column_name != 'A': return prev_row_type

        if ((not cell.full_text and prev_row_type == ROWTYPE_COMMENT)
                or 'comment' in cell.full_text.lower()):
            return ROWTYPE_COMMENT

        if any(rdg for rdg in ('(en)', '(de)', '(trl)', '(trs)')
               if rdg in cell.full_text.lower()):
            return ROWTYPE_READING

        return ROWTYPE_SCORE
