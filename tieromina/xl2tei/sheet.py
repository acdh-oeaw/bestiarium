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

    
    def __init__(self, sheet, wbformat=None):
        self.sheet = sheet
        self.wbformat = wbformat
        self.read()
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
        
        self.unknown = []

        def read_until(start_row_num=0, end_label_pattern=None):
            for row_num in range(start_row_num, self.sheet.nrows):
                row = self.sheet.row(row_num)
                row_label = row[0].value
                if self._is_empty(row): continue # skip empty rows
                elif end_label_pattern and  end_label_pattern in row_label.lower():
                    return row_num, None
                else: yield row_num, row

            return

        # Read Score
        self.score = Score(self.wbformat)
        for row_num, row in read_until(start_row_num=1,
                                       end_label_pattern='(trl)'):
            if row: self.score.append(row)

        # Read readings (transliteration, transcription and translations)
        self.readings = Readings()
        for row_num, row in read_until(start_row_num=row_num+1,
                                       end_label_pattern='comment'):
            self.readings.append(row)

        self.comments = Comments()
        # Read comments
        for row_num, row in read_until(start_row_num=row_num+1):
            self.comments.append(row)

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

