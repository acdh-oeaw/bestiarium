'''
The score of an omen from multiple witnesses
'''

from collections import UserDict, UserList, namedtuple


class Score(UserDict):
    '''
    A dict like class with
    key corresponding to a score_id and
    value containing the scoreline
    '''

    def add_to_score(self, row):
        scoreline = Scoreline(row)


class ScoreLine(UserList):
    def __init__(self, row: dict):
        super().__init__()
        col1, col2 = (row.get(col, '') for col in 'AB')
        self.witness = Witness(col1, col2)
        for col_name, cell in row:
            if col_name in 'AB':
                continue
            # if cell is is in red/italics - add position information
            # if the text contains 'ellipsis'  - add break
            # (open) square brackets and half square brackets - add break
            # (close) ... - end break


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
