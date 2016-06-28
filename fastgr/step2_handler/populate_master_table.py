import os
from PyQt4 import QtGui, QtCore

from step2_handler.generate_sumthing import GenerateSumthing


class PopulateMasterTable(object):
    
    auto_sum_ini_file = 'auto_sum.inp'
             
    def __init__(self, parent=None):
        self.parent = parent
        
    def run(self):
        o_generate = GenerateSumthing(folder= self.parent.current_folder)
        o_generate.create_sum_inp_file()
        
        self.read_auto_sum_file()
        self.populate_table()
        
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
        
        #remove first line (background)
        self._data_from_file = _data_table[1:]

    def populate_table(self):
        
        _index = 0

        for _entry in self._data_from_file:
            if _entry.strip() == "":
                continue
            name_value = _entry.split(" ")

            [name, value] = name_value
            _metadata = self.empty_metadata()
            _metadata['name'] = name
            _metadata['runs'] = value
                
            self.add_new_row(_metadata, row=_index)
            _index += 1
                
    def add_new_row(self, _metadata, row=0):
        
        self.parent.table.insertRow(row)
        
        _widget = QtGui.QCheckBox()
        _widget.setEnabled(True)
        self.parent.table.setCellWidget(row, 0, _widget)
        
        _item = QtGui.QTableWidgetItem(_metadata['name'])
        self.parent.table.setItem(row, 1, _item)

        _item = QtGui.QTableWidgetItem(_metadata['runs'])
        self.parent.table.setItem(row, 2, _item)
        
        if not _metadata['sample_formula']:
            _item = QtGui.QTableWidgetItem(_metadata['sample_formula'])
            self.parent.table.setItem(row, 3, _item)
            
        if not _metadata['mass_density']:
            _item = QtGui.QTableWidgetItem(_metadata['mass_density'])
            self.parent.table.setItem(row, 4, _item)
            
        if not _metadata['radius']:
            _item = QtGui.QTableWidgetItem(_metadata['radius'])
            self.parent.table.setItem(row, 5, _item)
            
        if not _metadata['packing_fraction']:
            _item = QtGui.QTableWidgetItem(_metadata['packing_fraction'])
            self.parent.table.setItem(row, 6, _item)
        
        _widget = QtGui.QComboBox()
        _widget.addItem("cylindrical")
        _widget.addItem("spherical")
        if _metadata['sample_shape'] == 'spherical':
            _widget.setCurrentIndex(1)
        self.parent.table.setCellWidget(row, 7, _widget)
        
        _layout = QtGui.QHBoxLayout()
        _widget = QtGui.QCheckBox()
        if _metadata['do_abs_correction'] == 'go':
            _widget.setCheckState(QtCore.Qt.Checked)
        _widget.setStyleSheet("border:  2px; solid-black")
        _widget.setEnabled(True)
        _layout.addStretch()
        _layout.addWidget(_widget)
        _layout.addStretch()
        _new_widget = QtGui.QWidget()
        _new_widget.setLayout(_layout)
        self.parent.table.setCellWidget(row, 8, _new_widget)

