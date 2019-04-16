from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import QMainWindow
from addie.utilities import load_ui
from addie.processing.idl.mantid_script_handler import MantidScriptHandler
from addie.utilities.file_handler import FileHandler
from addie.widgets.filedialog import get_save_file


class MantidReductionView(QMainWindow):

    def __init__(self, parent=None, father=None):
        self. parent = parent
        self.father = father

        QMainWindow.__init__(self, parent=parent)
        self.ui = load_ui('previewMantid.ui', baseinstance=self)

        self.populate_view()

    def populate_view(self):
        _parameters = self.father.parameters

        _script = ''
        runs = _parameters['runs']
        for _run in runs:
            o_mantid_script = MantidScriptHandler(parameters=_parameters, run=_run)
            _script += o_mantid_script.script
            _script += "\n\n"

        _script = "from mantid.simpleapi import *\nimport mantid\n\n" + _script

        self.ui.preview_mantid_script_textedit.setText(_script)

    def save_as_clicked(self):
        _current_folder = self.parent.current_folder
        _python_file, _ = get_save_file(parent=self.parent,
                                        caption='Output File Name',
                                        directory=_current_folder,
                                        filter={'python (*.py)':'py',
                                                'All Files (*.*)':''})
        if not _python_file:
            return

        _script = str(self.ui.preview_mantid_script_textedit.toPlainText())
        o_file_handler = FileHandler(filename=_python_file)
        o_file_handler.create_ascii(contain=_script, carriage_return=False)
