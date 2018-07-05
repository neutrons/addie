from PyQt4 import QtGui, QtCore
import datetime
from collections import namedtuple
import numpy as np
import os
import json
import re

from addie.ui_make_calibration import Ui_MainWindow as UiMainWindow
from addie.utilities.gui_handler import TableHandler


class MakeCalibrationLauncher(object):

    def __init__(self, parent=None):
        self.parent = parent

        if self.parent.make_calibration_ui is None:
            _make = MakeCalibrationWindow(parent=self.parent)
            _make.show()
            self.parent.make_calibration_ui = _make
        else:
            self.parent.make_calibration_ui.setFocus()
            self.parent.make_calibration_ui.activateWindow()


class MakeCalibrationWindow(QtGui.QMainWindow):

    table_column_width = [60, 250, 350, 350, 90, 300]
    table_row_height = 85
    entry_level =  0

    master_date = None  #QtCore.QDate()
    master_folder = 'N/A'

    addie_config_file = "addie/config.json"

    # will keep record of all the ui
    local_list_ui = namedtuple("local_list_ui", ["sample_environment_value",
                                                 "calibration_value",
                                                 "calibration_browser",
                                                 "calibration_browser_value",
                                                 "vanadium_value",
                                                 "vanadium_browser",
                                                 "vanadium_browser_value",
                                                 "date",
                                                 "output_dir_browser",
                                                 "output_dir_value",
                                                 "output_reset"])

    master_list_ui = {}
    master_list_value = {}

    def __init__(self, parent=None):
        self.parent = parent

        QtGui.QMainWindow.__init__(self, parent=parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

        self.init_widgets()
        self.init_date()
        self.update_add_remove_widgets()

    def init_date(self):
        """will initialize the master date using today's date"""
        now = datetime.datetime.now()
        day = now.day
        month = now.month
        year = now.year
        today = QtCore.QDate(year, month, day)
        self.master_date = today
        self.ui.master_date.setDate(today)

    def init_widgets(self):
        for index_col, col_size in enumerate(self.table_column_width):
            self.ui.tableWidget.setColumnWidth(index_col, col_size)

        # list of sample environment
        config_file = self.addie_config_file
        with open(config_file) as f:
            data = json.load(f)
        list_environment = data['sample_environment']
        self.ui.sample_environment_combobox.addItems(list_environment)

    def get_master_list_sample_environment(self):
        nbr_entry = self.ui.sample_environment_combobox.count()
        list_entry = []
        for _row in np.arange(nbr_entry):
            list_entry.append(str(self.ui.sample_environment_combobox.itemText(_row)))
        return list_entry

    def update_add_remove_widgets(self):
        nbr_row = self.ui.tableWidget.rowCount()
        if nbr_row > 0:
            _status = True
        else:
            _status = False
        self.ui.remove_row_button.setEnabled(_status)
        self.check_run_calibration_status()

    def master_browse_button_clicked(self):
        _master_folder = QtGui.QFileDialog.getExistingDirectory(caption="Select Output Folder ...",
                                                                directory=self.parent.output_folder,
                                                                options=QtGui.QFileDialog.ShowDirsOnly)
        if _master_folder:
            self.ui.master_output_directory_label.setText(str(_master_folder))
            self.master_folder = _master_folder
            self.check_run_calibration_status()

    def remove_row_button_clicked(self):
        o_gui = TableHandler(table_ui=self.ui.tableWidget)
        row_selected = o_gui.get_current_row()

        # no row selected
        if row_selected == -1:
            return

        entry = str(self.ui.tableWidget.item(row_selected, 0).text())
        self.ui.tableWidget.removeRow(row_selected)
        # remove list of ui from this row
        del self.master_list_ui[entry]
        self.update_add_remove_widgets()

    def add_row_button_clicked(self):
        o_gui = TableHandler(table_ui=self.ui.tableWidget)
        row_selected = o_gui.get_current_row()
        self.__insert_new_row(row=row_selected+1)
        self.update_add_remove_widgets()

    def _general_browser_clicked(self,
                                 sample_type='',
                                 value_ui=None):
        _file = QtGui.QFileDialog.getOpenFileName(parent=self,
                                                  caption="Select {} File ...".format(sample_type),
                                                  directory=self.master_folder,
                                                  filter="NeXus (*.nxs*);; All (*.*)")
        if _file:
            # display base name of file selected (without path)
            value_ui.setText(os.path.basename(_file))
            # find run number
            base_nexus = os.path.basename(_file)
            run_number = self.get_run_number_from_nexus_file_name(base_nexus_name=base_nexus)
            return [_file, run_number]

    def run_entered(self, entry=""):
        self.check_run_calibration_status()

    def get_run_number_from_nexus_file_name(self, base_nexus_name=''):
        if base_nexus_name == '':
            return None

        #nxs_ext = '.nxs'
        h5_ext = '.h5'

        [base_file_name, ext] = os.path.splitext(base_nexus_name)
        if ext == h5_ext:
            [base_file_name, _] = os.path.splitext(base_file_name)

        nexus_regex = re.compile("\w+_(\d+)")
        result = nexus_regex.match(base_file_name)
        if result:
            return result.group(1)
        return NoNe

    def vanadium_browser_clicked(self, entry=""):
        sample_type = "Vanadium"
        value_ui = self.master_list_ui[entry].vanadium_browser_value

        [_file, run_number] = self._general_browser_clicked(sample_type=sample_type,
                                                            value_ui=value_ui)
        if _file:
            self.master_list_value[entry]["vanadium_browser"] = _file
            self.master_list_ui[entry].vanadium_value.setText(str(run_number))
            self.check_run_calibration_status()

    def calibration_browser_clicked(self, entry=""):
        sample_type = "Calibration"
        value_ui = self.master_list_ui[entry].calibration_browser_value

        [_file, run_number] = self._general_browser_clicked(sample_type=sample_type,
                                                            value_ui=value_ui)
        if _file:
            self.master_list_value[entry]["calibration_browser"] = _file
            self.master_list_ui[entry].calibration_value.setText(str(run_number))
            self.check_run_calibration_status()

    def local_output_dir_clicked(self, entry=""):
        _local_folder = QtGui.QFileDialog.getExistingDirectory(caption="Select Output Folder ...",
                                                                directory=self.master_folder,
                                                                options=QtGui.QFileDialog.ShowDirsOnly)
        if _local_folder:
            _master_list_ui = self.master_list_ui[entry]
            _local_label = _master_list_ui.output_dir_value
            _local_label.setText(str(_local_folder))
            self.check_run_calibration_status()

    def local_reset_dir_clicked(self, entry=""):
        _master_list_ui = self.master_list_ui[entry]
        _local_label = _master_list_ui.output_dir_value
        _local_label.setText(str(self.master_folder))
        self.check_run_calibration_status()

    ## helper functions

    def __insert_new_row(self, row=-1):
        self.ui.tableWidget.insertRow(row)
        self.ui.tableWidget.setRowHeight(row, self.table_row_height)

        button_width = 80

        new_entry_level = self.entry_level + 1
        self.entry_level = new_entry_level

        #column0 - entry
        col=0
        _name = str(new_entry_level)
        item = QtGui.QTableWidgetItem(str(_name))
        self.ui.tableWidget.setItem(row, col, item)

        #new column - sample environment
        col = 1
        sample_combobox = QtGui.QComboBox()
        sample_combobox.setEditable(True)
        sample_combobox.setMaximumHeight(40)
        master_list_sample_environment = self.get_master_list_sample_environment()
        sample_combobox.addItems(master_list_sample_environment)
        master_list_sample_environment_index_selected = self.ui.sample_environment_combobox.currentIndex()
        sample_combobox.setCurrentIndex(master_list_sample_environment_index_selected)
        label = QtGui.QLabel("Select or Edit!")
        verti_layout = QtGui.QVBoxLayout()
        verti_layout.addWidget(sample_combobox)
        verti_layout.addWidget(label)
        widget = QtGui.QWidget()
        widget.setLayout(verti_layout)
        self.ui.tableWidget.setCellWidget(row, col, widget)

        # new column - calibration
        col = 2
        # first row
        label = QtGui.QLabel("Run #:")
        cali_value = QtGui.QLineEdit("")
        cali_value.returnPressed.connect(lambda entry=_name: self.run_entered(entry))
        cali_browser_button = QtGui.QPushButton("Browse...")
        cali_browser_button.setMinimumWidth(button_width)
        cali_browser_button.setMaximumWidth(button_width)
        cali_browser_button.clicked.connect(lambda state, entry=_name:  self.calibration_browser_clicked(entry))
        first_row = QtGui.QHBoxLayout()
        first_row.addWidget(label)
        first_row.addWidget(cali_value)
        first_row.addWidget(cali_browser_button)
        first_row_widget = QtGui.QWidget()
        first_row_widget.setLayout(first_row)
        # second row
        cali_browser_button_value = QtGui.QLabel("N/A")

        verti_layout = QtGui.QVBoxLayout()
        verti_layout.addWidget(first_row_widget)
        verti_layout.addWidget(cali_browser_button_value)
        col1_widget = QtGui.QWidget()
        col1_widget.setLayout(verti_layout)
        self.ui.tableWidget.setCellWidget(row, col, col1_widget)

        # new column - Vanadium
        col = 3
        # first row
        # first row
        label = QtGui.QLabel("Run #:")
        vana_value = QtGui.QLineEdit("")
        vana_value.returnPressed.connect(lambda entry=_name: self.run_entered(entry))
        vana_browser_button = QtGui.QPushButton("Browse...")
        vana_browser_button.setMinimumWidth(button_width)
        vana_browser_button.setMaximumWidth(button_width)
        vana_browser_button.clicked.connect(lambda state, entry=_name:  self.vanadium_browser_clicked(entry))
        first_row = QtGui.QHBoxLayout()
        first_row.addWidget(label)
        first_row.addWidget(vana_value)
        first_row.addWidget(vana_browser_button)
        first_row_widget = QtGui.QWidget()
        first_row_widget.setLayout(first_row)
        # second row
        vana_browser_button_value = QtGui.QLabel("N/A")

        verti_layout = QtGui.QVBoxLayout()
        verti_layout.addWidget(first_row_widget)
        verti_layout.addWidget(vana_browser_button_value)
        col1_widget = QtGui.QWidget()
        col1_widget.setLayout(verti_layout)
        self.ui.tableWidget.setCellWidget(row, col, col1_widget)

        # new column - date
        col = 4
        date = QtGui.QDateEdit()
        date.setDate(self.master_date)
        self.ui.tableWidget.setCellWidget(row, col, date)

        # new column - output dir
        col = 5
        browser_button = QtGui.QPushButton("Browse...")
        browser_button.setMinimumWidth(button_width)
        browser_button.setMaximumWidth(button_width)
        browser_button.clicked.connect(lambda state, entry=_name: self.local_output_dir_clicked(entry))
        browser_value = QtGui.QLabel(self.master_folder)
        reset = QtGui.QPushButton("Use Master")
        reset.setMinimumWidth(button_width)
        reset.setMaximumWidth(button_width)
        reset.clicked.connect(lambda state, entry=_name: self.local_reset_dir_clicked(entry))
        hori_layout = QtGui.QHBoxLayout()
        hori_layout.addWidget(browser_button)
        hori_layout.addWidget(browser_value)
        hori_layout.addWidget(reset)
        widget = QtGui.QWidget()
        widget.setLayout(hori_layout)
        self.ui.tableWidget.setCellWidget(row, col, widget)

        list_local_ui = self.local_list_ui(sample_environment_value=sample_combobox,
                                           calibration_value=cali_value,
                                           calibration_browser=cali_browser_button,
                                           calibration_browser_value=cali_browser_button_value,
                                           vanadium_value=vana_value,
                                           vanadium_browser=vana_browser_button,
                                           vanadium_browser_value=vana_browser_button_value,
                                           date=date,
                                           output_dir_browser=browser_button,
                                           output_dir_value=browser_value,
                                           output_reset=reset)
        self.master_list_ui[_name] = list_local_ui

        list_local_name = dict(vanadium_run_number="",
                               vanadium_browser="",
                               calibration_run_number="",
                               calibration_browser="")
        self.master_list_value[_name] = list_local_name

    def _check_local_column(self, run_value=None):
        _runs = str(run_value.text())
        if _runs.strip() == "":
            return False
        else:
            return True

    def _check_status_of_row(self, row=-1):
        _entry = str(self.ui.tableWidget.item(row, 0).text())
        local_list_ui = self.master_list_ui[_entry]

        # Calibration column
        if not self._check_local_column(run_value = local_list_ui.calibration_value):
            return False

        # Vanadium column
        if not self._check_local_column(run_value=local_list_ui.vanadium_value):
            return False

        # output dir
        browse_label = local_list_ui.output_dir_value
        if browse_label.text() == 'N/A':
            return False

        return True

    def _check_status_of_widgets(self):
        # table is empty
        nbr_row = self.ui.tableWidget.rowCount()
        if nbr_row == 0:
            return False

        for _row in np.arange(nbr_row):
            _status_row = self._check_status_of_row(row=_row)
            if _status_row:
                continue

            # if a row has missing infos, no need to continue
            return False

        return True

    def master_date_changed(self, datetime):
        self.master_date = datetime.date()

    def check_run_calibration_status(self):
        """Disable the Run Calibration button if any of the infos is missing"""
        _status = self._check_status_of_widgets()
        self.ui.run_calibration_button.setEnabled(_status)

    def run_calibration_button_clicked(self):
        print("running calibration")

    def closeEvent(self, c):
        self.parent.make_calibration_ui = None

