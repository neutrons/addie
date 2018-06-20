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

    def instrument_changed(self, index):
        instrument_selected = self.ui.instrument_comboBox.currentText()

    def cache_dir_button_clicked(self):
        _cache_folder = QtGui.QFileDialog.getExistingDirectory(caption="Select Cache Folder ...",
                                                              directory=self.parent.cache_folder,
                                                              options=QtGui.QFileDialog.ShowDirsOnly)
        if _cache_folder:
            self.ui.cache_dir_label.setText(str(_cache_folder))
            self.parent.cache_folder = str(_cache_folder)

    def output_dir_button_clicked(self):
        _output_folder = QtGui.QFileDialog.getExistingDirectory(caption="Select Output Folder ...",
                                                              directory=self.parent.output_folder,
                                                              options=QtGui.QFileDialog.ShowDirsOnly)
        if _output_folder:
            self.ui.output_dir_label.setText(str(_output_folder))
            self.parent.output_folder = str(_output_folder)

