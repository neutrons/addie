from __future__ import (absolute_import, division, print_function)

import copy
import sys
import os
import itertools
import psutil
from collections import OrderedDict
from qtpy.QtCore import QProcess
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QTableWidgetItem,
    QWidget)

from addie import __version__
from addie.initialization.widgets.configuration import ConfigurationInitializer
from addie.utilities import load_ui

import addie.menu.event_handler as menu_event_handler

from addie.help_handler.help_gui import help_button_activator
from addie.advanced.isotope_rep_gui import isrp_button_activator

from addie.utilities.job_monitor_thread import JobMonitorThread
from addie.utilities.job_status_handler import JobStatusHandler
from addie.utilities.job_status_handler import JobStatusHandlerMTS
from addie.utilities.logbook_thread import LogbookThread
from addie.utilities.logbook_handler import LogbookHandler

from addie.autoNOM.step1_gui_handler import Step1GuiHandler
import addie.autoNOM.event_handler as autonom_event_handler

from addie.processing.idl.step2_gui_handler import Step2GuiHandler
from addie.processing.idl.table_handler import TableHandler as IdlTableHandler
from addie.processing.idl.run_sum_scans import RunSumScans
from addie.processing.idl.run_thread import RunThread
from addie.processing.idl.create_sample_files import CreateSampleFiles
from addie.processing.idl.create_ndsum_file import CreateNdsumFile
from addie.processing.idl.run_ndabs import RunNDabs

import addie.processing.idl.event_handler as postprocessing_event_handler

from addie.mantid_handler.browse_file_folder_handler import BrowseFileFolderHandler
from addie.mantid_handler.mantid_reduction import GlobalMantidReduction
from addie.mantid_handler.mantid_thread import MantidThread

from addie.processing.mantid import launch_reduction as mantid_reduction_launcher
from addie.processing.mantid.master_table.align_and_focus_args import AlignAndFocusArgsHandling
from addie.processing.mantid.master_table.column_highlighting import ColumnHighlighting

import addie.processing.mantid.event_handler as processing_event_handler

import addie.addiedriver as driver
import addie.calculate_gr.edit_sq_dialog

# necessary to see all the icons
from addie.icons import icons_rc  # noqa

from addie.calculate_gr.pdf_lines_manager import PDFPlotManager

from addie.initialization.widgets import main_tab as main_tab_initialization
from addie.initialization.widgets import autonom_tab as autonom_tab_initialization
from addie.initialization.widgets import postprocessing_tab as postprocessing_tab_initialization
from addie.initialization.widgets import postprocessing_tab_m as postprocessing_tab_m_initialization
from addie.initialization.widgets import processing_tab as processing_tab_initialization
from addie.initialization.widgets import rietveld_tab as rietveld_tab_initialization
from addie.initialization.widgets import calculategr_tab as calculategr_tab_initialization

from addie.initialization.events import main_tab as main_tab_events_handler
from addie.initialization.events import autonom_tab as autonom_tab_events_handler
from addie.initialization.events import postprocessing_tab as postprocessing_tab_events_handler
from addie.initialization.events import postprocessing_tab_m as postprocessing_tab_m_events_handler
from addie.initialization.events import processing_tab as processing_tab_events_handler
from addie.initialization.events import rietveld_tab as rietveld_tab_events_handler
from addie.initialization.events import calculategr_tab as calculategr_tab_events_handler

from addie.rietveld import event_handler as rietveld_event_handler
from addie.rietveld import braggtree as bragg_event_handler
from addie.calculate_gr import event_handler as calculategr_event_handler
from addie.post_process_m import event_handler as post_processing_m_event_handler


class MainWindow(QMainWindow):
    """ Main addie window
    """

    first_oncat_authentication = True
    oncat = None  # object to use to retrieve IPTS numbers...etc. Created by oncat_authentication_handler.py

    # config.json ======================================================
    # those infos will be automatically retrieve from the config.json file
    facility = ''
    instrument = {"full_name": "",   # Powgen, Nomad ...
                  "short_name": ""}  # PG3, NOM ...
    list_instrument = {"full_name": [],
                       "short_name": []}
    config_calibration_folder = {"pre": "", "post": ""}
    config_characterization_folder = {"pre": "", "post": ""}

    calibration_extension = ""
    characterization_extension = ""

    cache_folder = './'  # defined in the advanced window
    output_folder = './'  # defined in the advanced window

    placzek_default = {}

    # list of arguments to use in Import from ONCat and to display for filters
    oncat_metadata_filters = []
    # end of config.json ======================================================

    # Master json created by master_table_loader_from_database where keys are "1-10,15,16" with list of json and
    # list of titles (used to fix conflicts when loading)
    # json_to_import = {'1,2,5-10': {'list_of_json': [json1, json2, json5, json6, json7, ... json10],
    #                                'title': "title_1_1,2,5-10'},
    #                   '20-30': {'list_of_json': [...',
    #                             'title': "title_20-30"},
    #                   ... }
    json_to_import = None

    # flag that will clear or not the master table before loading data
    clear_master_table_before_loading = True

    # load los.csv options
    ascii_loader_option = None   # None, 1, 2, 3, 4
    ascii_loader_dictionary = {}

    # intermediate and output grouping files
    grouping_dict = {'filename': "",
                     'nbr_groups': "N/A",
                     'enabled': False}
    intermediate_grouping = copy.deepcopy(grouping_dict)
    output_grouping = copy.deepcopy(grouping_dict)

    advanced_dict = {'push_bkg': False,
                     'ele_size': "1.0"}

    statusbar_display_time = 5000  # 5s

    # external ui (use to make sure there is only one open at a time
    import_from_database_ui = None
    import_from_database_ui_position = None

    import_from_run_number_ui = None
    import_from_run_number_ui_position = None

    oncat_authentication_ui_position = None

    conflicts_solver_ui_position = None

    advanced_window_ui = None
    make_calibration_ui = None
    make_calibration_ui_position = None
    table_tree_ui = None
    table_tree_ui_position = None
    placzek_ui = None
    reduction_configuration_ui = None
    reduction_configuration_ui_position = None
    key_value_pair_ui = None
    key_value_pair_ui_position = None

    material_ui = None
    material_ui_position = None

    mass_density_ui = None
    mass_density_ui_position = None

    geometry_ui_position = None
    resonance_ui_position = None
    scattering_ui_position = None

    # config file to initialize the widgets (example Q and R range in PDF tab)
    current_path = os.path.dirname(os.path.dirname(__file__))
    addie_config_file = os.path.join(
        os.path.dirname(
            addie.__file__),
        "config.json")

    # master table reduction configuration
    reduction_configuration = {}

    # configuration of master table
    config_dict = OrderedDict()
    reset_config_dict = OrderedDict()
    active_config_name = ''
    list_config_displayed = []

    # will list the various ui for each row using a random number as key
    dict_widget = {'ui': None,
                   'status': False}
    master_table_right_click_buttons = {
        'activate': copy.deepcopy(dict_widget),
        'activate_check_all': copy.deepcopy(dict_widget),
        'activate_uncheck_all': copy.deepcopy(dict_widget),
        'activate_inverse': copy.deepcopy(dict_widget),
        'cells': copy.deepcopy(dict_widget),
        'cells_paste': copy.deepcopy(dict_widget),
        'cells_copy': copy.deepcopy(dict_widget),
        'cells_clear': copy.deepcopy(dict_widget),
        'rows_paste': copy.deepcopy(dict_widget),
        'rows_copy': copy.deepcopy(dict_widget),
        'rows_duplicate': copy.deepcopy(dict_widget),
        'rows_remove': copy.deepcopy(dict_widget),
        'reset': copy.deepcopy(dict_widget),
        'clear': copy.deepcopy(dict_widget),
        'import_from_config_append': copy.deepcopy(dict_widget),
        'import_from_file_append': copy.deepcopy(dict_widget),
        'import_from_database_append': copy.deepcopy(dict_widget),
        'export': copy.deepcopy(dict_widget),
        'plot': copy.deepcopy(dict_widget),
    }

    placzek_default = {}

    master_table_list_ui = OrderedDict()
    master_table_cells_copy = {'temp': [],
                               'list_column': [],
                               'row': [],
                               }
    table_inserted_row = -1
    copied_row = -1

    table_headers = {'h1': [],
                     'h2': [],
                     'h3': [],
                     }

    table_width = {'h1': [],
                   'h2': [],
                   'h3': []}

    # to find which h1 column goes with wich h2 and which h3
    table_columns_links = {'h1': [],
                           'h2': [],
                           'h3': [],
                           }
    tree_dict = None
    tree_ui = None
    minimum_col_width = 10

    # headers from master table
    h1_header_table = None
    h2_header_table = None
    h3_header_table = None

    undo_table = {}
    max_undo_list = 10
    undo_index = max_undo_list
    undo_button_enabled = False
    redo_button_enabled = False

    debugging = False
    load_intermediate_step_ok = False
    remove_dynamic_temperature_flag = False
    current_folder = os.getcwd()
    configuration_folder = current_folder
    calibration_folder = ''
    characterization_folder = ''
    file_path = os.getcwd()
    table_selection_buffer = {}
    _run_thread_sum_scans = RunThread()
    advanced_window_idl_groupbox_visible = False

    logbook_thread = LogbookThread()
    number_of_last_log_files_to_display = 10
    previous_list_of_log_files = []

    _run_thread = RunThread()
    job_monitor_thread = JobMonitorThread()
    _mantid_thread_array = list(itertools.repeat(MantidThread(), 30))
    config_section_name = 'Configuration'
    job_monitor_interface = None
    logbook_interface = None
    job_list = []

    init_height_main_gui = 1058
    previous_splitter_height = -1
    first_time_resizing_blocked = True

    o_help_autonom = None
    o_help_ndabs = None
    o_help_scans = None
    o_help_mantid = None
    isrp_win = None

    # list of key/value defined in the settings advanced window
    global_key_value = {}
    align_and_focus_powder_from_files_blacklist = []

    idl_modes = ("idl", "idl_dev")

    def __init__(self, parent=None, processing_mode=None):
        """ Initialization
        Parameters
        ----------
        """

        print("Launching...This may take a while...")

        QMainWindow.__init__(self, parent)

        # Initialize the UI widgets
        self.ui = load_ui('mainWindow.ui', baseinstance=self)
        main_tab_initialization.run(main_window=self)

        status_bar_label = QLabel()
        self.ui.statusbar.addPermanentWidget(status_bar_label)
        o_gui = Step1GuiHandler(main_window=self)
        o_gui.set_main_window_title()

        # autoNOM tab
        self.autonom_tab_widget = QWidget()
        self.autonom_ui = load_ui(
            'splitui_autonom_tab.ui',
            baseinstance=self.autonom_tab_widget)
        self.ui.main_tab.insertTab(0, self.autonom_tab_widget, "autoNOM")
        autonom_tab_initialization.run(main_window=self)

        # post processing idl
        self.postprocessing_tab_widget = QWidget()
        self.postprocessing_ui = load_ui(
            'splitui_postprocessing_tab.ui',
            baseinstance=self.postprocessing_tab_widget)
        self.ui.main_tab.insertTab(
            1, self.postprocessing_tab_widget, "Post Processing")
        postprocessing_tab_initialization.run(main_window=self)

        # Mantid processing tab
        self.processing_tab_widget = QWidget()
        self.processing_ui = load_ui(
            'splitui_processing_tab.ui',
            baseinstance=self.processing_tab_widget)
        self.ui.main_tab.insertTab(2, self.processing_tab_widget, "Processing")
        processing_tab_initialization.run(main_window=self)

        # post processing mantid
        self.postprocessing_tab_widget_m = QWidget()
        self.postprocessing_ui_m = load_ui(
            'splitui_postprocessing_mantid_tab.ui',
            baseinstance=self.postprocessing_tab_widget_m)
        self.ui.main_tab.insertTab(
            3, self.postprocessing_tab_widget_m, "Post Processing")
        postprocessing_tab_m_initialization.run(main_window=self)

        # Rietveld  tab
        self.rietveld_tab_widget = QWidget()
        self.rietveld_ui = load_ui(
            'splitui_rietveld_tab.ui',
            baseinstance=self.rietveld_tab_widget)
        self.ui.main_tab.insertTab(4, self.rietveld_tab_widget, "Rietveld")
        rietveld_tab_initialization.run(main_window=self)

        # Calculate G(R) tab
        self.calculategr_tab_widget = QWidget()
        self.calculategr_ui = load_ui(
            'splitui_calculategr_tab.ui',
            baseinstance=self.calculategr_tab_widget)
        self.ui.main_tab.insertTab(
            5, self.calculategr_tab_widget, 'Calculate G(R)')
        calculategr_tab_initialization.run(main_window=self)

        self.init_parameters()

        # Set the post-processing mode
        self.post_processing = processing_mode  # mantid or 'idl'

        # define the driver
        self._myController = driver.AddieDriver()

        # class variable for easy access
        self._gssGroupName = None
        self._currDataDir = None
        self._inputFile = None
        self._inFixedDirectoryStructure = False
        self._currWorkDir = os.getcwd()
        self._bankDict = None
        self._stem = None
        self._full_merged_path = None
        self._workspace_files = None
        self._merged_data = dict()
        self._pystog_inputs_collect = dict()
        self._pystog_output_files = dict()

        # mutex-like variables
        self._noEventBankWidgets = False

        # help (refer to DGSPlanner and HFIR Powder reduction GUI)
        self._assistantProcess = QProcess(self)

        # a collection of sub window
        self._editSqDialog = None
        self._editedSofQDict = dict()

        # color management
        self._pdfColorManager = PDFPlotManager()

        # IDL config scripts
        idl_script_dir = "/SNS/NOM/shared/autoNOM/stable/"
        if self.post_processing == "idl_dev":
            idl_script_dir = "/SNS/NOM/shared/autoNOM/dev/"
        self.idl_script_dir = idl_script_dir
        self._autonom_script = os.path.join(idl_script_dir, "autoNOM.py")
        self._sum_scans_script = os.path.join(idl_script_dir, "sumscans.py")
        self._ndabs_script = os.path.join(idl_script_dir, "NDabs.py")
        self._is_sum_scans_python_checked = False

        # Connecting all the widgets
        main_tab_events_handler.run(main_window=self)
        autonom_tab_events_handler.run(main_window=self)
        postprocessing_tab_events_handler.run(main_window=self)
        postprocessing_tab_m_events_handler.run(main_window=self)
        processing_tab_events_handler.run(main_window=self)
        rietveld_tab_events_handler.run(main_window=self)
        calculategr_tab_events_handler.run(main_window=self)

        self.activate_reduction_tabs()

        print("ADDIE successfully launched.")

    # main window

    def evt_quit(self):
        """Quit the application"""
        self.close()

    def closeEvent(self, c):
        if self.advanced_window_ui:
            self.advanced_window_ui.closeEvent(c)
        if self.make_calibration_ui:
            self.make_calibration_ui.closeEvent(c)
        if self.table_tree_ui:
            self.table_tree_ui.closeEvent(c)
        if self.key_value_pair_ui:
            self.key_value_pair_ui.closeEvent(c)

    def cancel_clicked(self):
        self.close()

    # menu

    def do_show_help(self):
        menu_event_handler.do_show_help(self)

    def action_preview_ascii_clicked(self):
        menu_event_handler.action_preview_ascii_clicked(self)

    def action_load_configuration_clicked(self):
        menu_event_handler.action_load_configuration_clicked(self)

    def action_save_configuration_clicked(self):
        menu_event_handler.action_save_configuration_clicked(self)

    def action_undo_clicked(self):
        menu_event_handler.action_undo_clicked(self)

    def action_redo_clicked(self):
        menu_event_handler.action_redo_clicked(self)

    def help_about_clicked(self):
        menu_event_handler.help_about_clicked(self)

    def advanced_option_clicked(self):
        menu_event_handler.advanced_option_clicked(self)

    def activate_reduction_tabs(self):
        menu_event_handler.activate_reduction_tabs(self)

    def menu_ipts_file_transfer_clicked(self):
        menu_event_handler.menu_ipts_file_transfer_clicked(self)

    def window_job_monitor_clicked(self):
        menu_event_handler.window_job_monitor_clicked(self)

    def help_button_clicked_autonom(self):
        help_button_activator(parent=self, button_name="autonom")

    def isrp_button_clicked(self):
        isrp_button_activator(parent=self)

    # def save_raw_config(self):
    #     '''this will allow the user to reset the full table and get it back in its initial state'''
    #     o_current_table_config = TableConfig(main_window=self)
    #     current_config = o_current_table_config.get_current_config()
    #
    #     inside_dict = OrderedDict()
    #     inside_dict['table'] = current_config
    #     inside_dict['active'] = False
    #
    #     self.reset_config_dict = inside_dict

    def main_tab_widget_changed(self, tab_selected):
        if tab_selected == 0:
            Step1GuiHandler(main_window=self)
            autonom_event_handler.check_step1_gui(self)
        if tab_selected == 1:
            _o_gui = Step2GuiHandler(main_window=self)
            _o_gui.check_gui()

    def init_parameters(self):
        ConfigurationInitializer(parent=self)

    @property
    def controller(self):
        return self._myController

    # job utility
    def launch_job_manager(
            self,
            job_name='',
            script_to_run=None,
            thread_index=-1):
        job_handler = JobStatusHandler(parent=self, job_name=job_name,
                                       script_to_run=script_to_run,
                                       thread_index=thread_index)
        job_handler.start()

    # job utility for mantidtotalscattering
    def launch_job_manager_mts(
            self,
            job_name='',
            all_commands=None,
            thread_index=-1):
        job_handler = JobStatusHandlerMTS(parent=self, job_name=job_name,
                                          all_commands=all_commands,
                                          thread_index=thread_index)
        job_handler.start()

    def kill_job(self, row=-1):
        job_row = self.job_list[row]
        parent = psutil.Process(job_row['pid'])
        for child in parent.children(recursive=True):
            if child.status != psutil.STATUS_ZOMBIE:
                for count, item in enumerate(self.job_list):
                    job_row_tmp = item
                    if job_row_tmp['pid'] == child.pid:
                        job_row_tmp['status'] = "killed"
                        job_row_tmp['pid'] = None
                        self.job_list[count] = job_row_tmp
                child.kill()
        if parent.name() != 'addie':
            parent.kill()

        table_widget = self.job_monitor_interface.ui.tableWidget
        table_widget.removeCellWidget(row, 2)
        _item = QTableWidgetItem('Killed')
        table_widget.setItem(row, 2, _item)
        job_row['status'] = "killed"
        job_row['pid'] = None
        self.job_list[row] = job_row

    def start_refresh_text_thread(self):
        _run_thread = self.logbook_thread
        _run_thread.setup(parent=self)
        _run_thread.update_text.connect(self.update_logbook)
        _run_thread.start()

    def update_logbook(self, text):
        if self.job_monitor_interface is None:
            self.logbook_thread.stop()
        else:
            LogbookHandler(parent=self)

    # autoNOM

    def select_current_folder_clicked(self):
        autonom_event_handler.select_current_folder_clicked(self)

    def diamond_edited(self):
        autonom_event_handler.check_step1_gui(self)

    def diamond_background_edited(self):
        autonom_event_handler.check_step1_gui(self)

    def vanadium_edited(self):
        autonom_event_handler.check_step1_gui(self)

    def vanadium_background_edited(self):
        autonom_event_handler.check_step1_gui(self)

    def sample_background_edited(self):
        autonom_event_handler.check_step1_gui(self)

    def create_new_autonom_folder_button_clicked(self, status):
        autonom_event_handler.create_new_autonom_folder_button_clicked(
            self, status)

    def output_folder_radio_buttons(self):
        autonom_event_handler.output_folder_radio_buttons(self)

    def manual_output_folder_field_edited(self):
        autonom_event_handler.check_step1_gui(self)

    def manual_output_folder_button_clicked(self):
        autonom_event_handler.manual_output_folder_button_clicked(self)

    def check_step1_gui(self):
        autonom_event_handler.check_step1_gui(self)

    def run_autonom(self):
        autonom_event_handler.run_autonom(self)

    def create_exp_ini_clicked(self):
        autonom_event_handler.create_exp_ini_clicked(self)

    # post processing
    def run_mantid(self):
        mantid_reduction_launcher.run_mantid(self)

    def resize_table_post_processing_tab(self, height, width):
        pass

    def move_to_folder_clicked(self):
        postprocessing_event_handler.move_to_folder_clicked(self)

    def move_to_folder_step2(self):
        postprocessing_event_handler.move_to_folder_step2(self)

    def populate_table_clicked(self):
        postprocessing_event_handler.populate_table_clicked(self)

    def import_table_clicked(self):
        postprocessing_event_handler.import_table_clicked(main_window=self)

    def export_table_clicked(self):
        postprocessing_event_handler.export_table_clicked(main_window=self)

    def table_select_state_changed(self, state, row):
        postprocessing_event_handler.table_select_state_changed(
            self, state, row)

    def name_search_clicked(self):
        postprocessing_event_handler.name_search_clicked(self)

    def clear_name_search_clicked(self):
        postprocessing_event_handler.clear_name_search_clicked(self)

    def check_step2_gui(self, row, column):
        postprocessing_event_handler.check_step2_gui(self, row, column)

    # M

    def open_and_load_workspaces(self):
        post_processing_m_event_handler.open_and_load_workspaces(main_window=self)

    def save_mconfig(self):
        post_processing_m_event_handler.save_mconfig(main_window=self)

    def save_sconfig(self):
        post_processing_m_event_handler.save_sconfig(main_window=self)

    def load_sconfig(self):
        post_processing_m_event_handler.load_sconfig(main_window=self)

    def load_mconfig(self):
        post_processing_m_event_handler.load_mconfig(main_window=self)

    def extract_button(self):
        post_processing_m_event_handler.extract_button(main_window=self)

    def clear_post_processing_canvas(self):
        post_processing_m_event_handler.clear_canvas(main_window=self)

    def change_bank(self):
        post_processing_m_event_handler.change_bank(main_window=self)

    def set_merge_values(self):
        post_processing_m_event_handler.set_merge_values(main_window=self)

    def merge_banks(self):
        post_processing_m_event_handler.merge_banks(main_window=self)

    def execute_stog(self):
        post_processing_m_event_handler.execute_stog(main_window=self)

    def set_stog_values(self):
        post_processing_m_event_handler.set_stog_values(main_window=self)

    # PDF

    def check_q_range(self):
        _o_gui = Step2GuiHandler(main_window=self)
        _o_gui.check_gui()

    def hydrogen_clicked(self):
        o_gui = Step2GuiHandler(main_window=self)
        o_gui.hydrogen_clicked()

    def no_hydrogen_clicked(self):
        o_gui = Step2GuiHandler(main_window=self)
        o_gui.no_hydrogen_clicked()

    def yes_background_clicked(self):
        o_gui = Step2GuiHandler(main_window=self)
        o_gui.yes_background_clicked()

    def no_background_clicked(self):
        o_gui = Step2GuiHandler(main_window=self)
        o_gui.no_background_clicked()

    def background_combobox_changed(self, index):
        o_gui = Step2GuiHandler(main_window=self)
        o_gui.background_index_changed(row_index=index)

    def reset_q_range(self):
        o_gui = Step2GuiHandler(main_window=self)
        o_gui.reset_q_range()

    def run_ndabs_clicked(self):
        o_create_sample_files = CreateSampleFiles(parent=self)
        o_create_sample_files.run()

        list_sample_files = o_create_sample_files.list_sample_files

        o_create_ndsum_file = CreateNdsumFile(parent=self)
        o_create_ndsum_file.run()

        o_run_ndsum = RunNDabs(parent=self, list_sample_files=list_sample_files)
        o_run_ndsum.run()

    def check_fourier_filter_widgets(self):
        o_gui = Step2GuiHandler(main_window=self)
        o_gui.check_gui()

    def check_plazcek_widgets(self):
        o_gui = Step2GuiHandler(main_window=self)
        o_gui.check_gui()

    def table_right_click(self, position):
        _o_table = IdlTableHandler(parent=self)
        _o_table.right_click(position=position)

    def run_sum_scans_clicked(self):
        o_run_sum_scans = RunSumScans(parent=self)
        o_run_sum_scans.run()

    def output_file_name_changed(self):
        o_gui = Step2GuiHandler(main_window=self)
        o_gui.check_gui()

    def pdf_qmax_line_edit_changed(self):
        o_gui = Step2GuiHandler(main_window=self)
        o_gui.check_gui()

    def sum_scans_output_file_name_changed(self):
        o_gui = Step2GuiHandler(main_window=self)
        o_gui.check_gui()

    def help_button_clicked_ndabs(self):
        help_button_activator(parent=self, button_name="ndabs")

    def help_button_clicked_scans(self):
        help_button_activator(parent=self, button_name="scans")

    # Rietveld tab
    def open_and_load_bragg_files(self):
        rietveld_event_handler.open_and_load_bragg_files(main_window=self)

    def do_set_bragg_color_marker(self):
        rietveld_event_handler.do_set_bragg_color_marker(self)

    def do_rescale_bragg(self):
        rietveld_event_handler.do_rescale_bragg(self)

    def do_clear_gr(self):
        self.calculategr_ui.graphicsView_gr.reset()

    def do_clear_sq(self):
        self.calculategr_ui.graphicsView_sq.reset()

    def evt_change_gss_mode(self):
        rietveld_event_handler.evt_change_gss_mode(main_window=self)

    def evt_plot_bragg_bank(self):
        rietveld_event_handler.plot_bragg_bank(main_window=self)

    def evt_switch_bragg_unit(self):
        rietveld_event_handler.switch_bragg_unit(main_window=self)

    def do_clear_bragg_canvas(self):
        rietveld_event_handler.do_clear_bragg_canvas(self)

    def set_bragg_ws_to_plot(self, gss_group_name):
        rietveld_event_handler.set_bragg_ws_to_plot(self, gss_group_name)

    def mantid_browse_calibration_clicked(self):
        o_mantid_gui = BrowseFileFolderHandler(parent=self)
        o_mantid_gui.browse_file(type='calibration')

    def mantid_browse_characterization_clicked(self):
        o_mantid_gui = BrowseFileFolderHandler(parent=self)
        o_mantid_gui.browse_file(type='characterization')

    def mantid_output_directory_clicked(self):
        o_mantid_gui = BrowseFileFolderHandler(parent=self)
        o_mantid_gui.browse_folder()

    def do_mantid_run_reduction(self):
        o_mantid_run = GlobalMantidReduction(parent=self)
        o_mantid_run.run()

    def check_mantid_gui(self):
        o_gui = Step2GuiHandler(main_window=self)
        o_gui.check_gui()

    def help_button_clicked_mantid(self):
        help_button_activator(parent=self, button_name="mantid")
    # G(R) tab

    def do_generate_gr(self):
        calculategr_event_handler.generate_gr_step1(self)

    def evt_qmax_changed(self):
        calculategr_event_handler.evt_qmax_changed(self)

    def evt_qmin_changed(self):
        calculategr_event_handler.evt_qmin_changed(self)

    def do_load_sq(self):
        calculategr_event_handler.load_sq(self)

    def evt_change_sq_type(self):
        calculategr_event_handler.evt_change_sq_type(self)

    def do_rescale_sofq(self):
        calculategr_event_handler.do_rescale_sofq(self)

    def do_rescale_gofr(self):
        calculategr_event_handler.do_rescale_gofr(self)

    def do_show_sq_bound(self):
        calculategr_event_handler.do_show_sq_bound(self)

    def do_load_gr(self):
        calculategr_event_handler.do_load_gr(self)

    def do_save_gr(self):
        calculategr_event_handler.do_save_gr(self)

    def do_save_sq(self):
        calculategr_event_handler.do_save_sq(self)

    def do_edit_sq(self):
        calculategr_event_handler.do_edit_sq(self)

    def do_generate_sq(self):
        calculategr_event_handler.do_generate_sq(self)

    def do_set_gofr_color_marker(self):
        calculategr_event_handler.do_set_gofr_color_marker(self)

    def do_set_sq_color_marker(self):
        calculategr_event_handler.do_set_sq_color_marker(self)

    def do_reset_gr_tab(self):
        calculategr_event_handler.do_reset_gr_tab(self)

    def do_reset_gsas_tab(self):
        bragg_event_handler.BraggTree.do_reset_gsas_tab(self)

    def edit_sq(self, sq_name, scale_factor, shift):
        calculategr_event_handler.edit_sq(self, sq_name, scale_factor, shift)

    def clear_bank_checkboxes(self):
        calculategr_event_handler.clear_bank_checkboxes(self)

    def get_default_data_dir(self):
        return self._currDataDir

    def get_workflow(self):
        """
        Return the reference to the main workflow controller
        Returns: workflow controller
        """
        return self._myController

    def set_ipython_script(self, script):
        """
        Write a command (python script) to ipython console
        Parameters
        """
        # check
        assert isinstance(script, str)

        if len(script) == 0:
            # ignore
            return
        else:
            # write to the console
            self.ui.dockWidget_ipython.execute(script)

    def update_sq_boundary(self, boundary_index, new_position):
        calculategr_event_handler.update_sq_boundary(
            self, boundary_index, new_position)

    def add_edited_sofq(
            self,
            sofq_name,
            edited_sq_name,
            shift_value,
            scale_factor_value):
        calculategr_event_handler.add_edited_sofq(
            self, sofq_name, edited_sq_name, shift_value, scale_factor_value)

    def has_edit_sofq(self, raw_sofq_name, shift_value, scale_factor_value):
        calculategr_event_handler.has_edit_sofq(
            self, raw_sofq_name, shift_value, scale_factor_value)

    # Master table
    def personalization_table_clicked(self):
        processing_event_handler.personalization_table_clicked(self)

    def table_search(self):
        processing_event_handler.table_search(self)

    def table_search_clear(self):
        processing_event_handler.table_search_clear(self)

    def load_this_config(self, key='', resize=False):
        processing_event_handler.load_this_config(self, key=key, resize=resize)

    def h3_table_right_click(self, position):
        processing_event_handler.h3_table_right_click(self)

    def check_status_of_right_click_buttons(self):
        processing_event_handler.check_status_of_right_click_buttons(self)

    def scroll_h1_table(self, value):
        processing_event_handler.scroll_h1_table(self, value)

    def scroll_h2_table(self, value):
        processing_event_handler.scroll_h2_table(self, value)

    def scroll_h3_table(self, value):
        processing_event_handler.scroll_h3_table(self, value)

    def resizing_h1(self, index_column, old_size, new_size):
        processing_event_handler.resizing_h1(
            self, index_column, old_size, new_size)

    def resizing_h2(self, index_column, old_size, new_size):
        processing_event_handler.resizing_h2(
            self, index_column, old_size, new_size)

    def resizing_h3(self, index_column, old_size, new_size):
        processing_event_handler.resizing_h3(
            self, index_column, old_size, new_size)

    def init_tree(self):
        processing_event_handler.init_tree(self)

    def tree_item_changed(self, item, _):
        processing_event_handler.tree_item_changed(self, item)

    def master_table_select_state_changed(self, state, key):
        processing_event_handler.master_table_select_state_changed(
            self, state, key)

    # sample columns
    def master_table_sample_material_button_pressed(self, key):
        processing_event_handler.sample_material_button_pressed(self, key)

    def master_table_sample_material_line_edit_entered(self, key):
        processing_event_handler.sample_material_line_edit_entered(self, key)

    def master_table_sample_mass_density_button_pressed(self, key):
        processing_event_handler.sample_mass_density_button_pressed(self, key)

    def master_table_sample_mass_density_line_edit_entered(self, key):
        processing_event_handler.sample_mass_density_line_edit_entered(
            self, key)

    def master_table_sample_shape_changed(self, index, key):
        processing_event_handler.sample_shape_changed(self, index, key)

    def master_table_sample_abs_correction_changed(self, text, key):
        processing_event_handler.sample_abs_correction_changed(self, text, key)

    def master_table_sample_multi_scattering_correction_changed(
            self, text, key):
        processing_event_handler.sample_multi_scattering_correction_changed(
            self, text, key)

    def master_table_sample_inelastic_correction_changed(self, text, key):
        processing_event_handler.sample_inelastic_correction_changed(
            self, text, key)

    def master_table_sample_placzek_button_pressed(self, key):
        processing_event_handler.sample_placzek_button_pressed(self, key)

    def master_table_sample_dimensions_setter_button_pressed(self, key):
        processing_event_handler.sample_dimensions_setter_button_pressed(
            self, key)

    def master_table_resonance_setter_button_pressed(self, key):
        processing_event_handler.sample_resonance_button_pressed(self,key)

    def master_table_scattering_setter_button_pressed(self, key):
        processing_event_handler.self_scattering_button_pressed(self,key)

    # normalization columns
    def master_table_normalization_material_button_pressed(self, key):
        processing_event_handler.normalization_material_button_pressed(
            self, key)

    def master_table_normalization_material_line_edit_entered(self, key):
        processing_event_handler.normalization_material_line_edit_entered(
            self, key)

    def master_table_normalization_mass_density_button_pressed(self, key):
        processing_event_handler.normalization_mass_density_button_pressed(
            self, key)

    def master_table_normalization_mass_density_line_edit_entered(self, key):
        processing_event_handler.normalization_mass_density_line_edit_entered(
            self, key)

    def master_table_normalization_shape_changed(self, text, key):
        processing_event_handler.normalization_shape_changed(self, text, key)

    def master_table_normalization_abs_correction_changed(self, text, key):
        processing_event_handler.normalization_abs_correction_changed(
            self, text, key)

    def master_table_normalization_multi_scattering_correction_changed(
            self,
            text,
            key):
        processing_event_handler.normalization_multi_scattering_correction_changed(
            self, text, key)

    def master_table_normalization_inelastic_correction_changed(
            self, text, key):
        processing_event_handler.normalization_inelastic_correction_changed(
            self, text, key)

    def master_table_normalization_placzek_button_pressed(self, key):
        processing_event_handler.normalization_placzek_button_pressed(
            self, key)

    def master_table_normalization_dimensions_setter_button_pressed(self, key):
        processing_event_handler.normalization_dimensions_setter_button_pressed(
            self, key)

    def launch_import_from_database_handler(self):
        processing_event_handler.launch_import_from_database_handler(self)

    def launch_import_from_run_number_handler(self):
        processing_event_handler.launch_import_from_run_number_handler(self)

    # key/value
    def master_table_keyvalue_button_pressed(self, key):
        AlignAndFocusArgsHandling(main_window=self, key=key)

    # calibrations
    def make_calibration_clicked(self):
        processing_event_handler.make_calibration_clicked(self)

    def browse_calibration_clicked(self):
        processing_event_handler.browse_calibration_clicked(self)

    def from_oncat_to_master_table(
            self,
            json=None,
            with_conflict=False,
            ignore_conflicts=False):
        processing_event_handler.from_oncat_to_master_table(
            self, json=json, with_conflict=with_conflict, ignore_conflicts=ignore_conflicts)

    def reduction_configuration_button_clicked(self):
        processing_event_handler.reduction_configuration_button_clicked(self)

    def load_ascii(self, filename=''):
        processing_event_handler.load_ascii(
            main_window=self, filename=filename)

    def check_master_table_column_highlighting(self, row=None, column=-1):
        o_highlights = ColumnHighlighting(main_window=self)
        if column == -1:
            o_highlights.check_all()
        else:
            o_highlights.check_column(column=column)

    def apply_clicked(self):
        # do stuff
        self.close()


def main(config=None):

    if config is None:
        import argparse  # noqa
        parser = argparse.ArgumentParser(
            description='ADvanced DIffraction Environment')
        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s version {}'.format(__version__))
        parser.add_argument(
            '--mode',
            type=str,
            default='idl',
            help='Set processing mode (default=%(default)s)',
            choices=[
                'mantid',
                'idl',
                'idl_dev'])

        try:  # set up bash completion as a soft dependency
            import argcomplete  # noqa
            argcomplete.autocomplete(parser)
        except ImportError:
            pass  # silently skip this

        # parse the command line options
        config = parser.parse_args()

    app = QApplication(sys.argv)
    app.setOrganizationName("ORNL / SNS")
    app.setOrganizationDomain("https://neutrons.ornl.gov/")
    app.setApplicationName("ADDIE: ADvanced DIffraction Environment")
    app.setWindowIcon(QIcon(":/icon.png"))
    form = MainWindow(processing_mode=config.mode)
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
