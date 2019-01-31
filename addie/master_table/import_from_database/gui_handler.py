import copy

try:
    from PyQt4.QtGui import QTableWidgetItem
    from PyQt4 import QtGui, QtCore
except:
    try:
        from PyQt5.QtWidgets import QTableWidgetItem
        from PyQt5 import QtGui, QtCore
    except:
        raise ImportError("Requires PyQt4 or PyQt5")

from addie.utilities.gui_handler import TableHandler


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
        if window_ui.ipts_radio_button.isChecked():
            if str(window_ui.ipts_lineedit.text()).strip() != "":
                if parent.ipts_exist:
                    enable_import = True
            else:
                enable_import = True
        else:
            if str(window_ui.run_number_lineedit.text()).strip() != "":
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

    def _json_extractor(self, json=None, list_args=[]):
        if len(list_args) == 1:
            return json[list_args[0]]
        else:
            return self._json_extractor(json[list_args.pop(0)],
                                        list_args=list_args)

    def _set_table_item(self, json=None, metadata_filter={}, row=-1, col=-1):
        """Populate the filter metadada table from the oncat json file of only the arguments specified in
        the config.json file (oncat_metadata_filters)"""

        table_ui = self.table_ui

        def _format_proton_charge(raw_proton_charge):
            _proton_charge = raw_proton_charge / 1e12
            return "{:.3}".format(_proton_charge)

        title = metadata_filter['title']
        list_args = metadata_filter["path"]
        argument_value = self._json_extractor(json=json, list_args=copy.deepcopy(list_args))

        # if title is "Proton Charge" change format of value displayed
        if title == "Proton Charge (C)":
            argument_value = _format_proton_charge(argument_value)

        if table_ui is None:
            table_ui = self.ui.tableWidget_filter_result

        if self.parent.first_time_filling_table:
            table_ui.insertColumn(col)
            _item_title = QTableWidgetItem(title)
            table_ui.setHorizontalHeaderItem(col, _item_title)
        #            width = metadata_filter["column_width"]
        #            table_ui.setColumnWidth(col, width)

        _item = QTableWidgetItem("{}".format(argument_value))
        table_ui.setItem(row, col, _item)
