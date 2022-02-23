from __future__ import (absolute_import, division, print_function)
from collections import OrderedDict
import copy
import simplejson
import numpy as np
import os
import re

from qtpy.QtCore import Qt

from addie.processing.mantid.master_table.geometry_handler import table2mantid
from addie.processing.mantid.master_table.periodic_table.material_handler import \
    retrieving_molecular_mass_and_number_of_atoms_worked
from addie.processing.mantid.master_table.tree_definition import SAMPLE_FIRST_COLUMN, NORMALIZATION_FIRST_COLUMN
from addie.processing.mantid.master_table.utilities import Utilities
from addie.utilities import math_tools
from addie.processing.mantid.master_table.reduction_configuration_handler import SaveReductionConfiguration

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
                                    "Self": True,
                                    "Interference": False,
                                    "FitSpectrumWith": "GaussConvCubicSpline",
                                    "LambdaBinningForFit": "",
                                    "LambdaBinningForCalc": "",
                                    },
            "Resonance": {
                "Axis": "",
                "LowerLimits": "",
                "UpperLimits": ""
                }
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

placzek_fit_methods = ["GaussConvCubicSpline"]


class TableFileExporter:

    def __init__(self, parent=None):
        self.parent = parent
        self.table_ui = parent.processing_ui.h3_table
        self.__nan_list = ['N/A', 'None']

        # generic elements to take from the ui
        self.facility = self.parent.facility
        self.instrument = self.parent.instrument["short_name"]
        self.cachedir = self.parent.cache_folder
        self.outputdir = self.parent.output_folder
        if not self.parent.reduction_configuration:
            SaveReductionConfiguration(parent.reduction_configuration_ui, grand_parent=parent)
        if not self.parent.reduction_configuration['initial']:
            self.intermediate_grouping_file = ''
        else:
            self.intermediate_grouping_file = self.parent.intermediate_grouping['filename']
        if not self.parent.reduction_configuration['output']:
            self.output_grouping_file = ''
        else:
            self.output_grouping_file = self.parent.output_grouping['filename']

        self.calibration = str(self.parent.processing_ui.calibration_file.text())

        self.NA_list = ["None", "N/A", "", np.NaN]

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
            dictionary, activate = self.retrieve_row_info(row)
        else:
            dictionary = self.retrieve_row_infos()
        # create the directory if it doesn't already exist
        direc = os.path.dirname(filename)
        if not os.path.exists(direc):
            os.mkdir(direc)
        # write out the configuration
        with open(filename, 'w') as outfile:
            simplejson.dump(dictionary, outfile, indent=2, ignore_nan=True)

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
        if packing_fraction and packing_fraction not in self.__nan_list:
            dict_element["PackingFraction"] = float(
                packing_fraction.strip("\""))

        column += 1
        shape = self._get_selected_value(row=row, column=column)
        dict_element["Geometry"]["Shape"] = shape

        column += 1
        radius = str(
            self.parent.master_table_list_ui[key][element]['geometry']['radius']['value'].text())
        radius2 = 'N/A'
        height = 'N/A'
        height_avail = ['Cylinder', 'Hollow Cylinder', 'PAC03', 'PAC06',
                        'PAC08', 'PAC10', 'QuartzTube03']
        if shape in height_avail:
            height = str(
                self.parent.master_table_list_ui[key][element]['geometry']['height']['value'].text())
        elif shape == 'Sphere':
            pass
        if shape == "Hollow Cylinder":
            radius2 = str(
                self.parent.master_table_list_ui[key][element]['geometry']['radius2']['value'].text())

        dict_element["Geometry"]["Radius"] = np.NaN if (
            radius in self.__nan_list) else float(radius)
        dict_element["Geometry"]["Radius2"] = np.NaN if (
            radius2 in self.__nan_list) else float(radius2)
        dict_element["Geometry"]["Height"] = np.NaN if (
            height in self.__nan_list) else float(height)

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

        fit_method_index = int(self.parent.master_table_list_ui[key][element]['placzek_infos']['fit_spectrum_index'])
        fit_method = placzek_fit_methods[fit_method_index]
        self.parent.master_table_list_ui[key][element]['placzek_infos']['fit_spectrum_text'] = fit_method
        placzek_infos = self.parent.master_table_list_ui[key][element]['placzek_infos']

        if inelastic_correction not in self.__nan_list:
            dict_element["InelasticCorrection"]["Self"] = placzek_infos["is_self"]
            dict_element["InelasticCorrection"]["Interference"] = placzek_infos["is_interference"]
            dict_element["InelasticCorrection"]["SampleTemperature"] = placzek_infos["sample_t"]
            fit_spectrum_text = placzek_infos["fit_spectrum_text"].replace(
                ".",
                "").replace(
                " ",
                "")
            dict_element["InelasticCorrection"]["FitSpectrumWith"] = fit_spectrum_text
            dict_element["InelasticCorrection"]["LambdaBinningForFit"] = "{},{},{}".format(
                placzek_infos["lambda_fit_min"],
                placzek_infos["lambda_fit_delta"],
                placzek_infos["lambda_fit_max"])
            dict_element["InelasticCorrection"]["LambdaBinningForCalc"] = "{},{},{}".format(
                placzek_infos["lambda_calc_min"],
                placzek_infos["lambda_calc_delta"],
                placzek_infos["lambda_calc_max"])
        else:
            dict_element.pop("InelasticCorrection")

        if element == "sample":
            column += 1
            axis_tmp = self.parent.master_table_list_ui[key][element]['resonance']['axis']['value'].text()
            dict_element['Resonance']['Axis'] = axis_tmp
            lim_list_tmp = self.parent.master_table_list_ui[key][element]['resonance']['lower']['lim_list']
            dict_element['Resonance']['LowerLimits'] = lim_list_tmp
            lim_list_tmp = self.parent.master_table_list_ui[key][element]['resonance']['upper']['lim_list']
            dict_element['Resonance']['UpperLimits'] = lim_list_tmp
        elif element == "normalization":
            dict_element.pop('Resonance', None)

        if len(dict_element['Background']['Background']['Runs']) == 0:
            dict_element['Background']['Background'].pop('Runs')
        dict_element = self.delete_empty_rows(dict_element)

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
        _export_dictionary_sample = self._retrieve_element_infos(
            element='sample', row=row)
        _export_dictionary_normalization = self._retrieve_element_infos(
            element='normalization', row=row)
        _key_value_dict = self._get_key_value_dict(row=row)
        key = self.get_key_from_row(row)
        self.scattering_lower = self.parent.master_table_list_ui[key]['self_scattering_level']['lower']['val_list']
        self.scattering_upper = self.parent.master_table_list_ui[key]['self_scattering_level']['upper']['val_list']
        try:
            self.QBin_min = self.parent.reduction_configuration['pdf']['q_range']['min']
            self.QBin_del = self.parent.reduction_configuration['pdf']['q_range']['delta']
            self.QBin_max = self.parent.reduction_configuration['pdf']['q_range']['max']
            self.advanced_params = self.parent.reduction_configuration['advanced']
        except:
            self.QBin_min = 0
            self.QBin_del = 0.02
            self.QBin_max = 40
            self.advanced_params = {"push_data_positive": False,
                                    "abs_ms_ele_size": "1.0"}

        ele_size_tmp = [float(item) for item in re.split(',| ', self.advanced_params["abs_ms_ele_size"])]
        if len(ele_size_tmp) == 1:
            _export_dictionary_sample["AbsMSParameters"] = {"ElementSize": ele_size_tmp[0]}
        else:
            _export_dictionary_sample["AbsMSParameters"] = {"ElementSize": ele_size_tmp[:2]}
        _export_dictionary_normalization["AbsMSParameters"] = {"ElementSize": ele_size_tmp[0]}

        if len(self.scattering_lower) > 0 and len(self.scattering_upper) > 0:
            bank1_list = [self.scattering_lower[0], self.scattering_upper[0]]
            bank2_list = [self.scattering_lower[1], self.scattering_upper[1]]
            bank3_list = [self.scattering_lower[2], self.scattering_upper[2]]
            bank4_list = [self.scattering_lower[3], self.scattering_upper[3]]
            bank5_list = [self.scattering_lower[4], self.scattering_upper[4]]
            bank6_list = [self.scattering_lower[5], self.scattering_upper[5]]
        else:
            bank1_list = "N/A"
            bank2_list = "N/A"
            bank3_list = "N/A"
            bank4_list = "N/A"
            bank5_list = "N/A"
            bank6_list = "N/A"

        dictionary = {
            'Activate': activate,
            'Facility': self.facility,
            'Instrument': self.instrument,
            'Title': title,
            'Sample': _export_dictionary_sample,
            'Normalization': _export_dictionary_normalization,
            'Calibration': {
                "Filename": self.calibration},
            'CacheDir': self.cachedir,
            'OutputDir': self.outputdir,
            "Merging": {
                "QBinning": [self.QBin_min, self.QBin_del, self.QBin_max],
                "SumBanks": [],
                "Characterizations": "",
                "Grouping": {
                    "Initial": self.intermediate_grouping_file,
                    "Output": self.output_grouping_file,
                },
            },
            'AlignAndFocusArgs': _key_value_dict,
            'SelfScatteringLevelCorrection': {
                "Bank1": bank1_list,
                "Bank2": bank2_list,
                "Bank3": bank3_list,
                "Bank4": bank4_list,
                "Bank5": bank5_list,
                "Bank6": bank6_list
                }
        }

        #Checking for empty lists and values
        dictionary = self.delete_empty_rows(dictionary)
        dictionary.pop('Activate')

        return dictionary, activate

    #Shouldn't delete the main category
    def delete_empty_rows(self, dictionary):
        del_set = set()
        del_sub_set = set()
        for key in dictionary:
            if dictionary[key] in self.NA_list:
                del_set.add(key)
            try:
                if len(dictionary[key]) == 0:
                    del_set.add(key)
            except:
                pass
            if type(dictionary[key]) is dict:
                for sub_key in dictionary[key]:
                    if dictionary[key][sub_key] in self.NA_list:
                        del_sub_set.add(sub_key)
                        del_set.add(key)
                    try:
                        if len(dictionary[key][sub_key]) == 0:
                            del_sub_set.add(sub_key)
                            del_set.add(key)
                    except:
                        pass
        for key in del_set:
            for sub_key in del_sub_set:
                try:
                    if type(dictionary[key]) is dict:
                        if sub_key in dictionary[key]:
                            dictionary[key].pop(sub_key)
                    else:
                        dictionary.pop(key)
                except:
                    pass
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
            # force 3 digits index (to make sure loading back the table will be
            # done in the same order)
            full_export_dictionary["{:03}".format(
                row)], activate = self.retrieve_row_info(row)

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

        # Post-process for output: take out overall Density and add MassDensity
        # key

        dictionary.pop('Density')
        dictionary['MassDensity'] = np.NaN if (mass_density in self.__nan_list) else float(mass_density)

        return dictionary

    def _remove_keys_from_with_nan_values(
            self, dictionary, selected_values=None):
        """Remove keys in a dictionary if the value is NaN

        :param dictionary: Dictionary with keys we want to check
        :type dictionary: dict
        :param selected_values: Dictionary with keys we want to check
        :type dictionary: dict

        :return: Dictionary with keys removed where value is NaN
        :rtype: dict
        """
        # Set default to check all keys unless selected_values defined
        if selected_values is None:
            selected_values = list(dictionary.keys()).copy()

        # Warn if selected_values is not a proper subset of the keys in the
        # dict
        if not set(selected_values).issubset(dictionary.keys()):
            err_string = "Found keys that are not part dictionary\n"
            err_string += "  List with 'erroneous' key: {} \n".format(
                ",".join(selected_values))
            err_string += "  Dictionary keys: {} \n".format(
                ",".join(dictionary.keys()))
            raise Exception(err_string)

        # Remove keys with NaN values
        for key in selected_values:
            try:
                if np.isnan(dictionary[key]):
                    dictionary.pop(key)
            except TypeError:
                pass

        return dictionary

    def _check_necessary_geometry_keys_exist(self, geometry):
        """ Check we have necessary keys for the specified geometry shape

        :param geometry: Geometry from ADDIE Table (pre-reduction-ready)
        "type geometry: dict

        :return: Geometry dictionary that has been checked for necessary keys
        :rtype: dict
        """
        # Grab shape we need to check against
        shape = geometry['Shape']

        # Find necessary keys from geometry_handler.table2mantid dict
        shape_dict = table2mantid[shape].copy()
        necessary_keys = list(shape_dict.keys())

        # Make sure all necessary keys exist
        for key in necessary_keys:
            if key not in geometry:
                err_string = "Did not find key {} in geometry {}".format(
                    key, geometry)
                print(err_string)
                return False

        return True

    def _map_table_to_mantid_geometry(self, geometry):
        """ Map from table geometry to mantid geometry using geometry_handler.table2mantid

        :param geometry: Geometry from ADDIE Table (pre-reduction-ready and checked)
        "type geometry: dict

        :return: Reduction-ready geometry dictionary
        :rtype: dict
        """
        # Grab shape we need to check against
        shape = geometry['Shape']

        # Get map from geometry_handler.table2mantid dict
        shape_dict = table2mantid[shape].copy()

        # Construct new geometry dict with mantid keys and do value processing
        # for the mapping
        new_geometry = dict()
        for k, v in geometry.items():
            new_key = shape_dict[k]["Key"]
            if "ValueProcessor" in shape_dict[k]:
                value_processor = shape_dict[k]["ValueProcessor"]
                new_value = value_processor(v)
            else:
                new_value = v
            new_geometry[new_key] = new_value

        return new_geometry

    def geometry_selection_for_reduction(self, dictionary):
        """Processing of the pre-reduction-ready JSON's `Geometry` to return
        a reduction-ready `Geometry` section in the passed dictionary

        :param dictionary: Pre-reduction-ready JSON with preliminary `Geometry` section
        :type row: dict

        :return: JSON dictionary with reduction-ready `Geometry` section
        :rtype: dict
        """
        # Default value for geometry
        geometry = {'Shape': 'Cylinder', 'Radius': 1.0}

        # return a default geometry if not specified
        if 'Geometry' not in dictionary:
            dictionary['Geometry'] = geometry
            print("No Geometry found, default geometry added:", geometry)
            return dictionary

        # Remove all NaN values from Geometry
        dictionary['Geometry'] = self._remove_keys_from_with_nan_values(
            dictionary['Geometry'])

        # return if no shape in Geometry, will use default in Mantid
        if 'Shape' not in dictionary['Geometry']:
            return dictionary

        # Get geometry and check if we have the necessary geometry keys for the
        # shape
        geometry = dictionary['Geometry']
        if not self._check_necessary_geometry_keys_exist(geometry):
            return []

        # Construct new geometry dict based on table to mantid mapping
        geometry = self._map_table_to_mantid_geometry(geometry)
        dictionary['Geometry'] = geometry

        return dictionary

    def pre_validator(self, json_input):

        necessary_keys = ["Calibration"]
        invalid_values = ['', 'nan', "N/A"]

        for key in necessary_keys:
            if key not in json_input:
                print("Key {0:s} not found in the input. We cannot continue.".format(key))
                return False
            else:
                if not json_input[key]:
                    print("No valid key found in {0:s}. We cannot continue.".format(key))
                    return False
                else:
                    for key_1, item_1 in json_input[key].items():
                        if item_1 in invalid_values:
                            str_tmp = "Invalid value '{0:s}' given ".format(item_1)
                            str_tmp += "for key '{0:s}' ".format(key_1)
                            str_tmp += "of '{0:s}'. We cannot continue.".format(key)
                            print(str_tmp)
                            return False
        return True

    def convert_from_row_to_reduction(self, json_input):
        """Processing of the pre-reduction JSON's `Density` to return
        a reduction-ready `MassDensity` section in the passed dictionary

        :param dictionary: Pre-reduction JSON with preliminary `Density` section
        :type row: dict

        :return: JSON dictionary with reduction-ready `MassDensity` section
        :rtype: dict
        """
        reduction_input = json_input
        if not self.pre_validator(reduction_input):
            return []
        for element in ["Sample", "Normalization"]:
            element_section = reduction_input[element]
            element_section = self.density_selection_for_reduction(
                element_section)
            if not self.geometry_selection_for_reduction(element_section):
                return []

        return reduction_input
