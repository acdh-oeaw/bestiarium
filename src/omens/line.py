import logging
from collections import UserList

from .lemma import BreakEnd, BreakStart, Lemma

logger = logging.getLogger(__name__)


class Line(UserList):
    '''
    Common base class for rows in an Omen Spreadsheet (Score, Readings, etc.)
    '''

    def __init__(self, omen_prefix):
        super().__init__()
        self.omen_prefix = omen_prefix

    def connect_damaged_ends(self):
        '''
        The lemmas are reviewed once again and
        damages that span across lemmas
        are appropriately connected
        '''
        damage_stack = []
        for lemma in self.data:
            if isinstance(lemma, Lemma):
                for token in lemma.tokens:
                    if isinstance(token, BreakStart):
                        damage_stack.append(token.xml_id)
                    elif isinstance(token, BreakEnd):
                        try:
                            damage_start = damage_stack.pop()
                            token.corresp = damage_start
                        except IndexError:
                            logging.warning(
                                'Found damage end without beginning @ %s',
                                lemma)
