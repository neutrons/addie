from PyQt4 import QtGui

from fastgr.ui_helpGui import Ui_MainWindow as UiMainWindow

class HelpGui(QtGui.QMainWindow):
    
    '''
    button_name = ['autonom', 'ndabs', 'scans', 'mantid']
    '''
    
    def __init__(self, parent=None, button_name=''):
        self.parent = parent
        
        QtGui.QMainWindow.__init__(self, parent = parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)
        
        self.ui.button_name.setText(button_name)
        