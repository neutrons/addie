from addie.ui_table_tree import Ui_Dialog as UiDialog

try:
    from PyQt4.QtGui import QDialog
except ImportError:
    try:
        from PyQt5.QtWidgets import QDialog
    except ImportError:
        raise ImportError("Requires PyQt4 or PyQt5")

class TableTreeHandler:

    def __init__(self, parent=None):
        self.parent = parent

    def run(self):
        pass


class TableTree(QDialog):

    def __init__(self, parent=None):
        pass
