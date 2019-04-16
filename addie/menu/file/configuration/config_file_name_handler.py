from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import (QFileDialog)
import os

from addie.utilities.file_handler import FileHandler
from addie.widgets.filedialog import get_save_file


class ConfigFileNameHandler(object):

    filename = ''

    def __init__(self, parent=None):
        self.parent = parent

    def request_config_file_name(self, open_flag=True):
        _caption = 'Select or Define a Configuration File Name'
        _current_folder = self.parent.configuration_folder
        if open_flag:
            _file = QFileDialog.getOpenFileName(parent=self.parent,
                                                filter='config (*.cfg)',
                                                caption=_caption,
                                                directory=_current_folder)
            if isinstance(_file, tuple):
                _file = _file[0]
        else:
            _file, _ = get_save_file(parent=self.parent,
                                     filter={'config (*.cfg)':'cfg'},
                                     caption=_caption,
                                     directory=_current_folder)

        if not _file:
            self.filename = ''
            return

        _new_path = os.path.dirname(_file)
        self.parent.configuration_folder = _new_path
        o_file_handler = FileHandler(filename=_file)
        o_file_handler.check_file_extension(ext_requested='cfg')
        self.filename = o_file_handler.filename
