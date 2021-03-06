"""
Classes to decode the position information in a cell
"""
import logging
from xml.etree import ElementTree as ET

LINENUM_COLOR = "FFFF0000"


logger = logging.getLogger(__name__)


class Position:
    """
    Line and column position information in a score
    TODO: Omen 23.4 has a line number like ii 21 (23.5*)
    """

    @staticmethod
    def is_position_cell(cell):
        for chunk in cell.chunks:
            if chunk.cell_format.color == LINENUM_COLOR and chunk.cell_format.italics:
                return True

    def __init__(self, cell, witness, reference):
        self.witness = witness.split('___')[0]
        self.line = None
        self.column = None
        self.text = ""
        self.supplement_text = ""
        self.reference = reference

        # Separate text that does not confirm to line number formatting
        for chunk in cell.chunks:
            if chunk.cell_format.color == LINENUM_COLOR and chunk.cell_format.italics:
                self.text += chunk.text  # Line/column number info
            else:
                self.supplement_text += chunk.text  # Any other info

        if self.supplement_text:
            logger.warning(
                "Found more than one formatting in line number cell: \n%s", cell
            )
        # Identify if the cell contains column information
        parts = self.text.split()
        if parts[0][0].isnumeric() or parts[0][0] == "r" or parts[0][0] == "*":  # line number or reverse
            # Only line number - multiple columns obverse/reverse is not indicated
            self.line = LineInfo(self.witness, self.text, self.reference, self.supplement_text)

        elif parts[0][0].isalpha():  # column  number
            self.column = ColumnInfo(self.witness, parts[0])
            self.line = LineInfo(self.witness, " ".join(parts[1:]), self.supplement_text)
        else:
            logging.warning(
                f"Line/column number in an unexpected format at {cell.address} [witness {self.witness}]."
            )
            raise ValueError(
                f"Line/column number in an unexpected format at {cell.address} [witness {self.witness}]."
            )
            self.line = LineInfo(witness, self.text, self.supplement_text)

    def __repr__(self):
        return f"Witness: {self.witness}, Line: {self.line}, Column: {self.column}"


class LineInfo:
    """
    Line number information in the tablet
    """

    def __init__(self, witness, text, reference, supplement_text=""):
        self.witness = witness
        self.broken = "'" in text
        self.reverse = "r." in text
        self.text = text
        self.supplement_text = supplement_text
        self.reference = reference

    @property
    def tei(self):
        fixed_witt = self.witness.split('______')[0]
        if self.reference:
            lb = ET.Element("{http://www.tei-c.org/ns/1.0}lb", {"source": self.reference, "n": self.text,
                                                                "ed": fixed_witt})
        else:
            lb = ET.Element("{http://www.tei-c.org/ns/1.0}lb", {"n": self.text, "ed": fixed_witt})
        if self.broken:
            # TODO: Finalise/confirm encoding attribute
            lb.attrib["ana"] = "Broken"
        if self.reverse:
            # TODO: Finalise/confirm encoding attribute
            lb.attrib["ana"] = "Reverse"

        if self.supplement_text:
            # TODO: Finalise/confirm encoding attribute
            lb.attrib["extra_info"] = self.supplement_text
        return lb


class ColumnInfo:
    """
    Column number information in the tablet
    """

    def __init__(self, witness, text):
        self.witness = witness
        self.text = text

    @property
    def tei(self):
        fixed_witt = self.witness.split('______')[0]
        cb = ET.Element("cb", {"n": self.text, "ed": fixed_witt})
        return cb
