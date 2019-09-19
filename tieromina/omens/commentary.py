'''
Philological commentary of the omen
'''

from collections import UserList
from xml.etree import ElementTree as ET


class Commentary(UserList):
    '''
    List of comments from the omen sheet; each cell in an item in the cell
    '''

    def __init__(self):
        super().__init__()
        self.title = ''

    @property
    def tei_div(self):
        '''
        constructs a div element using TEI representation of comments
        '''
        comments_div = ET.Element('div', {'type': 'commentary'})
        comments_head = ET.SubElement(comments_div, 'head')
        comments_head.text = self.title

        for comment in self.data:
            p = ET.SubElement(comments_div, 'p')
            p.text = ''  # comment.address + '\n'
            for token in comment.tokens:
                p.text += token.text
        return comments_div

    def add_row(self, row):
        '''
        Adds philological commentary to the commentary attribute
        '''
        for cell in row:
            if not cell.full_text: continue

            if cell.column_name == 'A' and not self.title:
                self.title = cell.full_text
                continue

            self.data.append(cell)
