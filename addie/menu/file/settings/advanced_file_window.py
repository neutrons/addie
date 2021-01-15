from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import QMainWindow, QFileDialog

from addie.utilities import load_ui
from addie.initialization.widgets import main_tab as main_tab_initialization


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

        QMainWindow.__init__(self, parent=parent)
        self.ui = load_ui('advanced_window.ui', baseinstance=self)

        self.setWindowTitle("Advanced Window for Super User Only !")
        self.init_widgets()

    def init_widgets(self):
        _idl_status = False
        _mantid_status = False
        if self.parent.post_processing in self.parent.idl_modes:
            _idl_status = True
        else:
            _mantid_status = True

        self.ui.idl_config_group_box.setVisible(self.parent.advanced_window_idl_groupbox_visible)

        self.ui.idl_post_processing_button.setChecked(_idl_status)
        self.ui.mantid_post_processing_button.setChecked(_mantid_status)
        # When 'idl' or 'idl_dev' model is enabled from CLI, this should enable
        # the setting box, etc. by default without the need for explicitly
        # clicking on the 'IDL' radio button.
        self.post_processing_clicked()

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

        # IDL config
        self.ui.autonom_path_line_edit.setText(self.parent._autonom_script)
        self.ui.sum_scans_path_line_edit.setText(self.parent._sum_scans_script)
        self.ui.ndabs_path_line_edit.setText(self.parent._ndabs_script)
        self.ui.idl_config_browse_button_dialog = None

        self.ui.centralwidget.setContentsMargins(10, 10, 10, 10)

    def is_idl_selected(self):
        return self.ui.idl_post_processing_button.isChecked()

    def post_processing_clicked(self):
        if self.is_idl_selected():
            _post = 'idl'
            _idl_groupbox_visible = True
        else:
            _post = 'mantid'
            _idl_groupbox_visible = False

        self.ui.idl_config_group_box.setVisible(_idl_groupbox_visible)
        self.parent.post_processing = _post
        self.parent.activate_reduction_tabs() # hide or show right tabs
        self.parent.advanced_window_idl_groupbox_visible = _idl_groupbox_visible

    def instrument_changed(self, index):
        self.parent.instrument["short_name"] = self.list_instrument_short_name[index]
        self.parent.instrument["full_name"] = self.list_instrument_full_name[index]
        main_tab_initialization.set_default_folder_path(self.parent)

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

    # IDL Config - Line Edits
    def autonom_path_line_edited(self):
        """ update autonom script in top-level after line editing """
        _script = str(self.ui.autonom_path_line_edit.text())
        self.parent._autonom_script = _script

    def sum_scans_path_line_edited(self):
        """ update sum scans script in top-level after line editing """
        _script = str(self.ui.sum_scans_path_line_edit.text())
        self.parent._sum_scans_script = _script

    def ndabs_path_line_edited(self):
        """ update ndabs script in top-level after line editing """
        _script = str(self.ui.ndabs_path_line_edit.text())
        self.parent._ndabs_script = _script

    # IDL Config - Browse Buttons
    def _idl_button_clicked(self, line_edit):
        """ Utility function to handle IDL script path browse buttons """

        # Initialize with current script in line edit
        script = str(line_edit.text())

        # Get current working directory to open file dialog in
        _current_folder = self.parent.current_folder

        # Launch file dialog
        self.ui.idl_config_browse_button_dialog = QFileDialog(
            parent=self.ui,
            directory=_current_folder,
            caption="Select File",
            filter=("Python (*.py);; All Files (*.*)"))

        # Handle if we select a file or cancel
        if self.ui.idl_config_browse_button_dialog.exec_():
            files = self.ui.idl_config_browse_button_dialog.selectedFiles()

            if files[0] != '':
                script = str(files[0])
                line_edit.setText(script)

        # Set the class attribute back to None for monitoring / testing
        self.ui.idl_config_browse_button_dialog = None

        return script

    def autonom_path_browse_button_clicked(self):
        """ Handle browse button clicked for autonom script path """
        line_edit = self.ui.autonom_path_line_edit
        self.parent._autonom_script = self._idl_button_clicked(line_edit)

    def sum_scans_path_browse_button_clicked(self):
        """ Handle browse button clicked for sum scans script path """
        line_edit = self.ui.sum_scans_path_line_edit
        self.parent._sum_scans_script = self._idl_button_clicked(line_edit)

    def ndabs_path_browse_button_clicked(self):
        """ Handle browse button clicked for ndabs script path """
        line_edit = self.ui.ndabs_path_line_edit
        self.parent._ndabs_script = self._idl_button_clicked(line_edit)

    def sum_scans_python_version_checkbox_toggled(self):
        """ Handle the sum scans checkbox for using the python version """
        _is_checked = self.ui.sum_scans_python_version_checkbox.isChecked()
        self.parent._is_sum_scans_python_checked = _is_checked

    def closeEvent(self, c):
        self.parent.advanced_window_ui = None
