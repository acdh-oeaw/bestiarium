class WBFormat:
    '''
    Formatting info of the workbook
    '''
    LINE_NUM_COLOR = (255, 0, 0)

    def __init__(self, workbook):
        self.xf_list = workbook.xf_list
        self.font_list = workbook.font_list
        self.colour_map = workbook.colour_map
        return

    def _cell_font(self, cell):
        cell_format = self.xf_list[cell.xf_index]
        cell_font = self.font_list[cell_format.font_index]
        return cell_font

    def _cell_font_colour(self, cell):
        _cell_font = self._cell_font(cell)
        colour = self.colour_map[_cell_font.colour_index]
        return colour

    def _match_cell_font_color(self, cell, color):
        return self._cell_font_colour(cell) == color

    def is_line_num(self, cell):

        return self._match_cell_font_color(cell, WBFormat.LINE_NUM_COLOR)
