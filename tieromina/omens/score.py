'''
Represents a line from the score
'''
from collections import namedtuple


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


class Scoreline:
    '''
    A line from the score of the omen
    '''
    pass
