from __future__ import (absolute_import, division, print_function)

from addie.utilities.gui_handler import GuiHandler
from addie.processing.idl.export_table import ExportTable
from addie.menu.file.configuration.config_file_name_handler import ConfigFileNameHandler
from addie.utilities.file_handler import FileHandler


class ExportConfiguration(object):

    filename = ''

    def __init__(self, parent=None):
        self.parent = parent

    def run(self):
        self.request_config_file_name()
        if self.filename:
            self.collect_settings()
            self.save_settings()

    def collect_settings(self):

        configuration = {}
        o_gui_handler = GuiHandler(parent=self.parent)

        # autoNOM
        # working folder
        current_folder = self.parent.current_folder
        configuration['current_folder'] = current_folder

        # diamond
        diamond = self.parent.ui.diamond.text()
        configuration['diamond'] = diamond

        # diamond background
        diamond_background = self.parent.ui.diamond_background.text()
        configuration['diamond_background'] = diamond_background

        # vanadium
        vanadium = self.parent.ui.vanadium.text()
        configuration['vanadium'] = vanadium

        # vanadium background
        vanadium_background = self.parent.ui.vanadium_background.text()
        configuration['vanadium_background'] = vanadium_background

        # sample background
        sample_background = self.parent.ui.sample_background.text()
        configuration['sample_background'] = sample_background

        # first scan to be analyzed
        first_scan = self.parent.ui.first_scan.text()
        configuration['first_scan'] = first_scan

        # last scan to be analyzed
        last_scan = self.parent.ui.last_scan.text()
        configuration['last_scan'] = last_scan

        # frequency (dropdown)
        frequency = o_gui_handler.dropdown_get_value(widget_id=self.parent.ui.frequency)
        configuration['frequency'] = frequency
        index = o_gui_handler.dropdown_get_index(widget_id=self.parent.ui.frequency)
        configuration['frequency_index'] = index

        # recalibration (flag)
        recalibration = o_gui_handler.radiobutton_get_state(widget_id=self.parent.ui.recalibration_yes)
        configuration['recalibration'] = recalibration

        # renormalization (flag)
        renormalization = o_gui_handler.radiobutton_get_state(widget_id=self.parent.ui.renormalization_yes)
        configuration['renormalization'] = renormalization

        # autotemplate (flag)
        autotemplate = o_gui_handler.radiobutton_get_state(widget_id=self.parent.ui.autotemplate_yes)
        configuration['autotemplate'] = autotemplate

        # postprocessing (flag)
        postprocessing = o_gui_handler.radiobutton_get_state(widget_id=self.parent.ui.postprocessing_yes)
        configuration['postprocessing'] = postprocessing

        # comments
        comments = self.parent.ui.comments.text()
        configuration['comments'] = comments

        # create new autoNOM folder (flag)
        create_new_autonom_folder = o_gui_handler.radiobutton_get_state(widget_id=self.parent.ui.create_folder_button)
        configuration['create_new_autonom_folder'] = create_new_autonom_folder

        # automatic (flag)
        auto_autonom_folder = o_gui_handler.radiobutton_get_state(widget_id=self.parent.ui.auto_manual_folder)
        configuration['auto_autonom_folder'] = auto_autonom_folder

        # manual
        manual_autonom_folder_name = self.parent.ui.manual_output_folder_field.text()
        configuration['manual_autonom_folder_name'] = manual_autonom_folder_name

        # Post Processing
        # table
        o_table = ExportTable(parent=self.parent)
        o_table.run()
        table = o_table.output_text
        configuration['table'] = table

        # background No (flag)
        background_flag = o_gui_handler.radiobutton_get_state(widget_id=self.parent.ui.background_yes)
        configuration['background_flag'] = background_flag

        # background dropdown index
        background_index = o_gui_handler.dropdown_get_index(widget_id=self.parent.ui.background_comboBox)
        configuration['background_index'] = background_index

        # background no field
        background_no_field = self.parent.ui.background_no_field.text()
        configuration['background_no_field'] = background_no_field

        # PDF
        # NDabs fourier filter min
        ndabs_fourier_filter_min = self.parent.ui.fourier_filter_from.text()
        configuration['ndabs_fourier_filter_min'] = ndabs_fourier_filter_min

        # NDabs fourier filter max
        ndabs_fourier_filter_max = self.parent.ui.fourier_filter_to.text()
        configuration['ndabs_fourier_filter_max'] = ndabs_fourier_filter_max

        # Qmin
        q_min = self.parent.ui.q_range_min.text()
        configuration['q_min'] = q_min

        # Qmax
        q_max = self.parent.ui.q_range_max.text()
        configuration['q_max'] = q_max

        # plazcek fit range min
        plazcek_fit_range_min = self.parent.ui.plazcek_fit_range_min.text()
        configuration['plazcek_fit_range_min'] = plazcek_fit_range_min

        # plazcek fit range max
        plazcek_fit_range_max = self.parent.ui.plazcek_fit_range_max.text()
        configuration['plazcek_fit_range_max'] = plazcek_fit_range_max

        # hydrogen (flag)
        hydrogen_flag = o_gui_handler.radiobutton_get_state(widget_id=self.parent.ui.hydrogen_yes)
        configuration['hydrogen_flag'] = hydrogen_flag

        # muscat yes (flag)
        muscat_flag = o_gui_handler.radiobutton_get_state(widget_id=self.parent.ui.muscat_yes)
        configuration['muscat_flag'] = muscat_flag

        # scale data yes (flag)
        scale_data_flag = o_gui_handler.radiobutton_get_state(widget_id=self.parent.ui.scale_data_yes)
        configuration['scale_data_flag'] = scale_data_flag

        # run RMC yes (flag)
        #run_rmc_flag = o_gui_handler.radiobutton_get_state(widget_id = self.parent.ui.run_rmc_yes)
        #configuration['run_rmc_flag'] = run_rmc_flag

        # output file name
        output_file_name = self.parent.ui.run_ndabs_output_file_name.text()
        configuration['ndabs_output_file_name'] = output_file_name

        # Sum Scans Qmax
        pdf_qmax_line_edit = self.parent.ui.pdf_qmax_line_edit.text()
        configuration['pdf_qmax_line_edit'] = pdf_qmax_line_edit

        # Sum Scans Rmax
        pdf_sum_scans_rmax = self.parent.ui.sum_scans_rmax.text()
        configuration['pdf_sum_scans_rmax'] = pdf_sum_scans_rmax

        # Sum Scans output file name
        pdf_sum_scans_output_file_name = self.parent.ui.sum_scans_output_file_name.text()
        configuration['pdf_sum_scans_output_file_name'] = pdf_sum_scans_output_file_name

        # interactive mode (flag)
        interactive_mode_flag = o_gui_handler.radiobutton_get_state(widget_id=self.parent.ui.interactive_mode_checkbox)
        configuration['interactive_mode_flag'] = interactive_mode_flag

        # Rietveld
        # calibration
        mantid_calibration_value = self.parent.ui.mantid_calibration_value.text()
        configuration['mantid_calibration_value'] = mantid_calibration_value

        # characterization
        mantid_characterization_value = self.parent.ui.mantid_characterization_value.text()
        configuration['mantid_characterization_value'] = mantid_characterization_value

        # number of bins
        mantid_number_of_bins = self.parent.ui.mantid_number_of_bins.text()
        configuration['mantid_number_of_bins'] = mantid_number_of_bins

        # crop wavelength min
        mantid_min_crop_wavelength = self.parent.ui.mantid_min_crop_wavelength.text()
        configuration['mantid_min_crop_wavelength'] = mantid_min_crop_wavelength

        # crop wavelength max
        mantid_max_crop_wavelength = self.parent.ui.mantid_max_crop_wavelength.text()
        configuration['mantid_max_crop_wavelength'] = mantid_max_crop_wavelength

        # vanadium radius
        mantid_vanadium_radius = self.parent.ui.mantid_vanadium_radius.text()
        configuration['mantid_vanadium_radius'] = mantid_vanadium_radius

        # output directory
        mantid_output_directory_value = self.parent.ui.mantid_output_directory_value.text()
        configuration['mantid_output_directory_value'] = mantid_output_directory_value

        self.configuration = configuration

    def request_config_file_name(self):
        o_config_file = ConfigFileNameHandler(parent=self.parent)
        o_config_file.request_config_file_name(open_flag=False)
        self.filename = o_config_file.filename

    def save_settings(self):
        _output_filename = self.filename
        configuration = self.configuration
        o_file_handler = FileHandler(filename=_output_filename)
        o_file_handler.create_config_parser(section_name=self.parent.config_section_name,
                                            dictionary=configuration)

        # for key, value in configuration.iteritems():
        #   print("{}: {}".format(key, value))
