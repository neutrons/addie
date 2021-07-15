import numpy as np
from qtpy import QtGui

from addie.processing.mantid.master_table.utilities import Utilities

from addie.processing.mantid.master_table.tree_definition import (
    INDEX_OF_COLUMNS_SEARCHABLE,
    INDEX_OF_COLUMNS_WITH_CHEMICAL_FORMULA,
    INDEX_OF_COLUMNS_WITH_MASS_DENSITY,
    INDEX_OF_COLUMNS_SHAPE,
    INDEX_OF_COLUMNS_WITH_GEOMETRY_INFOS,
    INDEX_OF_ABS_CORRECTION,
    INDEX_OF_MULTI_SCATTERING_CORRECTION,
    INDEX_OF_INELASTIC_CORRECTION,
    LIST_COLUMNS_TO_SEARCH_FOR_FULL_HIGHLIGTHING,
    INDEX_OF_COLUMNS_WITH_RESONANCE_INFOS,
    INDEX_OF_COLUMNS_WITH_SCATTERING_LEVELS
)
from addie.processing.mantid.master_table.tree_definition import (
    COLUMNS_IDENTICAL_VALUES_COLOR,
    COLUMNS_DIFFERENT_VALUES_COLOR
)
from addie.processing.mantid.master_table.tree_definition import (
    INDEX_NORMALIZATION_START
)


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
        self.main_window.processing_ui.h3_table.blockSignals(True)

        self.column = column
        are_all_same = False

        self.set_data_type()

        if self.nbr_row > 1:

            for _ in np.arange(self.nbr_row):

                # item
                if column in INDEX_OF_COLUMNS_SEARCHABLE:
                    are_all_same = self.are_cells_identical()

                elif column in INDEX_OF_COLUMNS_WITH_CHEMICAL_FORMULA:
                    are_all_same = self.are_chemical_formula_identical()

                elif column in INDEX_OF_COLUMNS_WITH_MASS_DENSITY:
                    are_all_same = self.are_mass_density_identical()

                elif column in INDEX_OF_COLUMNS_SHAPE:
                    are_all_same = self.are_shape_identical()

                elif column in INDEX_OF_COLUMNS_WITH_GEOMETRY_INFOS:
                    are_all_same = self.are_geometry_identical()

                elif column in INDEX_OF_COLUMNS_WITH_RESONANCE_INFOS:
                    are_all_same = self.are_resonance_identical()

                elif column in INDEX_OF_COLUMNS_WITH_SCATTERING_LEVELS:
                    are_all_same = self.are_scattering_identical()

                elif column in INDEX_OF_ABS_CORRECTION:
                    are_all_same = self.are_abs_correction_identical()

                elif column in INDEX_OF_MULTI_SCATTERING_CORRECTION:
                    are_all_same = self.are_multi_correction_identical()

                elif column in INDEX_OF_INELASTIC_CORRECTION:
                    are_all_same = self.are_inelastic_correction_identical()

                elif column == LIST_COLUMNS_TO_SEARCH_FOR_FULL_HIGHLIGTHING[-1]:
                    are_all_same = self.are_align_and_focus_args_identical()

        self.apply_cell_background(are_all_the_same=are_all_same)
        self.main_window.processing_ui.h3_table.blockSignals(False)

    def apply_cell_background(self, are_all_the_same=False):
        if are_all_the_same:
            background_color = QtGui.QColor(
                COLUMNS_IDENTICAL_VALUES_COLOR[0],
                COLUMNS_IDENTICAL_VALUES_COLOR[1],
                COLUMNS_IDENTICAL_VALUES_COLOR[2]
            )
            background_color_stylesheet = "rgb({}, {}, {})".format(
                COLUMNS_IDENTICAL_VALUES_COLOR[0],
                COLUMNS_IDENTICAL_VALUES_COLOR[1],
                COLUMNS_IDENTICAL_VALUES_COLOR[2]
            )
        else:
            background_color = QtGui.QColor(
                COLUMNS_DIFFERENT_VALUES_COLOR[0],
                COLUMNS_DIFFERENT_VALUES_COLOR[1],
                COLUMNS_DIFFERENT_VALUES_COLOR[2]
            )
            background_color_stylesheet = "rgb({}, {}, {})".format(
                COLUMNS_DIFFERENT_VALUES_COLOR[0],
                COLUMNS_DIFFERENT_VALUES_COLOR[1],
                COLUMNS_DIFFERENT_VALUES_COLOR[2]
            )

        pen_color = "black"
        selection_color = "white"
        selection_background_color = "blue"

        for _row in np.arange(self.nbr_row):

            main_widget = self.main_window.processing_ui.h3_table.cellWidget(
                _row, self.column)

            if main_widget:

                if self.column in INDEX_OF_COLUMNS_SEARCHABLE:
                    self.main_window.processing_ui.h3_table.item(
                        _row, self.column).setBackground(background_color)
                else:
                    main_widget.setAutoFillBackground(True)
                    main_widget.setStyleSheet(
                        "color: {}; "
                        "background-color: {};"
                        "selection-color: {};"
                        "selection-background-color: {};".format(
                            pen_color,
                            background_color_stylesheet,
                            selection_color,
                            selection_background_color
                        )
                    )

            else:
                self.main_window.processing_ui.h3_table.item(
                    _row, self.column).setBackground(background_color)

    def are_cells_identical(self):
        def _get_item_value(row=-1, column=-1):
            item = self.main_window.processing_ui.h3_table.item(row, column)
            return str(item.text())

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

        # we are done for sphere geometry
        if shape_selected.lower() == "sphere":
            return True

        if not self._are_height_identical():
            return False

        # we are done for cylinder geometry
        if shape_selected.lower() == "cylinder":
            return True

        if not self._are_radius2_identical():
            return False
        return True

    def are_resonance_identical(self,type="Resonance"):
        if not self._are_axis_identical():
            return False

        if not self._are_lowerlim_identical(type):
            return False

        if not self._are_upperlim_identical(type):
            return False
        return True

    def are_scattering_identical(self,type="Scattering"):
        if not self._are_lowerlim_identical(type):
            return False

        if not self._are_upperlim_identical(type):
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
        table_list_ui = self.main_window.master_table_list_ui[key_from_row]
        return table_list_ui

    def _get_chemical_formula_widget_value(self, row=-1):
        master_table_list_ui_for_row = self._get_master_table_list_ui_for_row(
            row=row)
        widget_ui = master_table_list_ui_for_row[self.data_type]
        return str(widget_ui['material']['text'].text())

    def _get_mass_density_widget_value(self, row=-1):
        master_table_list_ui_for_row = self._get_master_table_list_ui_for_row(
            row=row)
        widget_ui = master_table_list_ui_for_row[self.data_type]
        return str(widget_ui['mass_density']['text'].text())

    def _get_shape_value(self, row=-1):
        master_table_list_ui_for_row = self._get_master_table_list_ui_for_row(
            row=row)
        widget_ui = master_table_list_ui_for_row[self.data_type]['shape']
        return str(widget_ui.currentText())

    # geometry Dimensions column
    def get_geometry_dimensions_widgets(self, row=-1):
        master_table_list_ui_for_row = self._get_master_table_list_ui_for_row(
            row=row)
        geometry = master_table_list_ui_for_row[self.data_type]['geometry']

        radius_ui = geometry['radius']['value']
        radius2_ui = geometry['radius2']['value']
        height_ui = geometry['height']['value']

        return {
            'radius': radius_ui,
            'radius2': radius2_ui,
            'height': height_ui
        }

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

    def _are_axis_identical(self):
        return self._are_resonance_value_identical(variable_name='axis')

    def _are_lowerlim_identical(self,type="Resonance"):
        if type == "Resonance":
            return self._are_resonance_value_identical(variable_name='lower')
        elif type == "Scattering":
            return self._are_scattering_value_identical(variable_name='lower')

    def _are_upperlim_identical(self,type="Resonance"):
        if type == "Resonance":
            return self._are_resonance_value_identical(variable_name='upper')
        elif type == "Scattering":
            return self._are_scattering_value_identical(variable_name='upper')

    def _are_resonance_value_identical(self, variable_name='axis'):
        ref_widgets = self._get_resonance_correction_widgets(row=0)
        ref_value = str(ref_widgets[variable_name].text())
        for _row in np.arange(1, self.nbr_row):
            val_widgets = self._get_resonance_correction_widgets(row=_row)
            _value = str(val_widgets[variable_name].text())
            if _value != ref_value:
                return False
            return True

    def _are_scattering_value_identical(self, variable_name='lower'):
        ref_widgets = self._get_scattering_correction_widgets(row=0)
        ref_value = str(ref_widgets[variable_name].text())
        for _row in np.arange(1,self.nbr_row):
            val_widgets = self._get_scattering_correction_widgets(row=_row)
            _value = str(val_widgets[variable_name].text())
            if _value != ref_value:
                return False
            return True

    def _get_abs_correction_widget_value(self, row=-1):
        master_table_list_ui_for_row = self._get_master_table_list_ui_for_row(
            row=row)
        widget_ui = master_table_list_ui_for_row[self.data_type]
        return str(widget_ui['abs_correction'].currentText())

    def _get_multi_correction_widget_value(self, row=-1):
        master_table_list_ui_for_row = self._get_master_table_list_ui_for_row(
            row=row)
        widget_ui = master_table_list_ui_for_row[self.data_type]
        return str(widget_ui['mult_scat_correction'].currentText())

    def _get_inelastic_correction_widget_value(self, row=-1):
        master_table_list_ui_for_row = self._get_master_table_list_ui_for_row(
            row=row)
        widget_ui = master_table_list_ui_for_row[self.data_type]
        return str(widget_ui['inelastic_correction'].currentText())

    def _get_resonance_correction_widgets(self, row=-1):
        master_table_list_ui_for_row = self._get_master_table_list_ui_for_row(
            row=row)
        resonance = master_table_list_ui_for_row[self.data_type]['resonance']

        axis_ui = resonance['axis']['value']
        lower_ui = resonance['lower']['value']
        upper_ui = resonance['upper']['value']

        return {
            'axis': axis_ui,
            'lower': lower_ui,
            'upper': upper_ui
        }

    def _get_scattering_correction_widgets(self, row=-1):
        master_table_list_ui_for_row = self._get_master_table_list_ui_for_row(
            row=row)
        scattering = master_table_list_ui_for_row['self_scattering_level']

        lower_ui = scattering['lower']['value']
        upper_ui = scattering['upper']['value']

        return {
            'lower': lower_ui,
            'upper': upper_ui
        }

    def _get_placzek_infos(self, row=-1):
        master_table_list_ui_for_row = self._get_master_table_list_ui_for_row(
            row=row)
        dict = master_table_list_ui_for_row[self.data_type]['placzek_infos']
        return dict

    def _get_align_and_focus_args_value(self, row=-1):
        master_table_list_ui_for_row = self._get_master_table_list_ui_for_row(
            row=row)
        dict = master_table_list_ui_for_row['align_and_focus_args_infos']
        return dict
