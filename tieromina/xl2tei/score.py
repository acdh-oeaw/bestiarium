from .tablet import Tablet

class Score:
    '''
    Represents the score section of an omen
    '''
    line_num_cols = []
    rows = {}

    def __init__(self,
                 wbformat):
        self.wbformat = wbformat

    def append(self, row):
        score_row = ScoreRow(row, self.wbformat)
        self.rows[score_row.tablet] = score_row
        return


class ScoreRow:
    '''
    Represents a single line/row from the score section
    '''   
    def __init__(self, row, wbformat):
        self.row = row
        self.tablet = Tablet(row[0].value, reference=row[1].value)
        for cell in row:
            pass
        
