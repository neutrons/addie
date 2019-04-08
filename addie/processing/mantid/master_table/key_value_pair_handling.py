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

    def cancel_clicked(self):
        self.close()

    def closeEvent(self, c):
        self.main_window.key_value_pair_ui_position = self.pos()
        self.main_window.key_value_pair_ui = None

