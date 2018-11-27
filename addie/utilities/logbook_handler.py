from __future__ import (absolute_import, division, print_function)
import glob
import os
import datetime

from addie.utilities.file_handler import FileHandler


class LogbookHandler(object):

    last_files = []

    def __init__(self, parent=None, max_number_of_log_files=10):
        self.parent = parent
        self.max_number_of_log_files = max_number_of_log_files

        self.retrieve_log_files()
        self.display_log_files()

    def retrieve_log_files(self):

        _number_of_log_files = self.max_number_of_log_files

        # get list of files that start by log
        list_log_files = glob.glob(self.parent.current_folder + "/logs/log.*")
        if list_log_files == []:
            return

        # sort files by time stamp
        list_log_files.sort(key=lambda x: os.path.getmtime(x))

        # last x files
        if len(list_log_files) > _number_of_log_files:
            self.last_files = list_log_files[-_number_of_log_files: -1]
        else:
            self.last_files = list_log_files

    def _get_text(self, filename=None):
        _file_handler = FileHandler(filename=filename)
        _file_handler.retrieve_contain()
        return _file_handler.file_contain

    def display_log_files(self):

        if self.parent.job_monitor_interface.ui.pause_refresh_logbook.isChecked():
            return

        list_files = self.last_files[::-1]
        if self.parent.previous_list_of_log_files == []:
            self.parent.previous_list_of_log_files = list_files
        else:
            if self.parent.previous_list_of_log_files == list_files:
                return

        if len(list_files) > 0:
            for _index, _file in enumerate(list_files):
                _title = 'LOG FILE => {}'.format(_file)
                _text = self._get_text(filename=_file)
                _end = '#####################'

                if _index == 0:
                    self.parent.job_monitor_interface.ui.logbook_text.setText(_title)
                else:
                    self.parent.job_monitor_interface.ui.logbook_text.append(_title)

                self.parent.job_monitor_interface.ui.logbook_text.append(_text)
                self.parent.job_monitor_interface.ui.logbook_text.append(_end)

            _time_format = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.parent.job_monitor_interface.ui.last_logbook_time.setText(_time_format)
        else:
            _time = str(datetime.datetime.now())
            self.parent.job_monitor_interface.ui.logbook_text.setText("{}: No Log Files Located !".format(_time))
