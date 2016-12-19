import os
import numpy as np
from PyQt4.QtCore import Qt
from PyQt4 import QtGui, QtCore
import fastgr.step2_handler.populate_master_table
from fastgr.step2_handler.export_table import ExportTable
from fastgr.step2_handler.import_table import ImportTable
from fastgr.utilities.file_handler import FileHandler
from fastgr.step2_handler.populate_background_widgets import PopulateBackgroundWidgets
import fastgr.step2_handler.step2_gui_handler


class TableHandler(object):
    
    list_selected_row = None
    
    def __init__(self, parent=None):
        self.parent = parent.ui
        self.parent_no_ui = parent
        
    def retrieve_list_of_selected_rows(self):
        self.list_selected_row = []
        for _row_index in range(self.parent.table.rowCount()):
            _widgets = self.parent.table.cellWidget(_row_index, 0).children()
            if len(_widgets) > 0:
                _selected_widget = self.parent.table.cellWidget(_row_index, 0).children()[1]
                if (_selected_widget.checkState() == Qt.Checked):
                    _entry = self._collect_metadata(row_index = _row_index)
                    self.list_selected_row.append(_entry)
        
    def _collect_metadata(self, row_index = -1):
        if row_index == -1:
            return []
        
        _name = self.retrieve_item_text(row_index, 1)
        _runs = self.retrieve_item_text(row_index, 2)
        _sample_formula = self.retrieve_item_text(row_index, 3)
        _mass_density = self.retrieve_item_text(row_index, 4)
        _radius = self.retrieve_item_text(row_index, 5)
        _packing_fraction = self.retrieve_item_text(row_index, 6)
        _sample_shape = self._retrieve_sample_shape(row_index)
        _do_abs_correction = self._retrieve_do_abs_correction(row_index)
        
        _metadata = {'name': _name,
                     'runs': _runs,
                     'sample_formula': _sample_formula,
                     'mass_density': _mass_density,
                     'radius': _radius,
                     'packing_fraction': _packing_fraction,
                     'sample_shape': _sample_shape,
                     'do_abs_correction': _do_abs_correction}
        
        return _metadata

    def retrieve_item_text(self, row, column):
        _item = self.parent.table.item(row, column)
        if _item is None:
            return ''
        else:
            return str(_item.text())
        
    def _retrieve_sample_shape(self, row_index):
        _widget = self.parent.table.cellWidget(row_index, 7)
        _selected_index = _widget.currentIndex()
        _sample_shape = _widget.itemText(_selected_index)
        return _sample_shape
            
    def _retrieve_do_abs_correction(self, row_index):
        _widget = self.parent.table.cellWidget(row_index, 8).children()[1]
        if (_widget.checkState() == Qt.Checked):
            return 'go'
        else:
            return 'nogo'

    def current_row(self):
        _row = self.parent.table.currentRow()
        return _row
            
    def right_click(self, position = None):
        _duplicate_row = -1
        _remove_row = -1
        _new_row = -1
        _copy = -1
        _paste = -1
        _cut = -1
        _refresh_table = -1
        _clear_table = -1
        _import = -1
        _export = -1
        _check_all = -1
        _uncheck_all = -1

        menu = QtGui.QMenu(self.parent_no_ui)

        if self.parent_no_ui.table_selection_buffer == {}:
            paste_status = False
        else:
            paste_status = True

        if (self.parent.table.rowCount() > 0):
            _undo = menu.addAction("Undo")
            _undo.setEnabled(self.parent_no_ui.undo_button_enabled)
            _redo = menu.addAction("Redo")
            _redo.setEnabled(self.parent_no_ui.redo_button_enabled)
            menu.addSeparator()
            _copy = menu.addAction("Copy")
            _paste = menu.addAction("Paste")
            self._paste_menu = _paste
            _paste.setEnabled(paste_status)
            _cut = menu.addAction("Clear")
            menu.addSeparator()
            _check_all = menu.addAction("Check All")
            _uncheck_all = menu.addAction("Unchecked All")
            menu.addSeparator()
            _invert_selection = menu.addAction("Inverse Selection")
            menu.addSeparator()
        
        _new_row = menu.addAction("Insert Blank Row")
        
        if (self.parent.table.rowCount() > 0):
            _duplicate_row = menu.addAction("Duplicate Row")
            _remove_row = menu.addAction("Remove Row(s)")
            menu.addSeparator()
            _refresh_table = menu.addAction("Refresh/Reset Table")
            _clear_table = menu.addAction("Clear Table")
        
        action = menu.exec_(QtGui.QCursor.pos())
        self.current_row = self.current_row()
            
        if action == _undo:
            self.parent_no_ui.action_undo_clicked()
        elif action == _redo:
            self.parent_no_ui.action_redo_clicked()
        elif action == _copy:
            self._copy()
        elif action == _paste:
            self._paste()
        elif action == _cut:
            self._cut()
        elif action == _duplicate_row:
            self._duplicate_row()
        elif action == _invert_selection:
            self._inverse_selection()
        elif action == _new_row:
            self._new_row()
        elif action == _remove_row:
            self._remove_selected_rows()
        elif action == _refresh_table:
            self._refresh_table()
        elif action == _clear_table:
            self._clear_table()
        elif action == _check_all:
            self.check_all()
        elif action == _uncheck_all:
            self.uncheck_all()
            
    def _import(self):
        _current_folder = self.parent_no_ui.current_folder
        _table_file = QtGui.QFileDialog.getOpenFileName(parent = self.parent_no_ui,
                                                             caption = "Select File",
                                                             directory = _current_folder,
                                                             filter = ("text (*.txt);; All Files (*.*)"))
        if _table_file:
            new_path = os.path.dirname(_table_file)
            self.parent_no_ui.current_folder = new_path
            
            self._clear_table()
            
            _import_handler = ImportTable(filename = _table_file, parent=self.parent_no_ui)
            _import_handler.run()
            
            _pop_back_wdg = PopulateBackgroundWidgets(parent = self.parent_no_ui)
            _pop_back_wdg.run()
            
            _o_gui = fastgr.step2_handler.step2_gui_handler.Step2GuiHandler(parent = self.parent_no_ui)
            _o_gui.check_gui()
            
    def _export(self):
        _current_folder = self.parent_no_ui.current_folder
        _table_file = QtGui.QFileDialog.getSaveFileName(parent = self.parent_no_ui,
                                                             caption = "Select File",
                                                             directory = _current_folder,
                                                             filter = ("text (*.txt);; All Files (*.*)"))
        if _table_file:
            _file_handler = FileHandler(filename = _table_file)
            _file_handler.check_file_extension(ext_requested='txt')
            _table_file = _file_handler.filename

            _export_handler = ExportTable(parent = self.parent_no_ui, 
                                          filename = _table_file)
            _export_handler.run()
           
    def _copy(self):
        _selection = self.parent.table.selectedRanges()
        _selection = _selection[0]
        left_column = _selection.leftColumn()
        right_column = _selection.rightColumn()
        top_row = _selection.topRow()
        bottom_row = _selection.bottomRow()
        
        self.parent_no_ui.table_selection_buffer = {'left_column': left_column,
                                                    'right_column': right_column,
                                                    'top_row': top_row,
                                                    'bottom_row': bottom_row}
        self._paste_menu.setEnabled(True)
    
    def _paste(self, _cut = False):
        _copy_selection = self.parent_no_ui.table_selection_buffer
        _copy_left_column = _copy_selection['left_column']
        
        #make sure selection start at the same column
        _paste_selection = self.parent.table.selectedRanges()
        _paste_left_column = _paste_selection[0].leftColumn()
        
        if not (_copy_left_column == _paste_left_column):
            _error_box = QtGui.QMessageBox.warning(self.parent_no_ui,  
                                                   "Check copy/paste selection!", 
                                                   "Check your selection!                   ")
            return
        
        _copy_right_column = _copy_selection["right_column"]
        _copy_top_row = _copy_selection["top_row"]
        _copy_bottom_row = _copy_selection["bottom_row"]
        
        _paste_top_row = _paste_selection[0].topRow()
        
        index = 0
        for _row in range(_copy_top_row, _copy_bottom_row+1):
            _paste_row = _paste_top_row + index
            for _column in range(_copy_left_column, _copy_right_column + 1):

                if _column in np.arange(1,7):
                    if _cut:
                        _item_text = ''
                    else:
                        _item_text = self.retrieve_item_text(_row, _column)
                    self.paste_item_text(_paste_row, _column, _item_text)

                if _column == 7:
                    if _cut:
                        _widget_index = 0
                    else:
                        _widget_index = self.retrieve_sample_shape_index(_row)
                    self.set_widget_index(_widget_index, _paste_row)

                if _column == 8:
                    if _cut:
                        _widget_state = QtCore.Qt.Unchecked
                    else:    
                        _widget_state = self.retrieve_do_abs_correction_state(_row)
                    self.set_widget_state(_widget_state, _paste_row)
                    
            index += 1
    
    def _inverse_selection(self):
        selected_range = self.parent_no_ui.ui.table.selectedRanges()
        nbr_column = self.parent.table.columnCount()

        self.select_all(status= True)

        # inverse selected rows
        for _range in selected_range:
            _range.leftColumn = 0
            _range.rightColun = nbr_column-1
            self.parent_no_ui.ui.table.setRangeSelected(_range, False)

    def select_all(self, status=True):
        nbr_row = self.parent.table.rowCount()
        nbr_column = self.parent.table.columnCount()
        selected_range = self.parent_no_ui.ui.table.selectedRanges()
        _full_range = QtGui.QTableWidgetSelectionRange(0, 0, nbr_row-1, nbr_column-1)
        self.parent.table.setRangeSelected(_full_range, status)

    def check_all(self):
        self.select_first_column(status = True)
        
    def uncheck_all(self):
        self.select_first_column(status = False)

    def select_row(self, row=-1, status=True):
        nbr_column = self.parent.table.columnCount()
        _range = QtGui.QTableWidgetSelectionRange(row, 0, row, nbr_column-1)
        self.parent.table.setRangeSelected(_range, status)

    def check_row(self, row=-1, status=True):
        _widgets = self.parent.table.cellWidget(row, 0).children()
        if len(_widgets) > 0:
            _selected_widget = self.parent.table.cellWidget(row, 0).children()[1]
            _selected_widget.setChecked(status)
        
    def select_first_column(self, status=True):
        for _row in range(self.parent.table.rowCount()):
            _widgets = self.parent.table.cellWidget(_row, 0).children()
            if len(_widgets) > 0:
                _selected_widget = self.parent.table.cellWidget(_row, 0).children()[1]
                _selected_widget.setChecked(status)

        _o_gui = fastgr.step2_handler.step2_gui_handler.Step2GuiHandler(parent = self.parent_no_ui)
        _o_gui.check_gui()
    
    def check_selection_status(self, state, row):
        list_ranges = self.parent.table.selectedRanges()
        for _range in list_ranges:
            bottom_row = _range.bottomRow()
            top_row = _range.topRow()
            range_row = range(top_row, bottom_row + 1)
        
            for _row in range_row:
                _widgets = self.parent.table.cellWidget(_row, 0).children()
                if len(_widgets) > 0:
                    _selected_widget = self.parent.table.cellWidget(_row, 0).children()[1]
                    _selected_widget.setChecked(state)
                    
        _o_gui = fastgr.step2_handler.step2_gui_handler.Step2GuiHandler(parent = self.parent_no_ui)
        _o_gui.check_gui()

    def _cut(self):
        self._copy()
        self._paste(_cut = True)
            
    def _duplicate_row(self):
        _row = self.current_row
        metadata_to_copy = self._collect_metadata(row_index = _row)
        o_populate = fastgr.step2_handler.populate_master_table.PopulateMasterTable(parent = self.parent)
        o_populate.add_new_row(metadata_to_copy, row = _row)
    
    def _new_row(self):
        _row = self.current_row
        if _row == -1:
            _row = 0
        o_populate = fastgr.step2_handler.populate_master_table.PopulateMasterTable(parent = self.parent_no_ui)
        _metadata = o_populate.empty_metadata()
        o_populate.add_new_row(_metadata, row = _row)
        
    def _remove_selected_rows(self):
        selected_range = self.parent_no_ui.ui.table.selectedRanges()
        _nbr_row_removed = 0
        _local_nbr_row_removed = 0
        for _range in selected_range:
            _top_row = _range.topRow()
            _bottom_row = _range.bottomRow()
            nbr_row = _bottom_row - _top_row + 1
            for i in np.arange(nbr_row):
                self._remove_row(row=_top_row - _nbr_row_removed)
                _local_nbr_row_removed += 1
            _nbr_row_removed = _local_nbr_row_removed    
            
        _pop_back_wdg = PopulateBackgroundWidgets(parent=self.parent_no_ui)
        _pop_back_wdg.run()
    
    def _remove_row(self, row=-1):
        if row == -1:
            row = self.current_row
        self.parent.table.removeRow(row)
        
        _o_gui = fastgr.step2_handler.step2_gui_handler.Step2GuiHandler(parent = self.parent_no_ui)
        _o_gui.check_gui()
        
    def _refresh_table(self):
        self.parent_no_ui.populate_table_clicked()

        _o_gui = fastgr.step2_handler.step2_gui_handler.Step2GuiHandler(parent = self.parent_no_ui)
        _o_gui.check_gui()

    def _clear_table(self):
        _number_of_row = self.parent.table.rowCount()
        self.parent.table.setSortingEnabled(False)
        for _row in np.arange(_number_of_row):
            self.parent.table.removeRow(0)
        self.parent.background_line_edit.setText("")
        self.parent.background_comboBox.clear()
    
        _o_gui = fastgr.step2_handler.step2_gui_handler.Step2GuiHandler(parent = self.parent_no_ui)
        _o_gui.check_gui()
        
    def set_widget_state(self, _widget_state, _row):
        _widget = self.parent.table.cellWidget(_row, 8).children()[1]
        _widget.setCheckState(_widget_state)
    
    def retrieve_do_abs_correction_state(self, _row):
        _widget = self.parent.table.cellWidget(_row, 8).children()[1]
        return _widget.checkState()
    
    def set_widget_index(self, _widget_index, _row):
        _widget = self.parent.table.cellWidget(_row, 7)
        _widget.setCurrentIndex(_widget_index)
    
    def paste_item_text(self, _row, _column, _item_text):    
        _item = self.parent.table.item(_row, _column)
        _item.setText(_item_text)
    
    def retrieve_sample_shape_index(self, row_index):
        _widget = self.parent.table.cellWidget(row_index, 7)
        _selected_index = _widget.currentIndex()
        return _selected_index
    
    def retrieve_item_text(self, row, column):
        _item = self.parent.table.item(row, column)
        if _item is None:
            return ''
        else:
            return str(_item.text())

    def name_search(self):
        nbr_row = self.parent.table.rowCount()
        if nbr_row == 0:
            return

        _string = str(self.parent.name_search.text()).lower()        
        if _string == '':
            self.select_all(status= False)
        else:
            for _row in range(nbr_row):
                _text_row = str(self.parent.table.item(_row, 1).text()).lower()
                if _string in _text_row:
                    self.select_row(row=_row, status=True)
                
        
        
        
        