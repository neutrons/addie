import os

from addie.autoNOM.step1_gui_handler import Step1GuiHandler
from addie.processing.mantid.master_table.master_table_exporter import TableFileExporter as MantidTableExporter
from addie.autoNOM.run_step1 import RunStep1
import traceback
from mantidqt.utils.asynchronous import AsyncTask

# Mantid Total Scattering
# (https://github.com/marshallmcdonnell/mantid_total_scattering)
try:
    import total_scattering
    print("Mantid Total Scattering Version: ", total_scattering.__version__)
    from total_scattering.reduction import TotalScatteringReduction
    MANTID_TS_ENABLED = True
except ImportError:
    print('total_scattering module not found. Functionality disabled')
    MANTID_TS_ENABLED = False


def select_current_folder_clicked(main_window):
    o_gui = Step1GuiHandler(main_window=main_window)
    o_gui.select_working_folder()
    main_window.check_step1_gui()


def create_new_autonom_folder_button_clicked(main_window, status):
    o_gui_handler = Step1GuiHandler(main_window=main_window)
    o_gui_handler.new_autonom_group_box(status=status)


def output_folder_radio_buttons(main_window):
    o_gui_handler = Step1GuiHandler(main_window=main_window)
    o_gui_handler.manual_output_folder_button_handler()
    o_gui_handler.check_go_button()


def manual_output_folder_button_clicked(main_window):
    o_gui = Step1GuiHandler(main_window=main_window)
    o_gui.select_manual_output_folder()
    main_window.check_step1_gui()


class JobPool(object):
    task_output = None,
    running = None
    task_exc_type, task_exc, task_exc_stack = None, None, None

    def __init__(self, configurations):
        self.jobs = []
        for config in configurations:
            print("CONFIG:", config)
            self.jobs.append(AsyncTask(TotalScatteringReduction, args=(config,),
                                       success_cb=self.on_success, error_cb=self.on_error,
                                       finished_cb=self.on_finished))

    def _start_next(self):
        if self.jobs:
            self.running = self.jobs.pop(0)
            self.running.start()
        else:
            self.running = None

    def start(self):
        if not self.jobs:
            raise RuntimeError('Cannot start empty job list')
        self._start_next()

    def on_success(self, task_result):
        # TODO should emit a signal
        self.task_output = task_result.output
        print('SUCCESS!!! {}'.format(self.task_output))

    def on_error(self, task_result):
        # TODO should emit a signal
        print('ERROR!!!')
        self.task_exc_type = task_result.exc_type
        self.task_exc = task_result.exc_value
        self.task_exc_stack = traceback.extract_tb(task_result.stack)
        traceback.print_tb(task_result.stack)

    def on_finished(self):
        '''Both success and failure call this method afterwards'''
        # TODO should emit a signal
        self._start_next()  # kick off the next one in the pool


def run_mantid(parent):
    num_rows = parent.processing_ui.h3_table.rowCount()
    if num_rows <= 0:
        raise RuntimeError('Cannot export empty table')

    exporter = MantidTableExporter(parent=parent)

    # write out the full table to disk
    # TODO make a class level name so it can be reused
    full_reduction_filename = os.path.join(
        os.path.expanduser('~'), '.mantid', 'addie.json')
    print('writing out full table to "{}"'.format(full_reduction_filename))
    exporter.export(full_reduction_filename)

    # append the individual rows to input list (reduction_inputs)
    reduction_inputs = []
    for row in range(num_rows):
        if not exporter.isActive(row):
            print('skipping row {} - inactive'.format(row + 1))  # REMOVE?
            continue
        print('Will be running row {} for reduction'.format(
            row + 1))  # TODO should be debug logging
        json_input = exporter.retrieve_row_info(row)
        reduction_inputs.append(json_input)
    if len(reduction_inputs) == 0:
        raise RuntimeError('None of the rows were activated')

    # locate total scattering script
    if MANTID_TS_ENABLED:
        pool = JobPool(reduction_inputs)
        pool.start()
    else:
        print('total_scattering module not found. Functionality disabled') # TODO should be on the status bar


def run_autonom(main_window):
    """Will first create the output folder, then create the exp.ini file"""
    _run_autonom = RunStep1(parent=main_window)
    _run_autonom.create_folder()
    print(os.getcwd())
    _run_autonom.create_exp_ini_file()


def create_exp_ini_clicked(main_window):
    _run_autonom = RunStep1(parent=main_window, run_autonom=False)
    _run_autonom.create_folder()
    _run_autonom.create_exp_ini_file()


def check_step1_gui(main_window):
    '''check the status of the step1 GUI in order to enable or not the GO BUTTON at the bottom'''
    o_gui_handler = Step1GuiHandler(main_window=main_window)
    o_gui_handler.check_go_button()
