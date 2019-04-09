from __future__ import (absolute_import, division, print_function)
import numpy as np
from qtpy.QtWidgets import QMainWindow, QTableWidgetItem

from addie.utilities import load_ui


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

    def __init__(self, main_window=None, key=None):
        self.main_window = main_window
        self.key = key

        QMainWindow.__init__(self, parent=main_window)
        self.ui = load_ui('manual_key_value_input.ui', baseinstance=self)

        self.init_widgets()

    def init_widgets(self):
        previous_key_value_dict = self._get_previous_key_value_dict()
        for _row,_key in enumerate(previous_key_value_dict.keys()):
            _value = previous_key_value_dict[_key]
            self._add_row(row=_row, key=_key, value=_value)

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
        self._check_remove_button()
        self.ui.new_key_widget.setFocus()

    def _add_new_row_at_bottom(self):
        nbr_row = self.get_nbr_row()
        key = str(self.ui.new_key_widget.text())
        value = str(self.ui.new_value_widget.text())
        self._add_row(row=nbr_row, key=key, value=value)
        self.ui.new_key_widget.setText("")
        self.ui.new_value_widget.setText("")

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

