from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import QTableWidgetSelectionRange
from qtpy.QtCore import Qt

import numpy as np

from addie.processing.mantid.master_table.tree_definition import INDEX_OF_COLUMNS_SEARCHABLE
from addie.processing.mantid.master_table.tree_definition import INDEX_OF_COLUMNS_WITH_COMBOBOX
from addie.processing.mantid.master_table.tree_definition import INDEX_OF_SPECIAL_COLUMNS_SEARCHABLE
from addie.processing.mantid.master_table.tree_definition import INDEX_OF_COLUMNS_WITH_GEOMETRY_INFOS
from addie.processing.mantid.master_table.tree_definition import INDEX_OF_COLUMNS_WITH_RESONANCE_INFOS
from addie.processing.mantid.master_table.tree_definition import INDEX_OF_COLUMNS_WITH_CHEMICAL_FORMULA
from addie.processing.mantid.master_table.tree_definition import INDEX_OF_COLUMNS_WITH_MASS_DENSITY
from addie.processing.mantid.master_table.tree_definition import INDEX_OF_COLUMNS_WITH_ALIGN_AND_FOCUS_ARGS
from addie.processing.mantid.master_table.tree_definition import INDEX_OF_COLUMNS_WITH_ITEMS
from addie.processing.mantid.master_table.tree_definition import INDEX_OF_COLUMNS_WITH_CHECKBOX
from addie.processing.mantid.master_table.tree_definition import INDEX_OF_COLUMNS_WITH_SCATTERING_LEVELS

from addie.processing.mantid.master_table.utilities import Utilities


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
        return np.arange(self.left_column, self.right_column + 1)

    def get_list_row(self):
        return np.arange(self.top_row, self.bottom_row + 1)


class SelectionHandlerMaster:

    def __init__(self, parent=None):
        self.parent = parent
        self.table_ui = self.parent.processing_ui.h3_table

    def get_ui_key_for_this_row(self, row=-1):
        _check_box_ui_of_this_row = self.table_ui.cellWidget(row, 0).children()[
            1]
        _table_list_ui = self.parent.master_table_list_ui
        for _key in _table_list_ui.keys():
            if _table_list_ui[_key]['active'] == _check_box_ui_of_this_row:
                return _key
        return None

    def get_list_ui_for_this_row(self, row=-1):
        _check_box_ui_of_this_row = self.table_ui.cellWidget(row, 0).children()[
            1]
        _table_list_ui = self.parent.master_table_list_ui
        for _key in _table_list_ui.keys():
            if _table_list_ui[_key]['active'] == _check_box_ui_of_this_row:
                list_ui = [
                    _check_box_ui_of_this_row,
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

    def check_right_click_buttons(self):
        nbr_row = self.table_ui.rowCount()
        if nbr_row == 0:
            status_button = False
        else:
            status_button = True

        self.parent.master_table_right_click_buttons['activate_check_all']['status'] = status_button
        self.parent.master_table_right_click_buttons['activate_uncheck_all']['status'] = status_button
        self.parent.master_table_right_click_buttons['activate_inverse']['status'] = status_button
        self.parent.master_table_right_click_buttons['cells_copy']['status'] = status_button
        self.parent.master_table_right_click_buttons['cells_clear']['status'] = status_button
        self.parent.master_table_right_click_buttons['rows_copy']['status'] = status_button
        self.parent.master_table_right_click_buttons['rows_duplicate']['status'] = status_button


class TransferH3TableWidgetState(SelectionHandlerMaster):

    def __init__(self, parent=None):
        SelectionHandlerMaster.__init__(self, parent=parent)

    def transfer_states(self, from_key=None, data_type='sample'):
        selection = self.table_ui.selectedRanges()
        o_selection = SelectionHandler(selection)

        master_table_row_ui = self.parent.master_table_list_ui

        # enable or disable all other selected rows (if only first column
        # selected)
        if (o_selection.nbr_column_selected() == 1):

            range_row = o_selection.get_list_row()
            column_selected = o_selection.first_column_selected()

            o_utilities = Utilities(parent=self.parent)
            from_row = o_utilities.get_row_index_from_row_key(row_key=from_key)

            # activate row widget (first column)
            if (column_selected == 0):

                #state = self.table_ui.cellWidget(from_row, 0).children()[1].checkState()
                state = master_table_row_ui[from_key]['active'].checkState()

                # apply state to all the widgets
                for _row in range_row:
                    _to_key = o_utilities.get_row_key_from_row_index(row=_row)
                    ui = master_table_row_ui[_to_key]['active']
                    ui.blockSignals(True)
                    ui.setCheckState(state)
                    ui.blockSignals(False)

            # sample or normalization, shape, abs. corr., mult. scat. corr or
            # inelastic corr.
            elif (column_selected in INDEX_OF_COLUMNS_WITH_COMBOBOX):

                ui = self.table_ui.cellWidget(
                    from_row, column_selected).children()[1]
                index = ui.currentIndex()

                for _row in range_row:
                    if _row == from_row:
                        continue

                    ui = self.table_ui.cellWidget(
                        _row, column_selected).children()[1]

                    if index > -1:
                        # ui.blockSignals(True)
                        ui.setCurrentIndex(index)
                        # ui.blockSignals(False)

            elif (column_selected in INDEX_OF_COLUMNS_WITH_CHEMICAL_FORMULA):

                o_utilities = Utilities(parent=self.parent)
                _from_key = o_utilities.get_row_key_from_row_index(
                    row=from_row)
                chemical_formula = str(
                    master_table_row_ui[_from_key][data_type]['material']['text'].text())
                for _row in range_row:
                    if _row == from_row:
                        continue

                    _to_key = o_utilities.get_row_key_from_row_index(row=_row)
                    master_table_row_ui[_to_key][data_type]['material']['text'].setText(
                        chemical_formula)

            elif (column_selected in INDEX_OF_COLUMNS_WITH_MASS_DENSITY):

                o_utilities = Utilities(parent=self.parent)
                _from_key = o_utilities.get_row_key_from_row_index(
                    row=from_row)

                mass_density_info = master_table_row_ui[_from_key][data_type]['mass_density_infos']
                mass_density_value = str(
                    master_table_row_ui[_from_key][data_type]['mass_density']['text'].text())

                for _row in range_row:
                    if _row == from_row:
                        continue

                    _to_key = o_utilities.get_row_key_from_row_index(row=_row)

                    master_table_row_ui[_to_key][data_type]['mass_density_infos'] = mass_density_info
                    master_table_row_ui[_to_key][data_type]['mass_density']['text'].setText(
                        mass_density_value)

            elif (column_selected in INDEX_OF_COLUMNS_WITH_GEOMETRY_INFOS):

                o_utilities = Utilities(parent=self.parent)
                _from_key = o_utilities.get_row_key_from_row_index(
                    row=from_row)

                radius = str(
                    master_table_row_ui[_from_key][data_type]['geometry']['radius']['value'].text())
                radius2 = str(
                    master_table_row_ui[_from_key][data_type]['geometry']['radius2']['value'].text())
                height = str(
                    master_table_row_ui[_from_key][data_type]['geometry']['height']['value'].text())

                for _row in range_row:
                    if _row == from_row:
                        continue

                    _to_key = o_utilities.get_row_key_from_row_index(row=_row)

                    master_table_row_ui[_to_key][data_type]['geometry']['radius']['value'].setText(
                        radius)
                    master_table_row_ui[_to_key][data_type]['geometry']['radius2']['value'].setText(
                        radius2)
                    master_table_row_ui[_to_key][data_type]['geometry']['height']['value'].setText(
                        height)


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
                self.parent.ui.statusbar.showMessage(
                    "Please select only 1 row!", self.parent.statusbar_display_time)
                return
            elif len(list_row) == 0:
                self.parent.ui.statusbar.setStyleSheet("color: red")
                self.parent.ui.statusbar.showMessage(
                    "Please select a row to copy from!", self.parent.statusbar_display_time)
                return

            row = list_row[0]

        self.parent.copied_row = row

        _table_ui = self.table_ui
        nbr_col = _table_ui.columnCount()
        _row_selection = QTableWidgetSelectionRange(row, 0, row, nbr_col - 1)
        _table_ui.setRangeSelected(_row_selection, True)
        self.parent.ui.statusbar.setStyleSheet("color: green")
        self.parent.ui.statusbar.showMessage(
            "Select another row to copy the current selected row to!",
            self.parent.statusbar_display_time)

        self.parent.master_table_cells_copy['temp'] = []
        self.parent.master_table_cells_copy['list_column'] = []
        self.parent.master_table_cells_copy['row'] = row
        #self.parent.master_table_right_click_buttons['rows_paste']['status'] = True

    def paste(self, row=None):
        if row is None:
            list_to_row = self.o_selection.get_list_row()
            nbr_col = self.table_ui.columnCount()
            _row_selection = QTableWidgetSelectionRange(list_to_row[0],
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
        msg = "No row(s) selected. Highlight any cell(s) in row(s) to duplicate followed by right click."
        if not rows_selected(list_to_row, msg):
            self.parent.ui.statusbar.setStyleSheet("color: red")
            self.parent.ui.statusbar.showMessage(msg, self.parent.statusbar_display_time)
            return
        for _row in list_to_row:
            for _column in list_column_copy:
                o_copy.copy_from_to(from_row=from_row,
                                    from_col=_column,
                                    to_row=_row)

    def remove(self, row=None):
        if row is None:
            list_to_row = self.o_selection.get_list_row()
            msg = "No row(s) selected! Highlight any cell(s) in row(s) to remove followed by right click."
            if not rows_selected(list_to_row, msg):
                self.parent.ui.statusbar.setStyleSheet("color: red")
                self.parent.ui.statusbar.showMessage(msg, self.parent.statusbar_display_time)
                return
            _first_row = list_to_row[0]
            for _ in list_to_row:
                self.remove(row=_first_row)
        else:
            # self.table_ui.blockSignals(True)
            self.table_ui.setRangeSelected(self.selection[0], False)
            self.table_ui.removeRow(row)
            # self.table_ui.blockSignals(False)
        self.check_right_click_buttons()


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

                if _column in INDEX_OF_COLUMNS_WITH_ITEMS:
                    self.table_ui.item(_row, _column).setText("")

                elif _column in INDEX_OF_COLUMNS_WITH_COMBOBOX:
                    self.table_ui.cellWidget(_row, _column).children()[
                        1].setCurrentIndex(0)

                elif _column in INDEX_OF_COLUMNS_WITH_CHECKBOX:
                    _disable_state = Qt.Unchecked
                    self.table_ui.cellWidget(_row, _column).children()[
                        1].setCheckState(_disable_state)

                elif _column in INDEX_OF_COLUMNS_WITH_GEOMETRY_INFOS:
                    o_utilities = Utilities(parent=self.parent)
                    _key = o_utilities.get_row_key_from_row_index(row=_row)

                    # sample
                    if _column == INDEX_OF_COLUMNS_WITH_GEOMETRY_INFOS[0]:
                        data_type = 'sample'
                    else:
                        data_type = 'normalization'

                    geometry = self.parent.master_table_list_ui[_key][data_type]['geometry']
                    geometry['radius']['value'].setText("N/A")
                    geometry['radius2']['value'].setText("N/A")
                    geometry['height']['value'].setText("N/A")

                elif _column in INDEX_OF_COLUMNS_WITH_RESONANCE_INFOS:
                    o_utilities = Utilities(parent=self.parent)
                    _key = o_utilities.get_row_key_from_row_index(row=_row)
                    data_type = 'sample'

                    resonance = self.parent.master_table_list_ui[_key][data_type]['resonance']
                    resonance['axis']['value'].setText("N/A")
                    resonance['lower']['value'].setText("N/A")
                    resonance['upper']['value'].setText("N/A")

                elif _column in INDEX_OF_COLUMNS_WITH_CHEMICAL_FORMULA:
                    o_utilities = Utilities(parent=self.parent)
                    _key = o_utilities.get_row_key_from_row_index(row=_row)

                    # sample
                    if _column == INDEX_OF_COLUMNS_WITH_CHEMICAL_FORMULA[0]:
                        data_type = 'sample'
                    else:
                        data_type = 'normalization'
                    material = self.parent.master_table_list_ui[_key][data_type]['material']
                    material['text'].setText("")

                elif _column in INDEX_OF_COLUMNS_WITH_MASS_DENSITY:
                    o_utilities = Utilities(parent=self.parent)
                    _key = o_utilities.get_row_key_from_row_index(row=_row)

                    # sample
                    if _column == INDEX_OF_COLUMNS_WITH_MASS_DENSITY[0]:
                        data_type = 'sample'
                    else:
                        data_type = 'normalization'

                    data_type_entry = self.parent.master_table_list_ui[_key][data_type]

                    mass_density = data_type_entry['mass_density']
                    mass_density['text'].setText("N/A")

                    mass_density_infos = data_type_entry['mass_density_infos']
                    mass_density_infos['number_density']['value'] = "N/A"
                    mass_density_infos['number_density']['selected'] = False
                    mass_density_infos['mass_density']['value'] = "N/A"
                    mass_density_infos['mass_density']['selected'] = True
                    mass_density_infos['mass']['value'] = "N/A"
                    mass_density_infos['mass']['selected'] = False

    def copy(self):
        ''' only 1 row at the time is allowed in the copy'''
        list_row = self.o_selection.get_list_row()
        nbr_row = len(list_row)

        if len(list_row) == 0:
            msg = "No cells selected! Highlight columns in the same row followed by right click."
            self.parent.ui.statusbar.setStyleSheet("color: red")
            self.parent.ui.statusbar.showMessage(msg, self.parent.statusbar_display_time)
            print("[Info] " + msg)
            return

        if nbr_row > 1:
            self.parent.ui.statusbar.setStyleSheet("color: red")
            self.parent.ui.statusbar.showMessage(
                "Selection of columns must be in the same row!",
                self.parent.statusbar_display_time)
            return

        list_column = self.o_selection.get_list_column()
        #nbr_column = len(list_column)

        # row_column_items = [['' for x in np.arange(nbr_column)]
        #                    for y in np.arange(nbr_row)]
#        for _row in np.arange(nbr_row):
        # for _column in np.arange(nbr_column):
        #    _item = self.table_ui.item(_row, _column)
        #    if _item:
        #        row_column_items[_row][_column] = _item.text()

        #self.parent.master_table_cells_copy['temp'] = row_column_items
        self.parent.master_table_cells_copy['list_column'] = list_column
        self.parent.master_table_cells_copy['row'] = list_row[0]
        self.parent.master_table_right_click_buttons['cells_paste']['status'] = True

    def paste(self):

        list_column_copy = self.parent.master_table_cells_copy['list_column']
        row_copy = self.parent.master_table_cells_copy['row']

        list_row_paste = self.o_selection.get_list_row()
        list_column_paste = self.o_selection.get_list_column()

        # nbr_row_paste = len(list_row_paste)
        # nbr_column_paste = len(list_column_paste)
        #
        #row_columns_items_to_copy = self.parent.master_table_cells_copy['temp']
        #[nbr_row_copy, nbr_column_copy] = np.shape(row_columns_items_to_copy)

        # if we don't select the same amount of columns, we stop here (and inform
        # user of issue in statusbar

        if list_column_copy[0] != list_column_paste[0]:
            self.parent.ui.statusbar.setStyleSheet("color: red")
            self.parent.ui.statusbar.showMessage(
                "The first column selected for Copy and Paste does not match!",
                self.parent.statusbar_display_time)
            return

        # we only clicked once cell before using PASTE, so we can copy as the
        # first column are the same
        if len(list_column_paste) == 1:

            o_copy = CopyCells(parent=self.parent)
            for _row_paste in list_row_paste:
                for _column in list_column_copy:
                    o_copy.copy_from_to(from_row=row_copy,
                                        from_col=_column,
                                        to_row=_row_paste)

        else:  # we clicked several columns before clicking PASTE

            # in this case, the COPY and PASTE number of columns have to match
            # perfectly

            # not the same number of copy and paste columns selected
            if len(list_column_copy) != len(list_column_paste):
                self.parent.ui.statusbar.setStyleSheet("color: red")
                self.parent.ui.statusbar.showMessage(
                    "Copy and Paste do not cover the same number of columns!",
                    self.parent.statusbar_display_time)
                return

            else:

                # copy and paste columns are not the same
                list_intersection = set(
                    list_column_copy).intersection(list_column_paste)
                if len(list_intersection) != len(list_column_copy):
                    self.parent.ui.statusbar.setStyleSheet("color: red")
                    self.parent.ui.statusbar.showMessage(
                        "Copy and Paste do not cover the same columns!",
                        self.parent.statusbar_display_time)
                    return

                else:

                    # we selected the same number of columns, the same ones and
                    # now we can copy countain
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
        self.table_ui = self.parent.processing_ui.h3_table

    def _copy_from_to_for_dict(self, from_row, to_row, data_type):
        """ Utility function that copies a dictionary of values
        from one row to another given the master table key as `data_type`

        :param from_row: Row index we will be copying from
        :type from_row: int
        :param to_row: Row index we will be copying to
        :type to_row: int
        :param data_type: Key in master table for column to copy dict value
        :type data_type: str
        """
        o_utilities = Utilities(parent=self.parent)
        _from_key = o_utilities.get_row_key_from_row_index(row=from_row)
        _to_key = o_utilities.get_row_key_from_row_index(row=to_row)
        _dict = self.parent.master_table_list_ui[_from_key][data_type]
        self.parent.master_table_list_ui[_to_key][data_type] = _dict

    def _copy_from_to_for_density(self, from_info, to_info, density_type):
        """ Utility function that copies the density using
        a density-type key.

        :param from_info: Mass density info dictionary to copy from
        :type from_info: dict
        :param to_info: Mass density info dictionary to copy to
        :type to_info: dict
        :param density_type: Density-type key to use for copy-paste
        :type density_type: str from ['number_density', 'mass_density', 'mass']
        """
        from_density = from_info[density_type]
        to_density = to_info[density_type]
        to_density['value'] = from_density['value']
        to_density['selected'] = from_density['selected']

    def copy_from_to(self, from_row=-1, from_col=-1, to_row=-1):

        if from_col in INDEX_OF_COLUMNS_WITH_ITEMS:
            _from_cell_value = self.table_ui.item(from_row, from_col).text()
            self.table_ui.item(to_row, from_col).setText(_from_cell_value)

        elif from_col in INDEX_OF_COLUMNS_WITH_COMBOBOX:
            ui = self.table_ui.cellWidget(from_row, from_col).children()[1]
            _from_index = ui.currentIndex()
            self.table_ui.cellWidget(to_row, from_col).children()[
                1].setCurrentIndex(_from_index)

        elif from_col in INDEX_OF_COLUMNS_WITH_CHECKBOX:
            ui = self.table_ui.cellWidget(from_row, from_col).children()[1]
            _state = ui.checkState()
            self.table_ui.cellWidget(to_row, from_col).children()[
                1].setCheckState(_state)

        elif from_col in INDEX_OF_COLUMNS_WITH_GEOMETRY_INFOS:
            o_utilities = Utilities(parent=self.parent)
            _from_key = o_utilities.get_row_key_from_row_index(row=from_row)
            _to_key = o_utilities.get_row_key_from_row_index(row=to_row)
            if from_col == INDEX_OF_COLUMNS_WITH_GEOMETRY_INFOS[0]:  # sample
                data_type = 'sample'
            else:
                data_type = 'normalization'

            from_geometry = self.parent.master_table_list_ui[_from_key][data_type]['geometry']
            _radius = str(from_geometry['radius']['value'].text())
            _radius2 = str(from_geometry['radius2']['value'].text())
            _height = str(from_geometry['height']['value'].text())

            to_geometry = self.parent.master_table_list_ui[_to_key][data_type]['geometry']
            to_geometry['radius']['value'].setText(_radius)
            to_geometry['radius2']['value'].setText(_radius2)
            to_geometry['height']['value'].setText(_height)

        elif from_col in INDEX_OF_COLUMNS_WITH_RESONANCE_INFOS:
            o_utilities = Utilities(parent=self.parent)
            _from_key = o_utilities.get_row_key_from_row_index(row=from_row)
            _to_key = o_utilities.get_row_key_from_row_index(row=to_row)
            data_type = 'sample'
            from_resonance = self.parent.master_table_list_ui[_from_key][data_type]['resonance']
            axis_val = str(from_resonance['axis']['value'].text())
            lower_val = str(from_resonance['lower']['value'].text())
            upper_val = str(from_resonance['upper']['value'].text())
            lower_list = from_resonance['lower']['lim_list']
            upper_list = from_resonance['upper']['lim_list']

            to_resonance = self.parent.master_table_list_ui[_to_key][data_type]['resonance']
            to_resonance['axis']['value'].setText(axis_val)
            to_resonance['lower']['value'].setText(lower_val)
            to_resonance['upper']['value'].setText(upper_val)
            to_resonance['lower']['lim_list'] = lower_list
            to_resonance['upper']['lim_list'] = upper_list

        elif from_col in INDEX_OF_COLUMNS_WITH_CHEMICAL_FORMULA:
            o_utilities = Utilities(parent=self.parent)
            _from_key = o_utilities.get_row_key_from_row_index(row=from_row)
            _to_key = o_utilities.get_row_key_from_row_index(row=to_row)
            if from_col == INDEX_OF_COLUMNS_WITH_CHEMICAL_FORMULA[0]:  # sample
                data_type = 'sample'
            else:
                data_type = 'normalization'
            from_material = self.parent.master_table_list_ui[_from_key][data_type]['material']
            to_material = self.parent.master_table_list_ui[_to_key][data_type]['material']
            _chemical_formula = str(from_material['text'].text())
            to_material['text'].setText(_chemical_formula)

        elif from_col in INDEX_OF_COLUMNS_WITH_MASS_DENSITY:
            o_utilities = Utilities(parent=self.parent)
            _from_key = o_utilities.get_row_key_from_row_index(row=from_row)
            _to_key = o_utilities.get_row_key_from_row_index(row=to_row)
            if from_col == INDEX_OF_COLUMNS_WITH_MASS_DENSITY[0]:  # sample
                data_type = 'sample'
            else:
                data_type = 'normalization'

            # Get the to and from dictionaries for either sample or
            # normalization
            from_data_type = self.parent.master_table_list_ui[_from_key][data_type]
            to_data_type = self.parent.master_table_list_ui[_to_key][data_type]

            # Convenience variables for the "from" variables
            from_mass_density = from_data_type['mass_density']
            from_info = from_data_type['mass_density_infos']

            # Convenience variables for the "to" variables
            to_mass_density = to_data_type['mass_density']
            to_info = to_data_type['mass_density_infos']

            # Copy-paste the "top-level" MassDensity (display in table)
            _mass_density = str(from_mass_density['text'].text())
            to_mass_density['text'].setText(_mass_density)

            # Copy-paste the NumberDensity in Widget
            self._copy_from_to_for_density(
                from_info, to_info, 'number_density')

            # Copy-paste the MassDensity in Widget
            self._copy_from_to_for_density(from_info, to_info, 'mass_density')

            # Copy-paste the Mass in Widget
            self._copy_from_to_for_density(from_info, to_info, 'mass')

        elif from_col in INDEX_OF_COLUMNS_WITH_ALIGN_AND_FOCUS_ARGS:
            data_type = 'align_and_focus_args_infos'
            self._copy_from_to_for_dict(from_row, to_row, data_type)

        elif from_col in INDEX_OF_COLUMNS_WITH_SCATTERING_LEVELS:
            o_utilities = Utilities(parent=self.parent)
            _from_key = o_utilities.get_row_key_from_row_index(row=from_row)
            _to_key = o_utilities.get_row_key_from_row_index(row=to_row)
            from_ss_level = self.parent.master_table_list_ui[_from_key]['self_scattering_level']
            ss_lower_val = str(from_ss_level['lower']['value'].text())
            ss_upper_val = str(from_ss_level['upper']['value'].text())
            ss_lower_list = from_ss_level['lower']['val_list']
            ss_upper_list = from_ss_level['upper']['val_list']

            to_ss_level = self.parent.master_table_list_ui[_to_key]['self_scattering_level']
            to_ss_level['lower']['value'].setText(ss_lower_val)
            to_ss_level['upper']['value'].setText(ss_upper_val)
            to_ss_level['lower']['lim_list'] = ss_lower_list
            to_ss_level['upper']['lim_list'] = ss_upper_list

        else:
            self.parent.ui.statusbar.setStyleSheet("color: red")
            msg_string = "Don't know how to copy/paste the cell from row #{} to row #{} at the column #{}"
            msg = msg_string.format(from_row, to_row, from_col)
            time = self.parent.statusbar_display_time * 2
            self.parent.ui.statusbar.showMessage(msg, time)


class TableHandler(SelectionHandlerMaster):

    list_of_columns_to_search_for = []

    def __init__(self, parent=None):
        SelectionHandlerMaster.__init__(self, parent=parent)

    def search(self, text=""):
        nbr_row = self.table_ui.rowCount()
        text = self.parent.processing_ui.name_search_3.text()
        if text == "":
            # show everything
            for _row in np.arange(nbr_row):
                self.table_ui.setRowHidden(_row, False)

        else:
            # look in all the searchable columns, row by row
            for _row in np.arange(nbr_row):
                hide_it = True

                for _col in INDEX_OF_COLUMNS_SEARCHABLE:
                    _text_cell = str(self.table_ui.item(
                        _row, _col).text()).lower()
                    if text.lower() in _text_cell:
                        hide_it = False

                for _col in INDEX_OF_SPECIAL_COLUMNS_SEARCHABLE:
                    if (_col == 6) or (
                            _col == 18):  # layout inside a layout for these cells
                        _text_widget = str(
                            self.table_ui.cellWidget(
                                _row, _col).children()[1].children()[1].text()).lower()
                    else:
                        _text_widget = str(self.table_ui.cellWidget(
                            _row, _col).children()[1].text()).lower()
                    if text.lower() in _text_widget:
                        hide_it = False

                self.table_ui.setRowHidden(_row, hide_it)

    def clear_search(self):
        self.parent.processing_ui.name_search_3.setText("")
        self.search("")


def rows_selected(selected_rows, message):
    if len(selected_rows) == 0 or any([item < 0 for item in selected_rows]):
        print("[Info] " + message)
        return False
    return True
