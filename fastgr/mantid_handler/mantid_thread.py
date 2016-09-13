from PyQt4 import QtCore
import os

from mantid.simpleapi import *
import mantid


class MantidThread(QtCore.QThread):
    
    def setup(self, runs=None, parameters=None):
        self.runs = runs
        self.parameters = parameters
        
    def run(self):
        pass
