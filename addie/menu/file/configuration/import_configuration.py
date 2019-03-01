from __future__ import (absolute_import, division, print_function)
import configparser
import os

from addie.menu.file.configuration.config_file_name_handler import ConfigFileNameHandler
from addie.utilities.conversion import str2bool
from addie.utilities.gui_handler import GuiHandler
from addie.autoNOM.step1_gui_handler import Step1GuiHandler
from addie.processing.idl.import_table import ImportTable
from addie.processing.idl.step2_gui_handler import Step2GuiHandler


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
        config = configparser.ConfigParser()
        config.read(self.filename)
        self.config = config

    def repopulate_gui(self):

        o_gui = GuiHandler(parent=self.parent)

        # step1

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
        o_gui.dropdown_set_index(widget_id=self.parent.ui.frequency, index=frequency_index)

        recalibration = self.get_tag("recalibration", data_type="bool")
        if recalibration:
            o_gui.radiobutton_set_state(widget_id=self.parent.ui.recalibration_yes, state=True)
        else:
            o_gui.radiobutton_set_state(widget_id=self.parent.ui.recalibration_no, state=True)

        renormalization = self.get_tag("renormalization", data_type="bool")
        if renormalization:
            o_gui.radiobutton_set_state(widget_id=self.parent.ui.renormalization_yes, state=True)
        else:
            o_gui.radiobutton_set_state(widget_id=self.parent.ui.renormalization_no, state=True)

        autotemplate = self.get_tag("autotemplate", data_type="bool")
        if autotemplate:
            o_gui.radiobutton_set_state(widget_id=self.parent.ui.autotemplate_yes, state=True)
        else:
            o_gui.radiobutton_set_state(widget_id=self.parent.ui.autotemplate_no, state=True)

        postprocessing = self.get_tag("postprocessing", data_type="bool")
        if postprocessing:
            o_gui.radiobutton_set_state(widget_id=self.parent.ui.postprocessing_yes, state=True)
        else:
            o_gui.radiobutton_set_state(widget_id=self.parent.ui.postprocessing_no, state=True)

        comments = self.get_tag("comments")
        self.parent.ui.comments.setText(comments)

        create_new_autonom_folder = self.get_tag("create_new_autonom_folder", data_type='bool')
        o_gui.radiobutton_set_state(widget_id=self.parent.ui.create_folder_button, state=create_new_autonom_folder)
        o_step1_handler = Step1GuiHandler(parent=self.parent)
        o_step1_handler.new_autonom_group_box(status=create_new_autonom_folder)

        auto_autonom_folder = self.get_tag("auto_autonom_folder", data_type="bool")
        if auto_autonom_folder:
            o_gui.radiobutton_set_state(widget_id=self.parent.ui.auto_manual_folder, state=True)
        else:
            o_gui.radiobutton_set_state(widget_id=self.parent.ui.manual_output_folder, state=True)

        o_step1_handler.manual_output_folder_button_handler()

        manual_autonom_folder_name = self.get_tag("manual_autonom_folder_name")
        self.parent.ui.manual_output_folder_field.setText(manual_autonom_folder_name)

        # step2

        table = self.get_tag("table")
        o_import_table = ImportTable(parent=self.parent)
        o_import_table.table_contain = table
        o_import_table.parse_config_table()
        o_import_table.populate_gui()

        o_gui_step2 = Step2GuiHandler(parent=self.parent)

        background_flag = self.get_tag("background_flag", data_type='bool')
        if background_flag:
            o_gui.radiobutton_set_state(widget_id=self.parent.ui.background_yes, state=True)
        else:
            o_gui.radiobutton_set_state(widget_id=self.parent.ui.background_no, state=True)
        o_gui_step2.step2_background_flag()

        background_no_field = self.get_tag("background_no_field")
        self.parent.ui.background_no_field.setText(background_no_field)

        background_index = self.get_tag("background_index", data_type='int')
        self.parent.ui.background_comboBox.setCurrentIndex(background_index)

        # PDF

        fourier_filter_min = self.get_tag("ndabs_fourier_filter_min")
        self.parent.ui.fourier_filter_from.setText(fourier_filter_min)

        fourier_filter_max = self.get_tag("ndabs_fourier_filter_max")
        self.parent.ui.fourier_filter_to.setText(fourier_filter_max)

        q_min = self.get_tag("q_min")
        self.parent.ui.q_range_min.setText(q_min)

        q_max = self.get_tag("q_max")
        self.parent.ui.q_range_max.setText(q_max)

        plazcek_fit_range_min = self.get_tag("plazcek_fit_range_min")
        self.parent.ui.plazcek_fit_range_min.setText(plazcek_fit_range_min)

        plazcek_fit_range_max = self.get_tag("plazcek_fit_range_max")
        self.parent.ui.plazcek_fit_range_max.setText(plazcek_fit_range_max)

        hydrogen_flag = self.get_tag("hydrogen_flag", data_type="bool")
        if hydrogen_flag:
            o_gui.radiobutton_set_state(widget_id=self.parent.ui.hydrogen_yes, state=True)
        else:
            o_gui.radiobutton_set_state(widget_id=self.parent.ui.hydrogen_no, state=True)

        muscat_flag = self.get_tag("muscat_flag", data_type="bool")
        if muscat_flag:
            o_gui.radiobutton_set_state(widget_id=self.parent.ui.muscat_yes, state=True)
        else:
            o_gui.radiobutton_set_state(widget_id=self.parent.ui.muscat_no, state=True)

        scale_data_flag = self.get_tag("scale_data_flag", data_type="bool")
        if scale_data_flag:
            o_gui.radiobutton_set_state(widget_id=self.parent.ui.scale_data_yes, state=True)
        else:
            o_gui.radiobutton_set_state(widget_id=self.parent.ui.scale_data_no, state=True)

        #run_rmc_flag = self.get_tag("run_rmc_flag", data_type = "bool")
        #o_gui.radiobutton_set_state(widget_id = self.parent.ui.run_rmc_yes, state = run_rmc_flag)

        output_file_name = self.get_tag("ndabs_output_file_name")
        self.parent.ui.run_ndabs_output_file_name.setText(output_file_name)

        pdf_qmax_line_edit = self.get_tag("pdf_qmax_line_edit")
        self.parent.ui.pdf_qmax_line_edit.setText(pdf_qmax_line_edit)

        try:
            pdf_sum_scans_output_file_name = self.get_tag("pdf_sum_scans_output_file_name")
            self.parent.ui.sum_scans_output_file_name.setText(pdf_sum_scans_output_file_name)
        except ValueError:
            pass

        try:
            pdf_sum_scans_rmax = self.get_tag("psd_sum_scans_rmax")
            self.parent.ui.sum_scans_rmax.setText(pdf_sum_scans_rmax)
        except ValueError:
            pass

        interactive_mode_flag = self.get_tag("interactive_mode_flag", data_type="bool")
        o_gui.radiobutton_set_state(widget_id=self.parent.ui.interactive_mode_checkbox, state=interactive_mode_flag)

        mantid_calibration_value = self.get_tag("mantid_calibration_value")
        self.parent.ui.mantid_calibration_value.setText(mantid_calibration_value)

        mantid_characterization = self.get_tag("mantid_characterization_value")
        self.parent.ui.mantid_characterization_value.setText(mantid_characterization)

        number_of_bins = self.get_tag("mantid_number_of_bins")
        self.parent.ui.mantid_number_of_bins.setText(number_of_bins)

        min_crop = self.get_tag("mantid_min_crop_wavelength")
        self.parent.ui.mantid_min_crop_wavelength.setText(min_crop)

        max_crop = self.get_tag("mantid_max_crop_wavelength")
        self.parent.ui.mantid_max_crop_wavelength.setText(max_crop)

        vanadium_radius = self.get_tag("mantid_vanadium_radius")
        self.parent.ui.mantid_vanadium_radius.setText(vanadium_radius)

        output_directory = self.get_tag("mantid_output_directory_value")
        self.parent.ui.mantid_output_directory_value.setText(output_directory)

        o_gui_step2.check_gui()

    def get_tag(self, tag_name, data_type='string'):
        config = self.config
        _section_name = self.section_name
        try:
            value = config.get(_section_name, tag_name)
        except:
            raise ValueError("Tag missing !")
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
        o_config_file = ConfigFileNameHandler(parent=self.parent)
        o_config_file.request_config_file_name()
        self.filename = o_config_file.filename
