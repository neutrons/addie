from __future__ import (absolute_import, division, print_function)

from qtpy.QtWidgets import QCheckBox, QSpacerItem, QSizePolicy, QTableWidgetItem, QLabel, QPushButton, \
    QComboBox, QFileDialog, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLineEdit
from qtpy import QtCore
import copy
import numpy as np
import random

from addie.processing.mantid.master_table.placzek_handler import PlaczekHandler
from addie.processing.mantid.master_table.selection_handler import TransferH3TableWidgetState
from addie.processing.mantid.master_table.periodic_table.chemical_formula_handler import format_chemical_formula_equation
from addie.processing.mantid.master_table.tree_definition import COLUMN_DEFAULT_HEIGHT, CONFIG_BUTTON_HEIGHT, CONFIG_BUTTON_WIDTH


class TableRowHandler:

    def __init__(self, main_window=None):
        self.main_window = main_window
        self.table_ui = main_window.processing_ui.h3_table

    def insert_blank_row(self):
        row = self._calculate_insert_row()
        self.insert_row(row=row)

    def transfer_widget_states(self, from_key=None, data_type='sample'):
        o_transfer = TransferH3TableWidgetState(parent=self.main_window)
        o_transfer.transfer_states(from_key=from_key, data_type=data_type)

    # global methods
    def shape_changed(self, shape_index=0, key=None, data_type='sample'):

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
        absorption_correction_ui = self.main_window.master_table_list_ui[key][data_type]['abs_correction']
        list_abs_correction = self.get_absorption_correction_list(shape=shape_index)
        update_ui(ui=absorption_correction_ui, new_list=list_abs_correction)

        # mult. scat. correction
        mult_scat_correction_ui = self.main_window.master_table_list_ui[key][data_type]['mult_scat_correction']
        list_mult_scat_correction = self.get_multi_scat_correction_list(shape=shape_index)
        update_ui(ui=mult_scat_correction_ui, new_list=list_mult_scat_correction)

        _enabled_radius_1 = True
        _enabled_radius_2 = True
        _enabled_height = True
        _label_radius_1 = 'Radius'
        _label_radius_2 = 'Outer Radius'
        if shape_index == 0: # cylindrical
            _enabled_radius_2 = False
        elif shape_index == 1: # spherical
            _enabled_height = False
            _enabled_radius_2 = False
        else:
            _label_radius_1 = 'Inner Radius'

        self.main_window.master_table_list_ui[key][data_type]['geometry']['radius']['value'].setVisible(_enabled_radius_1)
        self.main_window.master_table_list_ui[key][data_type]['geometry']['radius2']['value'].setVisible(_enabled_radius_2)
        self.main_window.master_table_list_ui[key][data_type]['geometry']['height']['value'].setVisible(_enabled_height)

        self.main_window.master_table_list_ui[key][data_type]['geometry']['radius']['label'].setVisible(_enabled_radius_1)
        self.main_window.master_table_list_ui[key][data_type]['geometry']['radius2']['label'].setVisible(_enabled_radius_2)
        self.main_window.master_table_list_ui[key][data_type]['geometry']['height']['label'].setVisible(_enabled_height)

        self.main_window.master_table_list_ui[key][data_type]['geometry']['radius']['units'].setVisible(_enabled_radius_1)
        self.main_window.master_table_list_ui[key][data_type]['geometry']['radius2']['units'].setVisible(_enabled_radius_2)
        self.main_window.master_table_list_ui[key][data_type]['geometry']['height']['units'].setVisible(_enabled_height)

        self.main_window.master_table_list_ui[key][data_type]['geometry']['radius']['label'].setText(_label_radius_1)
        self.main_window.master_table_list_ui[key][data_type]['geometry']['radius2']['label'].setText(_label_radius_2)

        # change state of other widgets of the same column if they are selected
        self.transfer_widget_states(from_key=key, data_type=data_type)

    def abs_correction_changed(self, value='', key=None, data_type='sample'):
        # change state of other widgets of the same column if they are selected
        self.transfer_widget_states(from_key=key, data_type=data_type)

    def inelastic_correction_changed(self, value=None, key=None, data_type='sample'):
        show_button = True
        if value == 0:
            show_button = False

        _ui = self.main_window.master_table_list_ui[key][data_type]['placzek_button']
        _ui.setVisible(show_button)

        # change state of other widgets of the same column if they are selected
        self.transfer_widget_states(from_key=key, data_type=data_type)

    def multi_scattering_correction(self, value='', key=None, data_type='sample'):
        # change state of other widgets of the same column if they are selected
        self.transfer_widget_states(from_key=key, data_type=data_type)

    def placzek_button_pressed(self, key=None, data_type='sample'):
        PlaczekHandler(parent=self.main_window, key=key, data_type=data_type)

    def activated_row_changed(self, key=None, state=None):
        data_type = 'sample'

        # change state of other widgets of the same column if they are selected
        self.transfer_widget_states(from_key=key, data_type=data_type)

    def grouping_button(self, key=None, grouping_type='input'):
        message = "Select {} grouping".format(grouping_type)
        ext = 'Grouping (*.txt);;All (*.*)'
        file_name = QFileDialog.getOpenFileName(self.main_window,
                                                message,
                                                self.main_window.calibration_folder,
                                                ext)
        if file_name is None:
            return

    # utilities

    def generate_random_key(self):
        return random.randint(0, 1e5)

    def set_row_height(self, row, height):
        self.table_ui.setRowHeight(row, height)

    def fill_row(self, sample_runs='',
                 sample_chemical_formula='N/A',
                 sample_mass_density='N/A'):
        if dict == {}:
            return

        row = self._calculate_insert_row()
        self.insert_row(row=row, sample_runs=sample_runs,
                        sample_mass_density=sample_mass_density,
                        sample_chemical_formula=sample_chemical_formula)

    def insert_row(self, row=-1,
                   title='',
                   sample_runs='',
                   sample_mass_density='N/A',
                   sample_chemical_formula='N/A',
                   packing_fraction='N/A'):
        self.table_ui.insertRow(row)
        self.set_row_height(row, COLUMN_DEFAULT_HEIGHT)

        _list_ui_to_unlock = []

        _dimension_widgets = {'label': None, 'value': 'N/A', 'units': None}
        _full_dimension_widgets = {'radius': copy.deepcopy(_dimension_widgets),
                                   'radius2': copy.deepcopy(_dimension_widgets),
                                   'height': copy.deepcopy(_dimension_widgets)}
        _text_button = {'text': None, 'button': None}
        _mass_density_options = {'value': "N/A",
                                 "selected": False}
        _mass_density_infos = {'number_density': copy.deepcopy(_mass_density_options),
                               'mass_density': copy.deepcopy(_mass_density_options),
                               'mass': copy.deepcopy(_mass_density_options),
                               'molecular_mass': np.NaN,
                               'total_number_of_atoms': np.NaN,
                               }
        _material_infos = {'mantid_format': None,
                           'addie_format': None}
        _mass_density_infos['mass_density']["selected"] = True

        _master_table_row_ui = {'active': None,
                                'title': None,
                                'sample': {'runs': None,
                                           'background': {'runs': None,
                                                          'background': None,
                                                          },
                                           'material': copy.deepcopy(_text_button),
                                           'material_infos': copy.deepcopy(_material_infos),
                                           'mass_density': copy.deepcopy(_text_button),
                                           'mass_density_infos': copy.deepcopy(_mass_density_infos),
                                           'packing_fraction': None,
                                           'geometry': copy.deepcopy(_full_dimension_widgets),
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
                                                  'material': copy.deepcopy(_text_button),
                                                  'material_infos': copy.deepcopy(_material_infos),
                                                  'mass_density': copy.deepcopy(_text_button),
                                                  'mass_density_infos': copy.deepcopy(_mass_density_infos),
                                                  'packing_fraction': None,
                                                  'geometry': copy.deepcopy(_full_dimension_widgets),
                                                  'shape': None,
                                                  'abs_correction': None,
                                                  'mult_scat_correction': None,
                                                  'inelastic_correction': None,
                                                  'placzek_button': None,
                                                  'placzek_infos': None,
                                                  },
                                'key_value_button': None,
                                }

        random_key = self.generate_random_key()
        self.key = random_key

        # column 0 (active or not checkBox)
        _layout = QHBoxLayout()
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
        _widget.stateChanged.connect(lambda state=0, key=random_key:
                                     self.main_window.master_table_select_state_changed(state, key))
#        _widget.blockSignals(True)
        column = 0
        self.table_ui.setCellWidget(row, column, _new_widget)

        # sample

        column += 1
        # column 1 - title
        _item = QTableWidgetItem(title)
        _master_table_row_ui['title'] = _item
        self.table_ui.setItem(row, column, _item)

        # column 2 - sample runs
        column += 1
        _item = QTableWidgetItem(sample_runs)
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

        # column 5 - material (chemical formula)
        column += 1
        clean_sample_chemical_formula = format_chemical_formula_equation(sample_chemical_formula)
        _material_text = QLineEdit(clean_sample_chemical_formula)
        _material_text = QLabel(clean_sample_chemical_formula)
#        _material_text.setEnabled(True)
#         _material_text.returnPressed.connect(lambda key=random_key:
#                                self.parent.master_table_sample_material_line_edit_entered(key))
        _material_button = QPushButton("...")
        _material_button.setFixedHeight(CONFIG_BUTTON_HEIGHT)
        _material_button.setFixedWidth(CONFIG_BUTTON_WIDTH)
        _material_button.pressed.connect(lambda key=random_key:
                                         self.main_window.master_table_sample_material_button_pressed(key))

        _verti_layout = QVBoxLayout()
        _verti_layout.addWidget(_material_text)
        _verti_layout.addWidget(_material_button)
        _material_widget = QWidget()
        _material_widget.setLayout(_verti_layout)
        self.table_ui.setCellWidget(row, column, _material_widget)
        _master_table_row_ui['sample']['material']['text'] = _material_text
        _master_table_row_ui['sample']['material']['button'] = _material_button

        # column 6 - mass density
        column += 1
        _mass_text = QLineEdit(sample_mass_density)
        _mass_text.returnPressed.connect(lambda key=random_key:
                                         self.main_window.master_table_sample_mass_density_line_edit_entered(key))

        _mass_units = QLabel("g/cc")
        _top_widget = QWidget()
        _top_layout = QHBoxLayout()
        _top_layout.addWidget(_mass_text)
        _top_layout.addWidget(_mass_units)
        _top_widget.setLayout(_top_layout)
        _mass_button = QPushButton("...")
        _mass_button.setFixedHeight(CONFIG_BUTTON_HEIGHT)
        _mass_button.setFixedWidth(CONFIG_BUTTON_WIDTH)
        _mass_button.pressed.connect(lambda key=random_key:
                                     self.main_window.master_table_sample_mass_density_button_pressed(key))
        _verti_layout = QVBoxLayout()
        _verti_layout.addWidget(_top_widget)
        _verti_layout.addWidget(_mass_button)
        _mass_widget = QWidget()
        _mass_widget.setLayout(_verti_layout)
        self.table_ui.setCellWidget(row, column, _mass_widget)
        _master_table_row_ui['sample']['mass_density']['text'] = _mass_text
        _master_table_row_ui['sample']['mass_density']['button'] = _mass_button

        # column 7 - packing fraction
        column += 1
        if packing_fraction == "N/A":
            packing_fraction = "{}".format(self.main_window.packing_fraction)
        _item = QTableWidgetItem(packing_fraction)
        _master_table_row_ui['sample']['packing_fraction'] = _item
        self.table_ui.setItem(row, column, _item)

        # column 8 - shape (cylindrical or spherical)
        column += 1
        _layout = QHBoxLayout()
        _layout.setContentsMargins(0, 0, 0, 0)
        _widget = QComboBox()
        _shape_default_index = 0
        _widget.currentIndexChanged.connect(lambda index=_shape_default_index,
                                            key=random_key:
                                            self.main_window.master_table_sample_shape_changed(index, key))
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

        # column 9 - dimensions
        column += 1

        # layout 1
        _grid_layout = QGridLayout()

        _label1 = QLabel("Radius:")
        _grid_layout.addWidget(_label1, 1, 0)
        _value1 = QLabel("N/A")
        _grid_layout.addWidget(_value1, 1, 1)
        _dim1 = QLabel("cm")
        _grid_layout.addWidget(_dim1, 1, 2)

        _label2 = QLabel("Radius:")
        _label2.setVisible(False)
        _grid_layout.addWidget(_label2, 2, 0)
        _value2 = QLabel("N/A")
        _value2.setVisible(False)
        _grid_layout.addWidget(_value2, 2, 1)
        _dim2 = QLabel("cm")
        _dim2.setVisible(False)
        _grid_layout.addWidget(_dim2, 2, 2)

        _label3 = QLabel("Height:")
        _grid_layout.addWidget(_label3, 3, 0)
        _value3 = QLabel("N/A")
        _grid_layout.addWidget(_value3, 3, 1)
        _dim3 = QLabel("cm")
        _grid_layout.addWidget(_dim3, 3, 2)

        _master_table_row_ui['sample']['geometry']['radius']['value'] = _value1
        _master_table_row_ui['sample']['geometry']['radius2']['value'] = _value2
        _master_table_row_ui['sample']['geometry']['height']['value'] = _value3

        _master_table_row_ui['sample']['geometry']['radius']['label'] = _label1
        _master_table_row_ui['sample']['geometry']['radius2']['label'] = _label2
        _master_table_row_ui['sample']['geometry']['height']['label'] = _label3

        _master_table_row_ui['sample']['geometry']['radius']['units'] = _dim1
        _master_table_row_ui['sample']['geometry']['radius2']['units'] = _dim2
        _master_table_row_ui['sample']['geometry']['height']['units'] = _dim3

        _geometry_widget = QWidget()
        _geometry_widget.setLayout(_grid_layout)

        _set_dimensions_button = QPushButton("...")
        _set_dimensions_button.setFixedHeight(CONFIG_BUTTON_HEIGHT)
        _set_dimensions_button.setFixedWidth(CONFIG_BUTTON_WIDTH)
        _verti_layout = QVBoxLayout()
        _verti_layout.addWidget(_geometry_widget)
        _verti_layout.addWidget(_set_dimensions_button)
        _verti_widget = QWidget()
        _verti_widget.setLayout(_verti_layout)

        _set_dimensions_button.pressed.connect(lambda key=random_key:
                                               self.main_window.master_table_sample_dimensions_setter_button_pressed(key))

        self.table_ui.setCellWidget(row, column, _verti_widget)

        # column 10 - abs. correction
        column += 1
        _layout = QHBoxLayout()
        _layout.setContentsMargins(0, 0, 0, 0)
        _widget = QComboBox()
        _shape_default_value = 0
        list_abs_correction = self.get_absorption_correction_list(shape=_shape_default_value)
        _widget.currentIndexChanged.connect(lambda value=list_abs_correction[0],
                                            key = random_key:
                                            self.main_window.master_table_sample_abs_correction_changed(value, key))
        _widget.blockSignals(True)
        _list_ui_to_unlock.append(_widget)
        for _item in list_abs_correction:
            _widget.addItem(_item)
        _master_table_row_ui['sample']['abs_correction'] = _widget
        _layout.addWidget(_widget)
        _w = QWidget()
        _w.setLayout(_layout)
        self.table_ui.setCellWidget(row, column, _w)

        # column 11 - multi. scattering correction
        column += 1
        _layout = QHBoxLayout()
        _layout.setContentsMargins(0, 0, 0, 0)
        _widget = QComboBox()
        list_multi_scat_correction = self.get_multi_scat_correction_list(shape=_shape_default_value)
        _widget.currentIndexChanged.connect(lambda value=list_multi_scat_correction[0],
                                            key=random_key:
                                            self.main_window.master_table_sample_multi_scattering_correction_changed(value, key))
        _widget.blockSignals(True)
        _list_ui_to_unlock.append(_widget)
        for _item in list_multi_scat_correction:
            _widget.addItem(_item)
        _master_table_row_ui['sample']['mult_scat_correction'] = _widget
        _layout.addWidget(_widget)
        _w = QWidget()
        _w.setLayout(_layout)
        self.table_ui.setCellWidget(row, column, _w)

        # column 12 - inelastic correction
        column += 1
        _layout = QHBoxLayout()
        _layout.setContentsMargins(0, 0, 0, 0)
        _widget1 = QComboBox()
        _widget1.setMinimumHeight(20)
        list_inelastic_correction = self.get_inelastic_scattering_list(shape=_shape_default_value)
        for _item in list_inelastic_correction:
            _widget1.addItem(_item)
        _master_table_row_ui['sample']['inelastic_correction'] = _widget1
        _button = QPushButton("...")
        _button.setFixedHeight(CONFIG_BUTTON_HEIGHT)
        _button.setFixedWidth(CONFIG_BUTTON_WIDTH)
        _button.pressed.connect(lambda key=random_key:
                                self.main_window.master_table_sample_placzek_button_pressed(key))
        _master_table_row_ui['sample']['placzek_button'] = _button
        _button.setVisible(False)
        _master_table_row_ui['sample']['placzek_button'] = _button
        _layout.addWidget(_widget1)
        _layout.addWidget(_button)
        _widget = QWidget()
        _widget.setLayout(_layout)
        _default_value = 'None'
        _widget1.currentIndexChanged.connect(lambda value=_default_value,
                                             key=random_key:
                                             self.main_window.master_table_sample_inelastic_correction_changed(value, key))
        _widget.blockSignals(True)
        _list_ui_to_unlock.append(_widget)
        self.table_ui.setCellWidget(row, column, _widget)

        # save default placzek settings
        _master_table_row_ui['sample']['placzek_infos'] = self.formated_placzek_default()

        ## normalization

        # column 13 - sample runs
        column += 1
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, column, _item)

        # column 14 - background runs
        column += 1
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, column, _item)

        # column 15 - background background
        column += 1
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, column, _item)

        # column 16 - material (chemical formula)
        column += 1
        #_material_text = QLineEdit("")
        _material_text = QLabel("N/A")
        #_material_text.setEnabled(False)
        # _material_text.returnPressed.connect(lambda key=random_key:
        #                                      self.parent.master_table_normalization_material_line_edit_entered(key))
        _material_button = QPushButton("...")
        _material_button.setFixedHeight(CONFIG_BUTTON_HEIGHT)
        _material_button.setFixedWidth(CONFIG_BUTTON_WIDTH)
        _material_button.pressed.connect(lambda key=random_key:
                                         self.main_window.master_table_normalization_material_button_pressed(key))
        _verti_layout = QVBoxLayout()
        _verti_layout.addWidget(_material_text)
        _verti_layout.addWidget(_material_button)
        _material_widget = QWidget()
        _material_widget.setLayout(_verti_layout)
        self.table_ui.setCellWidget(row, column, _material_widget)
        _master_table_row_ui['normalization']['material']['text'] = _material_text
        _master_table_row_ui['normalization']['material']['button'] = _material_button

        # column 17 - mass density
        column += 1
        _mass_text = QLineEdit("N/A")
        _mass_text.returnPressed.connect(lambda key=random_key:
                                         self.main_window.master_table_normalization_mass_density_line_edit_entered(key))
        _mass_units = QLabel("g/cc")
        _top_widget = QWidget()
        _top_layout = QHBoxLayout()
        _top_layout.addWidget(_mass_text)
        _top_layout.addWidget(_mass_units)
        _top_widget.setLayout(_top_layout)
        _mass_button = QPushButton("...")
        _mass_button.setFixedWidth(CONFIG_BUTTON_WIDTH)
        _mass_button.setFixedHeight(CONFIG_BUTTON_HEIGHT)
        _mass_button.pressed.connect(lambda key=random_key:
                                     self.main_window.master_table_normalization_mass_density_button_pressed(key))
        _verti_layout = QVBoxLayout()
        _verti_layout.addWidget(_top_widget)
        _verti_layout.addWidget(_mass_button)
        _mass_widget = QWidget()
        _mass_widget.setLayout(_verti_layout)
        self.table_ui.setCellWidget(row, column, _mass_widget)
        _master_table_row_ui['normalization']['mass_density']['text'] = _mass_text
        _master_table_row_ui['normalization']['mass_density']['button'] = _mass_button

        # column 18 - packing fraction
        column += 1
        _item = QTableWidgetItem("")
        self.table_ui.setItem(row, column, _item)

        # column 19 - shape (cylindrical or spherical)
        column += 1
        _layout = QHBoxLayout()
        _layout.setContentsMargins(0, 0, 0, 0)
        _widget = QComboBox()
        _widget.currentIndexChanged.connect(lambda value=_shape_default_value,
                                            key=random_key:
                                            self.main_window.master_table_normalization_shape_changed(value, key))
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

        # column 20 - dimensions
        column += 1

        # layout 1
        _grid_layout = QGridLayout()

        _label1 = QLabel("Radius:")
        _grid_layout.addWidget(_label1, 1, 0)
        _value1 = QLabel("N/A")
        _grid_layout.addWidget(_value1, 1, 1)
        _dim1 = QLabel("cm")
        _grid_layout.addWidget(_dim1, 1, 2)

        _label2 = QLabel("Radius:")
        _label2.setVisible(False)
        _grid_layout.addWidget(_label2, 2, 0)
        _value2 = QLabel("N/A")
        _value2.setVisible(False)
        _grid_layout.addWidget(_value2, 2, 1)
        _dim2 = QLabel("cm")
        _dim2.setVisible(False)
        _grid_layout.addWidget(_dim2, 2, 2)

        _label3 = QLabel("Height:")
        _grid_layout.addWidget(_label3, 3, 0)
        _value3 = QLabel("N/A")
        _grid_layout.addWidget(_value3, 3, 1)
        _dim3 = QLabel("cm")
        _grid_layout.addWidget(_dim3, 3, 2)

        _master_table_row_ui['normalization']['geometry']['radius']['value'] = _value1
        _master_table_row_ui['normalization']['geometry']['radius2']['value'] = _value2
        _master_table_row_ui['normalization']['geometry']['height']['value'] = _value3

        _master_table_row_ui['normalization']['geometry']['radius']['label'] = _label1
        _master_table_row_ui['normalization']['geometry']['radius2']['label'] = _label2
        _master_table_row_ui['normalization']['geometry']['height']['label'] = _label3

        _master_table_row_ui['normalization']['geometry']['radius']['units'] = _dim1
        _master_table_row_ui['normalization']['geometry']['radius2']['units'] = _dim2
        _master_table_row_ui['normalization']['geometry']['height']['units'] = _dim3

        _geometry_widget = QWidget()
        _geometry_widget.setLayout(_grid_layout)

        _set_dimensions_button = QPushButton("...")
        _set_dimensions_button.setFixedHeight(CONFIG_BUTTON_HEIGHT)
        _set_dimensions_button.setFixedWidth(CONFIG_BUTTON_WIDTH)
        _verti_layout = QVBoxLayout()
        _verti_layout.addWidget(_geometry_widget)
        _verti_layout.addWidget(_set_dimensions_button)
        _verti_widget = QWidget()
        _verti_widget.setLayout(_verti_layout)

        _set_dimensions_button.pressed.connect(lambda key=random_key:
                                               self.main_window.master_table_normalization_dimensions_setter_button_pressed(key))  # noqa

        self.table_ui.setCellWidget(row, column, _verti_widget)

        # column 21 - abs. correctiona
        column += 1
        _layout = QHBoxLayout()
        _layout.setContentsMargins(0, 0, 0, 0)
        _widget = QComboBox()
        _widget.currentIndexChanged.connect(lambda value=list_abs_correction[0],
                                            key=random_key:
                                            self.main_window.master_table_normalization_abs_correction_changed(value, key))  # noqa
        _widget.blockSignals(True)
        _list_ui_to_unlock.append(_widget)
        for _item in list_abs_correction:
            _widget.addItem(_item)
        _widget.setCurrentIndex(0)
        _master_table_row_ui['normalization']['abs_correction'] = _widget
        _layout.addWidget(_widget)
        _w = QWidget()
        _w.setLayout(_layout)
        self.table_ui.setCellWidget(row, column, _w)

        # column 24 - multi. scattering correction
        column += 1
        _layout = QHBoxLayout()
        _layout.setContentsMargins(0, 0, 0, 0)
        _widget = QComboBox()
        _widget.currentIndexChanged.connect(lambda value=list_multi_scat_correction[0],
                                            key=random_key:
                                            self.main_window.master_table_normalization_multi_scattering_correction_changed(value, key))  # noqa
        _widget.blockSignals(True)
        _list_ui_to_unlock.append(_widget)
        for _item in list_multi_scat_correction:
            _widget.addItem(_item)
        _widget.setCurrentIndex(0)
        _master_table_row_ui['normalization']['mult_scat_correction'] = _widget
        _layout.addWidget(_widget)
        _w = QWidget()
        _w.setLayout(_layout)
        self.table_ui.setCellWidget(row, column, _w)

        # column 22 - inelastic correction
        column += 1
        _layout = QHBoxLayout()
        _layout.setContentsMargins(0, 0, 0, 0)
        _widget1 = QComboBox()
        _widget1.setMinimumHeight(20)
        list_inelastic_correction = self.get_inelastic_scattering_list(shape=_shape_default_value)
        for _item in list_inelastic_correction:
            _widget1.addItem(_item)
        _widget1.setCurrentIndex(0)
        _master_table_row_ui['normalization']['inelastic_correction'] = _widget1
        _button = QPushButton("...")
        _button.setFixedWidth(CONFIG_BUTTON_WIDTH)
        _button.setFixedHeight(CONFIG_BUTTON_HEIGHT)
        _button.pressed.connect(lambda key=random_key:
                                self.main_window.master_table_normalization_placzek_button_pressed(key))
        _master_table_row_ui['normalization']['placzek_button'] = _button
        _button.setVisible(False)
        _layout.addWidget(_widget1)
        _layout.addWidget(_button)
        _widget = QWidget()
        _widget.setLayout(_layout)
        _default_value = 'None'
        _widget1.currentIndexChanged.connect( lambda value=_default_value,
                                              key=random_key:
                                              self.main_window.master_table_normalization_inelastic_correction_changed(value, key))  # noqa
        _widget.blockSignals(True)
        _list_ui_to_unlock.append(_widget)
        self.table_ui.setCellWidget(row, column, _widget)

        # automatically populate placzek infos with default values
        _master_table_row_ui['normalization']['placzek_infos'] = self.formated_placzek_default()

        # column 23 - key/value pair
        column += 1
        _layout = QHBoxLayout()
        _spacer_kv1 = QSpacerItem(40, 20,
                              QSizePolicy.Expanding,
                              QSizePolicy.Minimum)
        _layout.addItem(_spacer_kv1)
        _button = QPushButton("...")
        _layout.addWidget(_button)
        _button.setFixedWidth(CONFIG_BUTTON_WIDTH)
        _button.setFixedHeight(CONFIG_BUTTON_HEIGHT)
        _button.pressed.connect(lambda key=random_key:
                                self.main_window.master_table_keyvalue_button_pressed(key))
        _new_widget = QWidget()
        _new_widget.setLayout(_layout)
        self.table_ui.setCellWidget(row, column, _new_widget)
        _master_table_row_ui['key_value_button'] = _button
        _spacer_kv2 = QSpacerItem(40, 20,
                              QSizePolicy.Expanding,
                              QSizePolicy.Minimum)
        _layout.addItem(_spacer_kv2)
        _layout.addStretch()

        ## recap

        self.main_window.master_table_list_ui[random_key] = _master_table_row_ui
        self.unlock_signals_ui(list_ui=_list_ui_to_unlock)
        self.main_window.check_status_of_right_click_buttons()

    def formated_placzek_default(self):
        config_placzek = self.main_window.placzek_default

        new_format = {'order_index': config_placzek['order']['index_selected'],
                      'is_self': config_placzek['self'],
                      'is_interference': config_placzek['interference'],
                      'fit_spectrum_index': config_placzek['fit_spectrum_with']['index_selected'],
                      'lambda_fit_min': config_placzek['lambda_binning_for_fit']['min'],
                      'lambda_fit_max': config_placzek['lambda_binning_for_fit']['max'],
                      'lambda_fit_delta': config_placzek['lambda_binning_for_fit']['delta'],
                      'lambda_calc_min': config_placzek['lambda_binning_for_calc']['min'],
                      'lambda_calc_max': config_placzek['lambda_binning_for_calc']['max'],
                      'lambda_calc_delta': config_placzek['lambda_binning_for_calc']['delta'],
                      }

        return new_format

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

    def get_multi_scat_correction_list(self, shape=0):
        if shape == 0: # cylindrical
            return ['None',
                    'Carpenter',
                    'Mayers']
        elif shape == 1: # spherical
            return ['None']
        elif shape == 2: # hollow cylindrical
            return ['None']

        return ['None']

    def get_inelastic_scattering_list(self, shape='cylindrical'):
        return ['None',
                'Placzek',
                ]

    def get_absorption_correction_list(self, shape=0):
        if shape == 0: # cylindrical
            return ['None',
                    'Carpenter',
                    'Mayers',
                    'Podman & Pings',
                    'Monte-Carlo',
                    'Numerical',
                    ]
        elif shape == 1: # spherical
            return ['None',
                    'Monte-Carlo',
                    ]
        elif shape== 2: # hollow cylinder
            return ['None',
                    'Monte-Carlo']

        return ['None']

    def _calculate_insert_row(self):
        selection = self.main_window.processing_ui.h3_table.selectedRanges()

        # no row selected, new row will be the first row
        if selection == []:
            return 0

        first_selection = selection[0]
        return first_selection.topRow()
