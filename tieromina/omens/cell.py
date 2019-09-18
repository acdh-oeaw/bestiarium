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

    def __init__(self, address):
        self.tokens = []
        self.address = address

    def add_token(self, token):
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
        column_name = ''
        for char in self.address:
            if char.isalpha():
                column_name += char
            else:
                return column_name
        return column_name

    def __str__(self):
        return self.full_text

    def __repr__(self):
        return f'Number of tokens: {len(self.tokens)}\nFull text: {self.full_text}'
