from xml.etree import ElementTree as ET

from .cell import Cell, Token


class Lemma:
    '''
    Lemma as specified in the score
    Equivalent of "Cell"
    '''
    def __init__(self, cell, witness):
        self.witness = witness
        self.cell = cell

    @property
    def xml_id(self):
        return f'w{self.cell.column_name}'

    @property
    def tei(self):
        '''
        returns the TEI representation
        TODO: Align this with the convention
        '''
        w = ET.Element('rdg', {'wit': self.witness.xml_id})
        w.text = ''
        anchor = None
        for token in self.cell.tokens:
            for char in token.text:
                if char == '[':
                    anchor = ET.SubElement(w, 'anchor', {'type': 'breakStart'})
                    anchor.tail = ''
                elif char == ']':
                    anchor = ET.SubElement(w, 'anchor', {'type': 'breakEnd'})
                    anchor.tail = ''
                else:
                    if anchor is not None:
                        anchor.tail += char
                    else:
                        w.text += char
        return w
