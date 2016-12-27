from PyQt4 import QtGui
from fastgr.ui_iptsFileTransfer import Ui_Dialog as UiDialog


class IptsFileTransferDialog(QtGui.QDialog):
    
    def __init__(self, parent=None):
        self.parent = parent
        
        QtGui.QDialog.__init__(self, parent=parent)
        self.ui = UiDialog()
        self.ui.setupUi(self)
        
    def cancel_clicked(self):
        self.close()