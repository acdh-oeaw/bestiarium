"""
A standalone representation of contents inside a cell in a spreadsheet
"""
from typing import NamedTuple


class CellFormat(NamedTuple):
    """
    Holds text cell_format properties
    at a cell level or within a cell
    """

    bold: bool = False
    italics: bool = False
    subscript: bool = False
    superscript: bool = False
    color: str = None
    bgcolor: str = None


class Chunk(NamedTuple):
    """
    Smallest unit of information in a cell with the same formatting
    """

    given_text: str
    cell_format: CellFormat
    complete: bool = False  # whether this is the only chunk in the cell

    @property
    def text(self):
        return self.given_text.strip()


class Cell:
    """
    A list of "Chunk" objects, the address of the cell and some methods
    """

    def __init__(self, address: str = ""):
        self.chunks = []
        self.address = address

    def add_chunk(self, chunk: Chunk):
        self.chunks.append(chunk)

    @property
    def full_text(self):
        """
        Returns full text from the cell without formatting
        """
        text = ""
        for chunk in self.chunks:
            if not chunk.text:
                continue

            text = text + chunk.text.strip()

        return text

    @property
    def is_empty(self):
        return str(self.full_text).strip() == ""

    @property
    def column_name(self):
        """
        Returns the column name from the cell address
        """
        col_name = ""
        for char in self.address:
            if char.isalpha():
                col_name += char
            else:
                return col_name
        return col_name

    @property
    def row_name(self):
        """
        Returns the row name from the cell address
        """
        r_name = ""
        for char in self.address:
            if char.isalpha():
                pass
            else:
                r_name += char
        return r_name

    def __str__(self):
        return f"[Cell {self.address}]: {self.chunks}"

    def __repr__(self):
        return f"Number of chunks: {len(self.chunks)}\nFull text: {self.full_text}"
