from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import QMainWindow, QFileDialog
from addie.utilities import load_ui


#class AdvancedWindow(QMainWindow):

class AdvancedWindowLauncher(object):

    def __init__(self, parent=None):
        self.parent = parent

        if self.parent.advanced_window_ui is None:
            _advanced = AdvancedWindow(parent=self.parent)
            _advanced.show()
            self.parent.advanced_window_ui = _advanced
        else:
            self.parent.advanced_window_ui.setFocus()
            self.parent.advanced_window_ui.activateWindow()


class AdvancedWindow(QMainWindow):
    
    def __init__(self, parent=None):
        self.parent = parent
        
        #QtGui.QMainWindow.__init__(self, parent=parent)
        QMainWindow.__init__(self, parent=parent)
        self.ui = load_ui('advanced_window.ui', baseinstance=self)

        #self.ui = UiMainWindow()
        #self.ui.setupUi(self)
        
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

        instrument = self.parent.instrument["full_name"]
        list_instrument_full_name = self.parent.list_instrument["full_name"]
        self.list_instrument_full_name = list_instrument_full_name
        list_instrument_short_name = self.parent.list_instrument["short_name"]
        self.list_instrument_short_name = list_instrument_short_name

        self.ui.instrument_comboBox.addItems(list_instrument_full_name)
        index_instrument = self.ui.instrument_comboBox.findText(instrument)
        self.ui.instrument_comboBox.setCurrentIndex(index_instrument)
        self.parent.instrument["short_name"] = list_instrument_short_name[index_instrument]
        self.parent.instrument["full_name"] = list_instrument_full_name[index_instrument]

        self.ui.cache_dir_label.setText(self.parent.cache_folder)
        self.ui.output_dir_label.setText(self.parent.output_folder)

    def post_processing_clicked(self):
        if self.ui.idl_post_processing_button.isChecked():
            _index = 0
            _post = 'idl'
        else:
            _index = 1
            _post = 'mantid'

        self.parent.ui.stackedWidget.setCurrentIndex(_index)
        self.parent.post_processing = _post
        self.parent.activate_reduction_tabs() # hide or show right tabs

    def instrument_changed(self, index):
        self.parent.instrument["short_name"] = self.list_instrument_short_name[index]
        self.parent.instrument["full_name"] = self.list_instrument_full_name[index]
        self.parent.set_default_folders_path()

    def cache_dir_button_clicked(self):
        _cache_folder = QFileDialog.getExistingDirectory(caption="Select Cache Folder ...",
                                                              directory=self.parent.cache_folder,
                                                              options=QFileDialog.ShowDirsOnly)
        if _cache_folder:
            self.ui.cache_dir_label.setText(str(_cache_folder))
            self.parent.cache_folder = str(_cache_folder)

    def output_dir_button_clicked(self):
        _output_folder = QFileDialog.getExistingDirectory(caption="Select Output Folder ...",
                                                              directory=self.parent.output_folder,
                                                              options=QFileDialog.ShowDirsOnly)
        if _output_folder:
            self.ui.output_dir_label.setText(str(_output_folder))
            self.parent.output_folder = str(_output_folder)

    def closeEvent(self, c):
        self.parent.advanced_window_ui = None

# =======
#     def __init__(self, parent=None):
#         self.parent = parent
#
#         QMainWindow.__init__(self, parent=parent)
#         self.ui = load_ui('advanced_window.ui', baseinstance=self)
#
#         self.setWindowTitle("Advanced Window for Super User Only !")
# >>>>>>> master
