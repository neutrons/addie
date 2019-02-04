from collections import OrderedDict
import copy
import numpy as np

try:
    from PyQt4.QtGui import QDialog, QComboBox, QLineEdit, QPushButton, QWidget, QHBoxLayout, QLabel, \
        QTableWidgetItem, QApplication, QMainWindow
    from PyQt4 import QtGui, QtCore
except:
    try:
        from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit, QPushButton, QWidget, QHBoxLayout, QLabel, \
            QTableWidgetItem, QApplication, QMainWindow
        from PyQt5 import QtGui, QtCore
    except:
        raise ImportError("Requires PyQt4 or PyQt5")

from addie.master_table.import_from_database.oncat_authentication_handler import OncatAuthenticationHandler
from addie.utilities.oncat import OncatErrorMessageWindow
from addie.utilities.oncat import pyoncatGetIptsList, pyoncatGetNexus, \
    pyoncatGetRunsFromIpts, pyoncatGetTemplate
from addie.master_table.tree_definition import LIST_SEARCH_CRITERIA
from addie.master_table.periodic_table.material_handler import MaterialHandler
from addie.master_table.table_row_handler import TableRowHandler
from addie.master_table.master_table_loader import AsciiLoaderOptionsInterface
from addie.master_table.import_from_database.global_rule_handler import GlobalRuleHandler
from addie.master_table.import_from_database.table_search_engine import TableSearchEngine
from addie.master_table.import_from_database.oncat_template_retriever import OncatTemplateRetriever
from addie.master_table.import_from_database.gui_handler import GuiHandler, ImportFromDatabaseTableHandler
from addie.master_table.import_from_database import utilities as ImportFromDatabaseUtilities
from addie.master_table.import_from_database.import_table_from_oncat_handler import ImportTableFromOncat
from addie.master_table.import_from_database.table_widget_rule_handler import TableWidgetRuleHandler
from addie.master_table.import_from_database.apply_rule_handler import ApplyRuleHandler

from addie.utilities.general import generate_random_key, remove_white_spaces
from addie.utilities.gui_handler import TableHandler

from addie.ui_import_from_database import Ui_MainWindow as UiMainWindow


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


class ImportFromDatabaseWindow(QMainWindow):

    filter_column_widths = [10, 50, 200, 100, 300]
    row_height = 40

    button_height = 30
    button_width = 150

    list_ui = {}

    ipts_exist = True
    nexus_json = {}
    nexus_json_from_template = {}
    metadata = {}

    list_of_nexus_found = []
    list_of_nexus_not_found = []
    list_of_nexus_filtered_out = []

    # first time filling the metadata filter table
    first_time_filling_table = True
    first_time_filling_preview_table = True

    oncat_template = {}

    def __init__(self, parent=None):
        self.parent = parent

        # QDialog.__init__(self, parent=parent)
        # self.ui = UiDialog()
        QMainWindow.__init__(self, parent=parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

        self.init_widgets()
        self.init_oncat_template()
        self.radio_button_changed()

    def init_oncat_template(self):
        """In order to display in the first tab all the metadata just like ONCat does
        on the web site, we need to retrieve the same template as ONCat uses. This is
        what is going on right here"""
        o_retriever = OncatTemplateRetriever(parent=self.parent)
        self.oncat_template = o_retriever.get_template_information()

    def init_widgets(self):
        if self.parent.oncat is None:
            return

        self.ui.tableWidget.setColumnHidden(0, True)

        self.ui.error_message.setStyleSheet("color: red")
        self.ui.error_message.setVisible(False)

        # retrieve list and display of IPTS for this user
        instrument = self.parent.instrument['short_name']
        facility = self.parent.facility

        list_ipts = pyoncatGetIptsList(oncat=self.parent.oncat,
                                       instrument=instrument,
                                       facility=facility)
        self.list_ipts = list_ipts
        self.ui.ipts_combobox.addItems(list_ipts)

        # add icons on top of widgets (clear, search)
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
        """using either the IPTS number selected or the runs defined, this will use the ONCat template to
        retrieve all the information from the template and populate the preview table """

        QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        QtGui.QApplication.processEvents()

        #if self.ui.import_button.isEnabled():
        o_import = ImportTableFromOncat(parent=self)
        o_import.from_oncat_template()

        nexus_json = self.nexus_json_from_template

        enabled_widgets = False
        if not (nexus_json == {}):
            enabled_widgets = True

        GuiHandler.preview_widget_status(self.ui, enabled_widgets=enabled_widgets)
        self.refresh_preview_table(nexus_json=copy.deepcopy(nexus_json))

        QApplication.restoreOverrideCursor()
        QtGui.QApplication.processEvents()

    def refresh_filter_page(self):

        QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        QtGui.QApplication.processEvents()

        if self.ui.import_button.isEnabled():
            o_import = ImportTableFromOncat(parent=self)
            o_import.from_oncat_config(insert_in_table=False)

        nexus_json = self.nexus_json

        enabled_widgets = False
        if not (nexus_json == {}):
            enabled_widgets = True

        GuiHandler.filter_widget_status(self.ui, enabled_widgets=enabled_widgets)
        self.refresh_filter_table(nexus_json=copy.deepcopy(nexus_json))
        self.update_rule_filter()

        QApplication.restoreOverrideCursor()
        QtGui.QApplication.processEvents()

    def refresh_preview_table(self, nexus_json=[]):
        """this function will use the template returned by ONCat during the initialization of this
        window and will, for all the runs specified, or all teh runs of the given IPTS, all the metadata
        defined in that template"""
        table_ui = self.ui.tableWidget_all_runs
        o_handler = ImportFromDatabaseTableHandler(table_ui=table_ui,
                                                   parent=self)
        o_handler.refresh_preview_table(nexus_json=nexus_json)

    def refresh_filter_table(self, nexus_json=[]):
        """This function takes the nexus_json returns by ONCat and
        fill the filter table with only the metadata of interests. Those
        are defined in the oncat_metadata_filters dictionary (coming from the json config)

        ex: title, chemical formula, mass density, Sample Env. Device and proton charge
        """
        if nexus_json == []:
            nexus_json = self.nexus_json

        table_ui = self.ui.tableWidget_filter_result
        o_handler = ImportFromDatabaseTableHandler(table_ui=table_ui,
                                                   parent=self)
        o_handler.refresh_table(nexus_json=nexus_json)

    def update_rule_filter(self):
        o_rule = ApplyRuleHandler(parent=self)
        o_rule.apply_global_rule()

    # EVENT HANDLER CREATED DURING RUN TIME ----------------------------

    def list_argument_changed(self, value, key):
        self.update_rule_filter()

    def list_argument_index_changed(self, value, key):
        self.update_rule_filter()

    def list_criteria_changed(self, value, key):
        self.update_rule_filter()

    def list_item_changed(self, value, key):
        """this method is reached when the user changes the name of the variable he wants to filter"""
        o_table = TableWidgetRuleHandler(parent=self)
        o_table.update_list_value_of_given_item(item_name=value, key=key)
        self.update_rule_filter()

    # EVENT HANDLER ---------------------------------------------------

    def change_user_clicked(self):
        OncatAuthenticationHandler(parent=self.parent)

    def radio_button_changed(self):

        QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        QtGui.QApplication.processEvents()

        ipts_widgets_status = False
        run_widgets_status = True
        if self.ui.ipts_radio_button.isChecked():
            ipts_widgets_status = True
            run_widgets_status = False
            if str(self.ui.ipts_lineedit.text()).strip() != "":
#                self.ipts_selection_changed()
                self.ipts_text_return_pressed()
            else:
                self.ipts_selection_changed()
                #self.ipts_text_changed(str(self.ui.ipts_lineedit.text()))
        else:
            self.ui.error_message.setVisible(False)
            self.run_number_return_pressed()

        self.ui.ipts_combobox.setEnabled(ipts_widgets_status)
        self.ui.ipts_lineedit.setEnabled(ipts_widgets_status)
        self.ui.ipts_label.setEnabled(ipts_widgets_status)
        self.ui.clear_ipts.setEnabled(ipts_widgets_status)

        self.ui.run_number_lineedit.setEnabled(run_widgets_status)
        self.ui.run_number_label.setEnabled(run_widgets_status)
        self.ui.clear_run.setEnabled(run_widgets_status)

        GuiHandler.check_import_button(self)

        QApplication.restoreOverrideCursor()
        QtGui.QApplication.processEvents()

    def clear_ipts(self):
        self.ui.ipts_lineedit.setText("")
        self.refresh_preview_table_of_runs()

    def clear_run(self):
        self.ui.run_number_lineedit.setText("")
        self.refresh_preview_table_of_runs()

    def import_button_clicked(self):
        o_dialog = AsciiLoaderOptions(parent=self.parent)
        o_dialog.show()

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
        self.update_rule_filter()

    def add_criteria_clicked(self):
        nbr_row = self.ui.tableWidget.rowCount()
        o_table_handler = TableWidgetRuleHandler(parent=self)
        o_table_handler.add_row(row=nbr_row)
        self.check_rule_widgets()
        self.refresh_global_rule(new_row=nbr_row)
        self.update_rule_filter()

    def ipts_selection_changed(self, ipts_selected=""):
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
        GuiHandler.check_import_button(self)

    def run_number_return_pressed(self):
        self.refresh_preview_table_of_runs()
        self.search_return_pressed()

    def run_number_text_changed(self, text):
        GuiHandler.check_import_button(self)

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

    def toolbox_changed(self, index):
        if index == 0:
            self.nexus_json = {}
        elif index == 1:
            self.refresh_filter_page()

    def build_result_dictionary(self, nexus_json=[]):
        """isolate the infos I need from ONCat result to insert in the main window, master table"""
        result_dict = OrderedDict()

        for _json in nexus_json:
            result_dict[_json['indexed']['run_number']] = {'chemical_formula': "{}".format(_json['metadata']['entry']['sample']['chemical_formula']),
                                                           'mass_density': "{}".format(_json['metadata']['entry']['sample']['mass_density']),
                                                           }
        return result_dict

    def cancel_button_clicked(self):
        self.close()

    def closeEvent(self, c):
        self.parent.import_from_database_ui = None
        self.parent.import_from_database_ui_position = self.pos()


class AsciiLoaderOptions(AsciiLoaderOptionsInterface):

    def accept(self):
        pass
        #self.close()