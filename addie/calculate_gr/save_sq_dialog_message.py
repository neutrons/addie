from qtpy.QtWidgets import QDialog
from qtpy import QtGui

from addie.utilities import load_ui


class SaveSqDialogMessageDialog(QDialog):

    def __init__(self, main_window=None):
        self.main_window = main_window
        QDialog.__init__(self, parent=main_window)
        self.ui = load_ui('save_sq_information_dialog.ui', baseinstance=self)

        self.init_widgets()

    def init_widgets(self):
        self.ui.message_label.setPixmap(QtGui.QPixmap(":/preview/save_sq_selection_image.png"))
