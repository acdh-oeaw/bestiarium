from .cell import Cell
from .namespaces import NS


class Row:
    '''
    A row/line in a sheet
    '''

    def __init__(self, *, sheet, xml):
        self.sheet = sheet
        self.xml = xml
        self.name = xml.attrib.get('r')

    @property
    def cells(self) -> Cell:
        '''
        Yields standalone cell instances representing the contents of a cell
        '''
        cells = self.xml.findall('spreadsheetml:c', NS)
        for elem in cells:
            yield Cell(self.sheet, elem)

    @property
    def is_empty(self):
        '''
        Returns True if the row contains no text
        '''
        for cell in self.cells:
            if cell.plain_text.strip():
                return False

        return True

    def cell_at_column(self, column: str) -> Cell:
        '''
        Returns the cell at the given column in the row
        '''
        return Cell(self.sheet,
                    self.xml.find(f'spreadsheetml:c[@r="{column}{self.name}"]',
                                  NS))

    def __str__(self):
        return f'{self.sheet}, row: {self.name}'

    def __repr__(self):
        return f'{self.sheet}, row: {self.name}'
