import logging


class Tablet:
    '''
    Represents a physical tablet on which a score/reading is based
    '''
    JOIN_DELIMITER = '+'
    
    def __init__(self, siglum_info, reference=None):
        self.siglum_info = siglum_info
        self.reference = reference
        
        siglum_parts = siglum_info.split(self.JOIN_DELIMITER)
        self.siglum = siglum_parts[0]

        self.joins = siglum_parts[1:] if len(siglum_parts) > 1 else None
        return

    def __hash__(self):
        return hash(str(self))

    def __eq__(self,other):
        return self.siglum_info == other.siglum_info and self.reference == other.reference


    def __str__(self):
        return f'{self.siglum_info} ({self.reference})'

    
    def __repr__(self):
        return f'Given text: {self.siglum_info} Reference: ({self.reference})\n' + \
            f'Siglum: {self.siglum}\nJoins: {self.joins}'
