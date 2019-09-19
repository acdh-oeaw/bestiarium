'''
Omen score - gathered from different witnesses
'''
import logging
import re
from collections import UserDict, UserList, namedtuple
from typing import List
from xml.etree import ElementTree as ET

from .cell import Cell

LINENUM_COLOR = 'FFFF0000'

logger = logging.getLogger(__name__)


class Witness(namedtuple('Witness', 'siglum, joins, reference')):
    '''
    A witness - siglum, joins and if applicable, reference
    '''

    def __new__(cls, row):
        '''
        Converts the first two column values for a score line into an immutable namedtuple,
        so it can be used as a key in the score dict
        '''
        try:
            if row[0].column_name == 'A':
                witness_parts = row[0].full_text.split('+.')
                siglum = witness_parts[0].rstrip('+')
                joins = tuple(witness_parts[1:])
            else:
                logger.error('First cell from column A missing')
                raise ValueError('col1 must be column A')
        except IndexError as ie:
            raise ie

        try:
            reference = row[1].full_text if row[1].column_name == 'B' else ''
        except IndexError as ie:
            reference = ''

        return super().__new__(
            cls, siglum=siglum, joins=joins, reference=reference)

    @property
    def xml_id(self):
        return "#wit_" + re.sub("[^A-Za-z0-9\-_:\.]+", "_", self.siglum)

    @property
    def tei(self):
        wit = ET.Element('witness', {'xml:id': self.xml_id})
        wit.text = witness.siglum


class ScoreLine(UserList):
    '''
    A line from the score of the omen
    '''

    def __init__(self, row: List[Cell]):
        super().__init__()
        self.witness = Witness(row)
        for cell in row:
            for i, token in enumerate(cell.tokens):
                if token.format.color == LINENUM_COLOR:
                    if token.format.italics:
                        position = Position(token.text)
                        if position.column: self.data.append(position.column)
                        if position.line: self.data.append(position.line)
                    else:  # non italicised text in line number cell
                        logger.warning(
                            'Non italicised text in line/column number cell: %s',
                            token)


class Position:
    '''
    Line and column position information in a score
    TODO: Omen 23.4 has a line number like ii 21 (23.5*)
    '''

    def __init__(self, text):
        # NOTE: Formatting is ignored

        self.text = text.replace('r. ', '')
        parts = self.text.split()

        if parts[0][0].isnumeric():
            # Only line number - multiple columns obverse/reverse is not indicated
            self.line = LineInfo(self.text, reverse='r.' in text)
            self.column = None

        elif parts[0].isalpha():
            self.column = ColumnInfo(parts[0])
            self.line = LineInfo(' '.join(parts[1:]))
        else:
            raise ValueError('Neither line nor column: "%s"', text)

    def __repr__(self):
        return (
            f'Reverse: {self.reverse}, Line: {self.line}, Column: {self.column}'
        )


class LineInfo:
    '''
    Line number information in the tablet
    '''

    def __init__(self, text, reverse=False):
        self.broken = "'" in text
        self.reverse = reverse
        self.text = text.replace("'", '')

    @property
    def tei(self):
        cb = ET.Element('lb', {'n': self.text})
        if self.reverse:
            cb.attrib['reverse'] = 'True'
        return cb


class ColumnInfo:
    '''
    Column number information in the tablet
    '''

    def __init__(self, text):
        self.text = text

    @property
    def tei(self):
        cb = ET.Element('cb', {'n': self.text})
        return cb


class Lemma:
    '''
    Lemma as specified in the score
    Equivalent of "Cell"
    '''

    @property
    def tei(self):
        '''
        returns the TEI representation
        '''
        pass


class Score(UserDict):
    '''
    A dict of score lines, identified by witness
    '''

    def add_row(self, row: List[Cell]):
        '''
        Adds the row to score
        '''
        # construct witness
        scoreline = ScoreLine(row)
        self.data[scoreline.witness] = scoreline

    @property
    def tei(self):
        '''
        returns the TEI representation
        '''
        score = ET.Element('div', {'type': 'score'})
        ab = ET.SubElement(score, 'ab')
        for witness, scoreline in self.data.items():
            for item in scoreline:
                item_tei = item.tei

                if isinstance(item, LineInfo) or isinstance(item, ColumnInfo):
                    item_tei.attrib['ed'] = scoreline.witness.xml_id
                    ab.append(item_tei)

        return score

    @property
    def witnesses(self):
        '''
        returns witnesses from the keys
        '''
        return list(self.data.keys())
