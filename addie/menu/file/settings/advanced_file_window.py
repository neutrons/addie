from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem
import numpy as np

from addie.utilities import load_ui
from addie.initialization.widgets import main_tab as main_tab_initialization
from addie.utilities.general import get_list_algo

COLUMNS_WIDTH = [150, 150]


class AdvancedWindowLauncher(object):

    def __init__(self, parent=None):
        self.parent = parent

        if self.parent.advanced_window_ui is None:
            _advanced = AdvancedWindow(parent=self.parent)
            _advanced.show()
            self.parent.advanced_window_ui = _advanced
        else:
            self.parent.advanced_window_ui.setFocus()
            self.parent.advanced_window_ui.activateWindow()


class AdvancedWindow(QMainWindow):

    def __init__(self, parent=None):
        self.parent = parent

        QMainWindow.__init__(self, parent=parent)
        self.ui = load_ui('advanced_window.ui', baseinstance=self)

        self.setWindowTitle("Advanced Window for Super User Only !")
        self.init_widgets()

    def init_widgets(self):
        _idl_status = False
        _mantid_status = False
        if self.parent.post_processing == 'idl':
            _idl_status = True
        else:
            _mantid_status = True

        self.ui.idl_groupbox.setVisible(self.parent.advanced_window_idl_groupbox_visible)

        self.ui.idl_post_processing_button.setChecked(_idl_status)
        self.ui.mantid_post_processing_button.setChecked(_mantid_status)

        instrument = self.parent.instrument["full_name"]
        list_instrument_full_name = self.parent.list_instrument["full_name"]
        self.list_instrument_full_name = list_instrument_full_name
        list_instrument_short_name = self.parent.list_instrument["short_name"]
        self.list_instrument_short_name = list_instrument_short_name

        self.ui.instrument_comboBox.addItems(list_instrument_full_name)
        index_instrument = self.ui.instrument_comboBox.findText(instrument)
        self.ui.instrument_comboBox.setCurrentIndex(index_instrument)
        self.parent.instrument["short_name"] = list_instrument_short_name[index_instrument]
        self.parent.instrument["full_name"] = list_instrument_full_name[index_instrument]

        self.ui.cache_dir_label.setText(self.parent.cache_folder)
        self.ui.output_dir_label.setText(self.parent.output_folder)

        self.ui.centralwidget.setContentsMargins(10, 10, 10, 10)

        self.show_global_key_value_widgets(visible=_mantid_status)
        if _mantid_status:
            self.populate_list_algo()
            self._set_column_widths()

    def show_global_key_value_widgets(self, visible=False):
        self.ui.global_key_value_groupBox.setVisible(visible)

    def _set_column_widths(self):
        for _col, _width in enumerate(COLUMNS_WIDTH):
            self.ui.key_value_table.setColumnWidth(_col, _width)

    def _remove_blacklist_algo(self, list_algo):
        list_algo_without_blacklist = []
        for _algo in list_algo:
            if not (_algo in self.parent.align_and_focus_powder_from_files_blacklist):
                list_algo_without_blacklist.append(_algo)

        return list_algo_without_blacklist

    def remove_from_list(self,
                         original_list=[],
                         to_remove=[]):
        if to_remove:
            clean_list_algo = []
            for _algo in original_list:
                if not(_algo in to_remove):
                    clean_list_algo.append(_algo)
            return clean_list_algo
        else:
            return original_list

    def populate_list_algo(self):
        self.ui.list_key_comboBox.clear()

        raw_list_algo = get_list_algo('AlignAndFocusPowderFromFiles')
        list_algo_without_blacklist = self._remove_blacklist_algo(raw_list_algo)

        global_list_keys = self.parent.global_key_value.keys()
        global_unused_list_algo = self.remove_from_list(original_list=list_algo_without_blacklist,
                                                        to_remove=global_list_keys)
        self.ui.list_key_comboBox.addItems(global_unused_list_algo)

    def add_key_value(self):
        self._add_new_row_at_bottom()
        self.update_key_value_widgets()
        self.populate_list_algo()
        self.ui.list_key_comboBox.setFocus()

    def _add_row(self, row=-1, key='', value=""):
        self.ui.key_value_table.insertRow(row)
        self._set_item(key, row, 0)
        self._set_item(value, row, 1)

    def _set_item(self, text, row, column):
        key_item = QTableWidgetItem(text)
        self.ui.key_value_table.setItem(row, column, key_item)

    def _add_new_row_at_bottom(self):
        nbr_row = self.get_nbr_row()
        key = self.get_current_selected_key()
        value = str(self.ui.new_value_widget.text())
        self.parent.global_key_value[key] = value
        self._add_row(row=nbr_row, key=key, value=value)
        self.ui.new_value_widget.setText("")

    def get_current_selected_key(self):
        return str(self.ui.list_key_comboBox.currentText())

    def get_nbr_row(self):
        return self.ui.key_value_table.rowCount()

    def _get_selected_row_range(self):
        selection = self.ui.key_value_table.selectedRanges()
        from_row = selection[0].topRow()
        to_row = selection[0].bottomRow()
        return np.arange(from_row, to_row+1)

    def _remove_rows(self, row_range):
        first_row_selected = row_range[0]
        for _ in row_range:
            self.ui.key_value_table.removeRow(first_row_selected)

    def remove_key_value_selected(self):
        selected_row_range = self._get_selected_row_range()
        self._remove_rows(selected_row_range)
        self.update_key_value_widgets()
        self.update_global_key_value()
        self.populate_list_algo()

    def update_global_key_value(self):
        nbr_row = self.get_nbr_row()
        global_key_value = {}
        for _row in np.arange(nbr_row):
            _key = self._get_cell_value(_row, 0)
            _value = self._get_cell_value(_row, 1)
            global_key_value[_key] = _value
        self.parent.global_key_value = global_key_value

    def _get_cell_value(self, row, column):
        item = self.ui.key_value_table.item(row, column)
        return str(item.text())

    def _what_state_remove_button_should_be(self):
        nbr_row = self.get_nbr_row()
        if nbr_row > 0:
            enable = True
        else:
            enable = False
        return enable

    def update_key_value_widgets(self):
        enable = self._what_state_remove_button_should_be()
        self.ui.remove_selection_button.setEnabled(enable)

    def post_processing_clicked(self):
        if self.ui.idl_post_processing_button.isChecked():
            # _index = 0
            _post = 'idl'
            _idl_groupbox_visible = True
        else:
            # _index = 1
            _post = 'mantid'
            _idl_groupbox_visible = False

        self.ui.idl_groupbox.setVisible(_idl_groupbox_visible)
#        self.parent.ui.stackedWidget.setCurrentIndex(_index)
        self.parent.post_processing = _post
        self.parent.activate_reduction_tabs() # hide or show right tabs
        self.parent.advanced_window_idl_groupbox_visible = _idl_groupbox_visible
        self.show_global_key_value_widgets(visible= not _idl_groupbox_visible)

    def instrument_changed(self, index):
        self.parent.instrument["short_name"] = self.list_instrument_short_name[index]
        self.parent.instrument["full_name"] = self.list_instrument_full_name[index]
        main_tab_initialization.set_default_folder_path(self.parent)

    def cache_dir_button_clicked(self):
        _cache_folder = QFileDialog.getExistingDirectory(caption="Select Cache Folder ...",
                                                         directory=self.parent.cache_folder,
                                                         options=QFileDialog.ShowDirsOnly)
        if _cache_folder:
            self.ui.cache_dir_label.setText(str(_cache_folder))
            self.parent.cache_folder = str(_cache_folder)

    def output_dir_button_clicked(self):
        _output_folder = QFileDialog.getExistingDirectory(caption="Select Output Folder ...",
                                                          directory=self.parent.output_folder,
                                                          options=QFileDialog.ShowDirsOnly)
        if _output_folder:
            self.ui.output_dir_label.setText(str(_output_folder))
            self.parent.output_folder = str(_output_folder)

    def add_global_key_value_to_all_rows(self):
        pass



    def closeEvent(self, c):
        self.add_global_key_value_to_all_rows()
        self.parent.advanced_window_ui = None
