'''
Omen score - gathered from different witnesses
'''
from collections import UserDict, namedtuple
from typing import List

from .cell import Cell

LINENUM_COLOR = 'FFFF0000'


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
                logging.error('First cell from column A missing')
                raise ValueError('col1 must be column A')
        except IndexError as ie:
            raise ie

        try:
            reference = row[1].full_text if row[1].column_name == 'B' else ''
        except IndexError as ie:
            reference = ''

        return super().__new__(
            cls, siglum=siglum, joins=joins, reference=reference)


class Scoreline:
    '''
    A line from the score of the omen
    '''

    def __init__(self, row: List[Cell]):
        pass


class Position:
    '''
    Line and column position information in a score
    '''

    @property
    def tei(self):
        '''
        returns the TEI representation
        '''
        pass


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
        witness = Witness(row)
        # self.data[witness] = Scoreline(row)
        pass

    @property
    def tei(self):
        '''
        returns the TEI representation
        '''
        score = ET.Element('div', {'type': 'score'})
        ab = ET.SubElement(score, 'ab')

        return score

    @property
    def witnesses(self):
        '''
        returns witnesses from the keys
        '''
        return list(self.data.keys())
