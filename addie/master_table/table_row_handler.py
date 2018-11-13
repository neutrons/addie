import numpy as np
import random

try:
    from PyQt4.QtGui import QCheckBox, QSpacerItem, QSizePolicy, QTableWidgetItem, QLabel, QPushButton, QComboBox, QWidget
    from PyQt4 import QtCore, QtGui
except ImportError:
    try:
        from PyQt5.QtWidgets import QCheckBox, QSpacerItem, QSizePolicy, QTableWidgetItem, QLabel, QPushButton, QWidget, QComboBox
        from PyQt5 import QtCore, QtGui
    except ImportError:
        raise ImportError("Requires PyQt4 or PyQt5")

# from qtpy.QWidgets import QCheckBox, QSpacerItem, QSizePolicy, QTableWidgetItem, QLabel, QPushButton, QWidget, QComboBox
# from qtpy import QtCore, QtGui

from addie.master_table.placzek_handler import PlaczekHandler


class TableRowHandler:

    def __init__(self, parent=None):
        self.parent = parent
        self.table_ui = self.parent.ui.h3_table

    def insert_blank_row(self):
        row = self._calculate_insert_row()
        self.insert_row(row=row)

    # global methods
    def shape_changed(self, shape='cylindrical', key=None, data_type='sample'):

        def update_ui(ui=None, new_list=[]):
            '''repopulate the ui with the new list and select old item selected
            if this item is in the new list as well'''

            # saving prev. item selected
            prev_item_selected = ui.currentText()

            # clean up
            ui.clear()

            # update list
            for _item in new_list:
                ui.addItem(_item)

            # re-select the same item (if still there)
            new_index_of_prev_item_selected = ui.findText(prev_item_selected)
            if new_index_of_prev_item_selected != -1:
                ui.setCurrentIndex(new_index_of_prev_item_selected)

            # abs. correction

        absorption_correction_ui = self.parent.master_table_list_ui[key][data_type]['abs_correction']
        list_abs_correction = self.get_absorption_correction_list(shape=shape)
        update_ui(ui=absorption_correction_ui, new_list=list_abs_correction)

        # mult. scat. correction
        mult_scat_correction_ui = self.parent.master_table_list_ui[key][data_type]['mult_scat_correction']
        list_mult_scat_correction = self.get_multi_scat_correction_list(shape=shape)
        update_ui(ui=mult_scat_correction_ui, new_list=list_mult_scat_correction)

    def inelastic_correction_changed(self, value='None', key=None, data_type='sample'):
        show_button = True
        if value.lower() == 'none':
            show_button = False

        _ui = self.parent.master_table_list_ui[key][data_type]['placzek_button']
        _ui.setVisible(show_button)

    def placzek_button_pressed(self, key=None, data_type='sample'):
        o_placzek = PlaczekHandler(parent=self.parent, key=key, data_type=data_type)

    def activated_row_changed(self, state=None):
        pass

    def generate_random_key(self):
        return random.randint(0, 1e5)

    def insert_row(self, row=-1):
        self.table_ui.insertRow(row)

        _master_table_row_ui = {'active': None,
                                'sample': {'shape': None,
                                           'abs_correction': None,
                                           'mult_scat_correction': None,
                                           'inelastic_correction': None,
                                           'placzek_button': None,
                                           'placzek_infos': None,
                                            },
                                'normalization': {'shape': None,
                                           'abs_correction': None,
                                           'mult_scat_correction': None,
                                           'inelastic_correction': None,
                                           'placzek_button': None,
                                           'placzek_infos': None,
                                            },
                                }

        random_key = self.generate_random_key()

        # column 0 (active or not checkBox)
        _layout = QtGui.QHBoxLayout()
        _widget = QCheckBox()
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
        _new_widget = QWidget()
        _new_widget.setLayout(_layout)
        QtCore.QObject.connect(_widget, QtCore.SIGNAL("stateChanged(int)"),
                               lambda state=0, key=random_key:
                               self.parent.master_table_select_state_changed(state, key))
        _widget.blockSignals(True)
        self.table_ui.setCellWidget(row, 0, _new_widget)

        ## sample

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
        _layout = QtGui.QHBoxLayout()
        _layout.setMargin(0)
        _widget = QComboBox()
        _shape_default_value = 'Cylindrical'
        QtCore.QObject.connect(_widget, QtCore.SIGNAL("currentIndexChanged(QString)"),
                               lambda value=_shape_default_value,
                               key=random_key:
                               self.parent.master_table_sample_shape_changed(value, key))
        _widget.blockSignals(True)
        _widget.addItem("cylindrical")
        _widget.addItem("spherical")
        _master_table_row_ui['sample']['shape'] = _widget
        _layout.addWidget(_widget)
        _w = QWidget()
        _w.setLayout(_layout)
        self.table_ui.setCellWidget(row, 7, _w)

        # column 8 - radius
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, 8, _item)

        # column 9 - height
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, 9, _item)

        # column 10 - abs. correction
        _layout = QtGui.QHBoxLayout()
        _layout.setMargin(0)
        _widget = QComboBox()
        list_abs_correction = self.get_absorption_correction_list(shape=_shape_default_value)
        for _item in list_abs_correction:
            _widget.addItem(_item)
        _master_table_row_ui['sample']['abs_correction'] = _widget
        _layout.addWidget(_widget)
        _w = QWidget()
        _w.setLayout(_layout)
        self.table_ui.setCellWidget(row, 10, _w)

        # column 11 - multi. scattering correction
        _layout = QtGui.QHBoxLayout()
        _layout.setMargin(0)
        _widget = QComboBox()
        list_multi_scat_correction = self.get_multi_scat_correction_list(shape=_shape_default_value)
        for _item in list_multi_scat_correction:
            _widget.addItem(_item)
        _master_table_row_ui['sample']['mult_scat_correction'] = _widget
        _layout.addWidget(_widget)
        _w = QWidget()
        _w.setLayout(_layout)
        self.table_ui.setCellWidget(row, 11, _w)

        # column 12 - inelastic correction
        _layout = QtGui.QHBoxLayout()
        _layout.setMargin(0)
        _widget1 = QComboBox()
        _widget1.setMinimumHeight(20)
        list_inelastic_correction = self.get_inelastic_scattering_list(shape=_shape_default_value)
        for _item in list_inelastic_correction:
                _widget1.addItem(_item)
        _master_table_row_ui['sample']['inelastic_correction'] = _widget1
        _button = QPushButton("...")
        QtCore.QObject.connect(_button, QtCore.SIGNAL("pressed()"),
                               lambda key=random_key:
                               self.parent.master_table_sample_placzek_button_pressed(key))
        _master_table_row_ui['sample']['placzek_button'] = _button
        _button.setFixedWidth(35)
        _button.setVisible(False)
        _master_table_row_ui['sample']['placzek_button'] = _button
        _layout.addWidget(_widget1)
        _layout.addWidget(_button)
        _widget = QWidget()
        _widget.setLayout(_layout)
        _default_value = 'None'
        QtCore.QObject.connect(_widget1, QtCore.SIGNAL("currentIndexChanged(QString)"),
                               lambda value=_default_value,
                               key=random_key:
                               self.parent.master_table_sample_inelastic_correction_changed(value, key))
        _widget.blockSignals(True)
        self.table_ui.setCellWidget(row, 12, _widget)

        ## normalization

        # column 13 - sample runs
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, 13, _item)

        # column 14 - background runs
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, 14, _item)

        # column 15 - background background
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, 15, _item)

        # column 16 - material
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, 16, _item)

        # column 17 - packing fraction
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, 17, _item)

        # column 18 - shape (cylindrical or spherical)
        _layout = QtGui.QHBoxLayout()
        _layout.setMargin(0)
        _widget = QComboBox()
        _shape_default_value = 'Cylindrical'
        QtCore.QObject.connect(_widget, QtCore.SIGNAL("currentIndexChanged(QString)"),
                               lambda value=_shape_default_value,
                               key=random_key:
                               self.parent.master_table_normalization_shape_changed(value, key))
        _widget.blockSignals(True)
        _widget.addItem("cylindrical")
        _widget.addItem("spherical")
        _master_table_row_ui['normalization']['shape'] = _widget
        _layout.addWidget(_widget)
        _w = QWidget()
        _w.setLayout(_layout)
        self.table_ui.setCellWidget(row, 18, _w)

        # column 19 - radius
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, 19, _item)

        # column 20 - height
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, 20, _item)

        # column 21 - abs. correction
        _layout = QtGui.QHBoxLayout()
        _layout.setMargin(0)
        _widget = QComboBox()
        list_abs_correction = self.get_absorption_correction_list(shape=_shape_default_value)
        for _item in list_abs_correction:
            _widget.addItem(_item)
        _master_table_row_ui['normalization']['abs_correction'] = _widget
        _layout.addWidget(_widget)
        _w = QWidget()
        _w.setLayout(_layout)
        self.table_ui.setCellWidget(row, 21, _w)

        # column 22 - multi. scattering correction
        _layout = QtGui.QHBoxLayout()
        _layout.setMargin(0)
        _widget = QComboBox()
        list_multi_scat_correction = self.get_multi_scat_correction_list(shape=_shape_default_value)
        for _item in list_multi_scat_correction:
            _widget.addItem(_item)
        _master_table_row_ui['normalization']['mult_scat_correction'] = _widget
        _layout.addWidget(_widget)
        _w = QWidget()
        _w.setLayout(_layout)
        self.table_ui.setCellWidget(row, 22, _w)

        # column 23 - inelastic correction
        _layout = QtGui.QHBoxLayout()
        _layout.setMargin(0)
        _widget1 = QComboBox()
        _widget1.setMinimumHeight(20)
        list_inelastic_correction = self.get_inelastic_scattering_list(shape=_shape_default_value)
        for _item in list_inelastic_correction:
                _widget1.addItem(_item)
        _master_table_row_ui['normalization']['inelastic_correction'] = _widget1
        _button = QPushButton("...")
        QtCore.QObject.connect(_button, QtCore.SIGNAL("pressed()"),
                               lambda key=random_key:
                               self.parent.master_table_normalization_placzek_button_pressed(key))
        _master_table_row_ui['normalization']['placzek_button'] = _button
        _button.setFixedWidth(35)
        _button.setVisible(False)
        _master_table_row_ui['normalization']['placzek_button'] = _button
        _layout.addWidget(_widget1)
        _layout.addWidget(_button)
        _widget = QWidget()
        _widget.setLayout(_layout)
        _default_value = 'None'
        QtCore.QObject.connect(_widget1, QtCore.SIGNAL("currentIndexChanged(QString)"),
                               lambda value=_default_value,
                               key=random_key:
                               self.parent.master_table_normalization_inelastic_correction_changed(value, key))
        _widget.blockSignals(True)
        self.table_ui.setCellWidget(row, 23, _widget)

        ## recap

        list_ui = self._get_list_ui_from_master_table_row_ui(_master_table_row_ui)
        self.parent.master_table_list_ui[random_key] = _master_table_row_ui
        self.unlock_signals_ui(list_ui=list_ui)

    def _get_list_ui_from_master_table_row_ui(self, master_table_row_ui):
        list_ui = []
        if master_table_row_ui['active']:
            list_ui.append(master_table_row_ui['active'])

        for _root in ['sample', 'normalization']:
            _sub_root = master_table_row_ui[_root]
            for _key in _sub_root.keys():
                _ui = _sub_root[_key]
                if _ui:
                    list_ui.append(_ui)

        return list_ui

    def unlock_signals_ui(self, list_ui=[]):
        if list_ui == []:
            return

        for _ui in list_ui:
            _ui.blockSignals(False)

    def get_multi_scat_correction_list(self, shape='cylindrical'):
        if shape.lower() == 'cylindrical':
            return ['None',
                    'Carpenter',
                    'Mayers']
        else:
            return ['None']

    def get_inelastic_scattering_list(self, shape='cylindrical'):
        return ['None',
                'Placzek',
                ]

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



