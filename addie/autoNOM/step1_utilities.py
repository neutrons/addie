from __future__ import (absolute_import, division, print_function)


class Step1Utilities(object):

    def __init__(self, main_window=None):
        self.main_window = main_window

    def is_diamond_text_empty(self):
        _diamond_field = str(self.main_window.autonom_ui.diamond.text()).strip().replace(" ", "")
        if _diamond_field == "":
            return True
        else:
            return False

    def is_diamond_background_text_empty(self):
        _diamond_background_field = str(self.main_window.autonom_ui.diamond_background.text()).strip().replace(" ", "")
        if _diamond_background_field == "":
            return True
        else:
            return False

    def is_vanadium_text_empty(self):
        _vanadium_field = str(self.main_window.autonom_ui.vanadium.text()).strip().replace(" ", "")
        if _vanadium_field == "":
            return True
        else:
            return False

    def is_vanadium_background_text_empty(self):
        _vanadium_background_field = str(self.main_window.autonom_ui.vanadium_background.text()).strip().replace(" ", "")
        if _vanadium_background_field == "":
            return True
        else:
            return False

    def is_sample_background_text_empty(self):
        _sample_background_field = str(self.main_window.autonom_ui.sample_background.text()).strip().replace(" ", "")
        if _sample_background_field == "":
            return True
        else:
            return False

    def is_create_folder_button_status_ok(self):
        if self.main_window.autonom_ui.create_folder_button.isChecked():
            if self.main_window.autonom_ui.manual_output_folder.isChecked() \
               and (str(self.main_window.autonom_ui.manual_output_folder_field.text()).strip() == ""):
                return False
            else:
                return True
        else:
            return True
