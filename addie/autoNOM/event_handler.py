import os

from addie.autoNOM.step1_gui_handler import Step1GuiHandler
from addie.processing.mantid.master_table.master_table_exporter import TableFileExporter as MantidTableExporter
from addie.autoNOM.run_step1 import RunStep1

# Mantid Total Scattering (https://github.com/marshallmcdonnell/mantid_total_scattering)
try:
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


def run_mantid(self):
        num_rows = self.processing_ui.h3_table.rowCount()
        if num_rows <= 0:
            raise RuntimeError('Cannot export empty table')

        exporter = MantidTableExporter(parent=self)

        # write out the full table to disk
        # TODO make a class level name so it can be reused
        full_reduction_filename = os.path.join(os.path.expanduser('~'), '.mantid', 'addie.json')
        print('writing out full table to "{}"'.format(full_reduction_filename))
        exporter.export(full_reduction_filename)

        # append the individual rows to input list (reduction_inputs)
        reduction_inputs = []
        for row in range(num_rows):
            if not exporter.isActive(row):
                print('skipping row {} - inactive'.format(row + 1))  # REMOVE?
                continue
            print('Will be running row {} for reduction'.format(row + 1))  # TODO should be debug logging
            json_input = exporter.retrieve_row_info(row)
            reduction_inputs.append(json_input)
        if len(reduction_inputs) == 0:
            raise RuntimeError('None of the rows were activated')

        # locate total scattering script
        if MANTID_TS_ENABLED:
            # TODO should allow for prefixing with mantidpython
            # TODO figure out how to launch the jobs in serial
            for json_input in reduction_inputs:
                TotalScatteringReduction(json_input)
                # TODO get this to work with launch_job_manager (example below for running from file):
                #cmd = ' '.join([pythonpath, mantid_ts_script, filename]).strip()
                #name = os.path.basename(filename).replace('.json', '')
                #print(cmd)
                #self.launch_job_manager(job_name=name, script_to_run=cmd)
        if MANTID_TS_ENABLED:
            print('total_scattering module not found. Functionality disabled')


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
