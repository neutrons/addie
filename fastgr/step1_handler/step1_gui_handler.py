from PyQt4 import QtGui
from  step1_handler.auto_populate_widgets import AutoPopulateWidgets


class Step1GuiHandler(object):
    
    def __init__(self, parent=None):
        self.parent = parent.ui
        self.parent_no_ui = parent
        
    def set_main_window_title(self):
        self.parent_no_ui.setWindowTitle(self.parent_no_ui.current_folder)
        
    def check_go_button(self):
        if self.all_mandatory_fields_non_empty():
            self.parent.run_autonom_script.setEnabled(True)
        else:
            self.parent.run_autonom_script.setEnabled(False)

    def all_mandatory_fields_non_empty(self):
        _diamond_field = str(self.parent.diamond.text()).strip().replace(" ", "")
        if _diamond_field == "":
            return False
        
        _diamond_background_field = str(self.parent.diamond_background.text()).strip().replace(" ", "")
        if _diamond_background_field == "":
            return False

        _vanadium_field = str(self.parent.vanadium.text()).strip().replace(" ", "")
        if _vanadium_field == "":
            return False

        _vanadium_background_field = str(self.parent.vanadium_background.text()).strip().replace(" ", "")
        if _vanadium_background_field == "":
            return False

        _sample_background_field = str(self.parent.sample_background.text()).strip().replace(" ", "")
        if _sample_background_field == "":
            return False
        
        if self.parent.manual_output_folder.isChecked() and (str(self.parent.manual_output_folder_field.text()).strip() == ""):
            return False
        
        return True
    
    def manual_output_folder_button_handler(self):
        if self.parent.manual_output_folder.isChecked():
            status = True
        else:
            status = False
        self.parent.manual_output_folder_field.setEnabled(status)
        
    def select_working_folder(self):
        _current_folder = self.parent_no_ui.current_folder
        _new_folder = QtGui.QFileDialog.getExistingDirectory(parent = self.parent_no_ui,
                                                             caption = "Select working directory",
                                                             directory = _current_folder)
        
        if str(_new_folder):
            self.parent_no_ui.current_folder = _new_folder
            o_gui = Step1GuiHandler(parent = self.parent_no_ui)
            o_gui.set_main_window_title()

            o_auto_populate = AutoPopulateWidgets(parent = self.parent_no_ui)
            o_auto_populate.run()
        
        
        