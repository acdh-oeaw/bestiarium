from .token import Token


class Score:
    '''
    represents the score of an omen
    '''
    parts = [
    ]  # defaultdict(dict) # each part is a dict ( {tablet:Token, ...})

    def add_lemma_to_score(self, tablet, position: int, cell_value):
        '''
        Adds the given lemma to the given position
        '''
        # self.parts[position][str(tablet)] = Token(cell_value)
        return

    def add_position_to_score(self, tablet):
        '''
        Adds line break/other position information
        '''
        # self.parts[position][str(tablet)] = Token(cell_value)


class ScorePart(dict):
    '''
    represents a particular lemma or line break or column
    in different tablets
    '''
    def add_part(self, tablet, cell_value):
        pass

