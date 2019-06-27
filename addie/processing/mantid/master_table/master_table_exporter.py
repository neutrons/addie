from __future__ import (absolute_import, division, print_function)
from collections import OrderedDict
import copy
import json
import numpy as np
import os

from qtpy.QtCore import Qt

from addie.processing.mantid.master_table.periodic_table.material_handler import retrieving_molecular_mass_and_number_of_atoms_worked
from addie.processing.mantid.master_table.tree_definition import SAMPLE_FIRST_COLUMN, NORMALIZATION_FIRST_COLUMN
from addie.processing.mantid.master_table.utilities import Utilities
from addie.utilities import math_tools

_export_dictionary = OrderedDict()

_element = {"Runs": "",
            "Background": {"Runs": "",
                           "Background": {"Runs": "",
                                          },
                           },
            "Material": "",
            "Density": {"MassDensity": np.NaN,
                        "UseMassDensity": True,
                        "NumberDensity": np.NaN,
                        "UseNumberDensity": False,
                        "Mass": np.NaN,
                        "UseMass": False},
            "PackingFraction": np.NaN,
            "Geometry": {"Shape": "",
                         "Radius": np.NaN,
                         "Radius2": np.NaN,
                         "Height": np.NaN,
                         },
            "AbsorptionCorrection": {"Type": "",
                                     },
            "MultipleScatteringCorrection": {"Type": "",
                                             },
            "InelasticCorrection": {"Type": "",
                                    "Order": "",
                                    "Self": True,
                                    "Interference": False,
                                    "FitSpectrumWith": "GaussConvCubicSpline",
                                    "LambdaBinningForFit": "",
                                    "LambdaBinningForCalc": "",
                                    },
            }

_data = {"Facility": "SNS",
         "Instrument": "NOM",
         "Title": "",
         "Sample": copy.deepcopy(_element),
         "Normalization": copy.deepcopy(_element),
         "Calibration": {"Filename": ""},
         "HighQLinearFitRange": np.NaN,
         "Merging": {"QBinning": [],
                     "SumBanks": [],
                     "Characterizations": "",
                     "Grouping": {"Initial": "",
                                  "Output": "",
                                  },
                     },
         "CacheDir": "./tmp",
         "OutputDir": "./output",
         "AlignAndFocusArgs": {},
         }

# _empty_row = {'Activate': True,
#               'Data': copy.deepcopy(_data)}


class TableFileExporter:

    def __init__(self, parent=None):
        self.parent = parent
        self.table_ui = parent.processing_ui.h3_table

        # generic elements to take from the ui
        self.facility = self.parent.facility
        self.instrument = self.parent.instrument["short_name"]
        self.cachedir = self.parent.cache_folder
        self.outputdir = self.parent.output_folder
        self.intermediate_grouping_file = self.parent.intermediate_grouping['filename']
        self.output_grouping_file = self.parent.output_grouping['filename']
        self.calibration = str(
            self.parent.processing_ui.calibration_file.text())

    def export(self, filename='', row=None):
        """create dictionary of all rows unless `row` argument is specified,
        which then only retrieves the single row

        :param filename: Filename to export the table to as JSON dump
        :type filename: str
        :param row: Row index to export to filename as JSON dump (optional)
        :type row: int
        """
        if not filename:
            raise RuntimeError('Cannot export data to empty filename')

        # put together the data to write out
        if row is not None:
            dictionary = self.retrieve_row_info(row)
        else:
            dictionary = self.retrieve_row_infos()

        # create the directory if it doesn't already exist
        direc = os.path.dirname(filename)
        if not os.path.exists(direc):
            os.mkdir(direc)

        # write out the configuration
        with open(filename, 'w') as outfile:
            json.dump(dictionary, outfile)

    def isActive(self, row):
        """Determine if `row` is activated for reduction

        :param row: Row to check if activated
        :type row: int

        :return: If the row is active
        :rtype: bool
        """
        # column 0 is 'Activate'
        return self._get_checkbox_state(row=row, column=0)

    def getRunDescr(self, row):
        """Get an <instrument>_<run number(s)> description of a given `row`

        :param row: Row index to retrieve the description
        :type row: int

        :return: String of <instrument>_<run number(s)> for row
        :rtype: str
        """
        runnumbers = self._get_item_value(row=row, column=SAMPLE_FIRST_COLUMN)
        if not runnumbers:
            return ''
        return '{}_{}'.format(self.instrument, runnumbers)

    def _get_checkbox_state(self, row=-1, column=-1):
        """Determine if checkbox is selected for cell in table at (row, column)

        :param row: Row index
        :type row: int
        :param column: Column index
        :type column: int

        :return: String of <instrument>_<run number(s)> for cell at (row, column)
        :rtype: str
        """
        state = self.table_ui.cellWidget(row, column).children()[
            1].checkState()
        return state == Qt.Checked

    def _get_item_value(self, row=-1, column=-1):
        """Get item from cell in table at (row, column)

        :param row: Row index
        :type row: int
        :param column: Column index
        :type column: int

        :return: String of item in cell at (row, column)
        :rtype: str
        """
        item = str(self.table_ui.item(row, column).text())
        return item

    def _get_text_value(self, row=-1, column=-1):
        """Get text value from cell in table at (row, column)

        :param row: Row index
        :type row: int
        :param column: Column index
        :type column: int

        :return: Text value in cell at (row, column)
        :rtype: str
        """
        widget = self.table_ui.cellWidget(row, column).children()[1]
        return str(widget.text())

    def _get_selected_value(self, row=-1, column=-1):
        """Get string of selected value from cell in table at (row, column)

        :param row: Row index
        :type row: int
        :param column: Column index
        :type column: int

        :return: String of selected value in cell at (row, column)
        :rtype: str
        """
        widget = self.table_ui.cellWidget(row, column).children()[1]
        return str(widget.currentText())

    def _retrieve_element_infos(self, element='sample', row=-1):
        """From the given row, and the given element (choices: [`sample`, `normalization`]),
        retrieve the widgets values as a pre-reduction JSON dictionary
        TODO: break this method down to smaller chunks for each key of dictionary

        :param element: Either the `sample` or `normalization` part of row
        :type column: str
        :param row: Row index
        :type row: int

        :return: Dictionary for the pre-reduction JSON formed from element's part of row in table
        :rtype: dict
        """

        dict_element = copy.deepcopy(_element)
        key = self.get_key_from_row(row)

        if element == 'sample':
            column = SAMPLE_FIRST_COLUMN
        else:
            column = NORMALIZATION_FIRST_COLUMN

        runs = self._get_item_value(row=row, column=column)
        dict_element['Runs'] = runs

        column += 1
        background_runs = self._get_item_value(row=row, column=column)
        dict_element["Background"]["Runs"] = background_runs

        column += 1
        background_background = self._get_item_value(row=row, column=column)
        dict_element["Background"]["Background"]["Runs"] = background_background

        column += 1
        material = self._get_text_value(row=row, column=column)
        dict_element["Material"] = material

        # mass density
        column += 1
        mass_density = str(
            self.parent.master_table_list_ui[key][element]['mass_density']['text'].text())
        dict_element["Density"]["MassDensity"] = mass_density
        dict_element["Density"]["UseMassDensity"] = \
            self.parent.master_table_list_ui[key][element]['mass_density_infos']['mass_density']['selected']
        dict_element["Density"]["NumberDensity"] = \
            self.parent.master_table_list_ui[key][element]['mass_density_infos']['number_density']['value']
        dict_element["Density"]["UseNumberDensity"] = \
            self.parent.master_table_list_ui[key][element]['mass_density_infos']['number_density']['selected']
        dict_element["Density"]["Mass"] = \
            self.parent.master_table_list_ui[key][element]['mass_density_infos']['mass']['value']
        dict_element["Density"]["UseMass"] = \
            self.parent.master_table_list_ui[key][element]['mass_density_infos']['mass']['selected']

        column += 1
        packing_fraction = self._get_item_value(row=row, column=column)
        dict_element["PackingFraction"] = packing_fraction

        column += 1
        shape = self._get_selected_value(row=row, column=column)
        dict_element["Geometry"]["Shape"] = shape

        column += 1
        radius = str(
            self.parent.master_table_list_ui[key][element]['geometry']['radius']['value'].text())
        radius2 = 'N/A'
        height = 'N/A'
        if shape == 'Cylinder':
            height = str(
                self.parent.master_table_list_ui[key][element]['geometry']['height']['value'].text())
        elif shape == 'Sphere':
            pass
        else:
            radius2 = str(
                self.parent.master_table_list_ui[key][element]['geometry']['radius2']['value'].text())

        dict_element["Geometry"]["Radius"] = np.NaN if (
            radius == 'N/A') else float(radius)
        dict_element["Geometry"]["Radius2"] = np.NaN if (
            radius2 == 'N/A') else float(radius2)
        dict_element["Geometry"]["Height"] = np.NaN if (
            height == 'N/A') else float(height)

        column += 1
        abs_correction = self._get_selected_value(row=row, column=column)
        dict_element["AbsorptionCorrection"]["Type"] = abs_correction

        column += 1
        multiple_scattering_correction = self._get_selected_value(
            row=row, column=column)
        dict_element["MultipleScatteringCorrection"]["Type"] = multiple_scattering_correction

        column += 1
        inelastic_correction = self._get_selected_value(row=row, column=column)
        dict_element["InelasticCorrection"]["Type"] = inelastic_correction

#        if inelastic_correction.lower() == 'placzek':

        placzek_infos = self.parent.master_table_list_ui[key][element]['placzek_infos']

        dict_element["InelasticCorrection"]["Order"] = placzek_infos["order_index"]
        dict_element["InelasticCorrection"]["Self"] = placzek_infos["is_self"]
        dict_element["InelasticCorrection"]["Interference"] = placzek_infos["is_interference"]
        dict_element["InelasticCorrection"]["FitSpectrumWith"] = placzek_infos["fit_spectrum_index"]
        dict_element["InelasticCorrection"]["LambdaBinningForFit"] = "{},{},{}".format(placzek_infos["lambda_fit_min"],
                                                                                       placzek_infos["lambda_fit_delta"],
                                                                                       placzek_infos["lambda_fit_max"])
        dict_element["InelasticCorrection"]["LambdaBinningForCalc"] = "{},{},{}".format(placzek_infos["lambda_calc_min"],
                                                                                        placzek_infos["lambda_calc_delta"],
                                                                                        placzek_infos["lambda_calc_max"])

        print("DICT ELEMENT:", dict_element)
        return dict_element

    def _get_key_value_dict(self, row=-1):
        """Get key from row, and return the AlignAndFocusArgs info values

        :param row: Row index
        :type row: int

        :return: Dictionary of the AlignAndFocusArgs info
        :rtype: dict
        """
        key = self.get_key_from_row(row)
        key_value_dict = self.parent.master_table_list_ui[key]['align_and_focus_args_infos']
        return key_value_dict

    def _check_only_one_density_method_selected(self, dictionary):
        """Check the density section of pre-reduction JSON only has one method selected.
        Raises exception if does not, just pass if complies.

        :param dictionary: Pre-reduction JSON with preliminary `Density` section
        :type row: dict
        """
        density = dictionary['Density']
        opts = iter([density['UseMassDensity'],
                     density['UseNumberDensity'], density['UseMass']])
        if not math_tools.oneAndOnlyOneTrue(opts):
            raise Exception(
                "Must use one and only one way to calculated MassDensity")

    def _get_mass_density_from_number_density(self, dictionary):
        """Take pre-reduction JSON with `NumberDensity` as selected method
        to calculate the mass density

        :param dictionary: Pre-reduction JSON with preliminary `Density` section
        :type row: dict

        :return: mass density
        :rtype: float
        """

        if 'Material' not in dictionary:
            raise Exception(
                "Must define chemical formula to use NumberDensity for reduction")
        density = dictionary['Density']
        number_density = density['NumberDensity']
        chemical_formula = dictionary['Material']
        mass, natoms = retrieving_molecular_mass_and_number_of_atoms_worked(
            chemical_formula)
        mass_density = math_tools.number_density2mass_density(
            number_density, natoms, mass)
        return mass_density

    def _get_mass_density_from_mass(self, dictionary):
        """Take pre-reduction JSON with `Mass` as selected method
        to calculate the mass density

        :param dictionary: Pre-reduction JSON with preliminary `Density` section
        :type row: dict

        :return: mass density
        :rtype: float
        """

        if 'Material' not in dictionary:
            raise Exception(
                "Must define chemical formula to use Mass for reduction")
        if 'Geometry' not in dictionary:
            raise Exception(
                "Must define a geometry to use Mass for reduction")

        mass = dictionary['Density']['Mass']
        volume = math_tools.get_volume_from_geometry(dictionary['Geometry'])
        mass_density = math_tools.mass2mass_density(mass, volume)
        return mass_density

    def get_key_from_row(self, row):
        """Get key from row

        :param row: Row index
        :type row: int

        :return: Get key for the row
        :rtype: str
        """
        o_util = Utilities(parent=self.parent)
        key = o_util.get_row_key_from_row_index(row=row)
        return key

    def retrieve_row_info(self, row):
        """Retrieve a single row's information in a pre-reduction JSON format

        :param row: Row index
        :type row: int

        :return: Dictionary for the row in a pre-reduction JSON format
        :rtype: dict
        """
        activate = self._get_checkbox_state(row=row, column=0)
        title = self._get_item_value(row=row, column=1)
        _export_dictionary_sample = self._retrieve_element_infos(element='sample',
                                                                 row=row)
        _export_dictionary_normalization = self._retrieve_element_infos(element='normalization',
                                                                        row=row)
        _key_value_dict = self._get_key_value_dict(row=row)

        dictionary = {'Activate': activate,
                      'Title': title,
                      'Sample': _export_dictionary_sample,
                      'Normalization': _export_dictionary_normalization,
                      'Calibration': {"Filename": self.calibration},
                      'Facility': self.facility,
                      'Instrument': self.instrument,
                      'CacheDir': self.cachedir,
                      'OutputDir': self.outputdir,
                      "Merging": {"QBinning": [],
                                  "SumBanks": [],
                                  "Characterizations": "",
                                  "Grouping": {"Initial": self.intermediate_grouping_file,
                                               "Output": self.output_grouping_file,
                                               },
                                  },
                      'AlignAndFocusArgs': _key_value_dict,
                      }
        return dictionary

    def retrieve_row_infos(self):
        """Retrieve all of the rows' information in a pre-reduction JSON format

        :param row: Row index
        :type row: int

        :return: Dictionary for all the rows in the table in a pre-reduction JSON format
        :rtype: dict
        """
        full_export_dictionary = OrderedDict()
        nbr_row = self.table_ui.rowCount()

        for row in range(nbr_row):
            # force 3 digits index (to make sure loading back the table will be done in the same order)
            full_export_dictionary["{:03}".format(
                row)] = self.retrieve_row_info(row)

        return full_export_dictionary

    def density_selection_for_reduction(self, dictionary):
        """Processing of the pre-reduction JSON's `Density` to return
        a reduction-ready `MassDensity` section in the passed dictionary

        :param dictionary: Pre-reduction JSON with preliminary `Density` section
        :type row: dict

        :return: JSON dictionary with reduction-ready `MassDensity` section
        :rtype: dict
        """
        # Default value for mass density
        mass_density = 1.0

        # return if density section not defined
        if 'Density' not in dictionary:
            dictionary['MassDensity'] = mass_density
            return dictionary

        # ensure one and only one way is selected for calculating MassDensity
        self._check_only_one_density_method_selected(dictionary)

        # convert to mass density
        density = dictionary['Density']
        if density['UseMassDensity']:
            mass_density = density['MassDensity']

        if density['UseNumberDensity']:
            mass_density = self._get_mass_density_from_number_density(
                dictionary)

        if density['UseMass']:
            mass_density = self._get_mass_density_from_mass(dictionary)

        # Post-process for output: take out overall Density and add MassDensity key
        dictionary.pop('Density')
        dictionary['MassDensity'] = mass_density

        return dictionary

    def convert_from_row_to_reduction(self, json_input):
        reduction_input = json_input
        print("\n\nBefore Reduction row:", reduction_input["Sample"])
        print("\n\nAfter Reduction row:",
              self.density_selection_for_reduction(reduction_input["Sample"]))

        return reduction_input
