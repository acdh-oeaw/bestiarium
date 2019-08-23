'''
A sheet from the workbook containing omens
'''
from typing import List

from xlrd import sheet

from .comments import Comments
from .score import Score
from .tablet import Tablet
from .wbformat import WBFormat
from .omenname import OmenName


class Sheet:
    '''
    Represents a sheet in an omens workbook;
    contains score, readings and commentary
    '''
    omen_name: str
    wbformat = None
    score = Score()

    def __init__(self, sheet: sheet.Sheet, wbformat: WBFormat = None):
        self.sheet = sheet
        if wbformat:
            self.wbformat = wbformat
        else:
            self.wbformat = WBFormat(sheet.book)

        self.omen_name = OmenName(sheet.name)
        self.read()

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
                if self._is_empty(row):
                    continue  # skip empty rows
                elif (end_label_pattern
                      and end_label_pattern in row_label.lower()):
                    break
                else:
                    relevant_rows.append(row)

            return relevant_rows, next_row

        # Read Score
        score_rows, next_row = read_until(start_row_num=1,
                                          end_label_pattern='(trl)')
        self.read_score(score_rows)

        # Read readings (transliteration, transcription and translations)
        reading_rows, next_row = read_until(start_row_num=next_row,
                                            end_label_pattern='comment')

        # Read comments
        comment_rows, _ = read_until(start_row_num=next_row)
        self.comments = Comments(comment_rows)

    def read_score(self, score_rows: List[List[sheet.Cell]]):
        '''
        Reads a score row, makes note of columns that contain line numbers
        and the columns that contain words
        '''
        for row in score_rows:
            tablet = Tablet(row[0].value, row[1].value)
            self.score.add_lemma_to_score(tablet, 0, 'a')

    @staticmethod
    def _is_empty(row: List[sheet.Cell]) -> bool:
        '''
        returns False if the row or column contains at least one non empty cell
        '''
        for cell in row:
            if cell.value:
                return False
        return True
