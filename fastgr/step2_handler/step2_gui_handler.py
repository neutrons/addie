from PyQt4 import QtGui, QtCore
import os

from step2_handler.table_handler import TableHandler


class Step2GuiHandler(object):

    hidrogen_range = [1, 50]
    no_hidrogen_range = [10, 50]
    current_folder = ""
    default_q_range = [0.2, 31.4]
    
    def __init__(self, parent=None):
        self.parent_no_ui = parent
        self.parent = parent.ui
        self.current_folder = parent.current_folder
        
    def move_to_folder(self):
        _current_folder = self.current_folder
        _new_folder = QtGui.QFileDialog.getExistingDirectory(parent = self.parent_no_ui,
                                                             caption = "Select working directory",
                                                             directory = self.current_folder)
        
        if str(_new_folder):
            os.chdir(_new_folder)
            self.parent.current_folder_label.setText(_new_folder)
        
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
        self.check_run_ndabs_button()
        self.check_run_sum_scans_button()
        
    def check_run_sum_scans_button(self):
        
        _status = True
        if not self.parent.table.rowCount() > 0:
            _status = False
            
        if not self.at_least_one_row_checked():
            _status = False
            
        self.parent.run_sum_scans_button.setEnabled(_status)
        
    def check_run_ndabs_button(self):
        
        _status = True
        if not self.parent.table.rowCount() > 0:
            _status = False
            
        if not self.at_least_one_row_checked():
            _status = False
            
        if self.any_fourier_filter_widgets_empty():
            _status = False
            
        if self.any_plazcek_widgets_empty():
            _status = False

        if self.any_q_range_widgets_empty():
            _status = False

        # make sure the row checked have none empty metadata fields
        if _status:
            for _row in range(self.parent.table.rowCount()):
                _this_row_status_ok = self.check_if_this_row_is_ok(_row)
                if not _this_row_status_ok:
                    _status = False
                    break

        self.parent.run_ndabs_button.setEnabled(_status)

    def at_least_one_row_checked(self):
        o_table_handler = TableHandler(parent = self.parent_no_ui)
        o_table_handler.retrieve_list_of_selected_rows()
        list_of_selected_row = o_table_handler.list_selected_row
        if len(list_of_selected_row) > 0:
            return True
        else:
            return False

    def check_if_this_row_is_ok(self, row):
        _status_ok = True
        _selected_widget = self.parent.table.cellWidget(row, 0)
        if (_selected_widget.checkState() == QtCore.Qt.Checked):
            _table_handler = TableHandler(parent = self.parent_no_ui)
            for _column in range(1,7):
                if _table_handler.retrieve_item_text(row, _column) == '':
                    _status_ok = False
                    break

        return _status_ok

    def any_plazcek_widgets_empty(self):
        _min = str(self.parent.plazcek_fit_range_min.text()).strip()
        if _min == "":
            return True
    
        _max = str(self.parent.plazcek_fit_range_max.text()).strip()
        if _max == "":
            return True

        return False
        
    def any_q_range_widgets_empty(self):
        _min = str(self.parent.q_range_min.text()).strip()
        if _min == "":
            return True
    
        _max = str(self.parent.q_range_max.text()).strip()
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
    
    def reset_q_range(self):
        _q_min = "%s" %str(self.default_q_range[0])
        _q_max = "%s" %str(self.default_q_range[1])
        self.parent.q_range_min.setText(_q_min)
        self.parent.q_range_max.setText(_q_max)
        