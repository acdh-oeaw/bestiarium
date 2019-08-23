import logging
from typing import NamedTuple

class Tablet(NamedTuple):
    witness : str
    ref: str = ''    
    JOIN_DELIMITER = '+'

    @property
    def siglum(self):
        return self.witness.split(self.JOIN_DELIMITER)[0]

    @property
    def joins(self):
        if self.JOIN_DELIMITER in self.witness:
            return self.witness.split(self.JOIN_DELIMITER)[1:]
        return []
    
    @property
    def witness_id(self):
        return "wit_" + re.sub("[^A-Za-z0-9\-_:\.]+", "_", self.witness)

    def __str__(self):
        return f'{self.siglum}_{self.ref}'
