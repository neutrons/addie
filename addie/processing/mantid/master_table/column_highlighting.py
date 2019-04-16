import numpy as np
from qtpy import QtGui
from qtpy.QtWidgets import QTableWidgetItem

from addie.processing.mantid.master_table.utilities import Utilities

from addie.processing.mantid.master_table.tree_definition import (INDEX_OF_COLUMNS_SEARCHABLE,
                                                                  INDEX_OF_COLUMNS_WITH_CHEMICAL_FORMULA,
                                                                  INDEX_OF_COLUMNS_WITH_MASS_DENSITY,
                                                                  INDEX_OF_COLUMNS_SHAPE,
                                                                  INDEX_OF_COLUMNS_WITH_GEOMETRY_INFOS,
                                                                  INDEX_OF_ABS_CORRECTION,
                                                                  INDEX_OF_MULTI_SCATTERING_CORRECTION,
                                                                  INDEX_OF_INELASTIC_CORRECTION,
                                                                  LIST_COLUMNS_TO_SEARCH_FOR_FULL_HIGHLIGTHING)
from addie.processing.mantid.master_table.tree_definition import (COLUMNS_IDENTICAL_VALUES_COLOR,
                                                                  COLUMNS_SAME_VALUES_COLOR)
from addie.processing.mantid.master_table.tree_definition import INDEX_NORMALIZATION_START


class ColumnHighlighting:

    data_type = 'sample'
    column = -1

    def __init__(self, main_window=None):
        self.main_window = main_window
        self.nbr_row = self.get_nbr_row()

    def set_data_type(self):
        if self.column >= INDEX_NORMALIZATION_START:
            self.data_type = 'normalization'

    def get_nbr_row(self):
        nbr_row = self.main_window.processing_ui.h3_table.rowCount()
        return nbr_row

    def get_nbr_column(self):
        nbr_column = self.main_window.processing_ui.h3_table.columnCount()
        return nbr_column

    def check_all(self):
        nbr_column = self.get_nbr_column()
        for _col in np.arange(nbr_column):
            self.check_column(column=_col)

    def check_column(self, column=-1):
        self.column = column
        are_all_the_same = False

        self.set_data_type()

        if self.nbr_row > 1:

            for _ in np.arange(self.nbr_row):

                # item
                if column in INDEX_OF_COLUMNS_SEARCHABLE:
                    are_all_the_same = self.are_cells_identical()

                elif column in INDEX_OF_COLUMNS_WITH_CHEMICAL_FORMULA:
                    are_all_the_same = self.are_chemical_formula_identical()

                elif column in INDEX_OF_COLUMNS_WITH_MASS_DENSITY:
                    are_all_the_same = self.are_mass_density_identical()

                elif column in INDEX_OF_COLUMNS_SHAPE:
                    are_all_the_same = self.are_shape_identical()

                elif column in INDEX_OF_COLUMNS_WITH_GEOMETRY_INFOS:
                    are_all_the_same = self.are_geometry_identical()

                elif column in INDEX_OF_ABS_CORRECTION:
                    are_all_the_same = self.are_abs_correction_identical()

                elif column in INDEX_OF_MULTI_SCATTERING_CORRECTION:
                    are_all_the_same = self.are_multi_correction_identical()

                elif column in INDEX_OF_INELASTIC_CORRECTION:
                    are_all_the_same = self.are_inelastic_correction_identical()

                elif column == LIST_COLUMNS_TO_SEARCH_FOR_FULL_HIGHLIGTHING[-1]:
                    are_all_the_same = self.are_align_and_focus_args_identical()

        self.apply_cell_background(are_all_the_same=are_all_the_same)

    def apply_cell_background(self, are_all_the_same=False):
        if are_all_the_same:
            # background_color = QtGui.QColor(COLUMNS_IDENTICAL_VALUES_COLOR[0],
            #                                 COLUMNS_IDENTICAL_VALUES_COLOR[1],
            #                                 COLUMNS_IDENTICAL_VALUES_COLOR[2])
            background_color_stylesheet = "rgb({}, {}, {})".format(COLUMNS_IDENTICAL_VALUES_COLOR[0],
                                                                   COLUMNS_IDENTICAL_VALUES_COLOR[1],
                                                                   COLUMNS_IDENTICAL_VALUES_COLOR[2])
        else:
            # background_color = QtGui.QColor(COLUMNS_SAME_VALUES_COLOR[0],
            #                                 COLUMNS_SAME_VALUES_COLOR[1],
            #                                 COLUMNS_SAME_VALUES_COLOR[2])
            background_color_stylesheet = "rgb({}, {}, {})".format(COLUMNS_SAME_VALUES_COLOR[0],
                                                                   COLUMNS_SAME_VALUES_COLOR[1],
                                                                   COLUMNS_SAME_VALUES_COLOR[2])

        pen_color = "black"
        selection_color = "white"
        selection_background_color = "blue"

        for _row in np.arange(self.nbr_row):

            main_widget = self.main_window.processing_ui.h3_table.cellWidget(_row, self.column)
            if (self.column in INDEX_OF_COLUMNS_WITH_CHEMICAL_FORMULA) or \
                    (self.column in INDEX_OF_COLUMNS_WITH_MASS_DENSITY) or \
                    (self.column in INDEX_OF_COLUMNS_WITH_GEOMETRY_INFOS) or \
                    (self.column in INDEX_OF_COLUMNS_SHAPE) or \
                    (self.column in INDEX_OF_ABS_CORRECTION) or \
                    (self.column in INDEX_OF_MULTI_SCATTERING_CORRECTION) or \
                    (self.column in INDEX_OF_INELASTIC_CORRECTION) or \
                    (self.column == LIST_COLUMNS_TO_SEARCH_FOR_FULL_HIGHLIGTHING):
                main_widget.setAutoFillBackground(True)
                # main_widget.setStyleSheet("background-color: {};".format(background_color_stylesheet))
            else:
                main_widget.setAutoFillBackground(False)
                # main_widget.setStyleSheet("background-color: {};".format(background_color_stylesheet))
                # self.main_window.processing_ui.h3_table.item(_row, self.column).setBackground(background_color)
            main_widget.setStyleSheet("color: {}; "
                                      "background-color: {};"
                                      "selection-color: {};"
                                      "selection-background-color: {};".format(pen_color,
                                                                          background_color_stylesheet,
                                                                          selection_color,
                                                                          selection_background_color))

    def are_cells_identical(self):
        def _get_item_value(row=-1, column=-1):
            return str(self.main_window.processing_ui.h3_table.item(row, column).text())

        ref_value = _get_item_value(0, self.column)
        for _row in np.arange(1, self.nbr_row):
            _value = _get_item_value(row=_row, column=self.column)
            if _value != ref_value:
                return False
        return True

    def are_chemical_formula_identical(self):
        ref_value = self._get_chemical_formula_widget_value(row=0)
        for _row in np.arange(1, self.nbr_row):
            _value = self._get_chemical_formula_widget_value(row=_row)
            if _value != ref_value:
                return False
        return True

    def are_mass_density_identical(self):
        ref_value = self._get_mass_density_widget_value(row=0)
        for _row in np.arange(1, self.nbr_row):
            _value = self._get_mass_density_widget_value(row=_row)
            if _value != ref_value:
                return False
        return True

    def are_shape_identical(self):
        ref_value = self._get_shape_value(row=0)
        for _row in np.arange(1, self.nbr_row):
            _value = self._get_shape_value(row=_row)
            if _value != ref_value:
                return False
        return True

    def are_geometry_identical(self):
        if not self.are_shape_identical():
            return False

        shape_selected = self._get_shape_value(row=0)

        # compare radius
        if not self._are_radius_identical():
            return False

        # we are done for spherical geometry
        if shape_selected.lower() is "spherical":
            return True

        if not self._are_height_identical():
            return False

        # we are done for cylindrical geometry
        if shape_selected.lower() is "cylindrical":
            return True

        if not self._are_radius2_identical():
            return False
        return True

    def are_abs_correction_identical(self):
        ref_value = self._get_abs_correction_widget_value(row=0)
        for _row in np.arange(1, self.nbr_row):
            _value = self._get_abs_correction_widget_value(row=_row)
            if _value != ref_value:
                return False
        return True

    def are_multi_correction_identical(self):
        ref_value = self._get_multi_correction_widget_value(row=0)
        for _row in np.arange(1, self.nbr_row):
            _value = self._get_multi_correction_widget_value(row=_row)
            if _value != ref_value:
                return False
        return True

    def are_inelastic_correction_identical(self):
        ref_value = self._get_inelastic_correction_widget_value(row=0)
        for _row in np.arange(1, self.nbr_row):
            _value = self._get_inelastic_correction_widget_value(row=_row)
            if _value != ref_value:
                return False

        # if placzek selected,
        if ref_value.lower() == 'placzek':
            ref_dict = self._get_placzek_infos(row=0)
            for _row in np.arange(1, self.nbr_row):
                _dict = self._get_placzek_infos(row=_row)
                if _dict != ref_dict:
                    return False
        return True

    def are_align_and_focus_args_identical(self):
        ref_value = self._get_align_and_focus_args_value(row=0)
        for _row in np.arange(1, self.nbr_row):
            _value = self._get_align_and_focus_args_value(row=_row)
            if _value != ref_value:
                return False
        return True

    def _get_master_table_list_ui_for_row(self, row=-1):
        o_utilities = Utilities(parent=self.main_window)
        key_from_row = o_utilities.get_row_key_from_row_index(row=row)
        master_table_list_ui = self.main_window.master_table_list_ui[key_from_row]
        return master_table_list_ui

    def _get_chemical_formula_widget_value(self, row=-1):
        master_table_list_ui_for_row = self._get_master_table_list_ui_for_row(row=row)
        widget_ui = master_table_list_ui_for_row[self.data_type]['material']['text']
        return str(widget_ui.text())

    def _get_mass_density_widget_value(self, row=-1):
        master_table_list_ui_for_row = self._get_master_table_list_ui_for_row(row=row)
        widget_ui = master_table_list_ui_for_row[self.data_type]['mass_density']['text']
        return str(widget_ui.text())

    def _get_shape_value(self, row=-1):
        master_table_list_ui_for_row = self._get_master_table_list_ui_for_row(row=row)
        widget_ui = master_table_list_ui_for_row[self.data_type]['shape']
        return str(widget_ui.currentText())

    # geometry Dimensions column
    def get_geometry_dimensions_widgets(self, row=-1):
        master_table_list_ui_for_row = self._get_master_table_list_ui_for_row(row=row)
        radius_ui = master_table_list_ui_for_row[self.data_type]['geometry']['radius']['value']
        radius2_ui = master_table_list_ui_for_row[self.data_type]['geometry']['radius2']['value']
        height_ui = master_table_list_ui_for_row[self.data_type]['geometry']['height']['value']
        return {'radius': radius_ui,
                'radius2': radius2_ui,
                'height': height_ui}

    def _are_radius_identical(self):
        return self._are_geometry_value_identical(variable_name='radius')

    def _are_height_identical(self):
        return self._are_geometry_value_identical(variable_name='height')

    def _are_radius2_identical(self):
        return self._are_geometry_value_identical(variable_name='radius2')

    def _are_geometry_value_identical(self, variable_name='radius'):
        ref_widgets = self.get_geometry_dimensions_widgets(row=0)
        ref_radius = str(ref_widgets[variable_name].text())
        for _row in np.arange(1, self.nbr_row):
            val_widgets = self.get_geometry_dimensions_widgets(row=_row)
            _value = str(val_widgets[variable_name].text())
            if _value != ref_radius:
                return False
        return True

    def _get_abs_correction_widget_value(self, row=-1):
        master_table_list_ui_for_row = self._get_master_table_list_ui_for_row(row=row)
        widget_ui = master_table_list_ui_for_row[self.data_type]['abs_correction']
        return str(widget_ui.currentText())

    def _get_multi_correction_widget_value(self, row=-1):
        master_table_list_ui_for_row = self._get_master_table_list_ui_for_row(row=row)
        widget_ui = master_table_list_ui_for_row[self.data_type]['mult_scat_correction']
        return str(widget_ui.currentText())

    def _get_inelastic_correction_widget_value(self, row=-1):
        master_table_list_ui_for_row = self._get_master_table_list_ui_for_row(row=row)
        widget_ui = master_table_list_ui_for_row[self.data_type]['inelastic_correction']
        return str(widget_ui.currentText())

    def _get_placzek_infos(self, row=-1):
        master_table_list_ui_for_row = self._get_master_table_list_ui_for_row(row=row)
        dict = master_table_list_ui_for_row[self.data_type]['placzek_infos']
        return dict

    def _get_align_and_focus_args_value(self, row=-1):
        master_table_list_ui_for_row = self._get_master_table_list_ui_for_row(row=row)
        dict = master_table_list_ui_for_row['align_and_focus_args_infos']
        return dict
