from PyQt4 import QtGui

from fastgr.ui_advanced_window import Ui_MainWindow as UiMainWindow


class AdvancedWindow(QtGui.QMainWindow):
    
    def __init__(self, parent = None):
        self.parent = parent
        
        QtGui.QMainWindow.__init__(self, parent = parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)
        
        self.setWindowTitle("Advanced Window for Super User Only !")
        
