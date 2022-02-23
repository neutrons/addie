from __future__ import (absolute_import, division, print_function)

from qtpy.QtWidgets import QDialog
from addie.utilities import load_ui

from addie.processing.mantid.master_table.table_row_handler import TableRowHandler

from addie.processing.mantid.master_table.tree_definition import INDEX_OF_COLUMNS_WITH_SCATTERING_LEVELS


class ScatteringSetter(QDialog):
    column = 0

    def __init__(self, parent=None, key=None):
        self.parent = parent
        self.key = key

        QDialog.__init__(self, parent=parent)
        self.ui = load_ui('self_scattering_setter.ui', baseinstance=self)

        self.group_widgets()
        self.init_widgets_layout()
        self.init_widgets_content()

        if parent.scattering_ui_position:
            self.move(parent.scattering_ui_position)

        o_table = TableRowHandler(main_window=self.parent)
        o_table.transfer_widget_states(
            from_key=self.key)

        self.check_save_button()
        self.set_column_index()

    def set_column_index(self):
        self.column = INDEX_OF_COLUMNS_WITH_SCATTERING_LEVELS[0]

    def group_widgets(self):
        self.group = {'lower': [self.ui.lower_label,
                                self.ui.lower_value],
                      'upper': [self.ui.upper_label,
                                self.ui.upper_value],
                      'format': [self.ui.label]
                      }

    def __get_label_value(self, scattering_type):
        '''helper function to retrieve value of labels from master table.
        :argument:
        scattering_type being 'lower' or 'upper'
        '''
        return str(self.parent.master_table_list_ui[self.key]
                   ['self_scattering_level'][scattering_type]['value'].text())

    def __set_label_value(self, scattering_type, value,val_list=False):
        '''helper function to set value of label in master table.
        :argument:
        scattering_type being 'lower' or 'upper'
        value: value to set
        '''

        self.parent.master_table_list_ui[self.key]['self_scattering_level'][scattering_type]['value'].setText(
            value)
        if val_list:
            if len(value.strip()) == 0:
                list_tmp = []
            else:
                list_tmp = self.limit_str2list(value)
            self.parent.master_table_list_ui[self.key]['self_scattering_level'][scattering_type]['val_list'] = list_tmp

    def init_widgets_content(self):
        '''populate the widgets using the value from the master table'''

        upper = '20.0,20.0,20.0,30.0,30.0,10.0'
        lower = '30.0,25.0,30.0,40.0,40.0,15.0'

        lower = self.__get_label_value('lower')
        upper = self.__get_label_value('upper')

        self.ui.lower_value.setText(lower)
        self.ui.upper_value.setText(upper)

    def init_widgets_layout(self):
        '''using the shape defined for this row, will display the right widgets and will populate
        them with the right values'''
        self.ui.lower_label.setText("Lower Limit")
        self.ui.upper_label.setText("Upper Limit")
        self.ui.label.setText("Limit Format: \"20.0,20.0,20.0,30.0,30.0,10.0\"")
        return

    def value_changed(self, text):
        self.check_save_button()

    def check_save_button(self):
        save_button_status = False

        lower = str(self.ui.lower_value.text())
        upper = str(self.ui.upper_value.text())

        if self.check_list_format(lower) and self.check_list_format(upper):
            save_button_status = True
        else:
            if len(lower.strip()) == 0 and len(upper.strip()) == 0:
                save_button_status = True

        self.ui.ok.setEnabled(save_button_status)

    def accept(self):

        upper = '20.0,20.0,20.0,30.0,30.0,10.0'
        lower = '30.0,25.0,30.0,40.0,40.0,15.0'

        lower = str(self.ui.lower_value.text())
        upper = str(self.ui.upper_value.text())
        self.__set_label_value('lower', lower, True)
        self.__set_label_value('upper', upper, True)

        o_table = TableRowHandler(main_window=self.parent)
        o_table.transfer_widget_states(
            from_key=self.key)

        self.parent.check_master_table_column_highlighting(column=self.column)
        self.close()

    def closeEvent(self, c):
        self.parent.scattering_ui_position = self.pos()

    def limit_str2list(self,lim_str):
        lim_list = lim_str.split(",")
        return self.cast_list(lim_list,float)

    def cast_list(self,cast_list, data_type):
        return list(map(data_type, cast_list))

    def check_list_format(self,lim_str):
        try:
            lim_list = lim_str.split(",")
            self.cast_list(lim_list,float)
            if len(lim_list) == 6:
                return True
        except:
            return False
