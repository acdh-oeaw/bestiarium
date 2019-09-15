from typing import NamedTuple


class Format(NamedTuple):
    '''
    Holds text format properties
    at a cell level or within a cell
    '''
    bold: bool = False
    italics: bool = False
    subscript: bool = False
    superscript: bool = False
    color: str = None
    bgcolor: str = None


class Token(NamedTuple):
    '''
    Smallest unit of information in a cell with the same formatting
    '''
    text: str
    format: Format
    complete: bool = False  # whether this is the only token in the cell
