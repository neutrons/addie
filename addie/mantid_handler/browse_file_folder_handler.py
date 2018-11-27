from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import (QFileDialog)
import os


class BrowseFileFolderHandler(object):

    _output_ext = '/rietveld'

    def __init__(self, parent=None):
        self.parent = parent
        self.current_folder = parent.file_path

    def browse_file(self, type='calibration'):

        if type == 'calibration':
            _current_folder = self.parent.calibration_folder
            _filter = "calib (*.h5);;all (*.*)"
            _caption = "Select Calibration File"
            _output_ui = self.parent.ui.mantid_calibration_value
        else:
            _current_folder = self.parent.characterization_folder
            _filter = "characterization (*-rietveld.txt);;all (*.*)"
            _caption = "Select Characterization File"
            _output_ui = self.parent.ui.mantid_characterization_value

        _file = QFileDialog.getOpenFileName(parent=self.parent,
                                            filter=_filter,
                                            caption=_caption,
                                            directory=_current_folder)
        if not _file:
            return
        if isinstance(_file, tuple):
            _file = _file[0]

        _output_ui.setText(str(_file))
        _path = os.path.dirname(str(_file))

        if type == 'calibration':
            self.parent.calibration_current_folder = _path
        else:
            self.parent.characterization_current_folder = _path

    def browse_folder(self):
        _current_folder = self.current_folder
        _caption = "Select Output Folder"

        _folder = QFileDialog.getExistingDirectory(parent=self.parent,
                                                   caption=_caption,
                                                   directory=_current_folder)
        if not _folder:
            return
        if isinstance(_folder, tuple):
            _folder = _folder[0]

        self.parent.ui.mantid_output_directory_value.setText(str(_folder) + self._output_ext)
