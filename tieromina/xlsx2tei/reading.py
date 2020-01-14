'''
Represents a group of transliteration, transcription and translation
'''
from collections import UserList


class Reading(UserList):
    '''
    A subtype of user list,
    contains a list of rows
    that represent a reading
    '''
    def is_not_empty(self):
        '''
        Returns true if there is at least one reading row
        '''
        return len(self.data) > 0
