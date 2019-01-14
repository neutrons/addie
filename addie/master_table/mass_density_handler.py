try:
    from PyQt4.QtGui import QDialog
except:
    try:
        from PyQt5.QtWidgets import QDialog
    except:
        raise ImportError("Requires PyQt4 or PyQt5")

from addie.ui_mass_density import Ui_Dialog as UiDialog


class MassDensityHandler:

    def __init__(self, parent=None, key=None, data_type='sample'):
        if parent.mass_density_ui is None:
            o_mass = MassDensityWindow(parent=parent, key=key, data_type=data_type)
            o_mass.show()
            parent.mass_density_ui = o_mass
        else:
            parent.mass_density_ui.setFocus()
            parent.mass_density_ui.activateWindow()


class MassDensityWindow(QDialog):

    def __init__(self, parent=None, key=None, data_type='sample'):
        self.parent = parent
        self.key = key
        self.data_type = data_type

        QDialog.__init__(self, parent=parent)
        self.ui = UiDialog()
        self.ui.setupUi(self)

    def accept(self):
        self.parent.mass_density_ui = None
        self.close()

    def reject(self):
        self.parent.mass_density_ui = None
        self.close()

    def closeEvent(self, c):
        pass

