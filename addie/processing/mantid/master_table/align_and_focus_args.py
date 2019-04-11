from __future__ import (absolute_import, division, print_function)
import numpy as np
from qtpy.QtWidgets import QMainWindow, QTableWidgetItem

from addie.utilities import load_ui
from addie.utilities.general import get_list_algo

COLUMNS_WIDTH = [150, 150]


class AlignAndFocusArgsHandling:

    def __init__(self, main_window=None, key=None):
        if main_window.key_value_pair_ui is None:
            o_key_value = AlignAndFocusArgsWindow(main_window=main_window, key=key)
            main_window.key_value_pair_ui = o_key_value
            if main_window.key_value_pair_ui_position:
                main_window.key_value_pair_ui.move(main_window.key_value_pair_ui_position)
            o_key_value.show()
        else:
            main_window.key_value_pair_ui.setFocus()
            main_window.key_value_pair_ui.activateWindow()


class AlignAndFocusArgsWindow(QMainWindow):

    list_algo_without_blacklist = None
    unused_list_algo = None

    local_list_key_loaded = []

    def __init__(self, main_window=None, key=None):
        self.main_window = main_window
        self.key = key

        QMainWindow.__init__(self, parent=main_window)
        self.ui = load_ui('manual_key_value_input.ui', baseinstance=self)

        self.init_widgets()

    def init_widgets(self):
        self._init_previous_key_value()
        self._set_column_widths()
        self._init_list_algo_combobox()

    def _init_list_algo_combobox(self):
        list_algo = get_list_algo('AlignAndFocusPowderFromFiles')
        list_algo_without_blacklist = self.remove_blacklist_algo(list_algo)
        self.list_algo_without_blacklist = list_algo_without_blacklist
        self.populate_list_algo()

    def populate_list_algo(self):
        self.ui.list_key_comboBox.clear()
        self.create_clean_list_algo()
        self.ui.list_key_comboBox.addItems(self.unused_list_algo)

    def remove_blacklist_algo(self, list_algo):
        list_algo_without_blacklist = []
        for _algo in list_algo:
            if not(_algo in self.main_window.align_and_focus_from_files_blacklist):
                list_algo_without_blacklist.append(_algo)

        return list_algo_without_blacklist

    def create_clean_list_algo(self):
        list_algo = self.list_algo_without_blacklist

        previous_key_value_dict = self._get_previous_key_value_dict()
        list_key_already_loaded = previous_key_value_dict.keys()
        global_unused_list_algo = self.remove_from_list(original_list=list_algo,
                                                        to_remove=list_key_already_loaded)

        local_list_key_loaded = self.get_local_list_key_loaded()
        global_and_local_unused_list_algo = self.remove_from_list(original_list=global_unused_list_algo,
                                                                  to_remove=local_list_key_loaded)

        self.unused_list_algo = global_and_local_unused_list_algo

    def get_local_list_key_loaded(self):
        nbr_row = self.ui.key_value_table.rowCount()
        list_local_key_loaded = []
        for _row in np.arange(nbr_row):
            _item = str(self.ui.key_value_table.item(_row, 0).text())
            list_local_key_loaded.append(_item)
        return list_local_key_loaded

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

    def _set_column_widths(self):
        for _col, _width in enumerate(COLUMNS_WIDTH):
            self.ui.key_value_table.setColumnWidth(_col, _width)

    def _init_previous_key_value(self):
        previous_key_value_dict = self._get_previous_key_value_dict()
        for _row, _key in enumerate(previous_key_value_dict.keys()):
            _value = previous_key_value_dict[_key]
            self._add_row(row=_row, key=_key, value=_value)
            self.local_list_key_loaded.append(_key)

    def _get_previous_key_value_dict(self):
        master_table_list_ui = self.main_window.master_table_list_ui[self.key]
        return master_table_list_ui['align_and_focus_args_infos']

    def ok_clicked(self):
        self._save_key_value_infos()
        self.close()

    def _save_key_value_infos(self):
        master_table_list_ui = self.main_window.master_table_list_ui[self.key]
        key_value_dict = self._get_key_value_dict()
        master_table_list_ui['align_and_focus_args_infos'] = key_value_dict
        self.main_window.master_table_list_ui[self.key] = master_table_list_ui

    def _get_key_value_dict(self):
        key_value_dict = {}
        for _row in np.arange(self.get_nbr_row()):
            _key = str(self.ui.key_value_table.item(_row, 0).text())
            _value = str(self.ui.key_value_table.item(_row, 1).text())
            key_value_dict[_key] = _value
        return key_value_dict

    def add_clicked(self):
        self._add_new_row_at_bottom()
        self.populate_list_algo()
        self._check_remove_button()
        self.ui.list_key_comboBox.setFocus()

    def _add_new_row_at_bottom(self):
        nbr_row = self.get_nbr_row()
        key = self.get_current_selected_key()
        self.local_list_key_loaded.append(key)
        value = str(self.ui.new_value_widget.text())
        self._add_row(row=nbr_row, key=key, value=value)
        self.ui.new_value_widget.setText("")

    def get_current_selected_key(self):
        return str(self.ui.list_key_comboBox.currentText())

    def _add_row(self, row=-1, key='', value=""):
        self.ui.key_value_table.insertRow(row)
        self._set_item(key, row, 0)
        self._set_item(value, row, 1)

    def _set_item(self, text, row, column):
        key_item = QTableWidgetItem(text)
        self.ui.key_value_table.setItem(row, column, key_item)

    def remove_clicked(self):
        selected_row_range = self._get_selected_row_range()
        self._remove_rows(selected_row_range)
        self._check_remove_button()
        self.populate_list_algo()

    def _remove_rows(self, row_range):
        first_row_selected = row_range[0]
        for _ in row_range:
            self.ui.key_value_table.removeRow(first_row_selected)

    def _get_selected_row_range(self):
        selection = self.ui.key_value_table.selectedRanges()
        from_row = selection[0].topRow()
        to_row = selection[0].bottomRow()
        return np.arange(from_row, to_row+1)

    def get_nbr_row(self):
        return self.ui.key_value_table.rowCount()

    def _check_remove_button(self):
        enable = self._what_state_remove_button_should_be()
        self.ui.remove_selection_button.setEnabled(enable)

    def _what_state_remove_button_should_be(self):
        nbr_row = self.get_nbr_row()
        if nbr_row > 0:
            enable = True
        else:
            enable = False
        return enable

    def cancel_clicked(self):
        self.close()

    def closeEvent(self, c):
        self.main_window.key_value_pair_ui_position = self.pos()
        self.main_window.key_value_pair_ui = None
