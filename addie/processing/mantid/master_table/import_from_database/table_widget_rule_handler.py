from __future__ import (absolute_import, division, print_function)

import numpy as np

from qtpy.QtWidgets import QComboBox, QTableWidgetItem
from qtpy import QtCore

from addie.utilities.general import generate_random_key
from addie.processing.mantid.master_table.tree_definition import LIST_SEARCH_CRITERIA
from addie.utilities.gui_handler import unlock_signals_ui


class TableWidgetRuleHandler:

    def __init__(self, parent=None):
        self.parent = parent
        self.table_ui = parent.ui.tableWidget
        self.row_height = parent.row_height

    def define_unique_rule_name(self, row):
        """this method makes sure that the name of the rule defined is unique and does not exist already"""
        nbr_row = self.table_ui.rowCount()
        list_rule_name = []
        for _row in np.arange(nbr_row):
            if self.table_ui.item(_row, 1):
                _rule_name = str(self.table_ui.item(_row, 1).text())
                list_rule_name.append(_rule_name)

        offset = 0
        while True:
            if ("{}".format(offset + row)) in list_rule_name:
                offset += 1
            else:
                return offset + row

    def add_row(self, row=-1):
        """this add a default row to the table that takes care
        of the rules"""
        _random_key = generate_random_key()

        _list_ui_for_this_row = {}
        _list_ui_to_unlock = []

        self.table_ui.insertRow(row)
        self.table_ui.setRowHeight(row, self.row_height)

        # key
        _item = QTableWidgetItem("{}".format(_random_key))
        self.table_ui.setItem(row, 0, _item)

        # rule #
        _rule_name = self.define_unique_rule_name(row)
        _item = QTableWidgetItem("{}".format(_rule_name))
        _item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        self.table_ui.setItem(row, 1, _item)

        # search argument
        _widget = QComboBox()
        _list_ui_for_this_row['list_items'] = _widget
        list_items = LIST_SEARCH_CRITERIA[self.parent.parent.instrument['short_name'].lower()]
        _widget.addItems(list_items)
        self.table_ui.setCellWidget(row, 2, _widget)
        _widget.blockSignals(True)
        _list_ui_to_unlock.append(_widget)
        _widget.currentIndexChanged.connect(lambda value=list_items[0],
                                            key = _random_key:
                                            self.parent.list_item_changed(value, key))

        # criteria
        list_criteria = ['is', 'contains']
        _widget = QComboBox()
        _list_ui_for_this_row['list_criteria'] = _widget
        _widget.addItems(list_criteria)
        self.table_ui.setCellWidget(row, 3, _widget)
        _widget.blockSignals(True)
        _list_ui_to_unlock.append(_widget)
        _widget.currentIndexChanged.connect(lambda value=list_criteria[0],
                                            key = _random_key:
                                            self.parent.list_criteria_changed(value, key))

        # argument
        _widget = QComboBox()
        _widget.setEditable(True)
        _list_ui_for_this_row['list_items_value'] = _widget
        list_values = list(self.parent.metadata['Chemical Formula'])
        _widget.addItems(list_values)
        self.table_ui.setCellWidget(row, 4, _widget)
        _widget.blockSignals(True)
        _list_ui_to_unlock.append(_widget)
        _widget.editTextChanged.connect(lambda value=list_values[0],
                                        key = _random_key:
                                        self.parent.list_argument_changed(value, key))
        _widget.currentIndexChanged.connect(lambda value=list_values[0],
                                            key = _random_key:
                                            self.parent.list_argument_index_changed(value, key))

        if row == 0:
            self.table_ui.horizontalHeader().setVisible(True)

        unlock_signals_ui(list_ui=_list_ui_to_unlock)

        self.parent.list_ui[_random_key] = _list_ui_for_this_row
        self.parent.check_all_filter_widgets()

    def update_list_value_of_given_item(self, index=-1, key=None):
        """When user clicks, in the Tablewidget rule, the first row showing the name of the list element,
         for example 'Chemical formula', the list of available values will update automatically"""

        list_ui = self.parent.list_ui
        list_metadata = self.parent.metadata

        item_name = list_ui[key]['list_items'].itemText(index)

        combobox_values = list_ui[key]['list_items_value']
        combobox_values.blockSignals(True)
        combobox_values.clear()
        combobox_values.addItems(list(list_metadata[item_name]))
        combobox_values.blockSignals(False)
