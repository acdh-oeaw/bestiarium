from xml.etree import ElementTree as ET

from .cell import Cell, Chunk


class Token:
    '''
    A unit smaller than a chunk - separating breaks/damages from the words and noting where they stop
    '''

    def __init__(self, text, fmt, plain_txt=True):
        self.plain_text = plain_txt
        self.text = text
        self.fmt = fmt

    @property
    def xml_id(self):
        return self._xml_id

    @xml_id.setter
    def xml_id(self, xml_id):
        self._xml_id = xml_id

    def __repr__(self):
        return str(self.__dict__)


class BreakStart(Token):
    '''
    Anchor to mark the beginning of a break
    '''

    def __init__(self, text, fmt):
        super().__init__(text=text, fmt=fmt, plain_txt=False)
        self.span_to = ''

    @property
    def tei(self):
        if self.text == '[':
            anchor = ET.Element('anchor', {'type': 'breakStart'})
            anchor.tail = ''
        elif self.text == '˹':
            anchor = ET.Element('damageSpan', {'spanTo': self.span_to})
            anchor.tail = ''

        return anchor

    @property
    def end_token(self):
        return self._end_token

    @end_token.setter
    def end_token(self, end_token):
        self._end_token = end_token


class BreakEnd(Token):
    '''
    Anchor to mark the end of a break
    '''

    def __init__(self, text, fmt):
        super().__init__(text=text, fmt=fmt, plain_txt=False)

    @property
    def tei(self):
        anchor = ET.Element('anchor', {'type': 'breakEnd'})
        anchor.tail = ''
        return anchor


class Missing(Token):
    '''
    Missing signs
    '''

    def __init__(self, text, fmt):
        super().__init__(text=text, fmt=fmt, plain_txt=False)
        self.quantity = 1

    def widen_gap(self):
        self.quantity += 1

    @property
    def tei(self):

        anchor = ET.Element('gap', {
            'quantity': self.quantity,
            'unit': 'signs'
        })
        anchor.tail = ''


class Lemma:
    '''
    Lemma as specified in the score
    Equivalent of "Cell"
    '''

    def __init__(self, cell):
        self.column_name = cell.column_name
        self.tokens = []
        token_text = ''
        for chunk in cell.chunks:
            if token_text:
                self.tokens.append(
                    Token(text=token_text, fmt=chunk.cell_format))
                token_text = ''
            for char in chunk.text:
                if char in '[]˹˺':
                    # TODO: Check that spaces mean nothing in general
                    self.tokens.append(
                        Token(text=token_text, fmt=chunk.cell_format))
                    token_text = ''
                    if char in '[˹':
                        self.tokens.append(
                            BreakStart(text=char, fmt=chunk.cell_format))
                    elif char in '˺]':
                        self.tokens.append(
                            BreakEnd(text=char, fmt=chunk.cell_format))
                    elif char == 'x':
                        if isinstance(self.tokens[-1], Missing):
                            self.tokens[-1].widen_gap()
                        else:
                            self.tokens.append(Missing(fmt=chunk.cell_format))
                    else:
                        pass
                else:
                    token_text += char

        if token_text:
            self.tokens.append(Token(text=token_text, fmt=chunk.cell_format))

    @property
    def xml_id(self):
        return f'w{self.column_name}'

    def score_tei(self, witness):
        '''
        returns the TEI representation
        TODO: Align this with the convention
        '''
        w = ET.Element('rdg', {'wit': witness.xml_id})
        w = self.tei_body(w)
        return w

    @property
    def reading_tei(self):
        w = ET.Element('w')
        w = self.tei_body(w)
        return w

    def tei_body(self, w):
        w.text = ''
        anchor = None
        for token in self.tokens:
            if token.plain_text is True:
                if anchor is not None:
                    anchor.tail += token.text
                else:
                    w.text += token.text
            else:
                anchor = token.tei
                w.append(anchor)
        return w
