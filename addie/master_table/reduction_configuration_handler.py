import json

try:
    from PyQt4.QtGui import QDialog, QFileDialog
    from PyQt4 import QtCore, QtGui
except ImportError:
    try:
        from PyQt5.QtWidgets import QDialog, QFileDialog
        from PyQt5 import QtCore, QtGui
    except ImportError:
        raise ImportError("Requires PyQt4 or PyQt5")

from addie.ui_reduction_configuration_dialog import Ui_Dialog as UiDialog

from addie.make_calibration_handler.make_calibration import MakeCalibrationLauncher
from addie.master_table.utilities import LoadGroupingFile


class ReductionConfigurationHandler:

    def __init__(self, parent=None):

        if parent.reduction_configuration_ui == None:
            parent.reduction_configuration_ui = ReductionConfiguration(parent=parent)
            parent.reduction_configuration_ui.show()
            if parent.reduction_configuration_ui_position:
                parent.reduction_configuration_ui.move(parent.reduction_configuration_ui_position)
            else:
                parent.reduction_configuration_ui.activateWindow()
                parent.reduction_configuration_ui.setFocus()


class ReductionConfiguration(QDialog):

    list_grouping_intermediate_browse_widgets = []
    list_grouping_output_browse_widgets = []

    def __init__(self, parent=None):
        self.parent = parent
        QDialog.__init__(self, parent=parent)
        self.ui = UiDialog()
        self.ui.setupUi(self)
        self.init_widgets()
        self.parent.set_default_folders_path()

    def init_widgets(self):
        '''init all widgets with values in case we already opened that window, or populated with
        default values'''
        self.ui.reset_pdf_q_range_button.setIcon(QtGui.QIcon(":/MPL Toolbar/reset_logo.png"))
        self.ui.reset_pdf_r_range_button.setIcon(QtGui.QIcon(":/MPL Toolbar/reset_logo.png"))

        # init all widgets with previous or default values
        LoadReductionConfiguration(parent=self, grand_parent=self.parent)

        self.list_grouping_intermediate_browse_widgets = [self.ui.intermediate_browse_button,
                                                          self.ui.intermediate_browse_value,
                                                          self.ui.intermediate_browse_groups_value,
                                                          self.ui.intermediate_browse_groups_label]
        self.list_grouping_intermediate_widgets = [self.ui.intermediate_from_calibration_label,
                                                   self.ui.intermediate_from_calibration_groups_label,
                                                   self.ui.intermediate_from_calibration_groups_value]

        self.list_grouping_output_browse_widgets = [self.ui.output_browse_button,
                                                          self.ui.output_browse_value,
                                                          self.ui.output_browse_groups_value,
                                                          self.ui.output_browse_groups_label]
        self.list_grouping_output_widgets = [self.ui.output_from_calibration_label,
                                                   self.ui.output_from_calibration_groups_label,
                                                   self.ui.output_from_calibration_groups_value]

        intermediate_grouping = self.parent.intermediate_grouping
        status_intermediate = intermediate_grouping['enabled']
        self.change_status_intermediate_buttons(status=status_intermediate)
        self.ui.intermediate_browse_radio_button.setChecked(status_intermediate)
        self.ui.intermediate_browse_value.setText(intermediate_grouping['filename'])
        self.ui.intermediate_browse_groups_value.setText(str(intermediate_grouping['nbr_groups']))

        output_grouping = self.parent.output_grouping
        status_output = output_grouping['enabled']
        self.change_status_output_buttons(status=status_output)
        self.ui.output_browse_radio_button.setChecked(status_output)
        self.ui.output_browse_value.setText(output_grouping['filename'])
        self.ui.output_browse_groups_value.setText(str(output_grouping['nbr_groups']))

    def _check_status_intermediate_buttons(self):
        '''this method will enabled or not all the widgets of the intermediate groups browse section'''
        status_browse_widgets = self.ui.intermediate_browse_radio_button.isChecked()
        self.parent.intermediate_grouping['enabled'] = status_browse_widgets
        self.change_status_intermediate_buttons(status=status_browse_widgets)

    def change_status_intermediate_buttons(self, status=False):
        for _widget in self.list_grouping_intermediate_browse_widgets:
            _widget.setEnabled(status)
        for _widget in self.list_grouping_intermediate_widgets:
            _widget.setEnabled(not status)

    def _check_status_output_buttons(self):
        '''this method will enabled or not all the widgets of the output groups browse section'''
        status_browse_widgets = self.ui.output_browse_radio_button.isChecked()
        self.parent.output_grouping['enabled'] = status_browse_widgets
        self.change_status_output_buttons(status=status_browse_widgets)

    def change_status_output_buttons(self, status=False):
        for _widget in self.list_grouping_output_browse_widgets:
            _widget.setEnabled(status)
        for _widget in self.list_grouping_output_widgets:
            _widget.setEnabled(not status)

    def intermediate_radio_button_clicked(self):
        self._check_status_intermediate_buttons()

    def intermediate_browse_radio_button_clicked(self):
        self._check_status_intermediate_buttons()

    def output_radio_button_clicked(self):
        self._check_status_output_buttons()

    def output_browse_radio_button_clicked(self):
        self._check_status_output_buttons()

    def intermediate_browse_button_clicked(self):
        _characterization_folder = self.parent.characterization_folder
        _intermediate_group_file = QtGui.QFileDialog.getOpenFileName(parent=self.parent,
                                                                   caption="Select Grouping File",
                                                                   directory=_characterization_folder,
                                                                   filter="XML (*.xml)")
        if _intermediate_group_file:
            self.ui.intermediate_browse_value.setText(_intermediate_group_file)
            o_grouping = LoadGroupingFile(filename=_intermediate_group_file)
            nbr_groups = o_grouping.get_number_of_groups()
            self.ui.intermediate_browse_groups_value.setText(str(nbr_groups))
            self.parent.intermediate_grouping['filename'] = _intermediate_group_file
            self.parent.intermediate_grouping['nbr_groups'] = nbr_groups

    def output_browse_button_clicked(self):
        _characterization_folder = self.parent.characterization_folder
        _output_group_file = QtGui.QFileDialog.getOpenFileName(parent=self.parent,
                                                                   caption="Select Grouping File",
                                                                   directory=_characterization_folder,
                                                                   filter="XML (*.xml)")
        if _output_group_file:
            self.ui.output_browse_value.setText(_output_group_file)
            o_grouping = LoadGroupingFile(filename=_output_group_file)
            nbr_groups = o_grouping.get_number_of_groups()
            self.ui.output_browse_groups_value.setText(str(nbr_groups))
            self.parent.output_grouping['filename'] = _output_group_file
            self.parent.output_grouping['nbr_groups'] = nbr_groups

    def pdf_reset_q_range_button(self):
        pass

    def pdf_reset_r_range_button(self):
        pass

    # def make_calibration_clicked(self):
    #     MakeCalibrationLauncher(parent=self, grand_parent=self.parent)
    #
    # def browse_calibration_clicked(self):
    #     _calibration_folder = self.parent.calibration_folder
    #     _calibration_file = QtGui.QFileDialog.getOpenFileName(parent = self.parent,
    #                                                           caption = "Select Calibration File",
    #                                                           directory = _calibration_folder,
    #                                                           filter = self.parent.calibration_extension)
    #     if _calibration_file:
    #         self.ui.calibration_file.setText(_calibration_file)

    def pdf_browse_characterization_clicked(self):
        _characterization_folder = self.parent.characterization_folder
        _characterization_file = QtGui.QFileDialog.getOpenFileName(parent=self.parent,
                                                                   caption="Select Characterization File",
                                                                   directory=_characterization_folder,
                                                                   filter=self.parent.characterization_extension)
        if _characterization_file:
            self.ui.pdf_characterization_file.setText(_characterization_file)

    def close_button(self):
        # save state of buttons
        SaveReductionConfiguration(parent=self, grand_parent=self.parent)

        # close
        self.close()

    def closeEvent(self, event=None):
        self.parent.reduction_configuration_ui = None
        self.parent.reduction_configuration_ui_position = self.pos()

    def cancel_clicked(self):
        self.close()

# class LoadGroupingFile:
#     '''This class reads the XML file and will return the number of groups <group ID=""> found in that file'''
#
#     def __init__(self, filename=''):
#         self.filename = filename
#
#     def get_number_of_groups(self):
#         xmldoc = minidom.parse(self.filename)
#         itemlist = xmldoc.getElementsByTagName('group')
#         return len(itemlist)
#

class LoadReductionConfiguration:

    def __init__(self, parent=None, grand_parent=None):

        # list of sample environment
        if grand_parent.reduction_configuration == {}:
            config_file = grand_parent.addie_config_file
            with open(config_file) as f:
                data = json.load(f)
            pdf_q_range = data['pdf']['q_range']
            pdf_r_range = data['pdf']['r_range']
            pdf_reduction_configuration_file = data["pdf"]["reduction_configuration_file"]
            pdf_characterization_file = data["pdf"]["characterization_file"]

            bragg_characterization_file = data["bragg"]["characterization_file"]
            bragg_number_of_bins = data["bragg"]["number_of_bins"]
            bragg_wavelength = data["bragg"]["wavelength"]

            #calibration_file = data["pdf_bragg"]["calibration_file"]
            push_data_positive = data["advanced"]["push_data_positive"]

        else:
            pdf_q_range = grand_parent.reduction_configuration['pdf']['q_range']
            pdf_r_range = grand_parent.reduction_configuration['pdf']['r_range']
            pdf_reduction_configuration_file = grand_parent.reduction_configuration['pdf']['reduction_configuration_file']
            pdf_characterization_file = grand_parent.reduction_configuration['pdf']['characterization_file']

            bragg_characterization_file = grand_parent.reduction_configuration["bragg"]["characterization_file"]
            bragg_number_of_bins = grand_parent.reduction_configuration["bragg"]["number_of_bins"]
            bragg_wavelength = grand_parent.reduction_configuration["bragg"]["wavelength"]

            #calibration_file = grand_parent.reduction_configuration["pdf_bragg"]["calibration_file"]
            push_data_positive = grand_parent.reduction_configuration["advanced"]["push_data_positive"]

        # PDF and Bragg
        #self._set_text_value(ui=parent.ui.calibration_file, value=calibration_file)

        # PDF
        self._set_text_value(ui=parent.ui.pdf_q_range_min, value=pdf_q_range["min"])
        self._set_text_value(ui=parent.ui.pdf_q_range_max, value=pdf_q_range["max"])
        self._set_text_value(ui=parent.ui.pdf_q_range_delta, value=pdf_q_range["delta"])
        self._set_text_value(ui=parent.ui.pdf_r_range_min, value=pdf_r_range["min"])
        self._set_text_value(ui=parent.ui.pdf_r_range_max, value=pdf_r_range["max"])
        self._set_text_value(ui=parent.ui.pdf_r_range_delta, value=pdf_r_range["delta"])
        self._set_text_value(ui=parent.ui.pdf_reduction_configuration_file, value=pdf_reduction_configuration_file)
        self._set_text_value(ui=parent.ui.pdf_characterization_file, value=pdf_characterization_file)

        # Bragg
        self._set_text_value(ui=parent.ui.bragg_characterization_file, value=bragg_characterization_file)
        self._set_text_value(ui=parent.ui.bragg_number_of_bins, value=bragg_number_of_bins)
        self._set_text_value(ui=parent.ui.bragg_wavelength_min, value=bragg_wavelength["min"])
        self._set_text_value(ui=parent.ui.bragg_wavelength_max, value=bragg_wavelength["max"])

        # advanced
        self._set_checkbox_value(ui=parent.ui.push_data_positive, value=push_data_positive)

    def _set_text_value(self, ui=None, value=""):
        if ui is None:
            return
        ui.setText(str(value))

    def _set_checkbox_value(self, ui=None, value=False):
        if ui is None:
            return
        ui.setChecked(value)


class SaveReductionConfiguration:

    def __init__(self, parent=None, grand_parent=None):
        reduction_configuration = {}

        # PDF and Bragg
        reduction_configuration['pdf_bragg'] = {}

        #calibration_file = self._get_text_value(parent.ui.calibration_file)
        #reduction_configuration['pdf_bragg']["calibration_file"] = calibration_file

        # PDF
        pdf_reduction_configuration = {}

        pdf_reduction_configuration['characterization_file'] = self._get_text_value(parent.ui.pdf_characterization_file)

        pdf_q_range_min = self._get_text_value(parent.ui.pdf_q_range_min)
        pdf_q_range_max = self._get_text_value(parent.ui.pdf_q_range_max)
        pdf_q_range_delta = self._get_text_value(parent.ui.pdf_q_range_delta)
        pdf_reduction_configuration['q_range'] = {'min': pdf_q_range_min,
                                                  'max': pdf_q_range_max,
                                                  'delta': pdf_q_range_delta}

        pdf_r_range_min = self._get_text_value(parent.ui.pdf_r_range_min)
        pdf_r_range_max = self._get_text_value(parent.ui.pdf_r_range_max)
        pdf_r_range_delta = self._get_text_value(parent.ui.pdf_r_range_delta)
        pdf_reduction_configuration['r_range'] = {'min': pdf_r_range_min,
                                                  'max': pdf_r_range_max,
                                                  'delta': pdf_r_range_delta}

        pdf_reduction_configuration_file = self._get_text_value(parent.ui.pdf_reduction_configuration_file)
        pdf_reduction_configuration['reduction_configuration_file'] = pdf_reduction_configuration_file

        reduction_configuration['pdf'] = pdf_reduction_configuration

        # Bragg
        bragg_reduction_configuration = {}

        bragg_characterization_file = self._get_text_value(parent.ui.bragg_characterization_file)
        bragg_reduction_configuration["characterization_file"] = bragg_characterization_file

        bragg_number_of_bins = self._get_text_value(parent.ui.bragg_number_of_bins)
        bragg_reduction_configuration["number_of_bins"] = bragg_number_of_bins

        bragg_wavelength_min = self._get_text_value(parent.ui.bragg_wavelength_min)
        bragg_wavelength_max = self._get_text_value(parent.ui.bragg_wavelength_max)
        bragg_reduction_configuration["wavelength"] = {'min': bragg_wavelength_min,
                                                       'max': bragg_wavelength_max}

        reduction_configuration['bragg'] = bragg_reduction_configuration

        # advanced
        advanced_reduction_configuration = {}
        advanced_reduction_configuration["push_data_positive"] = self._set_checkbox_value(ui=parent.ui.push_data_positive)

        reduction_configuration["advanced"] = advanced_reduction_configuration

        # final save
        grand_parent.reduction_configuration = reduction_configuration

    def _get_text_value(self, ui=None):
        if ui is None:
            return ""

        return str(ui.text())

    def _set_checkbox_value(self, ui=None):
        if ui is None:
            return False

        _state = ui.checkState()
        if _state == QtCore.Qt.Checked:
            return True
        else:
            return False

