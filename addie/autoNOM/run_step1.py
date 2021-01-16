from __future__ import (absolute_import, division, print_function)
import os
from qtpy.QtWidgets import (QMessageBox)
import glob

from addie.autoNOM.make_exp_ini_file_and_run_autonom import MakeExpIniFileAndRunAutonom


class RunStep1(object):

    keep_running_status = True
    folder = None
    auto_folder_base_name = 'autoNOM'

    def __init__(self, parent=None, run_autonom=True):
        # self.parent = parent.ui
        self.parent = parent.autonom_ui
        self.parent_no_ui = parent
        self.run_autonom = run_autonom

    def create_folder(self):
        self._current_path = os.getcwd()

        if not self.parent.create_folder_button.isChecked():
            self.folder = self._current_path
            return

        if self.parent.manual_output_folder.isChecked():
            self.create_manual_folder()
        else:
            self.create_auto_folder()

    def create_exp_ini_file(self):
        if self.keep_running_status is False:
            return

        _make_exp = MakeExpIniFileAndRunAutonom(parent=self.parent_no_ui, folder=self.folder)
        _make_exp.create()
        if self.run_autonom:
            _make_exp.run_autonom()

    def create_manual_folder(self):
        _folder_name = str(self.parent.manual_output_folder_field.text()).strip()
        _current_path = self._current_path
        _full_path = os.path.join(_current_path, _folder_name)
        self.folder = _full_path

        if os.path.exists(_full_path):
            message_box = QMessageBox()
            message_box.setText("Folder Exists Already!")
            message_box.setInformativeText("Do you want to replace it?")
            message_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            result = message_box.exec_()
            if result == QMessageBox.Yes:
                self._remove_folder(_full_path)
                self._make_folder(_full_path)
            else:
                self.keep_running_status = False
        else:
            self._make_folder(_full_path)

    def create_auto_folder(self):
        list_folder = [_folder for _folder in glob.glob(self.auto_folder_base_name + '*') if os.path.isdir(_folder)]
        if list_folder == []:
            _folder_name = self.auto_folder_base_name + '_00'
        else:
            _last_index = self.retrieve_last_incremented_index(list_folder)
            _new_index = "%.2d" % (int(_last_index)+1)
            _folder_name = self.auto_folder_base_name + '_' + _new_index

        _full_path = os.path.join(self._current_path, _folder_name)
        self.folder = _full_path

        self._make_folder(_full_path)
        if self.run_autonom:
            self.parent_no_ui.ui.statusbar.showMessage("Created folder: " + _full_path + " and running autoNOM script !")
        else:
            self.parent_no_ui.ui.statusbar.showMessage("Created folder: " + _full_path)

    def retrieve_last_incremented_index(self, list_folder):
        _list_index = []
        for _folder in list_folder:
            _folder_split = _folder.split('_')
            if len(_folder_split) > 1:
                try:
                    # checking that the variable is an integer
                    _list_index.append(int(_folder_split[1]))
                except:
                    pass

        if _list_index == []:
            return -1

        _list_index.sort()
        return(_list_index[-1])

    def _remove_folder(self, folder_name):
        os.rmdir(folder_name)

    def _make_folder(self, folder_name):
        os.mkdir(folder_name)
