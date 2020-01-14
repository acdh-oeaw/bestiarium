'''
Philological commentary on the omen
'''
import logging
from collections import UserList

from .row import Row


class Comment(UserList):
    @classmethod
    def is_comment(cls, row):
        '''
        Returns true
        if the first cell in the row
        contains the word comment
        '''
        try:
            return 'comment' in row.cell_at_column('A').plain_text.lower()
        except Exception as e:
            logging.warning(repr(e))
            return False

    @property
    def comments(self):
        for row in self.data:
            if row.is_empty: continue
            for cell in row.cells:
                # Ignore the first cell
                yield CommentRow(sheet=row.sheet, xml=row.xml)


class CommentRow(Row):
    @property
    def marked_up_text(self):
        row_str = ''
        for cell in self.cells:
            if cell.address.startswith('A'):
                # probably the title
                row_str += '<h6>'
            for formatted_chunk in cell.cell_contents:
                if formatted_chunk.cell_format.italics:
                    row_str += f'<i>{formatted_chunk.text}</i>'
                else:
                    row_str += f'{formatted_chunk.text} '

            if cell.address.startswith('A'):
                # probably the title
                row_str += '</h6>'

        return row_str
