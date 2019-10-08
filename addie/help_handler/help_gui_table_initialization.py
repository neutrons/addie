from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import (QPushButton, QTextEdit)  # noqa

from addie.autoNOM.step1_utilities import Step1Utilities
from addie.processing.idl.step2_utilities import Step2Utilities


class HelpGuiTableInitialization(object):

    row_height = 50
    widget_bad = "color: rgb(255, 0, 0)"
    widget_ok = "color: rgb(33, 118, 0)"
    jump_message = "Jump There!"

    def __init__(self, parent=None, button_name='autonom'):
        self.parent = parent
        self.ui = self.parent.parent.postprocessing_ui
        self.button_name = button_name

    def fill(self):
        if self.button_name == 'autonom':
            self.fill_autonom()
        elif self.button_name == 'ndabs':
            self.fill_ndabs()
        elif self.button_name == 'scans':
            self.fill_scans()
        elif self.button_name == 'mantid':
            self.fill_mantid()

    def refill(self):
        nbr_row = self.parent.ui.table_status.rowCount()
        for _row in range(nbr_row):
            self.parent.ui.table_status.removeRow(0)
        self.fill()

    # STEP 1

    def jump_to_step1_diamond(self):
        self.ui.tabWidget_2.setCurrentIndex(0)
        self.parent.parent.autonom_ui.diamond.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step1_diamond_background(self):
        self.ui.tabWidget_2.setCurrentIndex(0)
        self.parent.parent.autonom_ui.diamond_background.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step1_vanadium(self):
        self.ui.tabWidget_2.setCurrentIndex(0)
        self.parent.parent.autonom_ui.vanadium.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step1_vanadium_background(self):
        self.ui.tabWidget_2.setCurrentIndex(0)
        self.parent.parent.autonom_ui.vanadium_background.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step1_sample_background(self):
        self.ui.tabWidget_2.setCurrentIndex(0)
        self.parent.parent.autonom_ui.sample_background.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step1_create_folder(self):
        self.ui.tabWidget_2.setCurrentIndex(0)
        self.parent.parent.autonom_ui.manual_output_folder_field.setFocus()
        self.parent.parent.activateWindow()

    def fill_autonom(self):
        o_step1_handler = Step1Utilities(main_window=self.parent.parent)

        # diamond
        self.parent.ui.table_status.insertRow(0)
        self.parent.ui.table_status.setRowHeight(0, self.row_height)
        _widget = QTextEdit()
        _text = "Diamond Field Empty?<br/><b>AutoNom>Diamond</b>"
        _widget.setHtml(_text)
        if o_step1_handler.is_diamond_text_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(0, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step1_handler.is_diamond_text_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step1_diamond)
        self.parent.ui.table_status.setCellWidget(0, 1, _widget_2)

        # diamond background
        self.parent.ui.table_status.insertRow(1)
        self.parent.ui.table_status.setRowHeight(1, self.row_height)
        _widget = QTextEdit()
        _text = "Diamond Background Field Empty?<br/><b>AutoNom>Diamond Background</b>"
        _widget.setHtml(_text)
        if o_step1_handler.is_diamond_background_text_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(1, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step1_handler.is_diamond_background_text_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step1_diamond_background)
        self.parent.ui.table_status.setCellWidget(1, 1, _widget_2)

        # vanadium
        self.parent.ui.table_status.insertRow(2)
        self.parent.ui.table_status.setRowHeight(2, self.row_height)
        _widget = QTextEdit()
        _text = "Vanadium Field Empty?<br/><b>AutoNom>Vanadium</b>"
        _widget.setHtml(_text)
        if o_step1_handler.is_vanadium_text_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(2, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step1_handler.is_vanadium_text_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step1_vanadium)
        self.parent.ui.table_status.setCellWidget(2, 1, _widget_2)

        # vanadium background
        self.parent.ui.table_status.insertRow(3)
        self.parent.ui.table_status.setRowHeight(3, self.row_height)
        _widget = QTextEdit()
        _text = "Vanadium Background Field Empty?<br/><b>AutoNom>Vanadium Background</b>"
        _widget.setHtml(_text)
        if o_step1_handler.is_vanadium_background_text_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(3, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step1_handler.is_vanadium_background_text_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step1_vanadium_background)
        self.parent.ui.table_status.setCellWidget(3, 1, _widget_2)

        # sample background
        self.parent.ui.table_status.insertRow(4)
        self.parent.ui.table_status.setRowHeight(4, self.row_height)
        _widget = QTextEdit()
        _text = "Sample Background Field Empty?<br/><b>AutoNom>Sample Background</b>"
        _widget.setHtml(_text)
        if o_step1_handler.is_sample_background_text_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(4, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step1_handler.is_sample_background_text_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step1_sample_background)
        self.parent.ui.table_status.setCellWidget(4, 1, _widget_2)

        # create folder button
        self.parent.ui.table_status.insertRow(5)
        self.parent.ui.table_status.setRowHeight(5, self.row_height + 20)
        _widget = QTextEdit()
        _text = "Create Folder Button Status?<br/><b>AutoNom>Create New AutoNom Folder</b>"
        _widget.setHtml(_text)
        if o_step1_handler.is_create_folder_button_status_ok():
            _widget.setStyleSheet(self.widget_ok)
        else:
            _widget.setStyleSheet(self.widget_bad)
        self.parent.ui.table_status.setCellWidget(5, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(not o_step1_handler.is_create_folder_button_status_ok())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step1_create_folder)
        self.parent.ui.table_status.setCellWidget(5, 1, _widget_2)

    # STEP 2

    def jump_to_step2_table(self):
        self.ui.tabWidget_2.setCurrentIndex(1)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.table.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step2_fourier_from(self):
        self.ui.tabWidget_2.setCurrentIndex(1)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.fourier_filter_from.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step2_fourier_to(self):
        self.ui.tabWidget_2.setCurrentIndex(1)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.fourier_filter_to.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step2_plazcek_from(self):
        self.ui.tabWidget_2.setCurrentIndex(1)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.plazcek_fit_range_min.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step2_plazcek_to(self):
        self.ui.tabWidget_2.setCurrentIndex(1)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.plazcek_fit_range_max.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step2_q_min(self):
        self.ui.tabWidget_2.setCurrentIndex(1)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.q_range_min.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step2_q_max(self):
        self.ui.tabWidget_2.setCurrentIndex(1)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.q_range_max.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step2_output_empty(self):
        self.ui.tabWidget_2.setCurrentIndex(1)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.run_ndabs_output_file_name.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step2_scans_output_file_name(self):
        self.ui.tabWidget_2.setCurrentIndex(1)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.sum_scans_output_file_name.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step2_mantid_browse_calibration(self):
        self.ui.tabWidget_2.setCurrentIndex(1)
        self.ui.tabWidget.setCurrentIndex(1)
        self.ui.mantid_browse_calibration_button.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step2_mantid_browse_characterization(self):
        self.ui.tabWidget_2.setCurrentIndex(1)
        self.ui.tabWidget.setCurrentIndex(1)
        self.ui.mantid_browse_characterization_button.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step2_mantid_number_of_bins(self):
        self.ui.tabWidget_2.setCurrentIndex(1)
        self.ui.tabWidget.setCurrentIndex(1)
        self.ui.mantid_number_of_bins.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step2_mantid_min_crop_wavelength(self):
        self.ui.tabWidget_2.setCurrentIndex(1)
        self.ui.tabWidget.setCurrentIndex(1)
        self.ui.mantid_min_crop_wavelength.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step2_mantid_max_crop_wavelength(self):
        self.ui.tabWidget_2.setCurrentIndex(1)
        self.ui.tabWidget.setCurrentIndex(1)
        self.ui.mantid_max_crop_wavelength.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step2_mantid_vanadium_radius(self):
        self.ui.tabWidget_2.setCurrentIndex(1)
        self.ui.tabWidget.setCurrentIndex(1)
        self.ui.mantid_vanadium_radius.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step2_mantid_output_directory_button(self):
        self.ui.tabWidget_2.setCurrentIndex(1)
        self.ui.tabWidget.setCurrentIndex(1)
        self.ui.mantid_output_directoy_button.setFocus()
        self.parent.parent.activateWindow()

    def fill_scans(self):
        o_step2_handler = Step2Utilities(parent=self.parent.parent)

        # table status
        self.parent.ui.table_status.insertRow(0)
        self.parent.ui.table_status.setRowHeight(0, self.row_height)
        _widget = QTextEdit()
        _text = "Main Table Empty?<br/><b>Post Processing>Table</b>"
        _widget.setHtml(_text)
        if o_step2_handler.is_table_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(0, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step2_handler.is_table_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_table)
        self.parent.ui.table_status.setCellWidget(0, 1, _widget_2)

        # at least one row checked
        self.parent.ui.table_status.insertRow(1)
        self.parent.ui.table_status.setRowHeight(1, self.row_height)
        _widget = QTextEdit()
        _text = "Main Table Row Selected?<br/><b>Post Processing>Table</b>"
        _widget.setHtml(_text)
        if o_step2_handler.at_least_one_row_checked():
            _widget.setStyleSheet(self.widget_ok)
        else:
            _widget.setStyleSheet(self.widget_bad)
        self.parent.ui.table_status.setCellWidget(1, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(not o_step2_handler.at_least_one_row_checked())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_table)
        self.parent.ui.table_status.setCellWidget(1, 1, _widget_2)

        # output file name
        self.parent.ui.table_status.insertRow(2)
        self.parent.ui.table_status.setRowHeight(2, self.row_height)
        _widget = QTextEdit()
        _text = "Output File Name?<br/><b>Post Processing>Output File Name</b>"
        _widget.setHtml(_text)
        if not o_step2_handler.is_scans_output_file_name_empty():
            _widget.setStyleSheet(self.widget_ok)
        else:
            _widget.setStyleSheet(self.widget_bad)
        self.parent.ui.table_status.setCellWidget(2, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step2_handler.is_scans_output_file_name_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_scans_output_file_name)
        self.parent.ui.table_status.setCellWidget(2, 1, _widget_2)

    def fill_ndabs(self):
        o_step2_handler = Step2Utilities(parent=self.parent.parent)

        # table status
        self.parent.ui.table_status.insertRow(0)
        self.parent.ui.table_status.setRowHeight(0, self.row_height)
        _widget = QTextEdit()
        _text = "Main Table Empty?<br/><b>Post Processing>Table</b>"
        _widget.setHtml(_text)
        if o_step2_handler.is_table_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(0, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step2_handler.is_table_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_table)
        self.parent.ui.table_status.setCellWidget(0, 1, _widget_2)

        # at least one row checked
        self.parent.ui.table_status.insertRow(1)
        self.parent.ui.table_status.setRowHeight(1, self.row_height)
        _widget = QTextEdit()
        _text = "Main Table Row Selected?<br/><b>Post Processing>Table</b>"
        _widget.setHtml(_text)
        if o_step2_handler.at_least_one_row_checked():
            _widget.setStyleSheet(self.widget_ok)
        else:
            _widget.setStyleSheet(self.widget_bad)
        self.parent.ui.table_status.setCellWidget(1, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(not o_step2_handler.at_least_one_row_checked())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_table)
        self.parent.ui.table_status.setCellWidget(1, 1, _widget_2)

        # missing fields in row checked
        self.parent.ui.table_status.insertRow(2)
        self.parent.ui.table_status.setRowHeight(2, self.row_height)
        _widget = QTextEdit()
        _text = "Is missing metadata in row checked?<br/><b>Post Processing>Table</b>"
        _widget.setHtml(_text)
        if o_step2_handler.are_row_checked_have_missing_fields():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(2, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step2_handler.are_row_checked_have_missing_fields())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_table)
        self.parent.ui.table_status.setCellWidget(2, 1, _widget_2)

        # fourier filter from
        self.parent.ui.table_status.insertRow(3)
        self.parent.ui.table_status.setRowHeight(3, self.row_height)
        _widget = QTextEdit()
        _text = "Is Fourier From Widgets Empty?<br/><b>Post Processing>Fourier Filter From</b>"
        _widget.setHtml(_text)
        if o_step2_handler.is_fourier_filter_from_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(3, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step2_handler.is_fourier_filter_from_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_fourier_from)
        self.parent.ui.table_status.setCellWidget(3, 1, _widget_2)

        # fourier filter to
        self.parent.ui.table_status.insertRow(4)
        self.parent.ui.table_status.setRowHeight(4, self.row_height)
        _widget = QTextEdit()
        _text = "Is Fourier To Widgets Empty?<br/><b>Post Processing>Fourier Filter To</b>"
        _widget.setHtml(_text)
        if o_step2_handler.is_fourier_filter_to_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(4, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step2_handler.is_fourier_filter_to_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_fourier_to)
        self.parent.ui.table_status.setCellWidget(4, 1, _widget_2)

        # plazcek filter from
        self.parent.ui.table_status.insertRow(5)
        self.parent.ui.table_status.setRowHeight(5, self.row_height)
        _widget = QTextEdit()
        _text = "Is Plazcek From Widgets Empty?<br/><b>Post Processing>Plazcek Filter From</b>"
        _widget.setHtml(_text)
        if o_step2_handler.is_plazcek_from_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(5, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step2_handler.is_plazcek_from_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_plazcek_from)
        self.parent.ui.table_status.setCellWidget(5, 1, _widget_2)

        #  plazcek filter to
        self.parent.ui.table_status.insertRow(6)
        self.parent.ui.table_status.setRowHeight(6, self.row_height)
        _widget = QTextEdit()
        _text = "Is Plazcek To Widgets Empty?<br/><b>Post Processing>Plazcek Filter To</b>"
        _widget.setHtml(_text)
        if o_step2_handler.is_plazcek_to_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(6, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step2_handler.is_plazcek_to_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_plazcek_to)
        self.parent.ui.table_status.setCellWidget(6, 1, _widget_2)

        # q min
        self.parent.ui.table_status.insertRow(7)
        self.parent.ui.table_status.setRowHeight(7, self.row_height)
        _widget = QTextEdit()
        _text = "Is Q min Widgets Empty?<br/><b>Post Processing>Q min</b>"
        _widget.setHtml(_text)
        if o_step2_handler.is_q_min_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(7, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step2_handler.is_q_min_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_q_min)
        self.parent.ui.table_status.setCellWidget(7, 1, _widget_2)

        #  q max
        self.parent.ui.table_status.insertRow(8)
        self.parent.ui.table_status.setRowHeight(8, self.row_height)
        _widget = QTextEdit()
        _text = "Is Q max Widgets Empty?<br/><b>Post Processing>Q max</b>"
        _widget.setHtml(_text)
        if o_step2_handler.is_q_max_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(8, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step2_handler.is_q_max_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_q_max)
        self.parent.ui.table_status.setCellWidget(8, 1, _widget_2)

        #  output file name
        self.parent.ui.table_status.insertRow(9)
        self.parent.ui.table_status.setRowHeight(9, self.row_height)
        _widget = QTextEdit()
        _text = "Is Output File Name Empty?<br/><b>Post Processing>Output File Name</b>"
        _widget.setHtml(_text)
        if o_step2_handler.is_ndabs_output_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(9, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step2_handler.is_ndabs_output_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_output_empty)
        self.parent.ui.table_status.setCellWidget(9, 1, _widget_2)

    def fill_mantid(self):
        self.row_height = 62

        o_step1_handler = Step1Utilities(main_window=self.parent.parent)
        o_step2_handler = Step2Utilities(parent=self.parent.parent)

        # vanadium
        _row = 0
        self.parent.ui.table_status.insertRow(_row)
        self.parent.ui.table_status.setRowHeight(_row, self.row_height)
        _widget = QTextEdit()
        _text = "Vanadium Field Empty?<br/><b>AutoNom>Vanadium</b>"
        _widget.setHtml(_text)
        if o_step1_handler.is_vanadium_text_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(_row, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step1_handler.is_vanadium_text_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step1_vanadium)
        self.parent.ui.table_status.setCellWidget(_row, 1, _widget_2)

        # vanadium background
        _row = 1
        self.parent.ui.table_status.insertRow(_row)
        self.parent.ui.table_status.setRowHeight(_row, self.row_height)
        _widget = QTextEdit()
        _text = "Vanadium Background Field Empty?<br/><b>AutoNom>Vanadium Background</b>"
        _widget.setHtml(_text)
        if o_step1_handler.is_vanadium_background_text_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(_row, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step1_handler.is_vanadium_background_text_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step1_vanadium_background)
        self.parent.ui.table_status.setCellWidget(_row, 1, _widget_2)

        # table status
        _row = 2
        self.parent.ui.table_status.insertRow(_row)
        self.parent.ui.table_status.setRowHeight(_row, self.row_height)
        _widget = QTextEdit()
        _text = "Main Table Empty?<br/><b>Post Processing>Table</b>"
        _widget.setHtml(_text)
        if o_step2_handler.is_table_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(_row, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step2_handler.is_table_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_table)
        self.parent.ui.table_status.setCellWidget(_row, 1, _widget_2)

        # at least one row checked
        _row = 3
        self.parent.ui.table_status.insertRow(_row)
        self.parent.ui.table_status.setRowHeight(_row, self.row_height)
        _widget = QTextEdit()
        _text = "Main Table Row Selected?<br/><b>Post Processing>Table</b>"
        _widget.setHtml(_text)
        if o_step2_handler.at_least_one_row_checked():
            _widget.setStyleSheet(self.widget_ok)
        else:
            _widget.setStyleSheet(self.widget_bad)
        self.parent.ui.table_status.setCellWidget(_row, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(not o_step2_handler.at_least_one_row_checked())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_table)
        self.parent.ui.table_status.setCellWidget(_row, 1, _widget_2)

        # calibration
        _row = 4
        self.parent.ui.table_status.insertRow(_row)
        self.parent.ui.table_status.setRowHeight(_row, self.row_height)
        _widget = QTextEdit()
        _text = "Calibration File Selected?<br/><b>Post Processing>Rietveld>Calibration</b>"
        _widget.setHtml(_text)
        if o_step2_handler.is_mantid_calibration_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(_row, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step2_handler.is_mantid_calibration_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_mantid_browse_calibration)
        self.parent.ui.table_status.setCellWidget(_row, 1, _widget_2)

        # characterization
        _row += 1
        self.parent.ui.table_status.insertRow(_row)
        self.parent.ui.table_status.setRowHeight(_row, self.row_height)
        _widget = QTextEdit()
        _text = "Characterization File Selected?<br/><b>Post Processing>Rietveld>Characterization</b>"
        _widget.setHtml(_text)
        if o_step2_handler.is_mantid_characterization_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(_row, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step2_handler.is_mantid_characterization_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_mantid_browse_characterization)
        self.parent.ui.table_status.setCellWidget(_row, 1, _widget_2)

        # number of bins int
        _row += 1
        self.parent.ui.table_status.insertRow(_row)
        self.parent.ui.table_status.setRowHeight(_row, self.row_height)
        _widget = QTextEdit()
        _text = "Is Number of Bins an Int?<br/><b>Post Processing>Rietveld>Number of Bins</b>"
        _widget.setHtml(_text)
        if o_step2_handler.is_mantid_number_of_bins_no_int():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(_row, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step2_handler.is_mantid_number_of_bins_no_int())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_mantid_number_of_bins)
        self.parent.ui.table_status.setCellWidget(_row, 1, _widget_2)

        # min crop wavelegenth
        _row += 1
        self.parent.ui.table_status.insertRow(_row)
        self.parent.ui.table_status.setRowHeight(_row, self.row_height)
        _widget = QTextEdit()
        _text = "Is min Crop Wavelength a float?<br/><b>Post Processing>Rietveld>Crop Wavelength Min</b>"
        _widget.setHtml(_text)
        if o_step2_handler.is_mantid_min_crop_wavelength_no_float():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(_row, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step2_handler.is_mantid_min_crop_wavelength_no_float())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_mantid_min_crop_wavelength)
        self.parent.ui.table_status.setCellWidget(_row, 1, _widget_2)

        # max crop wavelegenth
        _row += 1
        self.parent.ui.table_status.insertRow(_row)
        self.parent.ui.table_status.setRowHeight(_row, self.row_height)
        _widget = QTextEdit()
        _text = "Is max Crop Wavelength a float?<br/><b>Post Processing>Rietveld>Crop Wavelength Max</b>"
        _widget.setHtml(_text)
        if o_step2_handler.is_mantid_max_crop_wavelength_no_float():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(_row, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step2_handler.is_mantid_max_crop_wavelength_no_float())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_mantid_max_crop_wavelength)
        self.parent.ui.table_status.setCellWidget(_row, 1, _widget_2)

        # vanadium radius
        _row += 1
        self.parent.ui.table_status.insertRow(_row)
        self.parent.ui.table_status.setRowHeight(_row, self.row_height)
        _widget = QTextEdit()
        _text = "Is Vanadium Radius a float?<br/><b>Post Processing>Rietveld>Vanadium Radius</b>"
        _widget.setHtml(_text)
        if o_step2_handler.is_mantid_vanadium_radius_not_float():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(_row, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step2_handler.is_mantid_vanadium_radius_not_float())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_mantid_vanadium_radius)
        self.parent.ui.table_status.setCellWidget(_row, 1, _widget_2)

        # output directory
        _row += 1
        self.parent.ui.table_status.insertRow(_row)
        self.parent.ui.table_status.setRowHeight(_row, self.row_height)
        _widget = QTextEdit()
        _text = "Is Output Directory Empty?<br/><b>Post Processing>Rietveld>Output Directory</b>"
        _widget.setHtml(_text)
        if o_step2_handler.is_mantid_output_directory_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(_row, 0, _widget)
        _widget_2 = QPushButton()
        _widget_2.setEnabled(o_step2_handler.is_mantid_output_directory_empty())
        _widget_2.setText(self.jump_message)
        _widget_2.clicked.connect(self.jump_to_step2_mantid_output_directory_button)
        self.parent.ui.table_status.setCellWidget(_row, 1, _widget_2)
