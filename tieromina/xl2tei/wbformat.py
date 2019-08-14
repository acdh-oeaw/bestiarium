class WBFormat:
    '''
    Formatting info of the workbook
    '''
    LINE_NUM_COLOR = (255, 0, 0)
    
    def __init__(self, **kwargs):
        self.xf_list = kwargs.get('xf_list')
        self.font_list = kwargs.get('font_list')
        self.colour_map = kwargs.get('colour_map')
        return
    
    
    def cell_font(self, cell):
        cell_format = self.xf_list[cell.xf_index]
        cell_font = self.font_list[cell_format.font_index]
        return cell_font
    
    def cell_font_color(self, cell):
        cell_font = self.cell_font(cell)
        cell_font_colour = self.colour_map[cell_font.colour_index]
        return cell_font_color

    def match_cell_font_color(self, cell, color):
        return self.cell_font_colour(cell) == color

    def is_line_num(self, cell):
        return match_cell_font_color(cell, WBFormat.LINE_NUM_COLOR)
    
        
    
        
