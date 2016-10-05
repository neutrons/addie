from PyQt4 import QtGui

from fastgr.ui_helpGui import Ui_MainWindow as UiMainWindow

class HelpGui(QtGui.QMainWindow):
    
    '''
    button_name = ['autonom', 'ndabs', 'scans', 'mantid']
    '''
    
    def __init__(self, parent=None, button_name=''):
        self.parent = parent
        self.button_name = button_name
        
        QtGui.QMainWindow.__init__(self, parent = parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)
        
        self.ui.button_name.setText(button_name)
        
    def closeEvent(self, event=None):
        if self.button_name == 'autonom':
            self.parent.o_help_autonom = None
        elif self.button_name == 'ndabs':
            self.parent.o_help_ndabs = None
        elif self.button_name == 'scans':
            self.parent.o_help_scans = None
        elif self.button_name == 'mantid':
            self.parent.o_help_mantid = None