'''
Represents the readings of an omen
'''
import re
from collections import UserDict, UserList, defaultdict
from typing import NamedTuple
from xml.etree import ElementTree as ET

from .lemma import Lemma


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
    words: list

    def __init__(self, row: list):
        super().__init__()
        self.words = []
        m = re.match(
            r'^(?P<label>[a-zA-Z\s]*)\s(?P<siglum>.*)\((?P<rdg_type>[a-zA-Z]*)\)$',
            row[0].full_text)
        if not m: raise ValueError('Unrecognised row header %s', row)
        self.reading_id = ReadingId(
            label=m.group('label'), siglum=m.group('siglum'))

        self.rdg_type = m.group('rdg_type')
        for cell in row:
            if not cell.full_text or cell.column_name in 'AB': continue
            self.words.append(Lemma(cell))

    @property
    def tei(self):
        ab = ET.Element('ab')
        if self.rdg_type == 'trl':
            ab.attrib['type'] = 'transliteration'
        elif self.rdg_type == 'trs':
            ab.attrib['type'] = 'transcription'
        else:
            ab.attrib['type'] = 'translation'
            ab.attrib['lang'] = self.rdg_type

        for word in self.words:
            w = word.reading_tei
            ab.append(w)
        return ab


class Readings(UserDict):
    '''
    Keys are ReadingId
    Comprises of readings which could be one or more of the following:
     - transliteration,
     - transcription,
     - translation
    '''

    def __init__(self):
        super().__init__()
        self.data = defaultdict(list)

    def add_to_readings(self, row: list):
        '''
        Identifies the score line and adds it to the score
        '''
        reading_line = ReadingLine(row)
        self.data[reading_line.reading_id].append(reading_line)

    @property
    def tei(self):
        for rdg_grp, lines in self.data.items():
            elem = ET.Element('div', {'n': rdg_grp.label})
            for line in lines:
                elem.append(line.tei)
            yield elem
