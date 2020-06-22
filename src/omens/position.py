'''
Classes to decode the position information in a cell
'''

LINENUM_COLOR = 'FFFF0000'

import logging
from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)


class Position:
    '''
    Line and column position information in a score
    TODO: Omen 23.4 has a line number like ii 21 (23.5*)
    '''
    @staticmethod
    def is_position_cell(cell):
        for chunk in cell.chunks:
            if chunk.cell_format.color == LINENUM_COLOR and chunk.cell_format.italics:
                return True

    def __init__(self, cell, witness):
        self.witness = witness
        self.line = None
        self.column = None
        self.text = ''
        self.supplement_text = ''

        # Separate text that does not confirm to line number formatting
        for chunk in cell.chunks:
            if chunk.cell_format.color == LINENUM_COLOR and chunk.cell_format.italics:
                self.text += chunk.text  # Line/column number info
            else:
                self.supplement_text += chunk.text  # Any other info

        if self.supplement_text:
            logger.warning(
                'Found more than one formatting in line number cell: \n%s',
                cell)
        # Identify if the cell contains column information
        parts = self.text.split()
        if (parts[0][0].isnumeric()
                or parts[0][0] == 'r'):  # line number or reverse
            # Only line number - multiple columns obverse/reverse is not indicated
            self.line = LineInfo(witness, self.text, self.supplement_text)

        elif parts[0][0].isalpha():  # column  number
            self.column = ColumnInfo(witness, parts[0])
            self.line = LineInfo(witness, ' '.join(parts[1:]),
                                 self.supplement_text)
        else:
            logging.warning('Neither line nor column: "%s" from witness "%s',
                            cell, witness)
            self.line = LineInfo(witness, self.text, self.supplement_text)

    def __repr__(self):
        return (
            f'Witness: {self.witness}, Line: {self.line}, Column: {self.column}'
        )


class LineInfo:
    '''
    Line number information in the tablet
    '''
    def __init__(self, witness, text, supplement_text=''):
        self.witness = witness
        self.broken = "'" in text
        self.reverse = "r." in text
        self.text = text
        self.supplement_text = supplement_text

    @property
    def tei(self):
        lb = ET.Element('lb', {'n': self.text, 'ed': self.witness.xml_id})
        if self.broken:
            # TODO: Finalise/confirm encoding attribute
            lb.attrib['broken'] = 'True'
        if self.reverse:
            # TODO: Finalise/confirm encoding attribute
            lb.attrib['reverse'] = 'True'

        if self.supplement_text:
            # TODO: Finalise/confirm encoding attribute
            lb.attrib['extra_info'] = self.supplement_text
        return lb


class ColumnInfo:
    '''
    Column number information in the tablet
    '''
    def __init__(self, witness, text):
        self.witness = witness
        self.text = text

    @property
    def tei(self):
        cb = ET.Element('cb', {'n': self.text, 'ed': self.witness.xml_id})
        return cb
