from collections import OrderedDict
import copy
import numpy as np

try:
    from PyQt4.QtGui import QDialog, QComboBox, QLineEdit, QPushButton, QWidget, QHBoxLayout, QLabel, \
        QTableWidgetItem, QApplication
    from PyQt4 import QtGui, QtCore
except:
    try:
        from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit, QPushButton, QWidget, QHBoxLayout, QLabel, \
            QTableWidgetItem, QApplication
        from PyQt5 import QtGui, QtCore
    except:
        raise ImportError("Requires PyQt4 or PyQt5")

from addie.master_table.import_from_database.oncat_authentication_handler import OncatAuthenticationHandler
from addie.utilities.oncat import OncatErrorMessageWindow
from addie.utilities.oncat import pyoncatGetIptsList, pyoncatGetNexus, pyoncatGetRunsFromIpts
from addie.master_table.tree_definition import LIST_SEARCH_CRITERIA
from addie.master_table.periodic_table.material_handler import MaterialHandler
from addie.master_table.table_row_handler import TableRowHandler
from addie.master_table.master_table_loader import AsciiLoaderOptionsInterface
from addie.master_table.import_from_database.global_rule_handler import GlobalRuleHandler
from addie.master_table.import_from_database.table_search_engine import TableSearchEngine
from addie.master_table.import_from_database.table_handler import TableHandler

from addie.utilities.general import generate_random_key, remove_white_spaces
from addie.utilities.list_runs_parser import ListRunsParser

from addie.ui_import_from_database import Ui_Dialog as UiDialog


class ImportFromDatabaseHandler:

    def __init__(self, parent=None):
        if parent.import_from_database_ui is None:
            o_import = ImportFromDatabaseWindow(parent=parent)
            o_import.show()
            parent.import_from_database_ui = o_import
            if parent.import_from_database_ui_position:
                parent.import_from_database_ui.move(parent.import_from_database_ui_position)
        else:
            parent.import_from_database_ui.setFocus()
            parent.import_from_database_ui.activateWindow()


class ImportFromDatabaseWindow(QDialog):

    filter_column_widths = [10, 50, 200, 100, 300]
    row_height = 40

    button_height = 30
    button_width = 150

    list_ui = {}

    ipts_exist = True
    nexus_json = {}
    metadata = {}

    list_of_nexus_found = []
    list_of_nexus_not_found = []
    list_of_nexus_filtered_out = []

    # first time filling the metadata filter table
    first_time_filling_table = True

    def __init__(self, parent=None):
        self.parent = parent

        QDialog.__init__(self, parent=parent)
        self.ui = UiDialog()
        self.ui.setupUi(self)

        self.init_widgets()
        self.radio_button_changed()

    def init_widgets(self):
        if self.parent.oncat is None:
            return

        self.ui.tableWidget.setColumnHidden(0, True)

        self.ui.error_message.setStyleSheet("color: red")
        self.ui.error_message.setVisible(False)

        # retrieve list of IPTS for this user
        instrument = self.parent.instrument['short_name']
        facility = self.parent.facility

        list_ipts = pyoncatGetIptsList(oncat=self.parent.oncat,
                                       instrument=instrument,
                                       facility=facility)
        self.list_ipts = list_ipts

        self.ui.ipts_combobox.addItems(list_ipts)

        self.ui.clear_ipts.setIcon(QtGui.QIcon(":/MPL Toolbar/clear_icon.png"))
        self.ui.clear_run.setIcon(QtGui.QIcon(":/MPL Toolbar/clear_icon.png"))

        self.ui.search_logo_label.setPixmap(QtGui.QPixmap(":/MPL Toolbar/search_icon.png"))
        self.ui.clear_search_button.setIcon(QtGui.QIcon(":/MPL Toolbar/clear_icon.png"))

        for _col, _width in enumerate(self.filter_column_widths):
            self.ui.tableWidget.setColumnWidth(_col, _width)

            self.ui.splitter.setStyleSheet("""
    	QSplitter::handle {
    	   image: url(':/MPL Toolbar/splitter_icon.png');
    	}
    	""")

    def change_user_clicked(self):
        OncatAuthenticationHandler(parent=self.parent)

    def radio_button_changed(self):
        ipts_widgets_status = False
        run_widgets_status = True
        if self.ui.ipts_radio_button.isChecked():
            ipts_widgets_status = True
            run_widgets_status = False
            self.ipts_text_changed(str(self.ui.ipts_lineedit.text()))
        else:
            self.ui.error_message.setVisible(False)

        self.ui.ipts_combobox.setEnabled(ipts_widgets_status)
        self.ui.ipts_lineedit.setEnabled(ipts_widgets_status)
        self.ui.ipts_label.setEnabled(ipts_widgets_status)
        self.ui.clear_ipts.setEnabled(ipts_widgets_status)

        self.ui.run_number_lineedit.setEnabled(run_widgets_status)
        self.ui.run_number_label.setEnabled(run_widgets_status)
        self.ui.clear_run.setEnabled(run_widgets_status)

        self.check_import_button()

    def preview_widget_status(self, enabled_widgets=False):
        self.ui.search_logo_label.setEnabled(enabled_widgets)
        self.ui.name_search.setEnabled(enabled_widgets)
        self.ui.clear_search_button.setEnabled(enabled_widgets)
        self.ui.list_of_runs_label.setEnabled(enabled_widgets)

    def filter_widget_status(self, enabled_widgets=False):
        self.ui.tableWidget.setEnabled(enabled_widgets)
        self.ui.add_criteria_button.setEnabled(enabled_widgets)
        self.ui.filter_result_label.setEnabled(enabled_widgets)
        self.ui.tableWidget_filter_result.setEnabled(enabled_widgets)

    def clear_ipts(self):
        self.ui.ipts_lineedit.setText("")
        self.refresh_preview_table_of_runs()

    def clear_run(self):
        self.ui.run_number_lineedit.setText("")
        self.refresh_preview_table_of_runs()


    def check_import_button(self):
        enable_import = False
        if self.ui.ipts_radio_button.isChecked():
            if str(self.ui.ipts_lineedit.text()).strip() != "":
                if self.ipts_exist:
                    enable_import = True
            else:
                enable_import = True
        else:
            if str(self.ui.run_number_lineedit.text()).strip() != "":
                enable_import = True

        self.ui.import_button.setEnabled(enable_import)


    def get_list_of_runs_found_and_not_found(self, str_runs="", oncat_result={}, check_not_found=True):
        if str_runs:
            o_parser = ListRunsParser(current_runs=str_runs)
            list_of_runs = o_parser.list_current_runs
        else:
            check_not_found = False

        list_of_runs_found = []
        for _json in oncat_result:
            _run_number = _json['indexed']['run_number']
            list_of_runs_found.append("{}".format(_run_number))

        if check_not_found:
            list_of_runs_not_found = set(list_of_runs) - set(list_of_runs_found)
        else:
            list_of_runs_not_found = []

        return {'not_found': list_of_runs_not_found,
                'found': list_of_runs_found}

    def build_result_dictionary(self, nexus_json=[]):
        """isolate the infos I need from ONCat result to insert in the main window, master table"""
        result_dict = OrderedDict()

        for _json in nexus_json:
            result_dict[_json['indexed']['run_number']] = {'chemical_formula': "{}".format(_json['metadata']['entry']['sample']['chemical_formula']),
                                                           'mass_density': "{}".format(_json['metadata']['entry']['sample']['mass_density']),
                                                           }
        return result_dict

    def insert_in_master_table(self, nexus_json=[]):
        if nexus_json == []:
            return

        runs_dict = self.build_result_dictionary(nexus_json=nexus_json)

        o_row = TableRowHandler(parent=self.parent)
        for _run in runs_dict.keys():
            _chemical_formula = runs_dict[_run]['chemical_formula']
            _mass_density = runs_dict[_run]['mass_density']
            _run = "{}".format(_run)

            o_row.fill_row(sample_runs=_run,
                           sample_chemical_formula=_chemical_formula,
                           sample_mass_density=_mass_density)

    def cancel_button_clicked(self):
        self.close()

    def chemical_formula_pressed(self, key):
        MaterialHandler(parent=self.parent,
                        database_window=self,
                        key=key,
                        data_type='database')

    def list_argument_changed(self, value, key):
        print("new value is {}".format(value))

    def list_argument_index_changed(self, value, key):
        print("index changed and value is now {}".format(value))

    def list_criteria_changed(self, value, key):
        pass

    def define_unique_rule_name(self, row):
        """this method makes sure that the name of the rule defined is unique and does not exist already"""
        nbr_row = self.ui.tableWidget.rowCount()
        list_rule_name = []
        for _row in np.arange(nbr_row):
            if self.ui.tableWidget.item(_row, 1):
                _rule_name = str(self.ui.tableWidget.item(_row, 1).text())
                list_rule_name.append(_rule_name)

        offset = 0
        while True:
            if ("{}".format(offset+row)) in list_rule_name:
                offset += 1
            else:
                return offset+row


    def _add_row(self, row=-1):
        """this add a row to the filter table (top table)"""
        _random_key = generate_random_key()

        _list_ui_for_this_row = {}

        self.ui.tableWidget.insertRow(row)
        self.ui.tableWidget.setRowHeight(row, self.row_height)

        # key
        _item = QTableWidgetItem("{}".format(_random_key))
        self.ui.tableWidget.setItem(row, 0, _item)

        # rule #
        _rule_name = self.define_unique_rule_name(row)
        _item = QTableWidgetItem("{}".format(_rule_name))
        self.ui.tableWidget.setItem(row, 1, _item)

        # search argument
        _widget = QComboBox()
        _list_ui_for_this_row['list_items'] = _widget
        list_items = LIST_SEARCH_CRITERIA[self.parent.instrument['short_name'].lower()]
        _widget.addItems(list_items)
        self.ui.tableWidget.setCellWidget(row, 2, _widget)
        QtCore.QObject.connect(_widget, QtCore.SIGNAL("currentIndexChanged(QString)"),
                               lambda value=list_items[0],
                               key = _random_key:
                               self.list_criteria_changed(value, key))

        # criteria
        list_criteria = ['is', 'contains']
        _widget = QComboBox()
        _list_ui_for_this_row['list_criteria'] = _widget
        _widget.addItems(list_criteria)
        self.ui.tableWidget.setCellWidget(row, 3, _widget)

        # argument
        _widget = QComboBox()
        _widget.setEditable(True)
        list_values = list(self.metadata['chemical_formula'])
        _widget.addItems(list_values)
        self.ui.tableWidget.setCellWidget(row, 4, _widget)
        QtCore.QObject.connect(_widget, QtCore.SIGNAL("editTextChanged(QString)"),
                               lambda value=list_values[0],
                                      key = _random_key:
                               self.list_argument_changed(value, key))
        QtCore.QObject.connect(_widget, QtCore.SIGNAL("currentIndexChanged(QString)"),
                               lambda value=list_values[0],
                                      key = _random_key:
                               self.list_argument_index_changed(value, key))

        if row == 0:
            self.ui.tableWidget.horizontalHeader().setVisible(True)

        # # argument
        # _layout = QHBoxLayout()
        # _lineedit = QLineEdit()
        # _lineedit.setVisible(False)
        # _label = QLabel()
        # _label.setVisible(True)
        # _button = QPushButton("Define Formula")
        # _button.setFixedHeight(self.button_height)
        # _button.setFixedWidth(self.button_width)
        # QtCore.QObject.connect(_button, QtCore.SIGNAL("pressed()"),
        #                         lambda key=_random_key:
        #                        self.chemical_formula_pressed(key))
        # _button.setVisible(True)
        #
        # _list_ui_for_this_row['value_lineedit'] = _lineedit
        # _list_ui_for_this_row['value_label'] = _label
        # _list_ui_for_this_row['value_button'] = _button
        #
        # _layout.addWidget(_lineedit)
        # _layout.addWidget(_label)
        # _layout.addWidget(_button)
        # _widget = QWidget()
        # _widget.setLayout(_layout)
        # self.ui.tableWidget.setCellWidget(row, 3, _widget)

        self.list_ui[_random_key] = _list_ui_for_this_row
        self.check_all_filter_widgets()

    def refresh_global_rule(self, full_reset=False, new_row=-1):
        if full_reset:
            list_rule_number = []
            nbr_row = self.ui.tableWidget.rowCount()
            for _row in np.arange(nbr_row):
                rule_number = "#{}".format(str(self.ui.tableWidget.item(_row, 1).text()))
                list_rule_number.append(rule_number)
            global_rule = " and ".join(list_rule_number)
        else:
            current_global_rule = str(self.ui.global_rule_lineedit.text())
            name_of_new_row = str(self.ui.tableWidget.item(new_row, 1).text())
            if current_global_rule == "":
                global_rule = "#{}".format(name_of_new_row)
            else:
                global_rule = current_global_rule + " and #{}".format(name_of_new_row)

        self.ui.global_rule_lineedit.setText(global_rule)

    def remove_criteria_clicked(self):
        _select = self.ui.tableWidget.selectedRanges()
        if not _select:
            return
        row = _select[0].topRow()
        _randome_key = str(self.ui.tableWidget.item(row, 0).text())
        self.list_ui.pop(_randome_key, None)
        self.ui.tableWidget.removeRow(row)
        self.check_all_filter_widgets()
        self.refresh_global_rule(full_reset=True)

    def add_criteria_clicked(self):
        nbr_row = self.ui.tableWidget.rowCount()
        self._add_row(row=nbr_row)
        self.check_rule_widgets()
        self.refresh_global_rule(new_row=nbr_row)

    def check_all_filter_widgets(self):
        self.check_remove_widget()
        self.check_rule_widgets()

    def check_rule_widgets(self):
        nbr_row = self.ui.tableWidget.rowCount()
        enable_global_rule_label = False
        enable_global_rule_value = False
        enable_global_rule_button = False
        if nbr_row == 0:
            pass
        elif nbr_row == 1:
            enable_global_rule_label = True
            enable_global_rule_value = True
        else:
            enable_global_rule_label = True
            enable_global_rule_value = True
            enable_global_rule_button = True

        self.ui.global_rule_label.setEnabled(enable_global_rule_label)
        self.ui.global_rule_lineedit.setEnabled(enable_global_rule_value)
        self.ui.global_rule_button.setEnabled(enable_global_rule_button)

    def check_remove_widget(self):
        nbr_row = self.ui.tableWidget.rowCount()
        if nbr_row > 0:
            self.ui.remove_criteria_button.setEnabled(True)
        else:
            self.ui.remove_criteria_button.setEnabled(False)

    def import_button_clicked(self):
        o_dialog = AsciiLoaderOptions(parent=self.parent)
        o_dialog.show()

    def import_button(self, insert_in_table=True):

        QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        self.list_of_runs_not_found = []

        if self.ui.run_radio_button.isChecked():

            # remove white space to string to make ONCat happy
            str_runs = str(self.ui.run_number_lineedit.text())
            str_runs = remove_white_spaces(str_runs)

            nexus_json = pyoncatGetNexus(oncat=self.parent.oncat,
                                         instrument=self.parent.instrument['short_name'],
                                         runs=str_runs,
                                         facility=self.parent.facility,
                                         )

            result = self.get_list_of_runs_found_and_not_found(str_runs=str_runs,
                                                               oncat_result=nexus_json)
            list_of_runs_not_found = result['not_found']
            self.list_of_runs_not_found = list_of_runs_not_found
            self.list_of_runs_found = result['found']

            # clear input widget
#            self.ui.run_number_lineedit.setText("")

        else:
            ipts = str(self.ui.ipts_combobox.currentText())

            nexus_json = pyoncatGetRunsFromIpts(oncat=self.parent.oncat,
                                                instrument=self.parent.instrument['short_name'],
                                                ipts=ipts,
                                                facility=self.parent.facility)

            result = self.get_list_of_runs_found_and_not_found(oncat_result=nexus_json,
                                                               check_not_found=False)

            self.list_of_runs_not_found = result['not_found']
            self.list_of_runs_found = result['found']

        if insert_in_table:
            self.insert_in_master_table(nexus_json=nexus_json)
        else:
            self.nexus_json = nexus_json
            self.isolate_metadata()

        QApplication.restoreOverrideCursor()

        if insert_in_table:
            self.close()

    def isolate_metadata(self):
        '''retrieve the metadata of interest from the json returns by ONCat'''

        # def _format_proton_charge(raw_proton_charge):
        #     _proton_charge = raw_proton_charge/1e12
        #     return "{:.3}".format(_proton_charge)

        nexus_json = self.nexus_json
        metadata = {}

        list_chemical_formula = []
        list_mass_density = []
        list_proton_charge = []
        list_device_name = []

        for _json in nexus_json:
            list_chemical_formula.append(str(_json['metadata']['entry']['sample']['chemical_formula']))
            list_mass_density.append(str(_json['metadata']['entry']['sample']['mass_density']))
            # _proton_charge = _format_proton_charge(_json['metadata']['entry']['proton_charge'])
            _proton_charge = _json['metadata']['entry']['proton_charge']
            list_proton_charge.append(str(_proton_charge))
            list_device_name.append(str(_json['metadata']['entry']['daslogs']['bl1b:se:sampletemp']['device_name']))

        metadata['chemical_formula'] = set(list_chemical_formula)
        metadata['mass_density'] = set(list_mass_density)
        metadata['proton_charge'] = set(list_proton_charge)
        metadata['device_name'] = str(list_device_name)

        self.metadata = metadata

    def files_not_found_more_clicked(self):
        list_of_runs_not_found = self.list_of_runs_not_found
        self.inform_of_list_of_runs(list_of_runs=list_of_runs_not_found,
                                    message='List of NeXus not found!')

    def files_filtered_out_more_clicked(self):
        pass

    def files_imported_more_clicked(self):
        pass

    def files_initially_selected_more_clicked(self):
        list_of_nexus_found = self.list_of_runs_found
        self.inform_of_list_of_runs(list_of_runs=list_of_nexus_found,
                                    message='List of NeXus found!')

    def inform_of_list_of_runs(self, list_of_runs='', message=''):
        if list_of_runs == '':
            return

        o_info = OncatErrorMessageWindow(parent=self,
                                         list_of_runs=list_of_runs,
                                         message=message)
        o_info.show()

    def refresh_preview_table_of_runs(self):
        if self.ui.import_button.isEnabled():
            self.import_button(insert_in_table=False)

        nexus_json = self.nexus_json

        enabled_widgets = False
        if not (nexus_json == {}):
            enabled_widgets = True

        self.preview_widget_status(enabled_widgets=enabled_widgets)
        self.refresh_result_table(nexus_json=copy.deepcopy(nexus_json),
                                  table_ui=self.ui.tableWidget_all_runs)

    def toolbox_changed(self, index):
        if index == 0:
            self.nexus_json = {}
        elif index == 1:
            self.refresh_filter_page()

            # if index == 2: # status page
            #     self.refresh_status_page()

    def refresh_filter_page(self):
        if self.ui.import_button.isEnabled():
            self.import_button(insert_in_table=False)

        nexus_json = self.nexus_json

        enabled_widgets = False
        if not (nexus_json == {}):
            enabled_widgets = True

        self.filter_widget_status(enabled_widgets=enabled_widgets)
        self.refresh_result_table(nexus_json=copy.deepcopy(nexus_json),
                                  table_ui=self.ui.tableWidget_filter_result)

    def clear_tableWidget(self, table_ui=None):
        nbr_row = table_ui.rowCount()
        for _ in np.arange(nbr_row):
            table_ui.removeRow(0)

    def _json_extractor(self, json=None, list_args=[]):
        if len(list_args) == 1:
            return json[list_args[0]]
        else:
            return self._json_extractor(json[list_args.pop(0)],
                                        list_args=list_args)

    def set_table_item(self, json=None, metadata_filter={}, row=-1, col=-1, table_ui=None):
        """Populate the filter metadada table from the oncat json file of only the arguments specified in
        the config.json file (oncat_metadata_filters)"""

        def _format_proton_charge(raw_proton_charge):
            _proton_charge = raw_proton_charge/1e12
            return "{:.3}".format(_proton_charge)

        title = metadata_filter['title']
        list_args = metadata_filter["path"]
        argument_value = self._json_extractor(json=json, list_args=copy.deepcopy(list_args))

        # if title is "Proton Charge" change format of value displayed
        if title == "Proton Charge (C)":
            argument_value = _format_proton_charge(argument_value)

        if table_ui is None:
            table_ui = self.ui.tableWidget_filter_result

        if self.first_time_filling_table:
            table_ui.insertColumn(col)
            _item_title = QTableWidgetItem(title)
            table_ui.setHorizontalHeaderItem(col, _item_title)
            width = metadata_filter["column_width"]
            table_ui.setColumnWidth(col, width)

        _item = QTableWidgetItem("{}".format(argument_value))
        table_ui.setItem(row, col, _item)

    def refresh_result_table(self, nexus_json=[], table_ui=None):
        """may either be the filter table or the raw preview table"""

        if table_ui is None:
            table_ui = self.ui.tableWidget_filter_result

        oncat_metadata_filters = self.parent.oncat_metadata_filters
        #if nexus_json == []:
        self.clear_tableWidget(table_ui=table_ui)
        #else:
        for _row, _json in enumerate(nexus_json):
            table_ui.insertRow(_row)
            for _column, metadata_filter in enumerate(oncat_metadata_filters):
                self.set_table_item(json=copy.deepcopy(_json),
                                    metadata_filter=metadata_filter,
                                    row=_row,
                                    col=_column,
                                    table_ui=table_ui)

            self.first_time_filling_table = False

    # def refresh_status_page(self):
    #     nexus_json = self.nexus_json
    #     nbr_of_raw_nexus = len(nexus_json)
    #
    #     # raw
    #     self.ui.number_of_files_initially_selected.setText("{}".format(nbr_of_raw_nexus))
    #     visible_list_of_files_initially_selected = False
    #     if nbr_of_raw_nexus > 0:
    #         visible_list_of_files_initially_selected = True
    #     self.ui.file_initially_selected_more.setVisible(visible_list_of_files_initially_selected)
    #
    #     # not found
    #     list_of_runs_not_found = self.list_of_runs_not_found
    #     self.ui.number_of_files_not_found.setText("{}".format(len(list_of_runs_not_found)))
    #     visible_list_of_runs_not_found_button = False
    #     if list_of_runs_not_found:
    #         # show button
    #        # self.inform_of_list_of_runs_not_found(list_of_runs=list_of_runs_not_found)
    #         visible_list_of_runs_not_found_button = True
    #     self.ui.file_not_found_more.setVisible(visible_list_of_runs_not_found_button)
    #
    #     # list of files filtered out
    #     visible_list_of_runs_filtered_out = False
    #     #FIXME HERE
    #     self.ui.files_filtered_out_more.setVisible(visible_list_of_runs_filtered_out)

    def ipts_selection_changed(self, ipts_selected):
        self.ui.ipts_lineedit.setText("")
        self.refresh_preview_table_of_runs()
        self.search_return_pressed()

    def ipts_text_return_pressed(self):
        self.refresh_preview_table_of_runs()
        self.search_return_pressed()

    def ipts_text_changed(self, ipts_text):
        if ipts_text.strip() != "":
            str_ipts = "IPTS-{}".format(ipts_text.strip())

            ipts_exist = False
            if str_ipts in self.list_ipts:
                ipts_exist = True
                index = self.ui.ipts_combobox.findText(str_ipts)
                self.ui.ipts_combobox.blockSignals(True)
                self.ui.ipts_combobox.setCurrentIndex(index)
                self.ui.ipts_combobox.blockSignals(False)
        else:
            ipts_exist = True  # we will use the combobox IPTS

        self.ipts_exist = ipts_exist
        self.check_import_button()
        self.search_return_pressed()

    def run_number_return_pressed(self):
        self.refresh_preview_table_of_runs()
        self.search_return_pressed()

    def run_number_text_changed(self, text):
        self.check_import_button()

    def edit_global_rule_clicked(self):
        GlobalRuleHandler(parent=self)

    def search_return_pressed(self):
        new_text = str(self.ui.name_search.text())
        self.search_text_changed(new_text)

    def search_text_changed(self, new_text):
        new_text = str(new_text)
        o_search = TableSearchEngine(table_ui=self.ui.tableWidget_all_runs)
        list_row_matching_string = o_search.locate_string(new_text)

        o_table = TableHandler(table_ui=self.ui.tableWidget_all_runs)
        o_table.show_list_of_rows(list_of_rows=list_row_matching_string)

    def clear_search_text(self):
        self.ui.name_search.setText("")
        self.search_return_pressed()

    def closeEvent(self, c):
        self.parent.import_from_database_ui = None
        self.parent.import_from_database_ui_position = self.pos()


class AsciiLoaderOptions(AsciiLoaderOptionsInterface):

    def accept(self):
        pass
        #self.close()