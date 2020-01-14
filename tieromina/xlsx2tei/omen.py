'''
Omen is a subtype of Sheet, as each sheet contains exactly one Omen.
Contains methods to read an omen
1. Assume that A1 contains the omen name and its relationship with other omens
2. Row 2 will always be empty
3. SCORE: Row 3 to the first empty line in the sheet
4. READINGs: Groups of lines spearated by an empty line
5. Philological commentary: Everything following a cell containing 'comment' in the column A
'''
from .comment import Comment
from .reading import Reading
from .score import Score
from .sheet import Sheet


class Omen(Sheet):
    '''
    Contains methods to read the omen name, score,
    readings (translations, transcriptions and transliterations)
    and the philological commentary
    '''
    @property
    def omen_name(self):
        '''
        The text in A1
        '''
        print('C3', self.cell_at('D3').plain_text)
        return self.cell_at('A1').plain_text

    @property
    def score(self):
        '''
        Row 3 to the first empty line in the sheet
        '''
        score = Score()
        for row in list(self.rows)[2:]:
            if row.is_empty:  # Stop when a blank line is introduced
                return Score

            score.append(row)

    @property
    def readings(self, start_rownum):
        '''
        A reading is a group of lines following the blank line after score
        An omen will have one or multiple readings
        A reading comprises of one or more of the following:
        - transliteration (aligned with the score)
        - transcription (aligned with the score)
        - translation (aligned with the score)
        '''
        reading = Reading()
        for row in list(self.rows)[start_rownum:]:
            if row.is_empty:  # Stop when a blank line is introduced
                if reading.is_not_empty:
                    # Do not yield at the first empty line, when no lines have been added to reading yet
                    yield reading
                    # Reinitialise reading
                    reading = Reading()
                else:
                    pass
            elif Comment.is_comment(row):
                # return if commentary section begins
                if reading.is_not_empty: yield reading
            else:
                reading.append(row)

    @property
    def comments(self, start_rownum):
        '''
        Everything that follows the row
        whose first column contains "philological commentary"
        belong to the comments section of the omen
        '''
        comment = Comment()
        for row in list(self.rows)[start_rownum:]:
            comment.append(row)

        return comment
