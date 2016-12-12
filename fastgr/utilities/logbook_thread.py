from PyQt4 import QtCore, QtGui
import os
import time


class LoogbookThread(QtCore.QThread):
    
    def __init__(self):
        QtCore.QThread.__init__(self)
    
    def setup(self, parent=None, logbook_interface=None, refresh_rate_s = 5):
        self.parent = parent
        self.logbook_interface = logbook_interface
        self.refresh_rate_s = refresh_rate_s
        
    def run(self):
        while(True):
            time.sleep(self.refresh_rate_s)
            self._checking_logbook()
        
    def stop(self):
        self.terminate()

    def _checking_logbook(self):
        _number_of_log_files = self.parent.number_of_last_log_files_to_display
        
                        
            
            
            