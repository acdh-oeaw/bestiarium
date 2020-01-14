'''
Represents a line in the tablet
Is a list of Lemmas (cells) from "ScoreRow"
'''
from collections import UserList

from .cell import Cell

LINEINFO_COLOR = 'FFFF0000'


class LineInfo(Cell):
    '''
    Subtype of Cell, contains line info
    indicated by red italicised text in the spreadsheet
    '''
    @classmethod
    def is_new_line(cls, cell) -> bool:
        if cell.cell_format.color == LINEINFO_COLOR:
            return True
        for chunk in cell.cell_contents:
            if chunk.cell_format.color == LINEINFO_COLOR:
                return True

    @property
    def label(self):
        return self.plain_text

    @property
    def line_num(self):
        if self.column or self.reverse:
            return self.label.split()[1].rstrip("'")

        return self.label.split()[0].rstrip("'")

    @property
    def broken(self):
        return "'" in self.label

    @property
    def column(self):
        if self.label[0].isalpha() and self.label[0] != 'r':
            return self.label.split()[0]

        return ''
        # TODO: Can there be column info following r.? For example: "r. ii 17"

    @property
    def reverse(self):
        return self.label.startswith('r.')

    @property
    def extra_info(self):
        '''
        Returns anything in the label that is
        not line/column number or obverse/reverse information
        '''
        return self.label.lstrip('r.').strip().lstrip(
            self.column).strip().lstrip(self.line_num).lstrip("'").strip()


class Line(UserList):
    def __init__(self, line_info: LineInfo):
        super().__init__()
        self.line_info = line_info
