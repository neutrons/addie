from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import QMainWindow

from addie.ui_advanced_window import Ui_MainWindow as UiMainWindow


class AdvancedWindow(QMainWindow):

    def __init__(self, parent=None):
        self.parent = parent

        QMainWindow.__init__(self, parent=parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Advanced Window for Super User Only !")
