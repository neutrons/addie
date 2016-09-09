from PyQt4 import QtGui, QtCore
import os


class BrowseFileFolderHandler(object):
    
    _output_ext = '/rietveld'
    
    def __init__(self, parent = None):
        self.parent = parent
        self.current_folder = parent.file_path
        
    def browse_file(self, type='calibration'):
        _current_folder = self.current_folder
        
        if type == 'calibration':
            _filter = "calib (*.h5);;all (*.*)"
            _caption = "Select Calibration File"
            _output_ui = self.parent.ui.mantid_calibration_value
        else:
            _filter = "characterization (-ritveld.txt);;all (*.*)"
            _caption = "Select Characterization File"
            _output_ui = self.parent.ui.mantid_characterization_value

        _file = QtGui.QFileDialog.getOpenFileName(parent = self.parent,
                                                  filter = _filter,
                                                  caption = _caption,
                                                  directory = _current_folder)
        
        if _file:
            _output_ui.setText(str(_file))
            self.parent.file_path = os.path.dirname(str(_file))
            
    def browse_folder(self):
        _current_folder = self.current_folder
        _caption  = "Select Output Folder"
        
        _folder = QtGui.QFileDialog.getExistingDirectory(parent = self.parent,
                                                         caption = _caption,
                                                         directory = _current_folder)
        
        if _folder:
            self.parent.ui.mantid_output_directory_value.setText(str(_folder) + self._output_ext)
