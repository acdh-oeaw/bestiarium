'''
Reading and related classe
'''


class Readings(dict):
    '''
    A dictionary of readings
    '''
    

class AlignedReading:
    '''
    A reading could be of one or more of the following:
    transliteration, transcription and translation
    It is identified by as "CopyText" or "Var" associated with a particulur siglum and reference
    '''

    def __init__(self, reading_id: str):
        self.reading_id = reading_id


class :
    '''
    Super class for transliteration and transcription
    '''

    pass


class Transliteration(AlignedReading):
    '''
    Translietration of the omen
    '''
    pass


class Transcription(AlignedReading):
    '''
    Transcription of the transliteration
    '''


class Translation(AlignedReading):
    '''
    Translation of the omen
    '''

    def __init__(self, lang: str):
        self.lang = lang

    pass
