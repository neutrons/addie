from __future__ import (absolute_import, division, print_function)
import os
from addie.processing.idl.exp_ini_file_loader import ExpIniFileLoader


class PopulateBackgroundWidgets(object):

    list_names = []
    exp_ini_back_file = 'N/A'
    current_folder = None
    we_are_done_here = False

    def __init__(self, main_window=None):
        self.main_window_postprocessing_ui = main_window.postprocessing_ui
        self.current_folder = main_window.current_folder

    def run(self):
        self.retrieve_list_names_from_table()
        if self.we_are_done_here:
            return
        self.reset_background_combobox_index()
        self.retrieve_background_file_from_exp_ini_file()
        self.populate_widgets()

    def refresh_contain(self):
        _index_selected = self.main_window_postprocessing_ui.background_comboBox.currentIndex()
        self.retrieve_list_names_from_table()
        self.main_window_postprocessing_ui.background_comboBox.clear()
        for _item in self.list_names:
            self.main_window_postprocessing_ui.background_comboBox.addItem(_item)
        self.main_window_postprocessing_ui.background_comboBox.setCurrentIndex(_index_selected)

    def retrieve_list_names_from_table(self):
        _list_names = []
        _nbr_row = self.main_window_postprocessing_ui.table.rowCount()
        if _nbr_row == 0:
            self.we_are_done_here = True
            return
        for _index_row in range(_nbr_row):
            _label = self.main_window_postprocessing_ui.table.item(_index_row, 1).text()
            _list_names.append(_label)

        self.list_names = _list_names

    def retrieve_background_file_from_exp_ini_file(self):
        _exp_ini_full_file_name = os.path.join(self.current_folder, 'exp.ini')
        _o_exp_ini = ExpIniFileLoader(full_file_name=_exp_ini_full_file_name)
        _metadata = _o_exp_ini.metadata
        self.exp_ini_back_file = _metadata['MTc']

    def reset_background_combobox_index(self):
        self.main_window_postprocessing_ui.background_comboBox.setCurrentIndex(0)

    def populate_widgets(self):
        self.main_window_postprocessing_ui.background_comboBox.clear()
        for _item in self.list_names:
            self.main_window_postprocessing_ui.background_comboBox.addItem(_item)

        background_text = self.main_window_postprocessing_ui.table.item(0, 2).text()
        self.main_window_postprocessing_ui.background_line_edit.setText(background_text)
        self.main_window_postprocessing_ui.background_no_field.setText(self.exp_ini_back_file)
