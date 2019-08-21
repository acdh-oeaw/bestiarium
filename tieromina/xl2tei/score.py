class Score:
    '''
    represents the "score" of an omen
    '''
    rows = {}
    
    def add_token_to_row(self, tablet, token):
        '''
        adds the token to corresponding row
        '''
        pass

    def add_position_to_row(self, tablet, token):
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
    def add_token(self, cell):
        '''
        adds token
        '''
        self.elements.append(Token(cell.value))
        return

    def add_position(self, cell):
        '''
        adds linebreak
        '''
        self.elements.append(Position(cell.value))
        return




    
