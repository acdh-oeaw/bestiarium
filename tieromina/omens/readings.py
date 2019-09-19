'''
Represents the readings of an omen
'''
from collections import UserDict, UserList
from typing import NamedTuple


class ReadingId(NamedTuple):
    '''
    Hashable identifier for a readling line
    '''
    label: str
    siglum: str = ''


class ReadingLine(UserList):
    '''
    A list of lemmas that make a reading line
    '''
    reading_type: str

    def __init__(self, reading_type: str):
        super().__init__()


class Readings(UserDict):
    '''
    Comprises of readings which could be one or more of the following:
     - transliteration,
     - transcription,
     - translation
    '''

    def add_to_score(self, row: list):
        '''
        Identifies the score line and adds it to the score
        '''
        m = re.match(
            r'^(?P<label>[a-zA-Z\s]*)\s(?P<siglum>.*)\((?P<rdg_type>[a-zA-Z]*)\)$',
            col1.full_text)
        if not m: raise ValueError('Unrecognised row header %s', row)
        reading_id = ReadingId(
            label=m.group('label'), siglum=m.group('siglum'))
        if reading_id not in self.data:
            self.data[reading_id] = []

        reading_line = ReadingLine(m.group('rdg_type'))
        self.data[reading_id].append(reading_line)

        return

    @property
    def tei(self):
        pass
