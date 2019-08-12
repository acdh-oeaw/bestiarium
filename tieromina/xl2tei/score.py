from .tablet import Tablet

class Score:
    '''
    Represents the score section of an omen
    '''
    line_num_cols = []
    rows = []

    def __init__(self,
                 line_num_format):
        self.line_num_format = line_num_format
        
    def append(self, row):
        score_row = ScoreRow(row)
        self.rows.append(ScoreRow(row))
        return


class ScoreRow:
    '''
    Represents a single line/row from the score section
    '''
    
    def __init__(self, row):
        self.row = row
        self.tablet = Tablet(row[0].value, reference=row[1].value)
        
        
