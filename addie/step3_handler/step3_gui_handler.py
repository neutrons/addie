from PyQt4 import QtGui, QtCore
import os

from addie.utilities.file_handler import FileHandler
from addie.step3_handler.preview_ascii_window import PreviewAsciiWindow


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
	    o_file_handler = FileHandler(filename = _ascii_file)
	    o_file_handler.retrieve_contain()
	    text_contain = o_file_handler.file_contain
	    
	    o_preview = PreviewAsciiWindow(parent = self.parent_no_ui, text = text_contain, filename=_ascii_file)
	    o_preview.show()
