'''
Omen - represents all the parts of a particular omen sheet
'''


class Omen:
    '''
    Omen, consisting of
    score, transliterations,
    transcription, translations
    and commentary
    '''
    tokens: str = []
    score = None
    readings = None
    comment = None

    def set_title(self, title: str):
        self.title = title
