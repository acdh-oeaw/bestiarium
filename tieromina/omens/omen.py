'''
Collection of classes used to describe various parts of an omen
'''
import logging
import re
from collections import namedtuple
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


class Omen:
    '''
    An omen - described by its score, transliteration transcription, translation and commentary
    '''
    omen_name: str = ''
    score: Dict = {}
    protasis: List[str] = []
    apodosis: List[str] = []

    # commentary: Commentary = None
    # reading: Reading = Reading()

    def __init__(self, sheet):
        self.read_from_sheet(sheet)

    def read_from_sheet(self, sheet):
        A1 = sheet.get_cell_at('A1')
        self.omen_name = A1.full_text

    @property
    def omen_div(self):
        omen_div = ET.Element('div', {'n': self.omen_name})
        return omen_div
