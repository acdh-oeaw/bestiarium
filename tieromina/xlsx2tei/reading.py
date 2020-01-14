'''
Represents a group of rows - one or more of Transliteration, transcription and translation
'''
from collections import UserList

from row import AlignedRow, Row


class Reading(UserList):
    '''
    A subtype of user list,
    contains a list of rows
    that represent a reading
    '''

    @property
    def is_not_empty(self):
        '''
        Returns true if there is at least one reading row
        '''
        return len(self.data) > 0

    @property
    def last_row(self):
        '''
        Returns the address of the last row in this reading
        '''
        return self.data[-1].name


class Transliteration(AlignedRow):
    '''
    A row from the Omens spreadsheet representing the transliteration, aligned with the score
    '''
    pass


class Transcription(AlignedRow):
    '''
    A row from the Omen spreadsheet representing the translcription, aligned with the score
    '''
    pass


class Translation(Row):
    '''
    Translated text of the omen, NOT aligned with the score
    '''
    pass
