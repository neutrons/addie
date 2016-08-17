from PyQt4 import QtGui, QtCore
from fastgr.utilities.file_handler import FileHandler


class ImportTable(object):
    
    file_contain = []
    contain_parsed = []
    
    def __init__(self, parent=None, filename=''):
        self.parent = parent
        self.filename = filename
        
    def run(self):
        self.load_ascii()
        self.parse_contain()
        self.populate_gui()
    
    def load_ascii(self):
        _filename = self.filename
        o_file = FileHandler(filename = _filename)
        o_file.retrieve_contain()
        self.file_contain = o_file.file_contain
        
    def parse_contain(self):
        _contain = self.file_contain
        _list_row = _contain.split("\n")

        _contain_parsed = []
        for _row in _list_row:
            _row_split = _row.split('|')
            _contain_parsed.append(_row_split)
            
        self.contain_parsed = _contain_parsed[1:]
        
    def populate_gui(self):
        _contain_parsed = self.contain_parsed
        for _row, _entry in enumerate(_contain_parsed):
            
            print(_entry)
            if _entry == ['']:
                continue
            
            self.parent.ui.table.insertRow(_row)
                        
            #name
            _item = QtGui.QTableWidgetItem(_entry[1])
            self.parent.ui.table.setItem(_row, 1, _item)
            
            #runs
            _item = QtGui.QTableWidgetItem(_entry[2])
            self.parent.ui.table.setItem(_row, 2, _item)
            
            #Sample formula
            if not _entry[3]:
                _item = QtGui.QTableWidgetItem(_entry[3])
                self.parent.ui.table.setItem(_row, 3, _item)
                
            #mass density
            if not _entry[4]:
                _item = QtGui.QTableWidgetItem(_entry[4])
                self.parent.ui.table.setItem(_row, 4, _item)
                
            #radius
            if not _entry[5]:
                _item = QtGui.QTableWidgetItem(_entry[5])
                self.parent.ui.table.setItem(_row, 5, _item)
                
            #packing fraction
            if not _entry[6]:
                _item = QtGui.QTableWidgetItem(_entry[6])
                self.parent.ui.table.setItem(_row, 6, _item)
                
            #sample shape
            _widget = QtGui.QComboBox()
            _widget.addItem("cylindrical")
            _widget.addItem("spherical")
            if _entry[7] == "spherical":
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

            #select
            _widget = QtGui.QCheckBox()
            _widget.setEnabled(True)
            if _entry[0] == "True":
                _widget.setChecked(True)
            QtCore.QObject.connect(_widget, QtCore.SIGNAL("stateChanged(int)"), lambda state = 0,
                                   row = _row: self.parent.table_select_state_changed(state, row))
            self.parent.ui.table.setCellWidget(_row, 0, _widget)
                
        