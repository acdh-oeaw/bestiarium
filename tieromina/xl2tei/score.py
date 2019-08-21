from .token import Token


class Score:
    '''
    represents the "score" of an omen
    '''
    rows = {}
    
    def add_token(self, tablet, token):
        '''
        adds the token to corresponding row
        '''
        if hash(tablet) not in self.rows:
            self.rows[hash(tablet)] = ScoreRow()

        self.rows[hash(tablet)].add_token(token)
        return

    def add_position(self, tablet, token):
        '''
        adds the line/column position to corresponding row
        '''
        pass


class ScoreRow:
    '''
    represents the score row - 
    corresponding to a single tablet 
    and/or reference
    '''
    elements = []
    
    def add_token(self, token):
        '''
        adds token
        '''
        self.elements.append(Token(token))
        return

    def add_position(self, token):
        '''
        adds linebreak
        '''
        self.elements.append(Position(token))
        return




    
