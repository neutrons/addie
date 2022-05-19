from __future__ import (absolute_import, division, print_function)
from qtpy.QtCore import (QThread)  # noqa
from qtpy.QtWidgets import (QTableWidgetItem)  # noqa
import time
import psutil


class JobMonitorThread(QThread):

    def __init__(self):
        QThread.__init__(self)

    def setup(self, parent=None, job_monitor_interface=None, refresh_rate_s=2):
        self.parent = parent
        self.job_monitor_interafce = job_monitor_interface
        self.job_monitor_interface = self.parent.job_monitor_interface
        self.refresh_rate_s = refresh_rate_s

    def run(self):
        while(True):
            time.sleep(self.refresh_rate_s)
            self._checking_status_of_jobs()

    def stop(self):
        self.terminate()

    def _checking_status_of_jobs(self):
        _job_list = self.parent.job_list
        for _row, _job in enumerate(_job_list):
            _pid = _job['pid']
            process = psutil.Process(_pid)
            if process is None:
                self.job_monitor_interafce.ui.tableWidget.removeCellWidget(_row, 2)
                _item = QTableWidgetItem("Done!")
                self.job_monitor_interafce.ui.tableWidget.setItem(_row, 2, _item)
            else:
                if _job['status'] == 'killed':
                    self.job_monitor_interafce.ui.tableWidget.removeCellWidget(_row, 2)
                    _item = QTableWidgetItem("Killed!")
                    self.job_monitor_interafce.ui.tableWidget.setItem(_row, 2, _item)
