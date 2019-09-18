'''
A standalone representation of contents inside a cell in a spreadsheet
'''
from .token import Token


class Cell:
    '''
    A list of "Token" objects, the address of the cell and some methods
    '''
    tokens = []

    def __init__(self, address):
        self.address = address

    def add_token(self, token):
        self.tokens.append(token)

    @property
    def full_text(self):
        '''
        Returns full text from the cell without formatting
        '''
        text = ''
        for token in self.get_tokens_in_cell(cell):
            text = text + token.text

        return text

    @property
    def column_name(self):
        '''
        Returns the column name from the cell address
        '''
        column_name = ''
        for char in address:
            if char.isalpha():
                column_name += char
            else:
                return column_name
        return column_name
