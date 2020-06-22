'''
A chapter is built by reading one or more workbooks
'''
from .omen import Omen
from .workbook import Workbook


class Chapter:
    '''
    Assuming that one workbook contains omens from one chapter,
    the chapter is first identified,
    existing data on the chapter is fetched
    new omens from the omen are added to the chapter
    '''

    def add_from_workbook(self, workbook):
        for sheet in workbook.sheets:
            omen = Omen(**sheet.__dict__)
