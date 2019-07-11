import os
import traceback
from mantidqt.utils.asynchronous import AsyncTask

from addie.processing.mantid.master_table.master_table_exporter import TableFileExporter as MantidTableExporter

# Mantid Total Scattering integration
# (https://github.com/marshallmcdonnell/mantid_total_scattering)
try:
    import total_scattering
    print("Mantid Total Scattering Version: ", total_scattering.__version__)
    from total_scattering.reduction import TotalScatteringReduction
    MANTID_TS_ENABLED = True
except ImportError:
    print('total_scattering module not found. Functionality disabled')
    MANTID_TS_ENABLED = False


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
        print(task_result)

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
        reduction_input = exporter.convert_from_row_to_reduction(json_input)
        reduction_inputs.append(reduction_input)
    if len(reduction_inputs) == 0:
        raise RuntimeError('None of the rows were activated')

    # locate total scattering script
    if MANTID_TS_ENABLED:
        pool = JobPool(reduction_inputs)
        pool.start()
    else:
        # TODO should be on the status bar
        print('total_scattering module not found. Functionality disabled')
