import logging
from xml.etree import ElementTree as ET


class Comments:
    '''
    Philological commentary on the omen
    '''
    def __init__(self):
        self.label = 'Philological Commentary'
        self.reference = ''
        self.text = []
        
    def append(self, row):
        '''
        Appends to the text of the comment
        '''
        row_text = ''
        for cell in row[1:]:
            if cell.value: row_text = row_text + ' ' + cell.value if row_text else cell.value

        self.text.append(row_text)
        return    

    @property
    def tei_export(self):
        export_div = ET.Element('div', {'n': self.label,
                                    'type': 'commentary'})
        for line in self.text:
            para = ET.SubElement(export_div, 'p')
            para.text = line

        return export_div
                            
                
            

    
