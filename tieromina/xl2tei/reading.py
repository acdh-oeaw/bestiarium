from collections import defaultdict
import logging
from xml.etree import ElementTree as ET

TRANSLITERATION, TRANSCRIPTION, TRANSLATION = 1,2,3
ROW_TYPES = {'(trl)': TRANSLITERATION,
             '(trs)': TRANSCRIPTION,
             '(en)': TRANSLATION,
             '(de)': TRANSLATION}

UNEXPECTED_ROW = f'Expecting cell to end with one of the following: {ROW_TYPES.keys()}'

class ReadingLabel:
    '''
    breaking down the reading
    '''
    def __init__(self, label):
        label = label.strip()
        for ending, row_type in ROW_TYPES.items():
            if label.endswith(ending):                                        
                self.row_type = row_type
                self.name = label.rstrip(ending)
                return
            
        raise ValueError(UNEXPECTED_ROW)


class ReadingGroup:
    '''
    A grouped set of transliteration, transcription and translation - 
    not necessarily all three
    '''
    name = ''
    translation = []
    transcription = []
    
    def __init__(self, row,  label):
        self.name = name
        self.append(row, label)
        return
    
    def append(self, row, label):
        if label.name != self.name:
            raise ValueError(
                'Wrong reading group. Expecting {}, received {}'.format(self.name,
                                                                        label.name))
        
        if label.row_type == TRANSLATION:
            self.translation.append(Translation(row))
        elif label.row_type == TRANSLITERATION:
            pass
        elif label.row_type == TRANSCRIPTION:
            pass
    
    
class Readings:
    '''
    Hashed reading groups 
    '''
    groups = defaultdict(ReadingGroup)

    def append(self, row):
        '''
        Appends the reading to its respective reading group
        '''
        label = ReadingLabel(row[0].value)
            
        try:
            # Append a row to existing row
            self.groups[label.name].append(row, label)
        except KeyError:
            # add a new reading group
            self.groups[label.name] = ReadingGroup(row, label)

        return
        
    def __str__(self):
        return str(self.groups)
        

class Translation:
    '''
    Translation of the omen
    '''
    def __init__(self, row):
        self.row = row
        self.reference = row[1].value if row[1].value else ''
        self.reference_pos = row[2].value if row[2].value else ''
        self.translation_text = ' '.join([cell.value for cell in row[2:]])
        self.clean_text = self.translation_text.translate({ord(i): None for i in '[]'})
        try:
            self.protasis, self.apodosis = self.clean_text.split('–')
        except ValueError:
            self.protasis, self.apodosis = '', ''

        
        return


class AlignedRow:
    '''
    Abstract class for rows containing 
    the score, translitrations and transcriptions
    '''
    pass

class Transliteration(AlignedRow):
    '''
    Transliteration of the omen
    '''
    pass

class Transcription(AlignedRow):
    '''
    Transcription of the transliteration
    '''
    pass
    
    
