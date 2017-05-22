from PyQt4 import QtGui
import os

from addie.utilities.file_handler import FileHandler


class ConfigFileNameHandler(object):
    
    filename = ''
    
    def __init__(self, parent=None):
        self.parent = parent
        
    def request_config_file_name(self, open_flag = True):
        _filter = 'config (*.cfg)'
        _caption = 'Select or Define a Configuration File Name'
        _current_folder = self.parent.configuration_folder
        if open_flag:
            _file = QtGui.QFileDialog.getOpenFileName(parent = self.parent,
                                                      filter = _filter,
                                                      caption = _caption,
                                                      directory = _current_folder)
        else:
            _file = QtGui.QFileDialog.getSaveFileName(parent = self.parent,
                                                      filter = _filter,
                                                      caption = _caption,
                                                      directory = _current_folder)
        if _file:
            _new_path = os.path.dirname(_file)
            self.parent.configuration_folder = _new_path
            o_file_handler = FileHandler(filename = _file)
            o_file_handler.check_file_extension(ext_requested='cfg')
            self.filename = o_file_handler.filename
    