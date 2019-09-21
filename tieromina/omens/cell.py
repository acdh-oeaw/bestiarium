'''
A standalone representation of contents inside a cell in a spreadsheet
'''
from typing import NamedTuple


class Format(NamedTuple):
    '''
    Holds text format properties
    at a cell level or within a cell
    '''
    bold: bool = False
    italics: bool = False
    subscript: bool = False
    superscript: bool = False
    color: str = None
    bgcolor: str = None


class Token(NamedTuple):
    '''
    Smallest unit of information in a cell with the same formatting
    '''
    text: str
    format: Format
    complete: bool = False  # whether this is the only token in the cell


class Cell:
    '''
    A list of "Token" objects, the address of the cell and some methods
    '''
    def __init__(self, address: str = ''):
        self.tokens = []
        self.address = address

    def add_token(self, token: Token):
        self.tokens.append(token)

    @property
    def full_text(self):
        '''
        Returns full text from the cell without formatting
        '''
        text = ''
        for token in self.tokens:
            text = text + token.text

        return text

    @property
    def column_name(self):
        '''
        Returns the column name from the cell address
        '''
        col_name = ''
        for char in self.address:
            if char.isalpha():
                col_name += char
            else:
                return col_name
        return col_name

    @property
    def row_name(self):
        '''
        Returns the row name from the cell address
        '''
        r_name = ''
        for char in self.address:
            if char.isalpha():
                pass
            else:
                r_name += char
        return r_name

    def __str__(self):
        return f'[Cell {self.address}]: {self.tokens}'

    def __repr__(self):
        return f'Number of tokens: {len(self.tokens)}\nFull text: {self.full_text}'
