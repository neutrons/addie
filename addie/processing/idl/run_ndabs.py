from __future__ import (absolute_import, division, print_function)
from addie.utilities.job_status_handler import JobStatusHandler


class RunNDabs(object):

    script_to_run = '/usr/bin/python /SNS/NOM/shared/autoNOM/stable/NDabs.py -f '

    def __init__(self, parent=None, list_sample_files=None):
        self.parent = parent
        if list_sample_files == []:
            return

        self.list_sample_files = list_sample_files

    def run(self):
        _str_list_sample_files = " ".join(self.list_sample_files)
        ui = self.parent.postprocessing_ui
        _output_filename = ui.run_ndabs_output_file_name.text()
        _script_to_run = "{} {}.ndsum {}".format(
            self.script_to_run,
            _output_filename,
            _str_list_sample_files)

        JobStatusHandler(parent=self.parent,
                         script_to_run=_script_to_run,
                         job_name='NDabs')

        print("[LOG] executing:")
        print("[LOG] " + _script_to_run)
