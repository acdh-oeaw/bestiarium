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

    def __new__(cls, col1: Cell, col2: Cell):
        '''
        Converts the first two column values for a score line into an immutable namedtuple,
        so it can be used as a key in the score dict
        '''
        if col1.column_name == 'A':
            witness_parts = col1.full_text.split('+.')
            siglum = witness_parts[0].rstrip('+')
            joins = tuple(witness_parts[1:])
        else:
            raise ValueError('col1 must be column A')

        reference = col2.full_text if col2.column_name == 'B' else ''

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

    def add_to_score(self, row: List[Cell]):
        '''
        Adds the row to score
        '''
        # construct witness
        witness = Witness(row[0], row[1])
        # self.data[witness] = Scoreline(row)
        pass

    @property
    def tei(self):
        '''
        returns the TEI representation
        '''
        pass

    @property
    def witnesses(self):
        '''
        returns witnesses from the keys
        '''
        return list(self.data.keys())
