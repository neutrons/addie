from PyQt4 import QtGui

from addie.ui_advanced_window import Ui_MainWindow as UiMainWindow


class AdvancedWindow(QtGui.QMainWindow):
    
    def __init__(self, parent=None):
        self.parent = parent
        
        QtGui.QMainWindow.__init__(self, parent=parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)
        
        self.setWindowTitle("Advanced Window for Super User Only !")
        self.init_widgets()

    def init_widgets(self):
        _idl_status = False
        _mantid_status = False
        if self.parent.post_processing == 'idl':
            _idl_status = True
        else:
            _mantid_status = True

        self.ui.idl_post_processing_button.setChecked(_idl_status)
        self.ui.mantid_post_processing_button.setChecked(_mantid_status)

    def post_processing_clicked(self):
        if self.ui.idl_post_processing_button.isChecked():
            _index = 0
            _post = 'idl'
        else:
            _index = 1
            _post = 'mantid'

        self.parent.ui.stackedWidget.setCurrentIndex(_index)
        self.parent.post_processing = _post