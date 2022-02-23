from __future__ import (absolute_import, division, print_function)
import simplejson
from qtpy.QtWidgets import QDialog, QFileDialog, QTableWidgetItem
from addie.utilities import load_ui
from qtpy import QtGui, QtCore
import numpy as np

from addie.processing.mantid.master_table.utilities import LoadGroupingFile
from addie.initialization.widgets.main_tab import set_default_folder_path
from addie.utilities.general import get_list_algo

COLUMNS_WIDTH = [150, 150]


class ReductionConfigurationHandler:

    def __init__(self, parent=None):

        if parent.reduction_configuration_ui is None:
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
    list_grouping_intermediate_widgets = []
    list_grouping_output_widgets = []

    global_key_value = {}

    def __init__(self, parent=None):
        self.parent = parent
        QDialog.__init__(self, parent=parent)
        self.ui = load_ui('reduction_configuration_dialog.ui', baseinstance=self)
        self.init_widgets()
        set_default_folder_path(self.parent)

    def init_widgets(self):
        '''init all widgets with values in case we already opened that window, or populated with
        default values'''
        self.ui.reset_pdf_q_range.setIcon(QtGui.QIcon(":/MPL Toolbar/reset_logo.png"))
        self.ui.reset_pdf_r_range.setIcon(QtGui.QIcon(":/MPL Toolbar/reset_logo.png"))

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

        self.ui.abs_ms_ele_size.setText(self.parent.advanced_dict["ele_size"])

        self.init_global_key_value_widgets()
        self.update_key_value_widgets()

    def init_global_key_value_widgets(self):
        self.populate_list_algo()
        self._set_column_widths()
        self.init_table()

    def _remove_blacklist_algo(self, list_algo):
        list_algo_without_blacklist = []
        for _algo in list_algo:
            if not (_algo in self.parent.align_and_focus_powder_from_files_blacklist):
                list_algo_without_blacklist.append(_algo)
        return list_algo_without_blacklist

    def _set_column_widths(self):
        for _col, _width in enumerate(COLUMNS_WIDTH):
            self.ui.key_value_table.setColumnWidth(_col, _width)

    def init_table(self):
        global_key_value = self.parent.global_key_value
        for _row, _key in enumerate(global_key_value.keys()):
            _value = global_key_value[_key]
            self._add_row(row=_row, key=_key, value=_value)

    def show_global_key_value_widgets(self, visible=False):
        self.ui.global_key_value_groupBox.setVisible(visible)

    def remove_from_list(self,
                         original_list=[],
                         to_remove=[]):
        if to_remove:
            clean_list_algo = []
            for _algo in original_list:
                if not(_algo in to_remove):
                    clean_list_algo.append(_algo)
            return clean_list_algo
        else:
            return original_list

    def populate_list_algo(self):
        self.ui.list_key_comboBox.clear()

        raw_list_algo = get_list_algo('AlignAndFocusPowderFromFiles')
        list_algo_without_blacklist = self._remove_blacklist_algo(raw_list_algo)

        global_list_keys = self.parent.global_key_value.keys()
        global_unused_list_algo = self.remove_from_list(original_list=list_algo_without_blacklist,
                                                        to_remove=global_list_keys)
        self.ui.list_key_comboBox.addItems(global_unused_list_algo)

    def add_key_value(self):
        self._add_new_row_at_bottom()
        self.update_key_value_widgets()
        self.populate_list_algo()
        self.ui.list_key_comboBox.setFocus()

    def _add_row(self, row=-1, key='', value=""):
        self.ui.key_value_table.insertRow(row)
        self._set_item(key, row, 0)
        self._set_item(value, row, 1, is_editable=True)

    def _set_item(self, text, row, column, is_editable=False):
        key_item = QTableWidgetItem(text)
        if not is_editable:
            key_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        self.ui.key_value_table.setItem(row, column, key_item)

    def _add_new_row_at_bottom(self):
        value = str(self.ui.new_value_widget.text())
        # do not allow to add row with empty value
        if value.strip() == "":
            return
        nbr_row = self.get_nbr_row()
        key = self.get_current_selected_key()
        self.parent.global_key_value[key] = value
        self.global_key_value[key] = value
        self._add_row(row=nbr_row, key=key, value=value)
        self.ui.new_value_widget.setText("")

    def get_current_selected_key(self):
        return str(self.ui.list_key_comboBox.currentText())

    def get_nbr_row(self):
        return self.ui.key_value_table.rowCount()

    def _get_selected_row_range(self):
        selection = self.ui.key_value_table.selectedRanges()
        if not selection:
            return None
        from_row = selection[0].topRow()
        to_row = selection[0].bottomRow()
        return np.arange(from_row, to_row+1)

    def _remove_rows(self, row_range):
        first_row_selected = row_range[0]
        for _ in row_range:
            self.ui.key_value_table.removeRow(first_row_selected)

    def remove_key_value_selected(self):
        selected_row_range = self._get_selected_row_range()
        if selected_row_range is None:
            return
        self._remove_rows(selected_row_range)
        self.update_key_value_widgets()
        self.update_global_key_value()
        self.populate_list_algo()

    def update_global_key_value(self):
        nbr_row = self.get_nbr_row()
        global_key_value = {}
        for _row in np.arange(nbr_row):
            _key = self._get_cell_value(_row, 0)
            _value = self._get_cell_value(_row, 1)
            global_key_value[_key] = _value
        self.parent.global_key_value = global_key_value
        self.global_key_value = global_key_value

    def _get_cell_value(self, row, column):
        item = self.ui.key_value_table.item(row, column)
        return str(item.text())

    def _what_state_remove_button_should_be(self):
        nbr_row = self.get_nbr_row()
        if nbr_row > 0:
            enable = True
        else:
            enable = False
        return enable

    def update_key_value_widgets(self):
        enable = self._what_state_remove_button_should_be()
        self.ui.remove_selection_button.setEnabled(enable)

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
        [_intermediate_group_file, _] = QFileDialog.getOpenFileName(parent=self.parent,
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
        [_output_group_file, _] = QFileDialog.getOpenFileName(parent=self.parent,
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

    def reset_pdf_q_range_button(self):
        pdf_q_range,pdf_r_range = self.get_reset_data()
        LoadReductionConfiguration._set_text_value(LoadReductionConfiguration,ui=self.ui.pdf_q_range_min,value=pdf_q_range["min"])
        LoadReductionConfiguration._set_text_value(LoadReductionConfiguration,ui=self.ui.pdf_q_range_max,value=pdf_q_range["max"])
        LoadReductionConfiguration._set_text_value(LoadReductionConfiguration,
                                                   ui=self.ui.pdf_q_range_delta,
                                                   value=pdf_q_range["delta"])

    def reset_pdf_r_range_button(self):
        pdf_q_range,pdf_r_range = self.get_reset_data()
        LoadReductionConfiguration._set_text_value(LoadReductionConfiguration,ui=self.ui.pdf_r_range_min,value=pdf_r_range["min"])
        LoadReductionConfiguration._set_text_value(LoadReductionConfiguration,ui=self.ui.pdf_r_range_max,value=pdf_r_range["max"])
        LoadReductionConfiguration._set_text_value(LoadReductionConfiguration,
                                                   ui=self.ui.pdf_r_range_delta,
                                                   value=pdf_r_range["delta"])

    def bragg_browse_characterization_clicked(self):
        _characterization_folder = self.parent.characterization_folder
        [_characterization_file, _] = QFileDialog.getOpenFileName(parent=self.parent,
                                                                  caption="Select Characterization File",
                                                                  directory=_characterization_folder,
                                                                  filter=self.parent.characterization_extension)
        if _characterization_file:
            self.ui.bragg_characterization_file.setText(_characterization_file)

    def pdf_browse_characterization_clicked(self):
        _characterization_folder = self.parent.characterization_folder
        [_characterization_file, _] = QFileDialog.getOpenFileName(parent=self.parent,
                                                                  caption="Select Characterization File",
                                                                  directory=_characterization_folder,
                                                                  filter=self.parent.characterization_extension)
        if _characterization_file:
            self.ui.pdf_characterization_file.setText(_characterization_file)

    def close_button(self):
        # save state of buttons
        SaveReductionConfiguration(parent=self, grand_parent=self.parent)

        self._retrieve_global_key_value()
        self.parent.global_key_value = self.global_key_value

        # close
        self.close()

    def _retrieve_global_key_value(self):
        global_key_value = {}

        nbr_row = self.ui.key_value_table.rowCount()
        for _row in np.arange(nbr_row):
            _key = self._get_cell_value(_row, 0)
            _value = self._get_cell_value(_row, 1)
            global_key_value[_key] = _value
        self.global_key_value = global_key_value

    def add_global_key_value_to_all_rows(self):
        global_list_key_value = self.parent.global_key_value

        list_table_ui = self.parent.master_table_list_ui
        if not list_table_ui:
            return

        for _random_key in list_table_ui.keys():
            _entry = list_table_ui[_random_key]
            current_local_key_value = _entry['align_and_focus_args_infos']
            if current_local_key_value == {}:
                _entry['align_and_focus_args_infos'] = global_list_key_value
            else:
                list_local_keys = current_local_key_value.keys()
                list_global_keys = global_list_key_value.keys()
                new_local_key_value = {}
                for _key in list_local_keys:
                    if _key in list_global_keys:
                        new_local_key_value[_key] = global_list_key_value[_key]
                    else:
                        new_local_key_value[_key] = current_local_key_value[_key]
                _entry['align_and_focus_args_infos'] = new_local_key_value
            list_table_ui[_random_key] = _entry

        self.parent.master_table_list_ui = list_table_ui

    def closeEvent(self, event=None):
        self.parent.reduction_configuration_ui = None
        self.parent.reduction_configuration_ui_position = self.pos()
        self.add_global_key_value_to_all_rows()

    def cancel_clicked(self):
        self.close()

    def get_reset_data(self):
        # list of sample environment
        if self.parent.reduction_configuration == {}:
            config_file = self.parent.addie_config_file
            with open(config_file) as f:
                data = simplejson.load(f)
            pdf_q_range = data['pdf']['q_range']
            pdf_r_range = data['pdf']['r_range']
        else:
            pdf_q_range = self.parent.reduction_configuration['pdf']['q_range']
            pdf_r_range = self.parent.reduction_configuration['pdf']['r_range']
        print(pdf_q_range,pdf_r_range)
        return pdf_q_range,pdf_r_range


class LoadReductionConfiguration:
    def __init__(self, parent=None, grand_parent=None):

        # list of sample environment
        if grand_parent.reduction_configuration == {}:
            config_file = grand_parent.addie_config_file
            with open(config_file) as f:
                data = simplejson.load(f)
            pdf_q_range = data['pdf']['q_range']
            pdf_r_range = data['pdf']['r_range']
            pdf_characterization_file = data["pdf"]["characterization_file"]

            bragg_characterization_file = data["bragg"]["characterization_file"]
            bragg_number_of_bins = data["bragg"]["number_of_bins"]
            bragg_wavelength = data["bragg"]["wavelength"]

            #calibration_file = data["pdf_bragg"]["calibration_file"]
            push_data_positive = data["advanced"]["push_data_positive"]
            abs_ms_ele_size = data["advanced"]["abs_ms_ele_size"]
        else:
            pdf_q_range = grand_parent.reduction_configuration['pdf']['q_range']
            pdf_r_range = grand_parent.reduction_configuration['pdf']['r_range']
            pdf_characterization_file = grand_parent.reduction_configuration['pdf']['characterization_file']

            bragg_characterization_file = grand_parent.reduction_configuration["bragg"]["characterization_file"]
            bragg_number_of_bins = grand_parent.reduction_configuration["bragg"]["number_of_bins"]
            bragg_wavelength = grand_parent.reduction_configuration["bragg"]["wavelength"]

            #calibration_file = grand_parent.reduction_configuration["pdf_bragg"]["calibration_file"]
            push_data_positive = grand_parent.reduction_configuration["advanced"]["push_data_positive"]
            abs_ms_ele_size = grand_parent.reduction_configuration["advanced"]["abs_ms_ele_size"]

        # PDF and Bragg
        #self._set_text_value(ui=parent.ui.calibration_file, value=calibration_file)

        # PDF
        self._set_text_value(ui=parent.ui.pdf_q_range_min, value=pdf_q_range["min"])
        self._set_text_value(ui=parent.ui.pdf_q_range_max, value=pdf_q_range["max"])
        self._set_text_value(ui=parent.ui.pdf_q_range_delta, value=pdf_q_range["delta"])
        self._set_text_value(ui=parent.ui.pdf_r_range_min, value=pdf_r_range["min"])
        self._set_text_value(ui=parent.ui.pdf_r_range_max, value=pdf_r_range["max"])
        self._set_text_value(ui=parent.ui.pdf_r_range_delta, value=pdf_r_range["delta"])
        self._set_text_value(ui=parent.ui.pdf_characterization_file, value=pdf_characterization_file)

        # Bragg
        self._set_text_value(ui=parent.ui.bragg_characterization_file, value=bragg_characterization_file)
        self._set_text_value(ui=parent.ui.bragg_number_of_bins, value=bragg_number_of_bins)
        self._set_text_value(ui=parent.ui.bragg_wavelength_min, value=bragg_wavelength["min"])
        self._set_text_value(ui=parent.ui.bragg_wavelength_max, value=bragg_wavelength["max"])

        # advanced
        self._set_checkbox_value(ui=parent.ui.push_data_positive, value=push_data_positive)
        self._set_text_value(ui=parent.ui.abs_ms_ele_size, value=abs_ms_ele_size)

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

        reduction_configuration['pdf_bragg'] = {}
        pdf_reduction_configuration = {}
        bragg_reduction_configuration = {}
        advanced_reduction_configuration = {}

        if parent is not None:
            val_tmp = self._get_text_value(parent.ui.pdf_characterization_file)
            pdf_reduction_configuration['characterization_file'] = val_tmp

            pdf_q_range_min = self._get_text_value(parent.ui.pdf_q_range_min)
            pdf_q_range_max = self._get_text_value(parent.ui.pdf_q_range_max)
            pdf_q_range_delta = self._get_text_value(parent.ui.pdf_q_range_delta)

            pdf_r_range_min = self._get_text_value(parent.ui.pdf_r_range_min)
            pdf_r_range_max = self._get_text_value(parent.ui.pdf_r_range_max)
            pdf_r_range_delta = self._get_text_value(parent.ui.pdf_r_range_delta)

            bragg_characterization_file = self._get_text_value(parent.ui.bragg_characterization_file)
            bragg_number_of_bins = self._get_text_value(parent.ui.bragg_number_of_bins)
            bragg_wavelength_min = self._get_text_value(parent.ui.bragg_wavelength_min)
            bragg_wavelength_max = self._get_text_value(parent.ui.bragg_wavelength_max)

            reduction_configuration['initial'] = parent.ui.intermediate_browse_radio_button.isChecked()
            reduction_configuration['output'] = parent.ui.output_browse_radio_button.isChecked()

            advanced_reduction_configuration["push_data_positive"] = self._set_checkbox_value(ui=parent.ui.push_data_positive)
            advanced_reduction_configuration["abs_ms_ele_size"] = self._get_text_value(ui=parent.ui.abs_ms_ele_size)
        else:
            pdf_reduction_configuration['characterization_file'] = ''

            pdf_q_range_min = '0.0'
            pdf_q_range_max = '40.0'
            pdf_q_range_delta = '0.02'

            pdf_r_range_min = '0.0'
            pdf_r_range_max = '40.0'
            pdf_r_range_delta = '0.02'

            bragg_characterization_file = ''
            bragg_number_of_bins = '-6000'
            bragg_wavelength_min = '0.1'
            bragg_wavelength_max = '2.9'

            reduction_configuration['initial'] = False
            reduction_configuration['output'] = False
            advanced_reduction_configuration["push_data_positive"] = False
            advanced_reduction_configuration["abs_ms_ele_size"] = "1.0"

        pdf_reduction_configuration['q_range'] = {'min': pdf_q_range_min,
                                                  'max': pdf_q_range_max,
                                                  'delta': pdf_q_range_delta}

        pdf_reduction_configuration['r_range'] = {'min': pdf_r_range_min,
                                                  'max': pdf_r_range_max,
                                                  'delta': pdf_r_range_delta}

        reduction_configuration['pdf'] = pdf_reduction_configuration

        bragg_reduction_configuration["characterization_file"] = bragg_characterization_file
        bragg_reduction_configuration["number_of_bins"] = bragg_number_of_bins
        bragg_reduction_configuration["wavelength"] = {'min': bragg_wavelength_min,
                                                       'max': bragg_wavelength_max}

        reduction_configuration['bragg'] = bragg_reduction_configuration
        reduction_configuration["advanced"] = advanced_reduction_configuration

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
