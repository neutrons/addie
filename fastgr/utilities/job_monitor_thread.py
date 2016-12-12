from PyQt4 import QtCore, QtGui
import os
import time


class JobMonitorThread(QtCore.QThread):
    
    def __init__(self):
        QtCore.QThread.__init__(self)
    
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
        _job_list= self.parent.job_list
        for _row, _job in enumerate(_job_list):
            _pid = _job['subprocess']
            stddata, stderr = _pid.communicate()
            if _pid.returncode == 0:
                self.job_monitor_interafce.ui.tableWidget.removeCellWidget(_row, 2)
                _item = QtGui.QTableWidgetItem("Done!")
                self.job_monitor_interafce.ui.tableWidget.setItem(_row, 2, _item)
                
            
            
            