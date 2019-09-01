from .token import Token


class Score:
    '''
    represents the score of an omen
    '''
    parts = [
    ]  # defaultdict(dict) # each part is a dict ( {tablet:Token, ...})

    def add_token(self, cell_value: str):
        pass
