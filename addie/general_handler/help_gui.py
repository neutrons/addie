from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import (QMainWindow)
from addie.utilities import load_ui
from addie.general_handler.help_gui_table_initialization import HelpGuiTableInitialization


class HelpGui(QMainWindow):

    '''
    button_name = ['autonom', 'ndabs', 'scans', 'mantid']
    '''
    column_widths = [330, 40]

    def __init__(self, parent=None, button_name=''):
        QMainWindow.__init__(self, parent)
        self.parent = parent
        self.button_name = button_name

        self.ui = load_ui(__file__, '../../designer/ui_helpGui.ui', baseinstance=self)

        self.init_global_gui()
        self.init_table()

    def init_table(self):
        self.o_table = HelpGuiTableInitialization(parent=self, button_name=self.button_name)
        self.o_table.fill()

    def init_global_gui(self):
        for index, col_width in enumerate(self.column_widths):
            self.ui.table_status.setColumnWidth(index, col_width)
        self.setWindowTitle("Button Status: {}".format(self.button_name))

    def refresh(self):
        self.o_table.refill()

    def closeEvent(self, event=None):
        if self.button_name == 'autonom':
            self.parent.o_help_autonom = None
        elif self.button_name == 'ndabs':
            self.parent.o_help_ndabs = None
        elif self.button_name == 'scans':
            self.parent.o_help_scans = None
        elif self.button_name == 'mantid':
            self.parent.o_help_mantid = None

    def hide_button_clicked(self):
        self.closeEvent(event=None)
        self.close()


def help_button_activator(parent=None, button_name='autonom'):
    #    pos = parent.mapToGlobal(parent.pos())
 #   width = parent.frameGeometry().width()
    if button_name == 'autonom':
        if parent.o_help_autonom is None:
            o_help = HelpGui(parent=parent, button_name=button_name)
            o_help.show()
            parent.o_help_autonom = o_help
        else:
            parent.o_help_autonom.refresh()
            parent.o_help_autonom.activateWindow()
    elif button_name == 'ndabs':
        if parent.o_help_ndabs is None:
            o_help = HelpGui(parent=parent, button_name=button_name)
            o_help.show()
            parent.o_help_ndabs = o_help
        else:
            parent.o_help_ndabs.refresh()
            parent.o_help_ndabs.activateWindow()
    elif button_name == 'scans':
        if parent.o_help_scans is None:
            o_help = HelpGui(parent=parent, button_name=button_name)
            o_help.show()
            parent.o_help_scans = o_help
        else:
            parent.o_help_scans.refresh()
            parent.o_help_scans.activateWindow()
    elif button_name == 'mantid':
        if parent.o_help_mantid is None:
            o_help = HelpGui(parent=parent, button_name=button_name)
            o_help.show()
            parent.o_help_mantid = o_help
        else:
            parent.o_help_mantid.refresh()
            parent.o_help_mantid.activateWindow()


def check_status(parent=None, button_name='autonom'):
    if (button_name == 'autonom') and parent.o_help_autonom:
        parent.o_help_autonom.refresh()
    if (button_name == 'ndabs') and parent.o_help_ndabs:
        parent.o_help_ndabs.refresh()
    if (button_name == 'scans') and parent.o_help_scans:
        parent.o_help_scans.refresh()
    if (button_name == 'mantid') and parent.o_help_mantid:
        parent.o_help_mantid.refresh()
