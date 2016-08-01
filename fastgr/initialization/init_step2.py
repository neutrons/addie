from PyQt4 import QtGui


class InitStep2(object):
    
    small_field_width = 120
    column_widths = [60, 250, 250, small_field_width, small_field_width + 30, small_field_width, small_field_width, 
                     small_field_width, small_field_width, 80]

    def __init__(self, parent=None):
        self.parent = parent
        
        self.init_table_dimensions()
        self.init_labels()

    def init_table_dimensions(self):
        
        for _index, _width in enumerate(self.column_widths):
            self.parent.ui.table.setColumnWidth(_index, _width)
            
    def init_labels(self):
        
        #q range
        _q_range_title = u"Q range (\u212B\u207B\u00b9)"
        self.parent.ui.q_range_group_box.setTitle(_q_range_title)
        
        #fourier filter
        _fourier_filter_title = u"Fourier filter (\u212B)"
        self.parent.ui.fourier_filter_group_box.setTitle(_fourier_filter_title)