import logging
from .comments import Comments
from .reading import Readings
from .score import Score

class Sheet:
    '''
    Represents a sheet in an omens workbook;
    contains score, readings and commentary
    '''
    chapter = ''

    
    def __init__(self, sheet, line_num_format=None):
        self.sheet = sheet
        self.line_num_format = line_num_format

        return

    def read(self):
        '''
        Reads the score first, 
        identifies 
        columns containing tokens and 
        columns containing line numbers
        Reads readings
        Then reads commentary
        '''
        
        self.comments = Comments()
        self.unknown = []

        def read_until(start_row_num=0, end_label_pattern=None):
            for row_num in range(start_row_num, self.sheet.nrows):
                row = self.sheet.row(row_num)
                row_label = row[0].value
                if self._is_empty(row): continue
                elif end_label_pattern and  end_label_pattern in row_label.lower():                    
                    yield row_num, None
                else: yield row_num, row

            return
                
        self.score = Score(self.line_num_format)
        for row_num, row in self.read_until(start_row_num=1, end_label_pattern='(trl)'):
            if row: self.score.append(row)

        self.readings = Readings()
        for row_num, row in self.read_until(start_row_num=row_num, end_label_pattern='comment'):
            self.readings.append(row)
            
        
            
            
        
    def classify_rows(self):
        '''
        Classifies rows into score/readings/comment or unknown.
        Blank lines are ignored
        The first line is ignored because it's only supposed to contain omen name
        unknown in BAD! :-x
        '''
        comment_started = False
        

            if self._is_empty(row):
                continue
            
            if not row_label  and not comment_started:
                self.unknown.append(row)

            elif comment_started:
                self.comments.append(row)

            el
                
            elif '(' in row_label and ')' in row_label:
                self.readings.append(row)

            else:
                self.score.append(row)
        
        return
    
    @staticmethod
    def _is_empty(row):
        '''
        returns False if the row or column contains at least one non empty cell
        '''
        for cell in row:
            if cell.value:
                return False
            
        return True

