from PyQt4 import QtGui


class InitStep2(object):
    
    small_field_width = 120
    column_widths = [60, 250, 250, small_field_width, small_field_width + 30, small_field_width, small_field_width, 
                     small_field_width, small_field_width, 80]

    def __init__(self, parent=None):
        self.parent = parent
        
        self.init_table_dimensions()

    def init_table_dimensions(self):
        
        for _index, _width in enumerate(self.column_widths):
            self.parent.ui.table.setColumnWidth(_index, _width)
        