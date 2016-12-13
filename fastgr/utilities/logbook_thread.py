from PyQt4 import QtCore, QtGui
import time


class LogbookThread(QtCore.QThread):
    
    last_files = []
    update_text = QtCore.pyqtSignal(str)
    refresh_rate_s = 5
    
    def __init__(self):
        QtCore.QThread.__init__(self)
    
    def setup(self, parent=None):
        self.parent = parent
        
    def run(self):
        while(True):
            self._displaying_log_files()
            time.sleep(self.refresh_rate_s)        
    
    def stop(self):
        self.terminate()

    def _displaying_log_files(self):
        self.update_text.emit('update list')

            