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

    def start(self):
        pass