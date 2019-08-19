'''
A sheet from the workbook containing omens
'''
import logging
from .wbformat import WBFormat
from .comments import Comments
from .reading import Readings
from .tablet import Tablet


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
            self.wbformat = WBFormat(xf_list=sheet.book.xf_list,
                                     font_list=sheet.book.font_list,
                                     colour_map=sheet.book.colour_map)
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
            for row_num in range(start_row_num, self.sheet.nrows):
                row = self.sheet.row(row_num)
                row_label = row[0].value
                if self._is_empty(row): continue # skip empty rows
                elif end_label_pattern and  end_label_pattern in row_label.lower():
                    return row_num, None
                else:
                    yield row_num, row

        # Read Score
        self.score = {}
        for row_num, row in read_until(start_row_num=1,
                                       end_label_pattern='(trl)'):
            self.read_score(row)

        # Read readings (transliteration, transcription and translations)
        self.readings = Readings()
        for row_num, row in read_until(start_row_num=row_num+1,
                                       end_label_pattern='comment'):
            self.readings.append(row)

        # Read comments
        self.comments = Comments()
        for row_num, row in read_until(start_row_num=row_num+1):
            self.comments.append(row)

        return

    def read_score(self, row):
        '''
        Reads a score row, makes note of columns that contain line numbers
        and the columns that contain words
        '''
        tablet = Tablet(row[0].value, reference=row[1].value)
        for i, cell in enumerate(row):
            if self.wbformat.is_line_num(cell):
                pass      
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

        


