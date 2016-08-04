import numpy as np
import os
from PyQt4 import QtCore, QtGui
import sys

import fastgr.step2
from fastgr.initialization.init_step2 import InitStep2
from fastgr.step2_handler.populate_master_table import PopulateMasterTable
from fastgr.step2_handler.populate_background_widgets import PopulateBackgroundWidgets
from fastgr.step2_handler.gui_handler import GuiHandler
from fastgr.step2_handler.table_handler import TableHandler
from fastgr.step2_handler.create_sample_files import CreateSampleFiles
from fastgr.step2_handler.create_ndsum_file import CreateNdsumFile


class MyApp(QtGui.QMainWindow, step2.Ui_MainWindow):
   
    debugging = True
   
    def __init__(self):
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
   
        init_step2 = InitStep2(parent = self)
   
    def populate_table_clicked(self):
        
        if self.debugging:
            self.current_folder = os.getcwd()  + '/autoNOM_00/'
        else:
            self.current_folder = os.getcwd()

        _pop_table = PopulateMasterTable(parent = self)
        _pop_table.run()
        
        _pop_back_wdg = PopulateBackgroundWidgets(parent = self)
        _pop_back_wdg.run()
        
        _o_gui = GuiHandler(parent = self)
        _o_gui.check_gui()
            
    def hidrogen_clicked(self):
        o_gui = GuiHandler(parent = self)
        o_gui.hidrogen_clicked()
    
    def no_hidrogen_clicked(self):
        o_gui = GuiHandler(parent = self)
        o_gui.no_hidrogen_clicked()
    
    def yes_background_clicked(self):
        o_gui = GuiHandler(parent = self)
        o_gui.yes_background_clicked()
    
    def no_background_clicked(self):
        o_gui = GuiHandler(parent = self)
        o_gui.no_background_clicked()
        
    def background_combobox_changed(self, index):
        o_gui = GuiHandler(parent = self)
        o_gui.background_index_changed(row_index = index)

    def create_sample_properties_files_clicked(self):
        o_create_sample_files = CreateSampleFiles(parent = self)
        o_create_sample_files.run()
        
    def run_ndabs_clicked(self):
        o_create_ndsum_file = CreateNdsumFile(parent = self)
        o_create_ndsum_file.run()
        
    def check_fourier_filter_widgets(self):
        o_gui = GuiHandler(parent = self)
        o_gui.check_gui()

    def check_plazcek_widgets(self):
        o_gui = GuiHandler(parent = self)
        o_gui.check_gui()
        
    def table_right_click(self, position):
        _o_table = TableHandler(parent = self)
        _o_table.right_click(position = position)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
