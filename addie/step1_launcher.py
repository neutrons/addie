from __future__ import (absolute_import, division, print_function)
import numpy as np
import os
from qtpy.QtWidgets import (QApplication, QMainWindow, QStyleFactory)  # noqa
import sys

import addie.step1
from addie.initialization.init_step1 import InitStep1
from addie.step1_handler.gui_handler import GuiHandler
from addie.step1_handler.run_step1 import RunStep1


class MyApp(QMainWindow, step1.Ui_MainWindow):
    def __init__(self):
        QApplication.setStyle(QStyleFactory.create("Cleanlooks"))
        QMainWindow.__init__(self)
        self.setupUi(self)

        init_step1 = InitStep1(parent=self)

    def diamond_edited(self):
        self.check_step1_gui()

    def diamond_background_edited(self):
        self.check_step1_gui()

    def vanadium_edited(self):
        self.check_step1_gui()

    def vanadium_background_edited(self):
        self.check_step1_gui()

    def sample_background_edited(self):
        self.check_step1_gui()

    def output_folder_radio_buttons(self):
        o_gui_handler = GuiHandler(parent=self)
        o_gui_handler.manual_output_folder_button_handler()
        o_gui_handler.check_go_button()

    def manual_output_folder_field_edited(self):
        self.check_step1_gui()

    def check_step1_gui(self):
        '''check the status of the step1 GUI in order to enable or not the GO BUTTON at the bottom'''
        o_gui_handler = GuiHandler(parent=self)
        o_gui_handler.check_go_button()

    def run_autonom(self):
        """Will first create the output folder, then create the exp.ini file"""
        _run_autonom = RunStep1(parent=self)
        _run_autonom.create_folder()
        _run_autonom.create_exp_ini_file()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
