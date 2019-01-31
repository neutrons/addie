from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import (QFileDialog, QMainWindow)
from addie.utilities import load_ui
from addie.step2_handler.mantid_script_handler import MantidScriptHandler
from addie.utilities.file_handler import FileHandler


class MantidReductionView(QMainWindow):

    def __init__(self, parent=None, father=None):
        self. parent = parent
        self.father = father

        QMainWindow.__init__(self, parent=parent)
        self.ui = load_ui(__file__, '../../../designer/ui_previewMantid.ui', baseinstance=self)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

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
        _python_file = QFileDialog.getSaveFileName(parent=self.parent,
                                                   caption="Output File Name",
                                                   directory=_current_folder,
                                                   filter=("python (*.py);; All Files (*.*)"))
        if not _python_file:
            return

        if isinstance(_python_file, tuple):
            _python_file = _python_file[0]
        _script = str(self.ui.preview_mantid_script_textedit.toPlainText())
        o_file_handler = FileHandler(filename=_python_file)
        o_file_handler.create_ascii(contain=_script, carriage_return=False)
