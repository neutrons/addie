from PyQt4.QtCore import Qt
from PyQt4 import QtGui
from step2_handler.populate_master_table import PopulateMasterTable


class TableHandler(object):
    
    list_selected_row = None
    
    def __init__(self, parent=None):
        self.parent = parent.ui
        self.parent_no_ui = parent
        
    def retrieve_list_of_selected_rows(self):
        self.list_selected_row = []
        for _row_index in range(self.parent.table.rowCount()):
            _selected_widget = self.parent.table.cellWidget(_row_index, 0)
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

        menu = QtGui.QMenu(self.parent_no_ui)
        _new_row = menu.addAction("Insert Blank Row")

        if (self.parent.table.rowCount() > 0):
            _duplicate_row = menu.addAction("Duplicate Row")
            menu.addSeparator()
            _remove_row = menu.addAction("Remove Top Row Selected")
        
        action = menu.exec_(QtGui.QCursor.pos())
        self.current_row = self.current_row()
            
        if action == _duplicate_row:
            self._duplicate_row()
        elif action == _new_row:
            self._new_row()
        elif action == _remove_row:
            self._remove_row()
            
    def _duplicate_row(self):
        _row = self.current_row
        metadata_to_copy = self._collect_metadata(row_index = _row)
        o_populate = PopulateMasterTable(parent = self.parent)
        o_populate.add_new_row(metadata_to_copy, row = _row)
    
    def _new_row(self):
        _row = self.current_row
        if _row == -1:
            _row = 0
        o_populate = PopulateMasterTable(parent = self.parent_no_ui)
        _metadata = o_populate.empty_metadata()
        o_populate.add_new_row(_metadata, row = _row)
    
    def _remove_row(self):
        _row = self.current_row
        self.parent.table.removeRow(_row)