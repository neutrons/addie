from __future__ import (absolute_import, division, print_function)
import numpy as np
import scipy.constants

from qtpy.QtWidgets import QMainWindow
from addie.utilities import load_ui

from addie.processing.mantid.master_table.table_row_handler import TableRowHandler
from addie.utilities.math_tools import is_number, volume_of_cylinder, volume_of_hollow_cylinder, volume_of_sphere


class MassDensityHandler:

    def __init__(self, parent=None, key=None, data_type='sample'):
        if parent.mass_density_ui is None:
            o_mass = MassDensityWindow(parent=parent, key=key, data_type=data_type)
            o_mass.show()
            parent.mass_density_ui = o_mass
            if parent.mass_density_ui_position:
                parent.mass_density_ui.move(parent.mass_density_ui_position)
        else:
            parent.mass_density_ui.setFocus()
            parent.mass_density_ui.activateWindow()


class MassDensityWindow(QMainWindow):

    chemical_formula_defined = False
    geometry_dimensions_defined = False

    total_number_of_atoms = np.NaN
    total_molecular_mass = np.NaN

    def __init__(self, parent=None, key=None, data_type='sample'):
        self.parent = parent
        self.key = key
        self.data_type = data_type

        QMainWindow.__init__(self, parent=parent)
        self.ui = load_ui('mass_density.ui', baseinstance=self)
        self.init_widgets()

    def init_widgets(self):
        self.ui.number_density_units.setText(u"Atoms/\u212B\u00B3")
        self.ui.mass_density_label.setText(u"g/cm\u00B3")
        self.ui.volume_units.setText(u"cm\u00B3")
        self.ui.ok.setEnabled(False)

        # error messages
        self.ui.mass_density_error_message.setStyleSheet("color: red")
        self.ui.number_density_error_message.setStyleSheet("color: red")
        self.ui.mass_error_message.setStyleSheet("color: red")

        # geometry
        geometry = str(self.parent.master_table_list_ui[self.key][self.data_type]['shape'].currentText())
        self.ui.geometry_label.setText(geometry)
        self.geometry_dimensions_defined = self._is_geometry_dimensions_defined()
        if self.geometry_dimensions_defined:
            self._calculate_and_display_geometry_volume()
        self.chemical_formula_defined = self._is_chemical_formula_defined()

        if self.chemical_formula_defined:
            self.total_number_of_atoms = self.parent.master_table_list_ui[self.key][
                self.data_type]['mass_density_infos']['total_number_of_atoms']
            list_ui_of_key = self.parent.master_table_list_ui[self.key]
            molecular_mass = list_ui_of_key[self.data_type]['mass_density_infos']['molecular_mass']
            self.total_molecular_mass = molecular_mass

        mass_density_list_ui = self.parent.master_table_list_ui[self.key][self.data_type]
        mass_density_infos = mass_density_list_ui['mass_density_infos']

        _mass_density = str(mass_density_list_ui['mass_density']['text'].text())
        self.ui.mass_density_line_edit.setText(_mass_density)

        _mass_density_checked = mass_density_infos['mass_density']['selected']
        _number_density_checked = mass_density_infos['number_density']['selected']

        _number_density = mass_density_infos['number_density']['value']
        self.ui.number_density_line_edit.setText(_number_density)

        _mass_value = mass_density_infos['mass']['value']
        self.ui.mass_line_edit.setText(_mass_value)

        if _mass_density_checked:
            self.ui.mass_density_radio_button.setChecked(True)
        elif _number_density_checked:
            self.ui.number_density_radio_button.setChecked(True)
        else:
            self.ui.mass_geometry_radio_button.setChecked(True)

        self.radio_button_changed()

        # if self.ui.number_density_radio_button.isChecked():
        #     self.ui.number_density_radio_button.setChecked(True)
        #     self.ui.mass_density_error_message.setVisible(not self.chemical_formula_defined)
        #     self.ui.number_density_error_message.setVisible(False)
        #
        # elif self.ui.mass_geometry_radio_button.isChecked():
        #     self.ui.mass_density_radio_button.setChecked(True)
        #     self.ui.mass_density_error_message.setVisible(False)
        #     self.ui.number_density_error_message.setVisible(False)
        #
        # else: # mass density selected
        #     self.ui.mass_density_error_message.setVisible(False)
        #     self.ui.number_density_error_message.setVisible(not self.chemical_formula_defined)

    def _is_chemical_formula_defined(self):
        if self.parent.master_table_list_ui[self.key][self.data_type]['material']['text'].text() == "":
            return False
        return True

    def _is_geometry_dimensions_defined(self):
        geometry_defined = str(self.ui.geometry_label.text())
        radius = str(self.parent.master_table_list_ui[self.key][self.data_type]['geometry']['radius']['value'].text())
        radius2 = str(self.parent.master_table_list_ui[self.key][self.data_type]['geometry']['radius2']['value'].text())
        height = str(self.parent.master_table_list_ui[self.key][self.data_type]['geometry']['height']['value'].text())

        if geometry_defined.lower() == 'cylindrical':
            if is_number(radius) and is_number(height):
                return True
        elif geometry_defined.lower() == 'spherical':
            if is_number(radius):
                return True
        else:
            if is_number(radius) and is_number(radius2) and is_number(height):
                return True

        return False

    def _calculate_and_display_geometry_volume(self):
        geometry_defined = str(self.ui.geometry_label.text())
        radius = str(self.parent.master_table_list_ui[self.key][self.data_type]['geometry']['radius']['value'].text())
        radius2 = str(self.parent.master_table_list_ui[self.key][self.data_type]['geometry']['radius2']['value'].text())
        height = str(self.parent.master_table_list_ui[self.key][self.data_type]['geometry']['height']['value'].text())

        if geometry_defined.lower() == 'cylindrical':
            volume = volume_of_cylinder(radius=radius, height=height)
        elif geometry_defined.lower() == 'spherical':
            volume = volume_of_sphere(radius=radius)
        else:
            volume = volume_of_hollow_cylinder(inner_radius=radius, outer_radius=radius2, height=height)

        str_volume = "{:.4}".format(volume)
        self.ui.volume_label.setText(str_volume)

    def mass_density_value_changed(self):
        # calculate number density if chemical formula defined
        if self.chemical_formula_defined:
            mass_density = np.float(self.ui.mass_density_line_edit.text())
            avogadro = scipy.constants.N_A
            number_density = mass_density * (avogadro / 1e24) * self.total_number_of_atoms / self.total_molecular_mass
            number_density = "{:.5}".format(number_density)
        else:
            number_density = 'N/A'
        self.ui.number_density_line_edit.setText(number_density)
        self.update_status_of_save_button()

    def number_density_value_changed(self):
        # calculate mass density if chemical formula defined
        if self.chemical_formula_defined:
            number_density = np.float(self.ui.number_density_line_edit.text())
            avogadro = scipy.constants.N_A
            mass_density = number_density * self.total_molecular_mass / self.total_number_of_atoms / (avogadro/1e24)
            mass_density = "{:.5}".format(mass_density)
        else:
            mass_density = 'N/A'
        self.ui.mass_density_line_edit.setText(mass_density)
        self.update_status_of_save_button()

    def mass_value_changed(self):
        if self.geometry_dimensions_defined and self.chemical_formula_defined:
            mass = np.float(self.ui.mass_line_edit.text())
            volume = np.float(self.ui.volume_label.text())
            avogadro = scipy.constants.N_A

            mass_density = mass / volume
            number_density = mass_density * (avogadro / 1e24) * self.total_number_of_atoms / self.total_molecular_mass
            number_density = "{:.5}".format(number_density)
            mass_density = "{:.5}".format(mass_density)
        else:
            mass_density = "N/A"
            number_density = "N/A"

        self.ui.mass_density_line_edit.setText(mass_density)
        self.ui.number_density_line_edit.setText(number_density)
        self.update_status_of_save_button()

    def radio_button_changed(self):
        mass_density_line_edit_status = False
        number_density_line_edit_status = False
        mass_line_edit_status = False
        if self.ui.mass_density_radio_button.isChecked():
            self.ui.mass_density_error_message.setVisible(False)
            self.ui.number_density_error_message.setVisible(not self.chemical_formula_defined)
            mass_density_line_edit_status = True
            self.ui.mass_error_message.setVisible(False)
        elif self.ui.number_density_radio_button.isChecked():
            self.ui.mass_density_error_message.setVisible(not self.chemical_formula_defined)
            self.ui.number_density_error_message.setVisible(False)
            number_density_line_edit_status = True
            self.ui.mass_error_message.setVisible(False)
        else:
            self.ui.mass_density_error_message.setVisible(not self.chemical_formula_defined)
            self.ui.number_density_error_message.setVisible(not self.chemical_formula_defined)
            mass_line_edit_status = True
            self.ui.mass_error_message.setVisible(not self.geometry_dimensions_defined)

        self.ui.mass_line_edit.setEnabled(mass_line_edit_status)
        self.ui.number_density_line_edit.setEnabled(number_density_line_edit_status)
        self.ui.mass_density_line_edit.setEnabled(mass_density_line_edit_status)

        self.update_status_of_save_button()

    def update_status_of_save_button(self):
        # check the active radio button and check if value is there to enable save button
        enabled_save_button = False
        if self.ui.mass_density_radio_button.isChecked():
            string_value = str(self.ui.mass_density_line_edit.text())
            if is_number(string_value):
                enabled_save_button = True
        elif self.ui.number_density_radio_button.isChecked():
            string_value = str(self.ui.number_density_line_edit.text())
            if is_number(string_value):
                enabled_save_button = True
        else:
            string_value = str(self.ui.mass_line_edit.text())
            if is_number(string_value) and self.chemical_formula_defined and \
                    self.geometry_dimensions_defined:
                enabled_save_button = True
        self.ui.ok.setEnabled(enabled_save_button)

    def save(self):
        # first validate fields in case user forgot to hit enter before leaving window
        if self.ui.mass_density_radio_button.isChecked():
            self.mass_density_value_changed()
        elif self.ui.number_density_radio_button.isChecked():
            self.number_density_value_changed()
        else:
            self.mass_value_changed()

        mass_density_list_ui = self.parent.master_table_list_ui[self.key][self.data_type]
        mass_density_infos = mass_density_list_ui['mass_density_infos']

        mass_density_flag = False
        number_density_flag = False
        mass_flag = False
        if self.ui.mass_density_radio_button.isChecked():
            mass_density_flag = True
        elif self.ui.number_density_radio_button.isChecked():
            number_density_flag = True
        else:
            mass_flag = True

        mass_density = str(self.ui.mass_density_line_edit.text())
        mass_density_list_ui['mass_density']['text'].setText(mass_density)
        mass_density_infos['mass_density']['value'] = mass_density
        mass_density_infos['mass_density']['selected'] = mass_density_flag

        number_density = str(self.ui.number_density_line_edit.text())
        mass_density_infos['number_density']['value'] = number_density
        mass_density_infos['number_density']['selected'] = number_density_flag

        mass = str(self.ui.mass_line_edit.text())
        mass_density_infos['mass']['value'] = mass
        mass_density_infos['mass']['selected'] = mass_flag

    def accept(self):
        self.save()
        o_table = TableRowHandler(main_window=self.parent)
        o_table.transfer_widget_states(from_key=self.key, data_type=self.data_type)
        self.close()

    def reject(self):
        self.close()

    def closeEvent(self, c):
        self.parent.mass_density_ui = None
        self.parent.mass_density_ui_position = self.pos()
