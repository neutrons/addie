try:
    from PyQt4.QtGui import QDialog
except:
    try:
        from PyQt5.QtWidgets import QDialog
    except:
        raise ImportError("Requires PyQt4 or PyQt5")

from addie.ui_mass_density import Ui_Dialog as UiDialog


class MassDensityHandler:

    def __init__(self, parent=None, key=None, data_type='sample'):
        if parent.mass_density_ui is None:
            o_mass = MassDensityWindow(parent=parent, key=key, data_type=data_type)
            o_mass.show()
            parent.mass_density_ui = o_mass
        else:
            parent.mass_density_ui.setFocus()
            parent.mass_density_ui.activateWindow()


class MassDensityWindow(QDialog):

    chemical_formula_defined = False

    def __init__(self, parent=None, key=None, data_type='sample'):
        self.parent = parent
        self.key = key
        self.data_type = data_type

        QDialog.__init__(self, parent=parent)
        self.ui = UiDialog()
        self.ui.setupUi(self)

        self.init_widgets()

    def init_widgets(self):
        self.ui.number_density_units.setText(u"Atoms/\u212B\u00B3")
        self.ui.mass_density_label.setText(u"g/cm\u00B3")

        # error messages
        self.ui.mass_density_error_message.setStyleSheet("color: red")
        self.ui.number_density_error_message.setStyleSheet("color: red")

        # geometry
        geometry = str(self.parent.master_table_list_ui[self.key][self.data_type]['shape'].currentText())
        self.ui.geometry_label.setText(geometry)

        self.chemical_formula_defined = self._is_chemical_formula_defined()

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

    def radio_button_changed(self):
        if self.ui.mass_density_radio_button.isChecked():
            self.ui.mass_density_error_message.setVisible(False)
            self.ui.number_density_error_message.setVisible(not self.chemical_formula_defined)
        elif self.ui.number_density_radio_button.isChecked():
            self.ui.mass_density_error_message.setVisible(not self.chemical_formula_defined)
            self.ui.number_density_error_message.setVisible(False)
        else:
            self.ui.mass_density_error_message.setVisible(False)
            self.ui.number_density_error_message.setVisible(False)

    def save(self):
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
        self.parent.mass_density_ui = None
        self.save()
        self.close()

    def reject(self):
        self.parent.mass_density_ui = None
        self.close()

    def closeEvent(self, c):
        pass

