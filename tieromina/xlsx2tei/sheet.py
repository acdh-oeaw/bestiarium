from .cell import Cell
from .namespaces import NS
from .row import Row


class Sheet:
    '''
    A single sheet from a workbook
    '''
    def __init__(self, *, sheet_name, xml, style, shared_strings):
        self.sheet_name = sheet_name
        self.xml = xml
        self.style = style
        self.shared_strings = shared_strings

    def __str__(self):
        return f'{self.sheet.sheet_name}'

    def cell_at(self, address: str) -> Cell:
        '''
        Returns cell at a given location (like A23)
        '''
        c = self.xml.find(f'.//*[@r="{address}"]')
        return Cell(self, c)

    def row_at(self, address: str) -> Cell:
        '''
        Returns row at a given location (like "23")
        '''
        row = self.xml.find(f'.//*[@r="{address}"]')
        return Row(self, row)

    @property
    def rows(self):
        '''
        Yields the row name and the row
        '''
        rows = self.xml.findall('spreadsheetml:sheetData/spreadsheetml:row',
                                NS)
        for row_element in rows:
            yield Row(sheet=self, xml=row_element)
