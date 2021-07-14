from __future__ import (absolute_import, division, print_function)

from qtpy.QtWidgets import QDialog
from addie.utilities import load_ui

from addie.processing.mantid.master_table.table_row_handler import TableRowHandler

from addie.processing.mantid.master_table.tree_definition import INDEX_OF_COLUMNS_WITH_RESONANCE_INFOS


class ResonanceSetter(QDialog):
    column = 0

    def __init__(self, parent=None, key=None, data_type='sample'):
        self.parent = parent
        self.key = key
        self.data_type = data_type

        QDialog.__init__(self, parent=parent)
        self.ui = load_ui('resonance_setter.ui', baseinstance=self)

        self.group_widgets()
        self.init_widgets_layout()
        self.init_widgets_content()

        if parent.resonance_ui_position:
            self.move(parent.resonance_ui_position)

        self.check_save_button()
        self.set_column_index()
        self.populate_axis()

    def set_column_index(self):
        self.column = INDEX_OF_COLUMNS_WITH_RESONANCE_INFOS[0] if self.data_type == 'sample' else \
            INDEX_OF_COLUMNS_WITH_RESONANCE_INFOS[1]

    def group_widgets(self):
        self.group = {'axis': [self.ui.axis_label,
                               self.ui.axis_value,
                               self.ui.axis_units],
                      'lower': [self.ui.lower_label,
                                self.ui.lower_value,
                                self.ui.lower_units],
                      'upper': [self.ui.upper_label,
                                self.ui.upper_value,
                                self.ui.upper_units],
                      'format': [self.ui.format_label]
                      }

    def populate_axis(self):
        self.ui.axis_value.addItem("None")
        self.ui.axis_value.addItem("Energy")
        self.ui.axis_value.addItem("Wavelength")
        axis = self.__get_label_value('axis')
        self.ui.axis_value.setCurrentText(axis)

    def __get_label_value(self, resonance_type):
        '''helper function to retrieve value of labels from master table.
        :argument:
        resonance_type being 'axis', 'lower' or 'upper'
        '''
        return str(self.parent.master_table_list_ui[self.key]
                   [self.data_type]['resonance'][resonance_type]['value'].text())

    def __set_label_value(self, resonance_type, value,val_list=False):
        '''helper function to set value of label in master table.
        :argument:
        resonance_type being 'axis', 'lower' or 'upper'
        value: value to set
        '''
        self.parent.master_table_list_ui[self.key][self.data_type]['resonance'][resonance_type]['value'].setText(
            value)
        if val_list:
            self.parent.master_table_list_ui[self.key][self.data_type]['resonance']\
                [resonance_type]['lim_list'] = self.limit_str2list(value)

    def init_widgets_content(self):
        '''populate the widgets using the value from the master table'''

        upper = 'N/A'
        lower = 'N/A'

        lower = self.__get_label_value('lower')
        upper = self.__get_label_value('upper')

        self.ui.lower_value.setText(lower)
        self.ui.upper_value.setText(upper)

    def init_widgets_layout(self):
        '''using the shape defined for this row, will display the right widgets and will populate
        them with the right values'''
        self.ui.axis_label.setText("Axis")
        self.ui.lower_label.setText("Lower Limit")
        self.ui.upper_label.setText("Upper Limit")
        self.ui.format_label.setText("Limit Format: \"1,2,3,4,5\"")
        return

    def value_changed(self, text):
        self.check_save_button()

    def check_save_button(self):
        save_button_status = False

        lower = str(self.ui.lower_value.text())
        upper = str(self.ui.upper_value.text())

        if self.is_list(lower) and self.is_list(upper):
            save_button_status = True

        self.ui.ok.setEnabled(save_button_status)

    def accept(self):

        lower = 'N/A'
        upper = 'N/A'

        axis = str(self.ui.axis_value.currentText())
        lower = str(self.ui.lower_value.text())
        upper = str(self.ui.upper_value.text())
        self.__set_label_value('axis', axis)
        self.__set_label_value('lower', lower,True)
        self.__set_label_value('upper', upper,True)

        o_table = TableRowHandler(main_window=self.parent)
        o_table.transfer_widget_states(
            from_key=self.key, data_type=self.data_type)

        self.parent.check_master_table_column_highlighting(column=self.column)

        self.close()

    def closeEvent(self, c):
        self.parent.resonance_ui_position = self.pos()

    def limit_str2list(self,lim_str):
        lim_list = lim_str.split(",")
        return self.cast_list(lim_list,float)

    def cast_list(self,cast_list, data_type):
        return list(map(data_type, cast_list))

    def is_list(self,lim_str):
        try:
            lim_list = lim_str.split(",")
            self.cast_list(lim_list,float)
            return True
        except:
            return False
