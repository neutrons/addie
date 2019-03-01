from __future__ import (absolute_import, division, print_function)
import numpy as np

from qtpy.QtWidgets import QDialog, QTableWidgetItem, QComboBox, QCheckBox, QSpacerItem, QSizePolicy, QHBoxLayout, \
        QWidget
from addie.utilities import load_ui
from qtpy import QtCore


class GlobalRuleHandler:

    def __init__(self, parent=None):
        o_global = GlobalRuleWindow(parent=parent)
        o_global.show()


class GlobalRuleWindow(QDialog):

    list_of_rule_names = []   # ['0', '1', '2']

    def __init__(self, parent=None):
        self.parent = parent

        QDialog.__init__(self, parent=parent)
        self.ui = load_ui('filter_rule_editor.ui', baseinstance=self)
        #self.ui = UiDialog()
        #self.ui.setupUi(self)

        self.init_widgets()
        self.load_global_rule_dict()
        self.refresh_global_rule()
        self.check_widgets()

    def get_list_of_rule_names(self):
        """make the list of rule name defined in the previous ui"""
        table_widget = self.parent.ui.tableWidget
        nbr_row = table_widget.rowCount()
        list_of_rule_names = []
        for _row in np.arange(nbr_row):
            _name = str(table_widget.item(_row, 1).text())
            list_of_rule_names.append(_name)
        return list_of_rule_names

    def init_widgets(self):
        list_of_rule_names = self.get_list_of_rule_names()
        self.list_of_rule_names = list_of_rule_names
        for _col_index, _name in enumerate(list_of_rule_names):
            self.ui.tableWidget.insertColumn(_col_index+2)
            item_title = QTableWidgetItem(_name)
            self.ui.tableWidget.setHorizontalHeaderItem(_col_index+2, item_title)

    def load_global_rule_dict(self):
        """Using the global_rule_dict, populate the interface and check the right rules"""
        global_rule_dict = self.parent.global_rule_dict
        list_of_rule_names = self.list_of_rule_names
        nbr_columns = self.ui.tableWidget.columnCount()

        for _row, _key in enumerate(global_rule_dict.keys()):
            self.add_row(row=_row)

            name_of_group = _key
            self.ui.tableWidget.item(_row, 0).setText(str(name_of_group))

            list_of_rules_for_this_group = global_rule_dict[_key]['list_rules']
            for _col_index, _rule in enumerate(list_of_rule_names):
                if _rule in list_of_rules_for_this_group:
                    self.ui.tableWidget.cellWidget(_row, _col_index+2).children()[1].setChecked(True)

            inner_rule = global_rule_dict[_key]['inner_rule']
            _inner_index = self.ui.tableWidget.cellWidget(_row, nbr_columns-1).findText(inner_rule)
            self.ui.tableWidget.cellWidget(_row, nbr_columns-1).blockSignals(True)
            self.ui.tableWidget.cellWidget(_row, nbr_columns-1).setCurrentIndex(_inner_index)
            self.ui.tableWidget.cellWidget(_row, nbr_columns-1).blockSignals(False)

            if _row > 0:
                outer_rule = global_rule_dict[_key]['outer_rule']
                _outer_index = self.ui.tableWidget.cellWidget(_row, 1).findText(outer_rule)
                self.ui.tableWidget.cellWidget(_row, 1).blockSignals(True)
                self.ui.tableWidget.cellWidget(_row, 1).setCurrentIndex(_outer_index)
                self.ui.tableWidget.cellWidget(_row, 1).blockSignals(False)

    def check_widgets(self):
        nbr_row = self.ui.tableWidget.rowCount()
        enable_remove_widget = True
        if nbr_row == 0:
            enable_remove_widget = False
        self.ui.remove_group_button.setEnabled(enable_remove_widget)

    def define_unique_group_name(self, row):
        """this method makes sure that the name of the group defined is unique and does not exist already"""
        nbr_row = self.ui.tableWidget.rowCount()
        list_group_name = []
        for _row in np.arange(nbr_row):
            if self.ui.tableWidget.item(_row, 0):
                if self.ui.tableWidget.item(_row, 1):
                    _group_name = str(self.ui.tableWidget.item(_row, 1).text())
                    list_group_name.append(_group_name)

        offset = 0
        while True:
            if ("{}".format(offset+row)) in list_group_name:
                offset += 1
            else:
                return "{}".format(offset+row)

    def add_row(self, row=-1, check_new_row=False):
        self.ui.tableWidget.insertRow(row)
        list_of_widgets_to_unlock = []

        # group name
        _column = 0
        _group_name = self.define_unique_group_name(row)
        _item = QTableWidgetItem(_group_name)
        _item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        self.ui.tableWidget.setItem(row, _column, _item)

        # group to group rule
        list_options = ["and", "or"]
        _column += 1
        if row > 0:
            _widget = QComboBox()
            _widget.addItems(list_options)
            self.ui.tableWidget.setCellWidget(row, _column, _widget)
            _widget.blockSignals(True)
            list_of_widgets_to_unlock.append(_widget)
            _widget.currentIndexChanged.connect(lambda value=list_options[0]:
                                                self.combobox_changed(value))

        else:
            _item = QTableWidgetItem("N/A")
            _item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget.setItem(row, _column, _item)

        # rule columns
        _column += 1
        for _offset in np.arange(len(self.list_of_rule_names)):
            _row_layout = QHBoxLayout()
            _widget = QCheckBox()
            _widget.blockSignals(True)
            if check_new_row and _offset == row:
                _widget.setCheckState(QtCore.Qt.Checked)
            list_of_widgets_to_unlock.append(_widget)
            _widget.stateChanged.connect(lambda value=0:
                                         self.checkbox_changed(value))

            _spacer1 = QSpacerItem(40,20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            _row_layout.addItem(_spacer1)
            _row_layout.addWidget(_widget)
            _spacer2 = QSpacerItem(40,20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            _row_layout.addItem(_spacer2)
            _rule_widget = QWidget()
            _rule_widget.setLayout(_row_layout)
            self.ui.tableWidget.setCellWidget(row, _column+_offset, _rule_widget)

        # inner group rule
        _column += len(self.list_of_rule_names)
        _widget = QComboBox()
        _widget.blockSignals(True)
        list_of_widgets_to_unlock.append(_widget)
        _widget.setEnabled(False)
        _widget.currentIndexChanged.connect(lambda value=list_options[0]:
                                            self.combobox_changed(value))

        list_options = ["and", "or"]
        _widget.addItems(list_options)
        self.ui.tableWidget.setCellWidget(row, _column, _widget)
        self.unlock_signals_ui(list_of_widgets_to_unlock)

    def unlock_signals_ui(self, list_ui=[]):
        if list_ui == []:
            return

        for _ui in list_ui:
            _ui.blockSignals(False)

    def check_status_of_inner_rule(self):
        """the inner rule ['and', 'or'] does not need to be enabled when there is only 1 (or zero)
        rule checked in the same row"""
        nbr_row = self.ui.tableWidget.rowCount()
        nbr_total_columns = self.ui.tableWidget.columnCount()
        nbr_rules = nbr_total_columns - 3

        for _row in np.arange(nbr_row):
            enabled_inner_rule_combobox = False
            if nbr_rules > 1:
                nbr_rules_checked = 0
                for _rule_index in np.arange(nbr_rules):
                    checkbox_ui = self.ui.tableWidget.cellWidget(_row, _rule_index + 2).children()[1]
                    is_checkbox_checked = checkbox_ui.isChecked()
                    if is_checkbox_checked:
                        nbr_rules_checked += 1
                if nbr_rules_checked > 1:
                    enabled_inner_rule_combobox = True
            self.ui.tableWidget.cellWidget(_row, nbr_total_columns-1).setEnabled(enabled_inner_rule_combobox)

    def checkbox_changed(self, value):
        self.check_status_of_inner_rule()
        self.refresh_global_rule()

    def combobox_changed(self, value):
        self.refresh_global_rule()

    def _retrieve_group_relation(self, row=-1, group_type='inner'):

        nbr_column = self.ui.tableWidget.columnCount()

        if group_type == 'inner':
            column = nbr_column - 1
        else:
            if row == 0:
                return ""
            column = 1

        widget = self.ui.tableWidget.cellWidget(row, column)
        if widget:
            return widget.currentText()
        else:
            return ""

    def _retrieve_rules_checked(self, row=-1):
        nbr_rules = len(self.list_of_rule_names)

        list_of_rules_checked = []

        global_offset_up_to_rule_name = 2
        for _index_rule in np.arange(nbr_rules):
            _widget = self.ui.tableWidget.cellWidget(row, global_offset_up_to_rule_name+_index_rule).children()[1]
            if _widget.checkState() == QtCore.Qt.Checked:
                rule_name= str(self.ui.tableWidget.horizontalHeaderItem(global_offset_up_to_rule_name+_index_rule).text())
                list_of_rules_checked.append("#{}".format(rule_name))

        return list_of_rules_checked

    def refresh_global_rule(self):
        self.save_global_rule_dict()
        global_rule = self.parent.create_global_rule_string()
        self.ui.rule_result.setText(global_rule)

    # Event Handler
    def add_group(self):
        self.ui.remove_group_button.setEnabled(True)
        nbr_row = self.ui.tableWidget.rowCount()
        self.add_row(row=nbr_row, check_new_row=True)

    def remove_group(self):
        _select = self.ui.tableWidget.selectedRanges()
        if not _select:
            return
        else:
            row = _select[0].topRow()
            self.ui.tableWidget.removeRow(row)
        self.check_widgets()
        self.refresh_global_rule()

    def save_global_rule_dict(self):
        nbr_row = self.ui.tableWidget.rowCount()
        total_nbr_columns = self.ui.tableWidget.columnCount()
        nbr_rules = total_nbr_columns - 3
        list_of_rule_names = self.list_of_rule_names

        global_rule_dict = {}
        for _row in np.arange(nbr_row):
            _row_rule_dict = {}

            group_name = str(self.ui.tableWidget.item(_row, 0).text())

            if _row == 0:
                outer_rule = None
            else:
                outer_rule = str(self.ui.tableWidget.cellWidget(_row, 1).currentText())

            inner_rule = str(self.ui.tableWidget.cellWidget(_row, total_nbr_columns-1).currentText())

            list_rules_checked = []
            for _rule_index in np.arange(nbr_rules):
                _is_checked = self.ui.tableWidget.cellWidget(_row, _rule_index+2).children()[1].isChecked()

                if _is_checked:
                    _name = list_of_rule_names[_rule_index]
                    list_rules_checked.append(_name)

            _row_rule_dict['group_name'] = group_name
            _row_rule_dict['list_rules'] = list_rules_checked
            _row_rule_dict['inner_rule'] = inner_rule
            _row_rule_dict['outer_rule'] = outer_rule

            global_rule_dict[_row] = _row_rule_dict

        self.parent.global_rule_dict = global_rule_dict

    def accept(self):
        # copy global rule into import_from_database ui
        self.save_global_rule_dict()
        global_rule_string = self.parent.create_global_rule_string()
        self.parent.ui.global_rule_lineedit.setText(global_rule_string)
        self.parent.update_rule_filter()
        self.close()
