from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import (QMainWindow)
from addie.utilities import load_ui


class PreviewAsciiWindow(QMainWindow):

    def __init__(self, parent=None, text=None, filename=None):
        self.parent = parent

        QMainWindow.__init__(self, parent=parent)
        self.ui = load_ui(__file__, '../../designer/ui_preview_ascii.ui', baseinstance=self)

        _title = filename
        self.setWindowTitle(_title)

        self.ui.preview_ascii_text_edit.setText(text)
