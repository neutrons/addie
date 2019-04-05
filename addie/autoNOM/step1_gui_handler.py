from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import (QFileDialog)
import os

from addie.autoNOM.auto_populate_widgets import AutoPopulateWidgets
from addie.help_handler.help_gui import check_status


class Step1GuiHandler(object):

    def __init__(self, main_window=None):
        self.main_window = main_window
        #self.main_window = parent

    def new_autonom_group_box(self, status=True):
        self.main_window.autonom_ui.name_of_output_folder.setEnabled(status)

    def set_main_window_title(self):
        self.main_window.setWindowTitle("working folder: " + self.main_window.current_folder)

    def check_go_button(self):
        if self.all_mandatory_fields_non_empty():
            self.main_window.autonom_ui.run_autonom_script.setEnabled(True)
            self.main_window.autonom_ui.create_exp_ini_button.setEnabled(True)
        else:
            self.main_window.autonom_ui.run_autonom_script.setEnabled(False)
            self.main_window.autonom_ui.create_exp_ini_button.setEnabled(False)
        check_status(parent=self.main_window, button_name='autonom')

    def all_mandatory_fields_non_empty(self):
        _diamond_field = str(self.main_window.autonom_ui.diamond.text()).strip().replace(" ", "")
        if _diamond_field == "":
            return False

        _diamond_background_field = str(self.main_window.autonom_ui.diamond_background.text()).strip().replace(" ", "")
        if _diamond_background_field == "":
            return False

        _vanadium_field = str(self.main_window.autonom_ui.vanadium.text()).strip().replace(" ", "")
        if _vanadium_field == "":
            return False

        _vanadium_background_field = str(self.main_window.autonom_ui.vanadium_background.text()).strip().replace(" ", "")
        if _vanadium_background_field == "":
            return False

        _sample_background_field = str(self.main_window.autonom_ui.sample_background.text()).strip().replace(" ", "")
        if _sample_background_field == "":
            return False

        if self.main_window.autonom_ui.create_folder_button.isChecked():
            if self.main_window.autonom_ui.manual_output_folder.isChecked() \
               and (str(self.main_window.autonom_ui.manual_output_folder_field.text()).strip() == ""):
                return False

        return True

    def manual_output_folder_button_handler(self):
        if self.main_window.autonom_ui.manual_output_folder.isChecked():
            status = True
        else:
            status = False
        self.main_window.autonom_ui.manual_output_folder_field.setEnabled(status)
        self.main_window.autonom_ui.manual_output_folder_button.setEnabled(status)

    def select_working_folder(self):
        _current_folder = self.main_window.current_folder
        _new_folder = QFileDialog.getExistingDirectory(parent=self.main_window,
                                                       caption="Select working directory",
                                                       directory=_current_folder)
        if not _new_folder:
            return
        if isinstance(_new_folder, tuple):
            _new_folder = _new_folder[0]
        self.main_window.current_folder = _new_folder
        # o_gui = Step1GuiHandler(parent=self.main_window)
        # o_gui.set_main_window_title()
        self.set_main_window_title()

        # move to new folder specifiy
        os.chdir(_new_folder)

        o_auto_populate = AutoPopulateWidgets(main_window=self.main_window)
        o_auto_populate.run()

    def select_manual_output_folder(self):
        # _current_folder = self.main_window.current_folder
        dlg = QFileDialog(parent=self.main_window,
                          caption="Select or Define Output Directory")
        dlg.setFileMode(QFileDialog.Directory)
        if dlg.exec_():
            output_folder_name = str(dlg.selectedFiles()[0])
            self.main_window.autonom_ui.manual_output_folder_field.setText(output_folder_name)
