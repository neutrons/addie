from __future__ import (absolute_import)
from qtpy.QtWidgets import (QMainWindow)
from addie.utilities import load_ui
from addie.advanced.isrp_gui_table_init import IsRepGuiTableInitialization


class IsoRepGui(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.parent = parent

        self.ui = load_ui('isoRepGui.ui', baseinstance=self)

        self.init_IsRepTable()

    def init_IsRepTable(self):
        self.o_table = IsRepGuiTableInitialization(parent=self)
        self.o_table.iso_rep_linker()

    def refresh(self):
        self.o_table.clear()

    def closeEvent(self, event=None):
        self.parent.isrp_win = None

    def hide_button_clicked(self):
        self.closeEvent(event=None)
        self.close()


def isrp_button_activator(parent=None):
    if parent.isrp_win is None:
        isotope_rep = IsoRepGui(parent=parent)
        isotope_rep.show()
        parent.isrp_win = isotope_rep
    else:
        parent.isrp_win.refresh()
        parent.isrp_win.activateWindow()
