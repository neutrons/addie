import ConfigParser
import os

from fastgr.configuration.config_file_name_handler import ConfigFileNameHandler
from fastgr.utilities.conversion import str2bool
from fastgr.utilities.gui_handler import GuiHandler
from fastgr.step1_handler.step1_gui_handler import Step1GuiHandler
from fastgr.step2_handler.import_table import ImportTable


class ImportConfiguration(object):
    
    config = None
    section_name = ''
    
    def __init__(self, parent=None):
        self.parent = parent
        self.section_name = parent.config_section_name
        
    def run(self):
        self.request_config_file_name()
        if self.filename:
            self.retrieve_settings()
            self.repopulate_gui()
        
    def retrieve_settings(self):
        config = ConfigParser.ConfigParser()
        config.read(self.filename)
        self.config = config
        
    def repopulate_gui(self):
        
        o_gui = GuiHandler(parent = self.parent)

        ## autoNOM
        # working folder
        current_folder = self.get_tag("current_folder")
        self.parent.current_folder = current_folder
        os.chdir(current_folder)
        
        diamond = self.get_tag("diamond")
        self.parent.ui.diamond.setText(diamond)
        
        diamond_background = self.get_tag("diamond_background")
        self.parent.ui.diamond_background.setText(diamond_background)
        
        vanadium = self.get_tag("vanadium")
        self.parent.ui.vanadium.setText(vanadium)
        
        vanadium_background = self.get_tag("vanadium_background")
        self.parent.ui.vanadium_background.setText(vanadium_background)
        
        sample_background = self.get_tag("sample_background")
        self.parent.ui.sample_background.setText(sample_background)
        
        first_scan = self.get_tag("first_scan")
        self.parent.ui.first_scan.setText(first_scan)
        
        last_scan = self.get_tag("last_scan")
        self.parent.ui.last_scan.setText(last_scan)
        
        frequency_index = self.get_tag("frequency_index", data_type='int')
        o_gui.dropdown_set_index(widget_id = self.parent.ui.frequency, index=frequency_index)

        recalibration = self.get_tag("recalibration", data_type="bool")
        o_gui.radiobutton_set_state(widget_id= self.parent.ui.recalibration_yes, state = recalibration)

        renormalization = self.get_tag("renormalization", data_type="bool")
        o_gui.radiobutton_set_state(widget_id = self.parent.ui.renormalization_yes, state = renormalization)
        
        autotemplate = self.get_tag("autotemplate", data_type = "bool")
        o_gui.radiobutton_set_state(widget_id = self.parent.ui.autotemplate_yes, state = autotemplate)
        
        postprocessing = self.get_tag("postprocessing", data_type = "bool")
        o_gui.radiobutton_set_state(widget_id = self.parent.ui.postprocessing_yes, state = postprocessing)
        
        comments = self.get_tag("comments")
        self.parent.ui.comments.setText(comments)
        
        create_new_autonom_folder = self.get_tag("create_new_autonom_folder", data_type = 'bool')
        o_gui.radiobutton_set_state(widget_id = self.parent.ui.create_folder_button, state = create_new_autonom_folder)
        o_step1_handler = Step1GuiHandler(parent = self.parent)
        o_step1_handler.new_autonom_group_box(status=create_new_autonom_folder)
        
        auto_autonom_folder = self.get_tag("auto_autonom_folder", data_type="bool")
        o_gui.radiobutton_set_state(widget_id = self.parent.ui.auto_manual_folder, state = auto_autonom_folder)
        o_step1_handler.manual_output_folder_button_handler()
        
        manual_autonom_folder_name = self.get_tag("manual_autonom_folder_name")
        self.parent.ui.manual_output_folder_field.setText(manual_autonom_folder_name)
        
        table = self.get_tag("table")
        o_import_table = ImportTable(parent = self.parent)
        o_import_table.table_contain = table
        o_import_table.parse_config_table()
        o_import_table.populate_gui()
        
        
    def get_tag(self, tag_name, data_type='string'):
        config = self.config
        _section_name = self.section_name
        value = config.get(_section_name, tag_name)
        if data_type == 'string':
            return value
        if data_type == 'bool':
            return str2bool(value)
        if data_type == 'int':
            return int(value)
        if data_type == 'float':
            return float(value)
        else:
            raise ValueError("data_type not supported!")
                
    def request_config_file_name(self):
        o_config_file = ConfigFileNameHandler(parent = self.parent)
        o_config_file.request_config_file_name()
        self.filename = o_config_file.filename
