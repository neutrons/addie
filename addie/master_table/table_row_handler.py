import numpy as np
import random

try:
    from PyQt4.QtGui import QCheckBox, QSpacerItem, QSizePolicy, QTableWidgetItem, QLabel, QPushButton, QComboBox, QWidget
    from PyQt4.QtGui import QFileDialog
    from PyQt4 import QtCore, QtGui
except ImportError:
    try:
        from PyQt5.QtWidgets import QCheckBox, QSpacerItem, QSizePolicy, QTableWidgetItem, QLabel, QPushButton, QWidget, QComboBox
        from PyQt5.QtWidgets import QFileDialog
        from PyQt5 import QtCore, QtGui
    except ImportError:
        raise ImportError("Requires PyQt4 or PyQt5")

# from qtpy.QWidgets import QCheckBox, QSpacerItem, QSizePolicy, QTableWidgetItem, QLabel, QPushButton, QWidget, QComboBox
# from qtpy import QtCore, QtGui

from addie.master_table.placzek_handler import PlaczekHandler
from addie.master_table.selection_handler import TransferH3TableWidgetState
from addie.master_table.tree_definition import COLUMN_DEFAULT_HEIGHT


class TableRowHandler:

    def __init__(self, parent=None):
        self.parent = parent
        self.table_ui = self.parent.ui.h3_table

    def insert_blank_row(self):
        row = self._calculate_insert_row()
        self.insert_row(row=row)

    def transfer_widget_states(self, state=None, value=''):
        o_transfer = TransferH3TableWidgetState(parent=self.parent)
        o_transfer.transfer_states(state=state, value=value)

    # global methods
    def shape_changed(self, shape='cylindrical', key=None, data_type='sample'):

        def update_ui(ui=None, new_list=[]):
            '''repopulate the ui with the new list and select old item selected
            if this item is in the new list as well'''

            ui.blockSignals(True)

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

            ui.blockSignals(False)

        # abs. correction
        absorption_correction_ui = self.parent.master_table_list_ui[key][data_type]['abs_correction']
        list_abs_correction = self.get_absorption_correction_list(shape=shape)
        update_ui(ui=absorption_correction_ui, new_list=list_abs_correction)

        # mult. scat. correction
        mult_scat_correction_ui = self.parent.master_table_list_ui[key][data_type]['mult_scat_correction']
        list_mult_scat_correction = self.get_multi_scat_correction_list(shape=shape)
        update_ui(ui=mult_scat_correction_ui, new_list=list_mult_scat_correction)

        # change state of other widgets of the same column if they are selected
        self.transfer_widget_states(value=shape)

        # change label of columns
        column1 = "Radius (cm)"
        column2 = ""
        column3 = "Height (cm)"

        if shape == 'spherical':
            column3 = ""
        elif shape == 'hollow cylinder':
            column1 = "Inner Radius (cm)"
            column2 = "Outer Radius (cm)"

        if data_type == 'sample':
            column_offset = 9
        else:
            column_offset = 22

        _item1 = QTableWidgetItem(column1)
        self.table_ui.setHorizontalHeaderItem(column_offset, _item1)
        _item2 = QTableWidgetItem(column2)
        self.table_ui.setHorizontalHeaderItem(column_offset+1, _item2)
        _item3 = QTableWidgetItem(column3)
        self.table_ui.setHorizontalHeaderItem(column_offset+2, _item3)

    def abs_correction_changed(self, value='', key=None, data_type='sample'):
        # change state of other widgets of the same column if they are selected
        self.transfer_widget_states(value=value)

    def inelastic_correction_changed(self, value=None, key=None, data_type='sample'):
        show_button = True
        if value.lower() == 'none':
            show_button = False

        _ui = self.parent.master_table_list_ui[key][data_type]['placzek_button']
        _ui.setVisible(show_button)

        # change state of other widgets of the same column if they are selected
        self.transfer_widget_states()

    def multi_scattering_correction(self, value='', key=None, data_type='sample'):
        # change state of other widgets of the same column if they are selected
        self.transfer_widget_states(value=value)

    def placzek_button_pressed(self, key=None, data_type='sample'):
        o_placzek = PlaczekHandler(parent=self.parent, key=key, data_type=data_type)

    def activated_row_changed(self, state=None):
        # change state of other widgets of the same column if they are selected
        self.transfer_widget_states(state=state)

    def grouping_button(self, key=None, grouping_type='input'):
        message = "Select {} grouping".format(grouping_type)
        ext = 'Grouping (*.txt);;All (*.*)'
        file_name = QFileDialog.getOpenFileName(self.parent,
                                                message,
                                                self.parent.calibration_folder,
                                                ext)
        if file_name is None:
            return

        # FIXME

    # utilities

    def generate_random_key(self):
        return random.randint(0, 1e5)

    def set_row_height(self, row, height):
        self.table_ui.setRowHeight(row, height)

    def insert_row(self, row=-1):
        self.table_ui.insertRow(row)
        self.set_row_height(row, COLUMN_DEFAULT_HEIGHT)

        _list_ui_to_unlock = []

        _master_table_row_ui = {'active': None,
                                'title': None,
                                'sample': {'runs': None,
                                           'background': {'runs': None,
                                                          'background': None,
                                                          },
                                           'material': None,
                                           'mass_density': None,
                                           'packing_fraction': None,
                                           'geometry': {'radius': None,
                                                        'radius2': None,
                                                        'height': None,
                                                        'geometry': None,
                                                        },
                                           'shape': None,
                                           'abs_correction': None,
                                           'mult_scat_correction': None,
                                           'inelastic_correction': None,
                                           'placzek_button': None,
                                           'placzek_infos': None,
                                            },
                                'normalization': {'runs': None,
                                           'background': {'runs': None,
                                                          'background': None,
                                                          },
                                           'material': None,
                                           'mass_density': None,
                                           'packing_fraction': None,
                                           'geometry': {'radius': None,
                                                        'radius2': None,
                                                        'height': None,
                                                        'geometry': None,
                                                        },
                                           'shape': None,
                                           'abs_correction': None,
                                           'mult_scat_correction': None,
                                           'inelastic_correction': None,
                                           'placzek_button': None,
                                           'placzek_infos': None,
                                            },
                                'input_grouping_button': None,
                                'input_grouping_label': None,
                                'output_grouping_button': None,
                                'output_grouping_label': None,
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
        _spacer = QSpacerItem(40, 20,
                               QSizePolicy.Expanding,
                               QSizePolicy.Minimum)
        _layout.addItem(_spacer)
        _layout.addStretch()
        _new_widget = QWidget()
        _new_widget.setLayout(_layout)
        QtCore.QObject.connect(_widget, QtCore.SIGNAL("stateChanged(int)"),
                               lambda state=0, key=random_key:
                               self.parent.master_table_select_state_changed(state, key))
        # _widget.stateChanged.connect(lambda state=0, key=random_key:
        #                        self.parent.master_table_select_state_changed(state, key))
#        _widget.blockSignals(True)
        column = 0
        self.table_ui.setCellWidget(row, column, _new_widget)

        # sample

        column += 1
        # column 1 - title
        _item = QTableWidgetItem("")
        _master_table_row_ui['title'] = _item
        self.table_ui.setItem(row, column, _item)

        # column 2 - sample runs
        column += 1
        _item = QTableWidgetItem("")
        _master_table_row_ui['sample']['runs'] = _item
        self.table_ui.setItem(row, column, _item)

        # column 3 - background runs
        column += 1
        _item = QTableWidgetItem("")
        _master_table_row_ui['sample']['background']['runs'] = _item
        self.table_ui.setItem(row, column, _item)

        # column 4 - background background
        column += 1
        _item = QTableWidgetItem("")
        _master_table_row_ui['sample']['background']['background'] = _item
        self.table_ui.setItem(row, column, _item)

        # column 5 - material
        column += 1
        _item = QTableWidgetItem("")
        _master_table_row_ui['sample']['material'] = _item
        self.table_ui.setItem(row, column, _item)

        # column 6 - mass density
        column += 1
        _item = QTableWidgetItem("")
        _master_table_row_ui['sample']['mass_density'] = _item
        self.table_ui.setItem(row, column, _item)

        # column 7 - packing fraction
        column += 1
        _item = QTableWidgetItem("")
        _master_table_row_ui['sample']['packing_fraction'] = _item
        self.table_ui.setItem(row, column, _item)

        # column 8 - shape (cylindrical or spherical)
        column += 1
        _layout = QtGui.QHBoxLayout()
        _layout.setMargin(0)
        _widget = QComboBox()
        _shape_default_value = 'Cylindrical'
        # _widget.currentIndexChanged.connect(lambda value=_shape_default_value,
        #                        key=random_key:
        #                        self.parent.master_table_sample_shape_changed(value, key))
        QtCore.QObject.connect(_widget, QtCore.SIGNAL("currentIndexChanged(QString)"),
                               lambda value=_shape_default_value,
                               key=random_key:
                               self.parent.master_table_sample_shape_changed(value, key))
        _list_ui_to_unlock.append(_widget)
        _widget.blockSignals(True)
        _widget.addItem("cylindrical")
        _widget.addItem("spherical")
        _widget.addItem("hollow cylinder")
        _master_table_row_ui['sample']['shape'] = _widget
        _layout.addWidget(_widget)
        _w = QWidget()
        _w.setLayout(_layout)
        self.table_ui.setCellWidget(row, column, _w)

        # column 9 - radius
        column += 1
        _item = QTableWidgetItem("")
        _master_table_row_ui['sample']['geometry']['radius'] = _item
        self.table_ui.setItem(row, column, _item)

        # column 10 - radius
        column += 1
        _item = QTableWidgetItem("")
        _master_table_row_ui['sample']['geometry']['radius2'] = _item
        self.table_ui.setItem(row, column, _item)

        # column 11 - height
        column += 1
        _item = QTableWidgetItem("")
        _master_table_row_ui['sample']['geometry']['height'] = _item
        self.table_ui.setItem(row, column, _item)

        # column 12 - abs. correction
        column += 1
        _layout = QtGui.QHBoxLayout()
        _layout.setMargin(0)
        _widget = QComboBox()
        list_abs_correction = self.get_absorption_correction_list(shape=_shape_default_value)
        # _widget.currentIndexChanged.connect(lambda value=list_abs_correction[0],
        #                        key = random_key:
        #                        self.parent.master_table_sample_abs_correction_changed(value, key))
        QtCore.QObject.connect(_widget, QtCore.SIGNAL("currentIndexChanged(QString)"),
                               lambda value=list_abs_correction[0],
                               key = random_key:
                               self.parent.master_table_sample_abs_correction_changed(value, key))
        _widget.blockSignals(True)
        _list_ui_to_unlock.append(_widget)
        for _item in list_abs_correction:
            _widget.addItem(_item)
        _master_table_row_ui['sample']['abs_correction'] = _widget
        _layout.addWidget(_widget)
        _w = QWidget()
        _w.setLayout(_layout)
        self.table_ui.setCellWidget(row, column, _w)

        # column 13 - multi. scattering correction
        column += 1
        _layout = QtGui.QHBoxLayout()
        _layout.setMargin(0)
        _widget = QComboBox()
        list_multi_scat_correction = self.get_multi_scat_correction_list(shape=_shape_default_value)
        # _widget.currentIndexChanged.connect(lambda value=list_multi_scat_correction[0],
        #                        key=random_key:
        #                        self.parent.master_table_sample_multi_scattering_correction_changed(value, key))
        QtCore.QObject.connect(_widget, QtCore.SIGNAL("currentIndexChanged(QString)"),
                               lambda value=list_multi_scat_correction[0],
                               key=random_key:
                               self.parent.master_table_sample_multi_scattering_correction_changed(value, key))
        _widget.blockSignals(True)
        _list_ui_to_unlock.append(_widget)
        for _item in list_multi_scat_correction:
            _widget.addItem(_item)
        _master_table_row_ui['sample']['mult_scat_correction'] = _widget
        _layout.addWidget(_widget)
        _w = QWidget()
        _w.setLayout(_layout)
        self.table_ui.setCellWidget(row, column, _w)

        # column 14 - inelastic correction
        column += 1
        _layout = QtGui.QHBoxLayout()
        _layout.setMargin(0)
        _widget1 = QComboBox()
        _widget1.setMinimumHeight(20)
        list_inelastic_correction = self.get_inelastic_scattering_list(shape=_shape_default_value)
        for _item in list_inelastic_correction:
                _widget1.addItem(_item)
        _master_table_row_ui['sample']['inelastic_correction'] = _widget1
        _button = QPushButton("...")
        # _button.pressed.connect(lambda key=random_key:
        #                        self.parent.master_table_sample_placzek_button_pressed(key))
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
        # _widget1.currentIndexChanged.connect(lambda value=_default_value,
        #                        key=random_key:
        #                        self.parent.master_table_sample_inelastic_correction_changed(value, key))
        QtCore.QObject.connect(_widget1, QtCore.SIGNAL("currentIndexChanged(QString)"),
                               lambda value=_default_value,
                               key=random_key:
                               self.parent.master_table_sample_inelastic_correction_changed(value, key))
        _widget.blockSignals(True)
        _list_ui_to_unlock.append(_widget)
        self.table_ui.setCellWidget(row, column, _widget)

        ## normalization

        # column 15 - sample runs
        column += 1
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, column, _item)

        # column 16 - background runs
        column += 1
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, column, _item)

        # column 17 - background background
        column += 1
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, column, _item)

        # column 18 - material
        column += 1
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, column, _item)

        # column 19 - mass density
        column += 1
        _item = QTableWidgetItem("")
        _master_table_row_ui['normalization']['mass_density'] = _item
        self.table_ui.setItem(row, column, _item)

        # column 20 - packing fraction
        column += 1
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, column, _item)

        # column 21 - shape (cylindrical or spherical)
        column += 1
        _layout = QtGui.QHBoxLayout()
        _layout.setMargin(0)
        _widget = QComboBox()
        _shape_default_value = 'Cylindrical'
        # _widget.currentIndexChanged.connect(lambda value=_shape_default_value,
        #                        key=random_key:
        #                        self.parent.master_table_normalization_shape_changed(value, key))
        QtCore.QObject.connect(_widget, QtCore.SIGNAL("currentIndexChanged(QString)"),
                               lambda value=_shape_default_value,
                               key=random_key:
                               self.parent.master_table_normalization_shape_changed(value, key))
        _widget.blockSignals(True)
        _list_ui_to_unlock.append(_widget)
        _widget.addItem("cylindrical")
        _widget.addItem("spherical")
        _widget.addItem("hollow cylinder")
        _master_table_row_ui['normalization']['shape'] = _widget
        _layout.addWidget(_widget)
        _w = QWidget()
        _w.setLayout(_layout)
        self.table_ui.setCellWidget(row, column, _w)

        # column 22 - radius
        column += 1
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, column, _item)

        # column 23 - radius2
        column += 1
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, column, _item)

        # column 24 - height
        column += 1
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, column, _item)

        # column 25 - abs. correctiona
        column += 1
        _layout = QtGui.QHBoxLayout()
        _layout.setMargin(0)
        _widget = QComboBox()
        # _widget.currentIndexChanged.connect(lambda value=list_abs_correction[0],
        #                            key=random_key:
        #                        self.parent.master_table_normalization_abs_correction_changed(value, key))
        QtCore.QObject.connect(_widget, QtCore.SIGNAL("currentIndexChanged(QString)"),
                               lambda value=list_abs_correction[0],
                                   key=random_key:
                               self.parent.master_table_normalization_abs_correction_changed(value, key))
        _widget.blockSignals(True)
        _list_ui_to_unlock.append(_widget)
#        list_abs_correction = self.get_absorption_correction_list(shape=_shape_default_value)
        for _item in list_abs_correction:
            _widget.addItem(_item)
        _master_table_row_ui['normalization']['abs_correction'] = _widget
        _layout.addWidget(_widget)
        _w = QWidget()
        _w.setLayout(_layout)
        self.table_ui.setCellWidget(row, column, _w)

        # column 26 - multi. scattering correction
        column += 1
        _layout = QtGui.QHBoxLayout()
        _layout.setMargin(0)
        _widget = QComboBox()
        # _widget.currentIndexChanged.connect(lambda value=list_multi_scat_correction[0],
        #                            key=random_key:
        #                        self.parent.master_table_normalization_multi_scattering_correction_changed(value, key))
        QtCore.QObject.connect(_widget, QtCore.SIGNAL("currentIndexChanged(QString)"),
                               lambda value=list_multi_scat_correction[0],
                                   key=random_key:
                               self.parent.master_table_normalization_multi_scattering_correction_changed(value, key))
        _widget.blockSignals(True)
        _list_ui_to_unlock.append(_widget)
        # list_multi_scat_correction = self.get_multi_scat_correction_list(shape=_shape_default_value)
        for _item in list_multi_scat_correction:
            _widget.addItem(_item)
        _master_table_row_ui['normalization']['mult_scat_correction'] = _widget
        #_widget.setCurrentIndex(0)
        _layout.addWidget(_widget)
        _w = QWidget()
        _w.setLayout(_layout)
        self.table_ui.setCellWidget(row, column, _w)

        # column 27 - inelastic correction
        column += 1
        _layout = QtGui.QHBoxLayout()
        _layout.setMargin(0)
        _widget1 = QComboBox()
        _widget1.setMinimumHeight(20)
        list_inelastic_correction = self.get_inelastic_scattering_list(shape=_shape_default_value)
        for _item in list_inelastic_correction:
                _widget1.addItem(_item)
        _master_table_row_ui['normalization']['inelastic_correction'] = _widget1
        _button = QPushButton("...")
        # _button.pressed.connect(lambda key=random_key:
        #                        self.parent.master_table_normalization_placzek_button_pressed(key))
        QtCore.QObject.connect(_button, QtCore.SIGNAL("pressed()"),
                               lambda key=random_key:
                               self.parent.master_table_normalization_placzek_button_pressed(key))
        _master_table_row_ui['normalization']['placzek_button'] = _button
        _button.setFixedWidth(35)
        _button.setVisible(False)
        _layout.addWidget(_widget1)
        _layout.addWidget(_button)
        _widget = QWidget()
        _widget.setLayout(_layout)
        _default_value = 'None'
        # _widget1.currentIndexChanged.connect( lambda value=_default_value,
        #                        key=random_key:
        #                        self.parent.master_table_normalization_inelastic_correction_changed(value, key))
        QtCore.QObject.connect(_widget1, QtCore.SIGNAL("currentIndexChanged(QString)"),
                               lambda value=_default_value,
                               key=random_key:
                               self.parent.master_table_normalization_inelastic_correction_changed(value, key))
        _widget.blockSignals(True)
        _list_ui_to_unlock.append(_widget)
        self.table_ui.setCellWidget(row, column, _widget)

        # automatically populate placzek infos with default values


        # FIXME



        # column 28 - Input Grouping
        column += 1
        _row1_layout = QtGui.QHBoxLayout()
        _row1_layout.setMargin(0)
        _label = QLabel("Default  or  ")
        _button = QPushButton("...")
        # _button.pressed.connect(lambda key=random_key:
        #                        self.parent.master_table_input_grouping_button_pressed(key))
        QtCore.QObject.connect(_button, QtCore.SIGNAL("pressed()"),
                               lambda key=random_key:
                               self.parent.master_table_input_grouping_button_pressed(key))
        _master_table_row_ui['input_grouping_button'] = _button
        _row1_widget = QWidget()
        _row1_layout.addWidget(_label)
        _row1_layout.addWidget(_button)
        _row1_widget.setLayout(_row1_layout)

        _row2_layout = QtGui.QHBoxLayout()
        _row2_layout.setMargin(0)
        _label = QLabel("(6 groups)")
        _master_table_row_ui['input_grouping_label'] = _label
        _spacer = QSpacerItem(40, 20,
                               QSizePolicy.Expanding,
                               QSizePolicy.Minimum)
        _row2_layout.addItem(_spacer)
        _row2_layout.addWidget(_label)
        _spacer = QSpacerItem(40, 20,
                               QSizePolicy.Expanding,
                               QSizePolicy.Minimum)
        _row2_layout.addItem(_spacer)
        _row2_widget = QWidget()
        _row2_widget.setLayout(_row2_layout)

        _verti_layout = QtGui.QVBoxLayout()
        _verti_layout.setMargin(0)
        _verti_widget = QWidget()
        _verti_layout.addWidget(_row1_widget)
        _verti_layout.addWidget(_row2_widget)
        _verti_widget.setLayout(_verti_layout)
        self.table_ui.setCellWidget(row, column, _verti_widget)

        # column 29 - Output Grouping
        column += 1
        _row1_layout = QtGui.QHBoxLayout()
        _row1_layout.setMargin(0)
        _label = QLabel("Default  or  ")
        _button = QPushButton("...")
        # _button.pressed.connect(lambda key=random_key:
        #                        self.parent.master_table_output_grouping_button_pressed(key))
        QtCore.QObject.connect(_button, QtCore.SIGNAL("pressed()"),
                               lambda key=random_key:
                               self.parent.master_table_output_grouping_button_pressed(key))
        _master_table_row_ui['output_grouping_button'] = _button
        _row1_widget = QWidget()
        _row1_layout.addWidget(_label)
        _row1_layout.addWidget(_button)
        _row1_widget.setLayout(_row1_layout)
        _row2_layout = QtGui.QHBoxLayout()
        _row2_layout.setMargin(0)
        _label = QLabel("(6 groups)")
        _master_table_row_ui['output_grouping_label'] = _label
        _spacer = QSpacerItem(40, 20,
                               QSizePolicy.Expanding,
                               QSizePolicy.Minimum)
        _row2_layout.addItem(_spacer)
        _row2_layout.addWidget(_label)
        _spacer = QSpacerItem(40, 20,
                               QSizePolicy.Expanding,
                               QSizePolicy.Minimum)
        _row2_layout.addItem(_spacer)
        _row2_widget = QWidget()
        _row2_widget.setLayout(_row2_layout)
        _verti_layout = QtGui.QVBoxLayout()
        _verti_layout.setMargin(0)
        _verti_widget = QWidget()
        _verti_layout.addWidget(_row1_widget)
        _verti_layout.addWidget(_row2_widget)
        _verti_widget.setLayout(_verti_layout)
        self.table_ui.setCellWidget(row, column, _verti_widget)

        ## recap

        #list_ui = self._get_list_ui_from_master_table_row_ui(_master_table_row_ui)
        self.parent.master_table_list_ui[random_key] = _master_table_row_ui
        self.unlock_signals_ui(list_ui=_list_ui_to_unlock)
        self.parent.check_status_of_right_click_buttons()

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



