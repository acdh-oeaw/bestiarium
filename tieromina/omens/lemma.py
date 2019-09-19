from xml.etree import ElementTree as ET

from .cell import Cell


class Lemma(Cell):
    '''
    Lemma as specified in the score
    Equivalent of "Cell"
    '''
    def __init__(self, cell):
        self.address = cell.address
        self.tokens = cell.tokens

    @property
    def tei(self):
        '''
        returns the TEI representation
        '''
        w = ET.Element('w')
        w.text = self.full_text
        return w
