from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import (QApplication)  # noqa

import subprocess
import time

from addie.utilities.job_monitor_interface import JobMonitorInterface


class JobStatusHandler(object):

    def __init__(self, parent=None,  job_name='', script_to_run=None, thread_index=-1):
        self.parent = parent

        if self.parent.job_monitor_interface is None:
            job_ui = JobMonitorInterface(parent=self.parent)
            job_ui.show()
            QApplication.processEvents()
            self.parent.job_monitor_interface = job_ui
            job_ui.launch_logbook_thread()
        else:
            self.parent.job_monitor_interface.activateWindow()
            job_ui = self.parent.job_monitor_interface

        if job_name == '':
            return

        job_list = self.parent.job_list
        p = subprocess.Popen(script_to_run.split())

        new_job = {'job_name': job_name,
                   'time': self.get_launch_time(),
                   'status': 'processing',
                   'pid': p.pid,
                   'subprocess': p}
        job_list.append(new_job)
        self.parent.job_list = job_list

        job_ui.refresh_table(job_list)

    def update_logbook_text(self, text):
        print(text)

    def get_local_time(self):
        local_hour_offset = time.timezone / 3600.
        _gmt_time = time.gmtime()
        [year, month, day, hour, minute, seconds, _wday, _yday, _isds] = _gmt_time
        return [year, month, day, hour-local_hour_offset, minute, seconds]

    def get_launch_time(self):
        local_time = self.get_local_time()
        return "%d %d %d %d:%d:%d" % (local_time[0], local_time[1], local_time[2],
                                      local_time[3], local_time[4], local_time[5])

    def start(self):
        pass


class JobStatusHandlerMTS(object):

    def __init__(self, parent=None,  job_name='', all_commands=None, thread_index=-1):
        self.parent = parent

        if self.parent.job_monitor_interface is None:
            job_ui = JobMonitorInterface(parent=self.parent)
            job_ui.show()
            QApplication.processEvents()
            self.parent.job_monitor_interface = job_ui
            job_ui.launch_logbook_thread()
        else:
            self.parent.job_monitor_interface.activateWindow()
            job_ui = self.parent.job_monitor_interface

        if job_name == '':
            return

        job_list = self.parent.job_list

        for cmd in all_commands:
            p = subprocess.Popen(cmd)

            new_job = {'job_name': job_name,
                       'time': self.get_launch_time(),
                       'status': 'processing',
                       'pid': p.pid,
                       'subprocess': p}
            job_list.append(new_job)
            self.parent.job_list = job_list

            job_ui.refresh_table(job_list)

    def update_logbook_text(self, text):
        print(text)

    def get_local_time(self):
        local_hour_offset = time.timezone / 3600.
        _gmt_time = time.gmtime()
        [year, month, day, hour, minute, seconds, _wday, _yday, _isds] = _gmt_time
        return [year, month, day, hour-local_hour_offset, minute, seconds]

    def get_launch_time(self):
        local_time = self.get_local_time()
        return "%d %d %d %d:%d:%d" % (local_time[0], local_time[1], local_time[2],
                                      local_time[3], local_time[4], local_time[5])

    def start(self):
        pass
