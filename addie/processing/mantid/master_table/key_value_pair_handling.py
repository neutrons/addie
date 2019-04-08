from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import QMainWindow
from addie.utilities import load_ui



class KeyValuePairHandling:

    def __init__(self, main_window=None, key=None):
        if main_window.key_value_pair_ui is None:
            o_key_value = KeyValuePairWindow(main_window=main_window)
            main_window.key_value_pair_ui = o_key_value
            if main_window.key_value_pair_ui_position:
                main_window.key_value_pair_ui.move(main_window.key_value_pair_ui_position)
            o_key_value.show()
        else:
            main_window.key_value_pair_ui.setFocus()
            main_window.key_value_pair_ui.activateWindow()


class KeyValuePairWindow(QMainWindow):

    def __init__(self, main_window=None, key=None):
        self.main_window = main_window
        self.key = key

        QMainWindow.__init__(self, parent=main_window)
        self.ui = load_ui('manual_key_value_input.ui', baseinstance=self)

        self.init_widgets()

    def init_widgets(self):
        pass

    def ok_clicked(self):
        # do something here
        self.close()

    def add_clicked(self):
        self._add_empty_row_at_bottom()
        self._check_remove_button()

    def _add_empty_row_at_bottom(self):
        nbr_row = self.get_nbr_row()
        self.ui.key_value_table.insertRow(nbr_row)

    def remove_clicked(self):
        self._check_remove_button()

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

