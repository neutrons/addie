from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import QMainWindow
from addie.utilities import load_ui


class AdvancedWindow(QMainWindow):

    def __init__(self, parent=None):
        self.parent = parent

        QMainWindow.__init__(self, parent=parent)
        self.ui = load_ui(__file__, '../../../designer/ui_advanced_window.ui', baseinstance=self)
        self.ui.setupUi(self)

        self.setWindowTitle("Advanced Window for Super User Only !")
