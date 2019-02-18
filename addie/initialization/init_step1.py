from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import (QLabel)
from addie.autoNOM.step1_gui_handler import Step1GuiHandler


class InitStep1(object):

    def __init__(self, parent=None):
        self.parent = parent

        self.parent.ui.diamond.setFocus(True)
        self.set_statusBar()
        self.set_title()

    def set_title(self):
        o_gui = Step1GuiHandler(parent=self.parent)
        o_gui.set_main_window_title()

    def set_statusBar(self):
        status_bar_label = QLabel()
        self.parent.ui.statusbar.addPermanentWidget(status_bar_label)
