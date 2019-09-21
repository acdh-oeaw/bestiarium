from xml.etree import ElementTree as ET

from .cell import Cell


class Lemma(Cell):
    '''
    Lemma as specified in the score
    Equivalent of "Cell"
    '''
    def __init__(self, cell, witness):
        self.witness = witness
        self.address = cell.address
        self.tokens = cell.tokens

    @property
    def xml_id(self):
        return f'w{self.column_name}'

    @property
    def tei(self):
        '''
        returns the TEI representation
        TODO: Align this with the convention
        '''
        w = ET.Element('rdg')
        for token in self.tokens:
            t = ET.SubElement(w, 'token')
            t.text = token.text
        return w
