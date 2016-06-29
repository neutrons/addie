class Step2GuiHandler(object):

    hidrogen_range = [1, 50]
    no_hidrogen_range = [10, 50]
    
    def __init__(self, parent=None):
        self.parent = parent.ui
        
    def hidrogen_clicked(self):
        _range = self.hidrogen_range
        self.populate_hidrogen_range(_range)
    
    def no_hidrogen_clicked(self):
        _range = self.no_hidrogen_range
        self.populate_hidrogen_range(_range)

    def populate_hidrogen_range(self, fit_range):
        min_value, max_value = fit_range
        self.parent.plazcek_fit_range_min.setText("%d" % min_value)
        self.parent.plazcek_fit_range_max.setText("%d" % max_value)
    
    def yes_background_clicked(self):
        self.parent.background_line_edit.setEnabled(True)
        self.parent.background_comboBox.setEnabled(True)
    
    def no_background_clicked(self):
        self.parent.background_line_edit.setEnabled(False)
        self.parent.background_comboBox.setEnabled(False)
        
    def background_index_changed(self, row_index = -1):
        if row_index == -1:
            return
        self.parent.background_line_edit.setText(self.parent.table.item(row_index, 2).text())
        
    def check_gui(self):
        self.check_create_sample_properties_files_button()
        
    def check_create_sample_properties_files_button(self):
        
        _status = True
        if not self.parent.table.rowCount() > 0:
            _status = False
            
        if self.any_fourier_filter_widgets_empty():
            _status = False
            
        if self.any_plazcek_widgets_empty():
            _status = False

        self.parent.create_sample_properties_files_button.setEnabled(_status)
        self.parent.run_ndabs_button.setEnabled(_status)

    def any_plazcek_widgets_empty(self):
        _min = str(self.parent.plazcek_fit_range_min.text()).strip()
        if _min == "":
            return True
    
        _max = str(self.parent.plazcek_fit_range_max.text()).strip()
        if _max == "":
            return True

        return False
        
    def any_fourier_filter_widgets_empty(self):
        _from = str(self.parent.fourier_filter_from.text()).strip()
        if _from == "":
            return True
        
        _to = str(self.parent.fourier_filter_to.text()).strip()
        if _to == "":
            return True
        
        return False