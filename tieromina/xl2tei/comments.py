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
                    
                
            

    
