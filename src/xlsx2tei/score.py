'''
Class representing the list of lines that make up Score in an omen
'''
import logging
from collections import UserList

from .line import Line, LineInfo
from .row import Row


class Score(UserList):
    '''
    Represents the Score - a list of "ScoreRow"s
    '''

    def append(self, row):
        super().append(ScoreRow(sheet=row.sheet, xml=row.xml))

    def is_not_empty(self):
        return len(self.data) > 0

    @property
    def last_row(self):
        '''
        Returns the address of the last row of the score
        '''
        return self.data[-1].name


class ScoreRow(Row):
    '''
    Represents a single row in "Score",
    corresponding to a witness
    and reference when available
    A ScoreRow contains one or more lines from the tablet
    A line begins with line number information in red,
    italiced text
    '''

    @property
    def witness(self):
        return self.cell_at_column('A')

    @property
    def reference(self):
        return self.cell_at_column('B')

    @property
    def lines(self):
        line = None
        for cell in list(self.cells)[2:]:
            if LineInfo.is_new_line(cell):
                # new line
                if line: yield line

                # create a new line
                line = Line(LineInfo(sheet=self.sheet, cell_element=cell.xml))
                continue

            if cell.is_not_empty:
                try:
                    line.append(cell)
                except AttributeError:
                    raise ValueError(
                        f'Found a cell {cell} in score without a new line cell'
                    )

        # return the last/online line
        if line: yield line
