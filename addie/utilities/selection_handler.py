import numpy as np
import pprint

try:
    from PyQt4.QtGui import QCheckBox, QLabel, QPushButton, QComboBox, QTableWidgetItem
    from PyQt4 import QtGui
except ImportError:
    try:
        from PyQt5.QtWidgets import QCheckBox, QLabel, QPushButton, QComboBox, QTableWidgetItem
        from PyQt5 import QtGui
    except ImportError:
        raise ImportError("Requires PyQt4 or PyQt5")


class SelectionHandler:

    right_column = -1
    left_column = -2
    top_row = -1
    bottom_row = -2

    def __init__(self, selection_range):

        if len(selection_range) == 0:
            return

        # only considering the first selection in this class
        selection_range = selection_range[0]

        self.selection_range = selection_range
        self.left_column = self.selection_range.leftColumn()
        self.right_column = self.selection_range.rightColumn()
        self.top_row = self.selection_range.topRow()
        self.bottom_row = self.selection_range.bottomRow()

    def nbr_column_selected(self):
        return (self.right_column - self.left_column) + 1

    def nbr_row_selected(self):
        return (self.top_row - self.bottom_row) + 1

    def first_column_selected(self):
        return self.left_column

    def first_row_selected(self):
        return self.top_row

    def get_list_column(self):
        return np.arange(self.left_column, self.right_column+1)

    def get_list_row(self):
        return np.arange(self.top_row, self.bottom_row+1)


class SelectionHandlerMaster:

    def __init__(self, parent=None):
        self.parent = parent
        self.table_ui = self.parent.ui.h3_table

    def get_ui_key_for_this_row(self, row=-1):
        _check_box_ui_of_this_row = self.table_ui.cellWidget(row, 0).children()[1]
        _table_list_ui = self.parent.master_table_list_ui
        for _key in _table_list_ui.keys():
            if _table_list_ui[_key]['active'] == _check_box_ui_of_this_row:
                return _key
        return None

    def get_list_ui_for_this_row(self, row=-1):
        _check_box_ui_of_this_row = self.table_ui.cellWidget(row, 0).children()[1]
        _table_list_ui = self.parent.master_table_list_ui
        for _key in _table_list_ui.keys():
            if _table_list_ui[_key]['active'] == _check_box_ui_of_this_row:
                list_ui = [_check_box_ui_of_this_row,
                        _table_list_ui[_key]['sample']['shape'],
                        _table_list_ui[_key]['sample']['abs_correction'],
                        _table_list_ui[_key]['sample']['mult_scat_correction'],
                        _table_list_ui[_key]['sample']['inelastic_correction'],
                        _table_list_ui[_key]['normalization']['abs_correction'],
                        _table_list_ui[_key]['normalization']['mult_scat_correction'],
                        _table_list_ui[_key]['normalization']['inelastic_correction'],
                        ]
                self.parent.master_table_list_ui[_key] = {}
                return list_ui
        return []

    def lock_signals(self, list_ui=[], lock=True):
        if list_ui == []:
            return

        for _ui in list_ui:
            if _ui is not None:
                _ui.blockSignals(lock)

class TransferH3TableWidgetState(SelectionHandlerMaster):

    def __init__(self, parent=None):
        SelectionHandlerMaster.__init__(self, parent=parent)

    def transfer_states(self, state=None, value=''):

        selection = self.parent.ui.h3_table.selectedRanges()
        o_selection = SelectionHandler(selection)

        # enable or disable all other selected rows (if only first column selected)
        if (o_selection.nbr_column_selected() == 1):

            range_row = o_selection.get_list_row()
            column_selected = o_selection.first_column_selected()

            # activate row widget
            if (column_selected == 0):

                # apply state to all the widgets
                for _row in range_row:
                    ui = self.table_ui.cellWidget(_row, 0).children()[1]
                    ui.blockSignals(True)
                    ui.setCheckState(state)
                    ui.blockSignals(False)

            # sample or normalization, shape, abs. corr., mult. scat. corr or inelastic corr.
            elif (column_selected in [7, 10, 11, 12, 18, 21, 22, 23]):

                for _row in range_row:
                    ui = self.table_ui.cellWidget(_row, column_selected).children()[1]
                    index = ui.findText(value)
                    # we found the text
                    if index > -1:
                        if not column_selected in [7, 18]:
                            ui.blockSignals(True)
                        ui.setCurrentIndex(index)
                        if not column_selected in [7, 18]:
                            ui.blockSignals(False)


class RowsHandler(SelectionHandlerMaster):

    def __init__(self, parent=None):
        SelectionHandlerMaster.__init__(self, parent=parent)
        selection = self.table_ui.selectedRanges()
        self.selection = selection
        self.o_selection = SelectionHandler(selection)

    def copy(self, row=None):
        # select entire row
        if row is None:
            list_row = self.o_selection.get_list_row()
            if len(list_row) > 1:
                self.parent.ui.statusbar.setStyleSheet("color: red")
                self.parent.ui.statusbar.showMessage("Please select only 1 row!",
                                                     self.parent.statusbar_display_time)
                return

            row = list_row[0]

        _table_ui = self.parent.ui.h3_table
        nbr_col = _table_ui.columnCount()
        _row_selection = QtGui.QTableWidgetSelectionRange(row, 0, row, nbr_col-1)
        _table_ui.setRangeSelected(_row_selection, True)
        self.parent.ui.statusbar.setStyleSheet("color: green")
        self.parent.ui.statusbar.showMessage("Select another row to copy the current selected row!",
                                             self.parent.statusbar_display_time)

        self.parent.master_table_cells_copy['temp'] = []
        self.parent.master_table_cells_copy['list_column'] = []
        self.parent.master_table_cells_copy['row'] = row
        self.parent.master_table_right_click_buttons['row_paste']['status'] = True

    def paste(self, row=None):
        if row is None:
            list_to_row = self.o_selection.get_list_row()
            nbr_col = self.table_ui.columnCount()
            _row_selection = QtGui.QTableWidgetSelectionRange(list_to_row[0],
                                                              0,
                                                              list_to_row[-1],
                                                              nbr_col - 1)
            self.table_ui.setRangeSelected(_row_selection, True)

            list_to_row = self.o_selection.get_list_row()

        else:
            list_to_row = [row]
        from_row = self.parent.master_table_cells_copy['row']
        nbr_col = self.table_ui.columnCount()
        o_copy = CopyCells(parent=self.parent)
        list_column_copy = np.arange(0, nbr_col)
        for _row in list_to_row:
            for _column in list_column_copy:
                o_copy.copy_from_to(from_row=from_row,
                                    from_col=_column,
                                    to_row=_row)

    def remove(self, row=None):
        if row is None:
            list_to_row = self.o_selection.get_list_row()
            _first_row = list_to_row[0]
            for _row in list_to_row:
                self.remove(row=_first_row)
        else:
            #self.table_ui.blockSignals(True)
            self.table_ui.setRangeSelected(self.selection[0], False)
            self.table_ui.removeRow(row)
            #self.table_ui.blockSignals(False)


class CellsHandler(SelectionHandlerMaster):

    def __init__(self, parent=None):
        SelectionHandlerMaster.__init__(self, parent=parent)
        selection = self.table_ui.selectedRanges()
        self.o_selection = SelectionHandler(selection)

    def clear(self):
        list_row = self.o_selection.get_list_row()
        list_column = self.o_selection.get_list_column()

        for _row in list_row:
            for _column in list_column:
                _item = self.table_ui.item(_row, _column)
                if _item:
                    _item.setText("")

    def copy(self):
        ''' only 1 row at the time is allowed in the copy'''
        list_row = self.o_selection.get_list_row()
        nbr_row = len(list_row)

        if nbr_row > 1:
            self.parent.ui.statusbar.setStyleSheet("color: red")
            self.parent.ui.statusbar.showMessage("Please select only 1 row!",
                                                 self.parent.statusbar_display_time)
            return

        list_column = self.o_selection.get_list_column()
        nbr_column = len(list_column)

        row_column_items = [['' for x in np.arange(nbr_column)]
                            for y in np.arange(nbr_row)]
        for _row in np.arange(nbr_row):
            for _column in np.arange(nbr_column):
                _item = self.table_ui.item(_row, _column)
                if _item:
                    row_column_items[_row][_column] = _item.text()

        self.parent.master_table_cells_copy['temp'] = row_column_items
        self.parent.master_table_cells_copy['list_column'] = list_column
        self.parent.master_table_cells_copy['row'] = list_row[0]
        self.parent.master_table_right_click_buttons['cell_paste']['status'] = True

    def paste(self):

        list_column_copy = self.parent.master_table_cells_copy['list_column']
        row_copy = self.parent.master_table_cells_copy['row']

        list_row_paste= self.o_selection.get_list_row()
        list_column_paste = self.o_selection.get_list_column()

        nbr_row_paste = len(list_row_paste)
        nbr_column_paste = len(list_column_paste)

        row_columns_items_to_copy = self.parent.master_table_cells_copy['temp']
        [nbr_row_copy, nbr_column_copy] = np.shape(row_columns_items_to_copy)

        # if we don't select the same amount of columns, we stop here (and inform
        # user of issue in statusbar

        if list_column_copy[0] != list_column_paste[0]:
            self.parent.ui.statusbar.setStyleSheet("color: red")
            self.parent.ui.statusbar.showMessage("Copy and Paste first column selected do not match!",
                                                 self.parent.statusbar_display_time)
            return

        # we only clicked once cell before using PASTE, so we can copy as the first column are the same
        if len(list_column_paste) == 1:

            o_copy = CopyCells(parent=self.parent)
            for _row_paste in list_row_paste:
                for _column in list_column_copy:
                    o_copy.copy_from_to(from_row=row_copy,
                                        from_col=_column,
                                        to_row=_row_paste)

        else: # we clicked several columns before clicking PASTE

            # in this case, the COPY and PASTE number of columns have to match perfectly

            # not the same number of copy and paste columns selected
            if len(list_column_copy) != len(list_column_paste):
                self.parent.ui.statusbar.setStyleSheet("color: red")
                self.parent.ui.statusbar.showMessage("Copy and Paste do not cover the same number of columns!",
                                                     self.parent.statusbar_display_time)
                return

            else:

                # copy and paste columns are not the same
                list_intersection = set(list_column_copy).intersection(list_column_paste)
                if len(list_intersection) != len(list_column_copy):
                    self.parent.ui.statusbar.setStyleSheet("color: red")
                    self.parent.ui.statusbar.showMessage("Copy and Paste do not cover the same columns!",
                                                         self.parent.statusbar_display_time)
                    return

                else:

                    # we selected the same number of columns, the same ones and now we can copy countain
                    o_copy = CopyCells(parent=self.parent)
                    for _row_paste in list_row_paste:
                        for _column in list_column_copy:
                            o_copy.copy_from_to(from_row=row_copy,
                                                from_col=_column,
                                                to_row=_row_paste)
                        _row_paste += 1


class CopyCells:

    def __init__(self, parent=None):
        self.parent = parent
        self.table_ui = self.parent.ui.h3_table

    def copy_from_to(self, from_row=-1, from_col=-1, to_row=-1):

        try:
            # let's assume the cell contain a regular item
            _from_cell_value = self.table_ui.item(from_row, from_col).text()
            self.table_ui.item(to_row, from_col).setText(_from_cell_value)
        except:
            # let's assume now that the cell contain a combobox
            ui = self.table_ui.cellWidget(from_row, from_col).children()[1]
            if isinstance(ui, QComboBox):
                _from_index = ui.currentIndex()
                self.table_ui.cellWidget(to_row, from_col).children()[1].setCurrentIndex(_from_index)
            elif isinstance(ui, QCheckBox):
                _state = ui.checkState()
                self.table_ui.cellWidget(to_row, from_col).children()[1].setCheckState(_state)
            else:
                self.parent.ui.statusbar.setStyleSheet("color: red")
                self.parent.ui.statusbar.showMessage("Don't know how to copy/paste the cell from row #{} to row #{} at the column #{}".format(from_row, to_row, from_col),
                                                     self.parent.statusbar_display_time*2)









