'''
Philological commentary on the omen
'''
import logging
from collections import UserList


class Comment(UserList):
    @classmethod
    def is_comment(cls, row):
        '''
        Returns true
        if the first cell in the row
        contains the word comment
        '''
        return 'comment' in row.cell_at_column('A').plain_text.lower()
