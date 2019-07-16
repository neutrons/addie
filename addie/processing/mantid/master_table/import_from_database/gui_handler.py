from __future__ import (absolute_import, division, print_function)

from qtpy.QtWidgets import QTableWidgetItem

import copy
import numpy as np

from addie.utilities.gui_handler import TableHandler
from addie.utilities.general import json_extractor


class FilterTableHandler:
    """Class to work with the table filter (top table of second tab)"""

    def __init__(self, table_ui=None):
        self.table_ui = table_ui

    def return_first_row_for_this_item_value(
            self, string_to_find="", column_to_look_for=-1):
        """return the first row found where the item value matches the string passed.
        If the string can not be found, return -1
        """
        nbr_rows = self.table_ui.rowCount()
        for _row in np.arange(nbr_rows):
            item_value = str(
                self.table_ui.item(
                    _row, column_to_look_for).text())
            if string_to_find == item_value:
                return _row
        return -1

    def get_combobox_value(self, row=-1, column=-1):
        combobox = self.table_ui.cellWidget(row, column)
        return str(combobox.currentText())

    def get_keyword_name(self, row=-1):
        """this method returns the value of the keyword selected for the given row"""
        return self.get_combobox_value(row=row, column=2)

    def get_criteria(self, row=-1):
        """this method returns the value of the criteria (is or contains) selected for the given row"""
        return self.get_combobox_value(row=row, column=3)

    def get_string_to_look_for(self, row=-1):
        """this method returns the value of the string to look for in all the metadata for the given keyword"""
        return self.get_combobox_value(row=row, column=4)


class FilterResultTableHandler:
    """class to work with the table listing the rows that match the rules"""

    def __init__(self, table_ui=None):
        self.table_ui = table_ui

    def get_column_of_given_keyword(self, keyword=''):
        """looking through all the columns headers to find the one that match the keyword argument. If it
        does, return the column index. If this keyword can not be found, return -1"""
        nbr_columns = self.table_ui.columnCount()
        for _col in np.arange(nbr_columns):
            column_header = str(
                self.table_ui.horizontalHeaderItem(_col).text())
            if column_header == keyword:
                return _col
        return -1

    def get_rows_of_matching_string(
            self,
            column_to_look_for=-1,
            string_to_find='',
            criteria='is'):
        nbr_row = self.table_ui.rowCount()
        list_matching_rows = []
        for _row in np.arange(nbr_row):
            string_at_this_row = str(
                self.table_ui.item(
                    _row, column_to_look_for).text())
            if criteria == 'is':
                if string_at_this_row == string_to_find:
                    list_matching_rows.append(_row)
            elif criteria == 'contains':
                if string_to_find in string_at_this_row:
                    list_matching_rows.append(_row)
        return list_matching_rows

    def get_number_of_visible_rows(self):
        nbr_row = self.table_ui.rowCount()
        nbr_visible_row = 0
        for _row in np.arange(nbr_row):
            if not self.table_ui.isRowHidden(_row):
                nbr_visible_row += 1

        return nbr_visible_row


class GuiHandler:

    @staticmethod
    def preview_widget_status(window_ui, enabled_widgets=False):
        """enable or not all the widgets related to the preview tab"""
        window_ui.search_logo_label.setEnabled(enabled_widgets)
        window_ui.name_search.setEnabled(enabled_widgets)
        window_ui.clear_search_button.setEnabled(enabled_widgets)
        window_ui.list_of_runs_label.setEnabled(enabled_widgets)

    @staticmethod
    def filter_widget_status(window_ui, enabled_widgets=False):
        """enable or not all the widgets related to the filter tab"""
        window_ui.tableWidget.setEnabled(enabled_widgets)
        window_ui.add_criteria_button.setEnabled(enabled_widgets)
        window_ui.filter_result_label.setEnabled(enabled_widgets)
        window_ui.tableWidget_filter_result.setEnabled(enabled_widgets)

    @staticmethod
    def check_import_button(parent):
        window_ui = parent.ui

        enable_import = False

        if window_ui.toolBox.currentIndex() == 0:  # import everything

            nbr_row = window_ui.tableWidget_all_runs.rowCount()
            if nbr_row > 0:
                enable_import = True

        else:  # rule tab

            o_gui = FilterResultTableHandler(
                table_ui=window_ui.tableWidget_filter_result)
            nbr_row_visible = o_gui.get_number_of_visible_rows()
            if nbr_row_visible > 0:
                enable_import = True

        window_ui.import_button.setEnabled(enable_import)


class ImportFromDatabaseTableHandler:

    def __init__(self, table_ui=None, parent=None):
        self.table_ui = table_ui
        self.parent = parent
        self.parent_parent = parent.parent

    def refresh_table(self, nexus_json={}):
        """This function takes the nexus_json returns by ONCat and
              fill the filter table with only the metadata of interests. Those
              are defined in the oncat_metadata_filters dictionary (coming from the json config)

              ex: title, chemical formula, mass density, Sample Env. Device and proton charge
              """
        oncat_metadata_filters = self.parent_parent.oncat_metadata_filters

        TableHandler.clear_table(self.table_ui)
        for _row, _json in enumerate(nexus_json):
            self.table_ui.insertRow(_row)
            for _column, metadata_filter in enumerate(oncat_metadata_filters):
                self._set_table_item(json=copy.deepcopy(_json),
                                     metadata_filter=metadata_filter,
                                     row=_row,
                                     col=_column)

            self.parent.first_time_filling_table = False

    def _set_table_item(self, json=None, metadata_filter={}, row=-1, col=-1):
        """Populate the filter metadada table from the oncat json file of only the arguments specified in
        the config.json file (oncat_metadata_filters)"""

        table_ui = self.table_ui

        def _format_proton_charge(raw_proton_charge):
            _proton_charge = raw_proton_charge / 1e12
            return "{:.3}".format(_proton_charge)

        title = metadata_filter['title']
        list_args = metadata_filter["path"]
        argument_value = json_extractor(json=json,
                                        list_args=copy.deepcopy(list_args))

        # if title is "Proton Charge" change format of value displayed
        if title == "Proton Charge (C)":
            argument_value = _format_proton_charge(argument_value)

        if table_ui is None:
            table_ui = self.ui.tableWidget_filter_result

        if self.parent.first_time_filling_table:
            table_ui.insertColumn(col)
            _item_title = QTableWidgetItem(title)
            table_ui.setHorizontalHeaderItem(col, _item_title)
            width = metadata_filter["column_width"]
            table_ui.setColumnWidth(col, width)

        _item = QTableWidgetItem("{}".format(argument_value))
        table_ui.setItem(row, col, _item)

    def refresh_preview_table(self, nexus_json=[]):
        """This function takes the nexus_json returns by ONCat using the ONCat template.
        It will then fill the Preview table to just inform the users of what are the
        infos of all the runs he is about to import or filter.
        """
        table_ui = self.table_ui
        TableHandler.clear_table(table_ui)

        oncat_template = self.parent.oncat_template
        for _row, json in enumerate(nexus_json):

            table_ui.insertRow(_row)

            for _col in oncat_template.keys():

                if self.parent.first_time_filling_preview_table:
                    title = oncat_template[_col]['title']
                    units = oncat_template[_col]['units']
                    if units:
                        title = "{} ({})".format(title, units)

                    table_ui.insertColumn(_col)
                    _item_title = QTableWidgetItem(title)
                    table_ui.setHorizontalHeaderItem(_col, _item_title)

                path = oncat_template[_col]['path']
                list_path = path.split(".")
                argument_value = json_extractor(
                    json=json, list_args=copy.deepcopy(list_path))

                # used to evaluate expression returned by ONCat
                if oncat_template[_col]['formula']:

                    # the expression will look like '{value/10e11}'
                    # so value will be replaced by argument_value and the
                    # expression will be evaluated using eval
                    value = argument_value  # noqa: F841
                    argument_value = eval(oncat_template[_col]['formula'])
                    argument_value = argument_value.pop()

                _item = QTableWidgetItem("{}".format(argument_value))
                table_ui.setItem(_row, _col, _item)

            self.parent.first_time_filling_preview_table = False
