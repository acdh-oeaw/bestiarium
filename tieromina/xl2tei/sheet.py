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
    omen_num = ''
    tradition = ''
    siglum = ''
    
    def __init__(self, sheet, wbformat=None):
        self.sheet = sheet
        self.wbformat = wbformat
        self.read_omen_name()
        self.read()
        return

    def read_omen_name(self):
        '''
        Reads the omen name from the sheet name and 
        compares it with the value in the top cell.
        Notes any link given in the top cell.
        '''        
        omen_parts = self.sheet.name.split('.')
        self.chapter = omen_parts[0]
        self.omen_num = omen_parts[-1]
        if len(omen_parts) > 2:
            self.tradition = omen_parts[2]
        elif len(omen_parts) > 3:
            self.siglum = omen_parts[3]
        elif len(omen_parts)>4 or len(omen_parts)>2:
            raise ValueError('Sheet name does not conform to Chapter.Number or Chapter.Tradition.Number or Chapter.Tradition.Siglum.Number formats')
            
        return

    @property
    def omen_name(self):
        return f'Omen {self.chapter}.{"."+self.tradition if self.tradition else ""}.{"."+self.siglum if self.siglum else ""}{self.omen_num}'
    
    def read(self):
        '''
        Reads the score first, 
        Then reads transliterations, transcriptions and translations
        Then reads commentary
        '''
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

