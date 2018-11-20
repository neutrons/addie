from qtpy.QtWidgets import (QMainWindow)

from addie.ui_preview_ascii import Ui_MainWindow as UiMainWindow


class PreviewAsciiWindow(QMainWindow):

    def __init__(self, parent = None, text=None, filename=None):
        self.parent = parent

        QMainWindow.__init__(self, parent = parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

        _title = filename
        self.setWindowTitle(_title)

        self.ui.preview_ascii_text_edit.setText(text)
