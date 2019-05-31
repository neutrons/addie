from __future__ import (absolute_import, division, print_function)
import os
from qtpy import QtGui, QtCore

from addie.utilities.file_handler import FileHandler


class ImportTable(object):

    file_contain = []
    table_contain = []
    contain_parsed = []
    full_contain_parsed = []

    def __init__(self, parent=None, filename=''):
        self.parent = parent
        self.filename = filename

    def run(self):
        self.load_ascii()
        self.parse_contain()
        self.change_path()
        self.populate_gui()

    def load_ascii(self):
        _filename = self.filename
        o_file = FileHandler(filename = _filename)
        o_file.retrieve_contain()
        self.file_contain = o_file.file_contain

    def parse_config_table(self):
        self._list_row = eval(self.table_contain)
        self.parser()

    def parse_contain(self):
        _contain = self.file_contain
        self._list_row = _contain.split("\n")
        self.parser()

    def parser(self):

        _list_row = self._list_row
        _contain_parsed = []
        for _row in _list_row:
            _row_split = _row.split('|')
            _contain_parsed.append(_row_split)

        self.contain_parsed = _contain_parsed[2:]
        self.full_contain_parsed = _contain_parsed

    def change_path(self):
        full_contain_parsed = self.full_contain_parsed

        try:
            _path_string_list = full_contain_parsed[0][0].split(':')
            self.parent.current_folder = _path_string_list[1].strip()
            os.chdir(self.parent.current_folder)
        except:
            pass

    def populate_gui(self):
        _contain_parsed = self.contain_parsed
        for _row, _entry in enumerate(_contain_parsed):

            if _entry == ['']:
                continue

            self.parent.ui.table.insertRow(_row)

            #select
            _layout = QtGui.QHBoxLayout()
            _widget = QtGui.QCheckBox()
            _widget.setEnabled(True)
            _layout.addWidget(_widget)
            _layout.addStretch()
            _new_widget = QtGui.QWidget()
            _new_widget.setLayout(_layout)

            #if _entry[0] == "True":
             #   _widget.setChecked(True)
            _widget.stateChanged.connect(lambda state = 0,
                                         row = _row: self.parent.table_select_state_changed(state, row))
            self.parent.ui.table.setCellWidget(_row, 0, _new_widget)

            #name
            _item = QtGui.QTableWidgetItem(_entry[1])
            self.parent.ui.table.setItem(_row, 1, _item)

            #runs
            _item = QtGui.QTableWidgetItem(_entry[2])
            self.parent.ui.table.setItem(_row, 2, _item)

            #Sample formula
            if _entry[3]:
                _item = QtGui.QTableWidgetItem(_entry[3])
            else:
                _item = QtGui.QTableWidgetItem("")
            self.parent.ui.table.setItem(_row, 3, _item)

            #mass density
            if _entry[4]:
                _item = QtGui.QTableWidgetItem(_entry[4])
            else:
                _item = QtGui.QTableWidgetItem("")
            self.parent.ui.table.setItem(_row, 4, _item)

            #radius
            if _entry[5]:
                _item = QtGui.QTableWidgetItem(_entry[5])
            else:
                _item = QtGui.QTableWidgetItem("")
            self.parent.ui.table.setItem(_row, 5, _item)

            #packing fraction
            if _entry[6]:
                _item = QtGui.QTableWidgetItem(_entry[6])
            else:
                _item = QtGui.QTableWidgetItem("")
            self.parent.ui.table.setItem(_row, 6, _item)

            #sample shape
            _widget = QtGui.QComboBox()
            _widget.addItem("Cylinder")
            _widget.addItem("Sphere")
            if _entry[7] == "Sphere":
                _widget.setCurrentIndex(1)
            self.parent.ui.table.setCellWidget(_row, 7, _widget)

            #do abs corr
            _layout = QtGui.QHBoxLayout()
            _widget = QtGui.QCheckBox()
            if _entry[8] == "True":
                _widget.setCheckState(QtCore.Qt.Checked)
            _widget.setStyleSheet("border:  2px; solid-black")
            _widget.setEnabled(True)
            _layout.addStretch()
            _layout.addWidget(_widget)
            _layout.addStretch()
            _new_widget = QtGui.QWidget()
            _new_widget.setLayout(_layout)
            self.parent.ui.table.setCellWidget(_row, 8, _new_widget)

        for _row, _entry in enumerate(_contain_parsed):

            if _entry == ['']:
                continue

            #select
            _widget = self.parent.ui.table.cellWidget(_row, 0).children()[1]
            if _entry[0] == "True":
                _widget.setChecked(True)
