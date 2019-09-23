from xml.etree import ElementTree as ET

from .cell import Cell, Chunk


class Token:
    '''
    A unit smaller than a chunk - separating breaks/damages from the words and noting where they stop
    '''

    def __init__(self, text, fmt):
        self.text = text
        self.fmt = fmt


class Lemma:
    '''
    Lemma as specified in the score
    Equivalent of "Cell"
    '''

    def __init__(self, cell, witness):
        self.witness = witness
        self.column_name = cell.column_name
        self.tokens = []
        for chunk in cell.chunks:
            self.tokens.append(Token(chunk.text, chunk.cell_format))

    @property
    def xml_id(self):
        return f'w{self.column_name}'

    @property
    def tei(self):
        '''
        returns the TEI representation
        TODO: Align this with the convention
        '''
        w = ET.Element('rdg', {'wit': self.witness.xml_id})
        w.text = ''
        anchor = None
        for token in self.tokens:
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
