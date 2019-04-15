import numpy as np
from qtpy import QtGui
from qtpy.QtWidgets import QTableWidgetItem

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


class ColumnHighlighting:

    def __init__(self, main_window=None, column=-1):
        self.main_window = main_window
        self.column = column

        self.nbr_row = self.get_nbr_row()

    def get_nbr_row(self):
        nbr_row = self.main_window.processing_ui.h3_table.rowCount()
        return nbr_row

    def check(self):
        column = self.column
        are_all_the_same = False

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

            elif (column in INDEX_OF_ABS_CORRECTION) or \
                    (column in INDEX_OF_MULTI_SCATTERING_CORRECTION):
                are_all_the_same = self.are_abs_or_multi_correction_identical()

            elif column in INDEX_OF_INELASTIC_CORRECTION:
                are_all_the_same = self.are_inelastic_correction_identical()

            elif column == LIST_COLUMNS_TO_SEARCH_FOR_FULL_HIGHLIGTHING[-1]:
                are_all_the_same = self.are_align_and_focus_args_identical()

        self.apply_cell_background(are_all_the_same=are_all_the_same)

    def apply_cell_background(self, are_all_the_same=False):
        if are_all_the_same:
            background_color = QtGui.QColor(COLUMNS_IDENTICAL_VALUES_COLOR[0],
                                            COLUMNS_IDENTICAL_VALUES_COLOR[1],
                                            COLUMNS_IDENTICAL_VALUES_COLOR[2])
            background_color_stylesheet = "rgb({}, {}, {})".format(COLUMNS_IDENTICAL_VALUES_COLOR[0],
                                                                   COLUMNS_IDENTICAL_VALUES_COLOR[1],
                                                                   COLUMNS_IDENTICAL_VALUES_COLOR[2])
        else:
            background_color = QtGui.QColor(COLUMNS_SAME_VALUES_COLOR[0],
                                            COLUMNS_SAME_VALUES_COLOR[1],
                                            COLUMNS_SAME_VALUES_COLOR[2])
            background_color_stylesheet = "rgb({}, {}, {})".format(COLUMNS_SAME_VALUES_COLOR[0],
                                                                   COLUMNS_SAME_VALUES_COLOR[1],
                                                                   COLUMNS_SAME_VALUES_COLOR[2])

        for _row in np.arange(self.nbr_row):

            if (self.column in INDEX_OF_COLUMNS_WITH_CHEMICAL_FORMULA) or \
                    (self.column in INDEX_OF_COLUMNS_WITH_MASS_DENSITY) or \
                    (self.column in INDEX_OF_COLUMNS_WITH_GEOMETRY_INFOS) or \
                    (self.column in INDEX_OF_COLUMNS_SHAPE) or \
                    (self.column in INDEX_OF_ABS_CORRECTION) or \
                    (self.column in INDEX_OF_MULTI_SCATTERING_CORRECTION) or \
                    (self.column in INDEX_OF_INELASTIC_CORRECTION) or \
                    (self.column == LIST_COLUMNS_TO_SEARCH_FOR_FULL_HIGHLIGTHING):
                main_widget = self.main_window.processing_ui.h3_table.cellWidget(_row, self.column)
                main_widget.setAutoFillBackground(True)
                main_widget.setStyleSheet("background-color: {};".format(background_color_stylesheet))
            else:
                self.main_window.processing_ui.h3_table.item(_row, self.column).setBackground(background_color)

    def are_cells_identical(self):
        return True

    def are_chemical_formula_identical(self):
        return True

    def are_mass_density_identical(self):
        return True

    def are_shape_identical(self):
        return True

    def are_geometry_identical(self):
        return True

    def are_abs_or_multi_correction_identical(self):
        return True

    def are_inelastic_correction_identical(self):
        return True

    def are_align_and_focus_args_identical(self):
        return True

