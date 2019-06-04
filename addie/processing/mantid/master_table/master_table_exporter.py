from __future__ import (absolute_import, division, print_function)
from collections import OrderedDict
import copy
import json
import numpy as np
import os

from qtpy.QtCore import Qt

from addie.processing.mantid.master_table.tree_definition import SAMPLE_FIRST_COLUMN, NORMALIZATION_FIRST_COLUMN
from addie.processing.mantid.master_table.utilities import Utilities

_export_dictionary = OrderedDict()

_element= {"Runs": "",
           "Background": {"Runs": "",
                          "Background": {"Runs": "",
                                         },
                          },
           "Material": "",
           "MassDensity": {"MassDensity": np.NaN,
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
         "Title" : "",
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
        self.calibration = str(self.parent.processing_ui.calibration_file.text())

    def export(self, filename='', row=None):
        """create dictionary of all rows unless that argument is specified"""
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
        # column 0 is 'Activate'
        return self._get_checkbox_state(row=row, column=0)

    def getRunDescr(self, row):
        runnumbers = self._get_item_value(row=row, column=SAMPLE_FIRST_COLUMN)
        if not runnumbers:
            return ''
        return '{}_{}'.format(self.instrument, runnumbers)

    def _get_checkbox_state(self, row=-1, column=-1):
        state = self.table_ui.cellWidget(row, column).children()[1].checkState()
        return state == Qt.Checked

    def _get_item_value(self, row=-1, column=-1):
        item = str(self.table_ui.item(row, column).text())
        return item

    def _get_text_value(self, row=-1, column=-1):
        widget = self.table_ui.cellWidget(row, column).children()[1]
        return str(widget.text())

    def _get_selected_value(self, row=-1, column=-1):
        widget = self.table_ui.cellWidget(row, column).children()[1]
        return str(widget.currentText())

    def _retrieve_element_infos(self, element='sample', row=-1):
        '''form the given row, and the given element (sample or normalization) will
        retrieve the widgets values'''

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
        mass_density = str(self.parent.master_table_list_ui[key][element]['mass_density']['text'].text())
        dict_element["MassDensity"]["MassDensity"] = mass_density
        dict_element["MassDensity"]["UseMassDensity"] = \
            self.parent.master_table_list_ui[key][element]['mass_density_infos']['mass_density']['selected']
        dict_element["MassDensity"]["NumberDensity"] = \
            self.parent.master_table_list_ui[key][element]['mass_density_infos']['number_density']['value']
        dict_element["MassDensity"]["UseNumberDensity"] = \
            self.parent.master_table_list_ui[key][element]['mass_density_infos']['number_density']['selected']
        dict_element["MassDensity"]["Mass"] = \
            self.parent.master_table_list_ui[key][element]['mass_density_infos']['mass']['value']
        dict_element["MassDensity"]["UseMass"] = \
            self.parent.master_table_list_ui[key][element]['mass_density_infos']['mass']['selected']

        column += 1
        packing_fraction =  self._get_item_value(row=row, column=column)
        dict_element["PackingFraction"] = packing_fraction

        column += 1
        shape = self._get_selected_value(row=row, column=column)
        dict_element["Geometry"]["Shape"] = shape

        column += 1
        radius = str(self.parent.master_table_list_ui[key][element]['geometry']['radius']['value'].text())
        radius2 = 'N/A'
        height = 'N/A'
        if shape == 'Cylinder':
            height = str(self.parent.master_table_list_ui[key][element]['geometry']['height']['value'].text())
        elif shape == 'Sphere':
            pass
        else:
            radius2 = str(self.parent.master_table_list_ui[key][element]['geometry']['radius2']['value'].text())

        dict_element["Geometry"]["Radius"] = int(radius)
        dict_element["Geometry"]["Radius2"] = int(radius2)
        dict_element["Geometry"]["Height"] = int(height)

        column += 1
        abs_correction = self._get_selected_value(row=row, column=column)
        dict_element["AbsorptionCorrection"]["Type"] = abs_correction

        column += 1
        multiple_scattering_correction = self._get_selected_value(row=row, column=column)
        dict_element["MultipleScatteringCorrection"]["Type"] = multiple_scattering_correction

        column += 1
        inelastic_correction = self._get_selected_value(row=row,column=column)
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
        return dict_element

    def _get_key_value_dict(self, row=-1):
        key = self.get_key_from_row(row)
        key_value_dict = self.parent.master_table_list_ui[key]['align_and_focus_args_infos']
        return key_value_dict

    def get_key_from_row(self, row):
        # retrieve the key according to row
        o_util = Utilities(parent=self.parent)
        key = o_util.get_row_key_from_row_index(row=row)
        return key

    def retrieve_row_info(self, row):
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
                      'Calibration': {"Filename": self.calibration },
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
        '''this method retrieves the infos from the table using the master_table_list_ui'''
        full_export_dictionary = OrderedDict()
        nbr_row = self.table_ui.rowCount()

        for row in range(nbr_row):
            # force 3 digits index (to make sure loading back the table will be done in the same order)
            full_export_dictionary["{:03}".format(row)] = self.retrieve_row_info(row)

        return full_export_dictionary
