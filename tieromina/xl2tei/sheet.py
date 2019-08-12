import logging
from .comments import Comments
from .score import Score

class Sheet:
    '''
    Represents a sheet in an omens workbook;
    contains score, readings and commentary
    '''
    chapter = ''
    readings = []
    comments = Comments()
    unknown = []
    witnesses = []
    
    def __init__(self, sheet, line_num_format=None):
        self.sheet = sheet
        self.line_num_format = line_num_format
        self.score = Score(self.line_num_format)
        self.classify_rows()
        if self.unknown:
            logging.warning('Found the following rows with no label - SKIPPED\n%s', self.unknown)

        return
                    
    def classify_rows(self):
        '''
        Classifies rows into score/readings/comment or unknown.
        Blank lines are ignored
        The first line is ignored because it's only supposed to contain omen name
        unknown in BAD! :-x
        '''
        comment_started = False
        for row_num in range(1, self.sheet.nrows):
            row = self.sheet.row(row_num)
            row_label = row[0].value
            if self._is_empty(row):
                continue
            
            if not row_label  and not comment_started:
                self.unknown.append(row)

            elif comment_started:
                self.comments.append(row)

            elif 'comment' in row_label.lower():
                comment_started = True
                self.comments.append(row)
                
            elif '(' in row_label and ')' in row_label:
                self.readings.append(row)

            else:
                self.score.append(row)
                
          
    @staticmethod
    def _is_empty(row):
        '''
        returns False if the row or column contains at least one non empty cell
        '''
        for cell in row:
            if cell.value:
                return False
            
        return True

