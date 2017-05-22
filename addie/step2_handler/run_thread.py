from PyQt4 import QtCore
import os


class RunThread(QtCore.QThread):
    
    def setup(self, script=None):
        self.script = script
        
    def run(self):
        if self.script is None:
            return
        
        os.system(self.script)
