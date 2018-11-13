import numpy as np
import random

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

    def sample_shape_changed(self, shape='Cylindrical', key=None):
        absorption_correction_ui = self.parent.master_table_list_ui[key]['abs_correction']

        # looking at previously item selected to select it again (if present)
        prev_item_selected = absorption_correction_ui.currentText()

        absorption_correction_ui.clear()
        list_abs_correction = self.get_absorption_correction_list(shape=shape)
        for _item in list_abs_correction:
            absorption_correction_ui.addItem(_item)

        new_index_of_prev_item_selected = absorption_correction_ui.findText(prev_item_selected)
        if new_index_of_prev_item_selected != -1:
            absorption_correction_ui.setCurrentIndex(new_index_of_prev_item_selected)

    def activated_row_changed(self, state=None):
        pass

    def generate_random_key(self):
        return random.randint(0, 1e5)

    def insert_row(self, row=-1):
        self.table_ui.insertRow(row)

        list_of_ui_signals_to_unlock = []

        _master_table_row_ui = {'active': None,
                                'shape': None,
                                'abs_correction': None,
                                }

        random_key = self.generate_random_key()

        # column 0 (active or not checkBox)
        _layout = QtGui.QHBoxLayout()
        _widget = QtGui.QCheckBox()
        _widget.setCheckState(QtCore.Qt.Checked)
        _widget.setEnabled(True)
        _master_table_row_ui['active'] = _widget
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
                               lambda state=0, key=random_key:
                               self.parent.master_table_select_state_changed(state, key))
        _widget.blockSignals(True)
        list_of_ui_signals_to_unlock.append(_widget)
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
                               lambda value=_shape_default_value,
                               key=random_key:
                               self.parent.master_table_sample_shape_changed(value, key))
        _widget.blockSignals(True)
        list_of_ui_signals_to_unlock.append(_widget)
        _widget.addItem("cylindrical")
        _widget.addItem("spherical")
        _master_table_row_ui['shape'] = _widget
        self.table_ui.setCellWidget(row, 7, _widget)

        # column 8 - radius
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, 8, _item)

        # column 9 - height
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, 9, _item)

        # column 10 - abs. correction
        _widget = QtGui.QComboBox()
        list_abs_correction = self.get_absorption_correction_list(shape=_shape_default_value)
        for _item in list_abs_correction:
            _widget.addItem(_item)
        _master_table_row_ui['abs_correction'] = _widget
        self.table_ui.setCellWidget(row, 10, _widget)

        # column 11 - multi. scattering correction

        # column 12 - inelastic correction




        self.parent.master_table_list_ui[random_key] = _master_table_row_ui
        self.unlock_signals_ui(list_ui=list_of_ui_signals_to_unlock)

    def unlock_signals_ui(self, list_ui=[]):
        if list_ui == []:
            return

        for _ui in list_ui:
            _ui.blockSignals(False)

    def get_absorption_correction_list(self, shape='cylindrical'):
        if shape.lower() == 'cylindrical':
            return ['None',
                    'Carpenter',
                    'Mayers',
                    'Podman & Pings',
                    'Monte Carlo',
                    'Numerical',
                    ]
        else:
            return ['None',
                    'Monte Carlo',
                    ]

    def _calculate_insert_row(self):
        selection = self.parent.ui.h3_table.selectedRanges()

        # no row selected, new row will be the first row
        if selection == []:
            return 0

        first_selection = selection[0]
        return first_selection.topRow()



