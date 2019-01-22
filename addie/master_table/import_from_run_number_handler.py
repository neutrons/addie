try:
    from PyQt4.QtGui import QDialog
except:
    try:
        from PyQt5.QtWidgets import QDialog
    except:
        raise ImportError("Requires PyQt4 or PyQt5")

from addie.master_table.oncat_authentication_handler import OncatAuthenticationHandler

from addie.ui_import_from_run_number import Ui_Dialog as UiDialog


class ImportFromRunNumbereHandler:

    def __init__(self, parent=None):
        if parent.import_from_run_number_ui is None:
            o_import = ImportFromRunNumbereWindow(parent=parent)
            o_import.show()
            parent.import_from_run_number_ui = o_import
            if parent.import_from_run_number_ui_position:
                parent.import_from_run_number_ui.move(parent.import_from_run_number_ui_position)
        else:
            parent.import_from_run_number_ui.setFocus()
            parent.import_from_run_number_ui.activateWindow()


class ImportFromRunNumberWindow(QDialog):

    def __init__(self, parent=None):
        self.parent = parent

        QDialog.__init__(self, parent=parent)
        self.ui = UiDialog()
        self.ui.setupUi(self)

        self.init_widgets()

    def init_widgets(self):
        pass

    def change_user_clicked(self):
        OncatAuthenticationHandler(parent=self.parent)

    def run_number_return_pressed(self):
        pass

    def import_button_clicked(self):
        pass

    def cancel_button_clicked(self):
        self.close()

    def closeEvent(self, c):
        self.parent.import_from_run_number_ui = None
        self.parent.import_from_run_number_ui_position = self.pos()