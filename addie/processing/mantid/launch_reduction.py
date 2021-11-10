import os
import traceback
from mantidqt.utils.asynchronous import AsyncTask

from addie.processing.mantid.master_table.master_table_exporter import TableFileExporter as MantidTableExporter

# Mantid Total Scattering integration
# (https://github.com/neutrons/mantid_total_scattering)
try:
    import total_scattering
    print("Mantid Total Scattering Version: ", total_scattering.__version__)
    from total_scattering.reduction.total_scattering_reduction import TotalScatteringReduction
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
        print("Cannot import empty table.")
        return

    exporter = MantidTableExporter(parent=parent)

    # write out the full table to disk
    # TODO make a class level name so it can be reused
    try:
        import shutil
        path = os.path.join(os.path.expanduser('~'),'.mantid' ,'JSON_output')
        shutil.rmtree(path)
    except:
        pass

    full_reduction_filename = os.path.join(
        os.path.expanduser('~'), '.mantid', 'addie.json')
    print('writing out full table to "{}"'.format(full_reduction_filename))
    for row in range(num_rows):
        dictionary,activate = exporter.retrieve_row_info(row)
        if activate == True:
            filename = os.path.join(os.path.expanduser('~'),'.mantid' ,'JSON_output',dictionary['Title'] +'_'+ str(row) + '.json') 
            exporter.export(filename,row)
            print("Row",row,"Successfully output to",filename)

    # append the individual rows to input list (reduction_inputs)
    reduction_inputs = []
    for row in range(num_rows):
        if not exporter.isActive(row):
            print('skipping row {} - inactive'.format(row + 1))  # REMOVE?
            continue
        print('Will be running row {} for reduction'.format(row + 1))  # TODO should be debug logging
        json_input = exporter.retrieve_row_info(row)[0]
        reduction_input = exporter.convert_from_row_to_reduction(json_input)
        if not reduction_input:
            return
        reduction_inputs.append(reduction_input)
    if len(reduction_inputs) == 0:
        print('None of the rows were activated')
        return

    # locate total scattering script
    if MANTID_TS_ENABLED:
        pool = JobPool(reduction_inputs)
        pool.start()
    else:
        # TODO should be on the status bar
        print('total_scattering module not found. Functionality disabled')
        return
