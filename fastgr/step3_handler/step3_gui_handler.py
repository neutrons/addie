from PyQt4 import QtGui, QtCore
import os

from fastgr.utilities.file_handler import FileHandler


class Step3GuiHandler(object):

    def __init__(self, parent=None):
        self.parent_no_ui = parent
        self.parent = parent.ui
        self.current_folder = parent.current_folder
        
    def browse_file(self):
        _current_folder = self.current_folder
        _ascii_file = QtGui.QFileDialog.getOpenFileName(parent = self.parent_no_ui,
                                                             caption = 'Select file to display',
                                                             directory = self.current_folder)
        
        if str(_ascii_file):
            self.parent.browse_ascii_name.setText(str(_ascii_file))
            o_file_handler = FileHandler(filename = _ascii_file)
            o_file_handler.retrieve_contain()
            text_contain = o_file_handler.file_contain
            self.parent.browse_ascii_text_edit.setText(text_contain)