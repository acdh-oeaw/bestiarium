'''
A sheet from the workbook containing omens
'''
import logging
from .wbformat import WBFormat
from .comments import Comments
from .reading import Readings
from .tablet import Tablet
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
    wbformat=None
    def __init__(self, sheet, wbformat=None):
        self.sheet = sheet
        if wbformat:
            self.wbformat = wbformat
        else:
            self.wbformat = WBFormat(sheet.book)
            
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
            self.tradition = omen_parts[1]
        if len(omen_parts) > 3:
            self.siglum = omen_parts[2]
        if len(omen_parts) > 4 or len(omen_parts) < 2:
            logging.error('Sheet name "{}" does not conform '.format(self.sheet.name) +
                          'to Chapter.Number or Chapter.Tradition.Number ' +
                          'or Chapter.Tradition.Siglum.Number formats')

        return

    @property
    def omen_name(self):
        return (f'Omen {self.chapter}' +
                f'{("."+self.tradition) if self.tradition else ""}' +
                f'{("."+self.siglum) if self.siglum else ""}' +
                f'.{self.omen_num}')


    def read(self):
        '''
        Reads the score first,
        Then reads transliterations, transcriptions and translations
        Then reads commentary
        '''
        def read_until(start_row_num=0, end_label_pattern=None):
            relevant_rows = []
            next_row = start_row_num
            for row_num in range(start_row_num, self.sheet.nrows):
                next_row += 1
                row = self.sheet.row(row_num)
                row_label = row[0].value
                if self._is_empty(row): continue # skip empty rows
                elif end_label_pattern and  end_label_pattern in row_label.lower():
                    break
                else:
                    relevant_rows.append(row)

            return relevant_rows, next_row

        # Read Score
        score_rows, next_row = read_until(start_row_num=1, end_label_pattern='(trl)')
        self.read_score(score_rows)

        # Read readings (transliteration, transcription and translations)
        reading_rows, next_row = read_until(start_row_num=next_row,
                                            end_label_pattern='comment')

        # Read comments
        comment_rows, _ = read_until(start_row_num=next_row)
        self.comments = Comments(comment_rows)

        return

    def read_score(self, score_rows):
        '''
        Reads a score row, makes note of columns that contain line numbers
        and the columns that contain words
        '''
        self.score = Score()
        for row in score_rows:
            tablet = Tablet(row[0].value, reference=row[1].value)
            for i, cell in enumerate(row):
                if self.wbformat.is_line_num(cell):
                    self.score.add_position(tablet, cell.value)
                else:
                    self.score.add_token(tablet, cell.value)
                    
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

        


