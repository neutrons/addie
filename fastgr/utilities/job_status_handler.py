import subprocess
import time

from fastgr.utilities.job_monitor_interface import JobMonitorInterface


class JobStatusHandler(object):
    
    def __init__(self, parent=None,  job_name='', script_to_run=None, thread_index=-1):
        self.parent = parent

        if self.parent.job_monitor_interface is None:
            job_ui = JobMonitorInterface(parent = self.parent)
            job_ui.show()
            self.parent.job_monitor_interface  = job_ui
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
                   'pid': p.pid}
        job_list.append(new_job)
        self.parent.job_list = job_list

        job_ui.refresh_table(job_list)

    def get_launch_time(self):
        return time.strftime("%d %b %Y %H:%M:%S", time.gmtime())

    def start(self):
        pass