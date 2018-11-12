import numpy as np

try:
    from PyQt4.QtGui import QCheckBox, QSpacerItem, QSizePolicy, QTableWidgetItem
    from PyQt4 import QtCore, QtGui
except ImportError:
    try:
        from PyQt5.QtWidgets import QCheckBox, QSpacerItem, QSizePolicy, QTableWidgetItem
        from PyQt5 import QtCore, QtGui
    except ImportError:
        raise ImportError("Requires PyQt4 or PyQt5")


class TableRowHandler:

    def __init__(self, parent=None):
        self.parent = parent
        self.table_ui = self.parent.ui.h3_table

    def insert_blank_row(self):
        row = self._calculate_insert_row()
        self.insert_row(row=row)

    def sample_shape_changed(self, shape='Cylindrical'):
        pass

    def activated_row_changed(self, state=None):
        pass


    def insert_row(self, row=-1):
        self.table_ui.insertRow(row)

        # column 0 (active or not checkBox)
        _layout = QtGui.QHBoxLayout()
        _widget = QtGui.QCheckBox()
        _widget.setCheckState(QtCore.Qt.Checked)
        _widget.setEnabled(True)
        _spacer = QSpacerItem(40, 20,
                              QSizePolicy.Expanding,
                              QSizePolicy.Minimum)
        _layout.addItem(_spacer)
        _layout.addWidget(_widget)
        _layout.addItem(_spacer)
        _layout.addStretch()
        _new_widget = QtGui.QWidget()
        _new_widget.setLayout(_layout)
        QtCore.QObject.connect(_widget, QtCore.SIGNAL("stateChanged(int)"),
                               lambda state=0:
                               self.parent.master_table_select_state_changed(state))
        self.table_ui.setCellWidget(row, 0, _new_widget)

        # column 1 - title
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, 1, _item)

        # column 2 - sample runs
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, 2, _item)

        # column 3 - background runs
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, 3, _item)

        # column 4 - background background
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, 4, _item)

        # column 5 - material
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, 5, _item)

        # column 6 - packing fraction
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, 6, _item)

        # column 7 - shape (cylindrical or spherical)
        _widget = QtGui.QComboBox()
        _shape_default_value = 'Cylindrical'
        QtCore.QObject.connect(_widget, QtCore.SIGNAL("currentIndexChanged(QString)"),
                               lambda value=_shape_default_value:
                               self.parent.master_table_sample_shape_changed(value))
        _widget.addItem("cylindrical")
        _widget.addItem("spherical")
        self.table_ui.setCellWidget(row, 7, _widget)

        # column 8 - radius
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, 8, _item)

        # column 9 - height
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, 9, _item)

        # column 10 - abs. correction
        _widget = QtGui.QComboBox()
        if _shape_default_value == 'Cylindrical':
            list_abs_correction = ['None',
                                   'Carpenter',
                                   'Mayers',
                                   'Podman & Pings',
                                   'Monte Carlo',
                                   'Numerical']
        else:
            list_abs_correction.remove('Carpenter')
            list_abs_correction.remove('Mayers')
            list_abs_correction.remove('Podman & Pings')
            list_abs_correction.remove('Numerical')

        for _item in list_abs_correction:
            _widget.addItem(_item)
        self.table_ui.setCellWidget(row, 10, _widget)

        # column 11 - multi. scattering correction

        # column 12 - inelastic correction







    def _calculate_insert_row(self):
        selection = self.parent.ui.h3_table.selectedRanges()

        # no row selected, new row will be the first row
        if selection == []:
            return 0

        first_selection = selection[0]
        return first_selection.topRow()



