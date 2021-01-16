from __future__ import (absolute_import, division, print_function)
from qtpy.QtCore import (Qt)
from qtpy.QtWidgets import (QFileDialog)
import os

import addie.processing.idl.table_handler
from addie.utilities.math_tools import is_int, is_float
from addie.help_handler.help_gui import check_status


class Step2GuiHandler(object):

    hidrogen_range = [1, 50]
    no_hidrogen_range = [10, 50]
    current_folder = ""
    default_q_range = [0.2, 31.4]
    default_ndabs_output_file_name = "sample_name"
    user_canceled = False

    def __init__(self, main_window=None):
        self.main_window = main_window
        self.current_folder = main_window.current_folder

    def move_to_folder(self):
        _new_folder = QFileDialog.getExistingDirectory(parent=self.main_window,
                                                       caption="Select working directory",
                                                       directory=self.current_folder)
        if not _new_folder:
            self.user_canceled = True
        else:
            if isinstance(_new_folder, tuple):
                _new_folder = _new_folder[0]
            os.chdir(_new_folder)
            self.main_window.current_folder = _new_folder
            self.main_window.setWindowTitle(_new_folder)

    def is_hydrogen_clicked(self):
        return self.main_window.postprocessing_ui.hydrogen_yes.isChecked()

    def hydrogen_clicked(self):
        _range = self.hidrogen_range
        self.populate_hidrogen_range(_range)

    def no_hydrogen_clicked(self):
        _range = self.no_hidrogen_range
        self.populate_hidrogen_range(_range)

    def populate_hidrogen_range(self, fit_range):
        min_value, max_value = fit_range
        self.main_window.postprocessing_ui.plazcek_fit_range_min.setText("%d" % min_value)
        self.main_window.postprocessing_ui.plazcek_fit_range_max.setText("%d" % max_value)

    def get_plazcek_range(self):
        fit_range_min = self.main_window.postprocessing_ui.plazcek_fit_range_min.text().strip()
        fit_range_max = self.main_window.postprocessing_ui.plazcek_fit_range_max.text().strip()
        return [fit_range_min, fit_range_max]

    def get_q_range(self):
        q_range_min = self.main_window.postprocessing_ui.q_range_min.text().strip()
        q_range_max = self.main_window.postprocessing_ui.q_range_max.text().strip()
        return [q_range_min, q_range_max]

    def step2_background_flag(self):
        if self.main_window.postprocessing_ui.background_no.isChecked():
            self.no_background_clicked()
        else:
            self.yes_background_clicked()

    def yes_background_clicked(self):
        self.main_window.postprocessing_ui.background_line_edit.setEnabled(True)
        self.main_window.postprocessing_ui.background_comboBox.setEnabled(True)

    def no_background_clicked(self):
        self.main_window.postprocessing_ui.background_line_edit.setEnabled(False)
        self.main_window.postprocessing_ui.background_comboBox.setEnabled(False)

    def background_index_changed(self, row_index=-1):
        if row_index == -1:
            return
        if self.main_window.postprocessing_ui.table.item(row_index, 2) is None:
            return
        _item = self.main_window.postprocessing_ui.table.item(row_index, 2)
        self.main_window.postprocessing_ui.background_line_edit.setText(_item.text())

    def step2_update_background_dropdown(self):
        row_index = self.main_window.postprocessing_ui.background_comboBox.currentIndex()
        self.background_index_changed(row_index=row_index)

    def check_gui(self):
        self.check_run_ndabs_button()
        self.check_run_sum_scans_button()
        self.check_import_export_buttons()

    def define_new_ndabs_output_file_name(self):
        """retrieve name of first row selected and use it to define output file name"""
        _output_file_name = self.define_new_output_file_name()
        self.main_window.postprocessing_ui.run_ndabs_output_file_name.setText(_output_file_name)

    def define_new_sum_scans_output_file_name(self):
        """retrieve name of first row selected and use it to define output file name"""
        _output_file_name = self.define_new_output_file_name()
        self.main_window.postprocessing_ui.sum_scans_output_file_name.setText(_output_file_name)

    def define_new_output_file_name(self):
        """retrieve name of first row selected and use it to define output file name"""
        o_table_handler = addie.processing.idl.table_handler.TableHandler(parent=self.main_window)
        o_table_handler.retrieve_list_of_selected_rows()
        list_of_selected_row = o_table_handler.list_selected_row
        if len(list_of_selected_row) > 0:
            _metadata_selected = o_table_handler.list_selected_row[0]
            _output_file_name = _metadata_selected['name']
        else:
            _output_file_name = self.default_ndabs_output_file_name
        return _output_file_name

    def get_sum_scans_script(self):
        return self.main_window._sum_scans_script

    def check_import_export_buttons(self):
        _export_status = False
        if self.main_window.postprocessing_ui.table.rowCount() > 0:
            _export_status = True

        self.main_window.postprocessing_ui.export_button.setEnabled(_export_status)

    def check_run_mantid_reduction_button(self):
        _status = True
        if not self.main_window.postprocessing_ui.table.rowCount() > 0:
            _status = False

        if _status and (not self.at_least_one_row_checked()):
            _status = False

        if _status and (self.main_window.postprocessing_ui.mantid_calibration_value.text() == 'N/A'):
            _status = False

        if _status and (self.main_window.postprocessing_ui.mantid_characterization_value.text() == 'N/A'):
            _status = False

        if _status and (self.main_window.postprocessing_ui.vanadium.text() == ""):
            _status = False

        if _status and (self.main_window.postprocessing_ui.vanadium_background.text() == ""):
            _status = False

        if _status and (not is_int(self.main_window.postprocessing_ui.mantid_number_of_bins.text())):
            _status = False

        if _status and (not is_float(self.main_window.postprocessing_ui.mantid_min_crop_wavelength.text())):
            _status = False

        if _status and (not is_float(self.main_window.postprocessing_ui.mantid_max_crop_wavelength.text())):
            _status = False

        if _status and (not is_float(self.main_window.postprocessing_ui.mantid_vanadium_radius.text())):
            _status = False

        if _status and (self.main_window.postprocessing_ui.mantid_output_directory_value.text() == "N/A"):
            _status = False

        self.main_window.postprocessing_ui.mantid_run_reduction.setEnabled(_status)
        check_status(parent=self.main_window, button_name='mantid')

    def check_run_sum_scans_button(self):

        _status = True
        if not self.main_window.postprocessing_ui.table.rowCount() > 0:
            _status = False

        if _status and (not self.at_least_one_row_checked()):
            _status = False

        if _status and self.main_window.postprocessing_ui.sum_scans_output_file_name.text() == "":
            _status = False

        self.main_window.postprocessing_ui.run_sum_scans_button.setEnabled(_status)
        check_status(parent=self.main_window, button_name='scans')

    def check_run_ndabs_button(self):

        _status = True
        if not self.main_window.postprocessing_ui.table.rowCount() > 0:
            _status = False

        if not self.at_least_one_row_checked():
            _status = False

        if self.any_fourier_filter_widgets_empty():
            _status = False

        if self.any_plazcek_widgets_empty():
            _status = False

        if self.any_q_range_widgets_empty():
            _status = False

        # make sure the row checked have none empty metadata fields
        if _status:
            for _row in range(self.main_window.postprocessing_ui.table.rowCount()):
                _this_row_status_ok = self.check_if_this_row_is_ok(_row)
                if not _this_row_status_ok:
                    _status = False
                    break

        if self.main_window.postprocessing_ui.run_ndabs_output_file_name.text() == '':
            _status = False

        self.main_window.postprocessing_ui.run_ndabs_button.setEnabled(_status)
        check_status(parent=self.main_window, button_name='ndabs')

    def at_least_one_row_checked(self):
        o_table_handler = addie.processing.idl.table_handler.TableHandler(parent=self.main_window)
        o_table_handler.retrieve_list_of_selected_rows()
        list_of_selected_row = o_table_handler.list_selected_row
        if len(list_of_selected_row) > 0:
            return True
        else:
            return False

    def check_if_this_row_is_ok(self, row):
        _status_ok = True
        _selected_widget = self.main_window.postprocessing_ui.table.cellWidget(row, 0).children()
        if len(_selected_widget) > 0:
            if (_selected_widget[1].checkState() == Qt.Checked):
                _table_handler = addie.processing.idl.table_handler.TableHandler(parent=self.main_window)
                for _column in range(1, 7):
                    if _table_handler.retrieve_item_text(row, _column) == '':
                        _status_ok = False
                        break

        return _status_ok

    def any_plazcek_widgets_empty(self):
        _min = str(self.main_window.postprocessing_ui.plazcek_fit_range_min.text()).strip()
        if _min == "":
            return True

        _max = str(self.main_window.postprocessing_ui.plazcek_fit_range_max.text()).strip()
        if _max == "":
            return True

        return False

    def any_q_range_widgets_empty(self):
        _min = str(self.main_window.postprocessing_ui.q_range_min.text()).strip()
        if _min == "":
            return True

        _max = str(self.main_window.postprocessing_ui.q_range_max.text()).strip()
        if _max == "":
            return True

        return False

    def any_fourier_filter_widgets_empty(self):
        _from = str(self.main_window.postprocessing_ui.fourier_filter_from.text()).strip()
        if _from == "":
            return True

        _to = str(self.main_window.postprocessing_ui.fourier_filter_to.text()).strip()
        if _to == "":
            return True

        return False

    def reset_q_range(self):
        _q_min = "%s" % str(self.default_q_range[0])
        _q_max = "%s" % str(self.default_q_range[1])
        self.main_window.postprocessing_ui.q_range_min.setText(_q_min)
        self.main_window.postprocessing_ui.q_range_max.setText(_q_max)
