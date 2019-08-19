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
        tablet = Tablet(row[0].value, reference=row[1].value)
        for i, cell in enumerate(row):
            if self.wbformat.is_line_num(cell):
                pass
        return


