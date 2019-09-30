from __future__ import (absolute_import, division, print_function)
import os
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (QCheckBox, QComboBox, QHBoxLayout, QMessageBox, QTableWidgetItem, QWidget)

from addie.processing.idl.generate_sumthing import GenerateSumthing


class PopulateMasterTable(object):

    auto_sum_ini_file = 'auto_sum.inp'
    error_reported = False

    def __init__(self, main_window=None):
        self.parent = main_window

    def run(self):

        try:
            o_generate = GenerateSumthing(parent=self.parent,
                                          folder=self.parent.current_folder)
            o_generate.create_sum_inp_file()

            self.read_auto_sum_file()
            self.populate_table()
        except IOError:
            QMessageBox.warning(self.parent, "File does not exist!", "Check your folder!         ")
            self.error_reported = True

    def empty_metadata(self):
        _metadata = {'name': "",
                     'runs': "",
                     'sample_formula': "",
                     'mass_density': "",
                     'radius': "",
                     'packing_fraction': "",
                     'sample_shape': "",
                     'do_abs_correction': ""}
        return _metadata

    def read_auto_sum_file(self):

        _full_auto_sum_file_name = os.path.join(self.parent.current_folder, self.auto_sum_ini_file)
        f = open(_full_auto_sum_file_name, 'r')
        _data = f.read()
        f.close()

        _data_table = _data.split("\n")

        # remove first line (background)
        self._data_from_file = _data_table[1:]

        print("[LOG] Reading auto_sum_file (%s)" % _full_auto_sum_file_name)
        print("[LOG] _data_table: ", _data_table)

    def populate_table(self):
        '''
        In this new version, the table will append the new entries
        '''

        #o_table = addie.processing_idl.table_handler.TableHandler(parent = self.parent)
        # o_table._clear_table()

        # disable sorting
        self.parent.postprocessing_ui.table.setSortingEnabled(False)

        _index = 0
        _columns_runs = self.get_columns_value(column=2)

        for _entry in self._data_from_file:
            if _entry.strip() == "":
                continue
            name_value = _entry.split(" ")

            [name, value] = name_value
            _metadata = self.empty_metadata()
            _metadata['name'] = name
            _metadata['runs'] = value

            if self.runs_already_in_table(runs=value, table_runs=_columns_runs):
                _index += 1
                continue

            self.add_new_row(_metadata, row=_index)
            _index += 1

        self.parent.postprocessing_ui.table.setSortingEnabled(True)

    def get_columns_value(self, column=2):
        column_values = []
        nbr_row = self.parent.postprocessing_ui.table.rowCount()
        for _row in range(nbr_row):
            _value = str(self.parent.postprocessing_ui.table.item(_row, column).text())
            column_values.append(_value)
        return column_values

    def runs_already_in_table(self, runs='', table_runs=[]):
        if runs in table_runs:
            return True
        return False

    def add_new_row(self, _metadata, row=0):

        self.parent.postprocessing_ui.table.insertRow(row)

        _layout = QHBoxLayout()
        _widget = QCheckBox()
        _widget.setEnabled(True)
        _layout.addWidget(_widget)
        _layout.addStretch()
        _new_widget = QWidget()
        _new_widget.setLayout(_layout)

        _widget.stateChanged.connect(lambda state=0, row=row:
                                     self.parent.table_select_state_changed(state, row))
        self.parent.postprocessing_ui.table.setCellWidget(row, 0, _new_widget)

        _item = QTableWidgetItem(_metadata['name'])
        self.parent.postprocessing_ui.table.setItem(row, 1, _item)

        _item = QTableWidgetItem(_metadata['runs'])
        self.parent.postprocessing_ui.table.setItem(row, 2, _item)

        if not _metadata['sample_formula']:
            _item = QTableWidgetItem(_metadata['sample_formula'])
            self.parent.postprocessing_ui.table.setItem(row, 3, _item)

        if not _metadata['mass_density']:
            _item = QTableWidgetItem(_metadata['mass_density'])
            self.parent.postprocessing_ui.table.setItem(row, 4, _item)

        if not _metadata['radius']:
            _item = QTableWidgetItem(_metadata['radius'])
            self.parent.postprocessing_ui.table.setItem(row, 5, _item)

        if not _metadata['packing_fraction']:
            _item = QTableWidgetItem(_metadata['packing_fraction'])
            self.parent.postprocessing_ui.table.setItem(row, 6, _item)

        _widget = QComboBox()
        _widget.addItem("Cylinder")
        _widget.addItem("Sphere")
        if _metadata['sample_shape'] == 'Sphere':
            _widget.setCurrentIndex(1)
        self.parent.postprocessing_ui.table.setCellWidget(row, 7, _widget)

        _layout = QHBoxLayout()
        _widget = QCheckBox()
        if _metadata['do_abs_correction'] == 'go':
            _widget.setCheckState(Qt.Checked)
        _widget.setStyleSheet("border:  2px; solid-black")
        _widget.setEnabled(True)
        _layout.addStretch()
        _layout.addWidget(_widget)
        _layout.addStretch()
        _new_widget = QWidget()
        _new_widget.setLayout(_layout)
        self.parent.postprocessing_ui.table.setCellWidget(row, 8, _new_widget)
