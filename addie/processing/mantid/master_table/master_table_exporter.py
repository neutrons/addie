from __future__ import (absolute_import, division, print_function)
from collections import OrderedDict
import copy
import numpy as np
import json

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
         "Calibration": "",
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
         }

# _empty_row = {'Activate': True,
#               'Data': copy.deepcopy(_data)}


class TableFileExporter:

    def __init__(self, parent=None, filename=''):
        self.parent = parent
        self.table_ui = parent.ui.h3_table
        self.filename = filename

    def create_dictionary(self):
        '''using the general infos, and the one from each row, this method creates the master
        dictionary that will be saved into a json file'''

        self.dict = self._retrieve_row_infos()

    def export(self):
        dict = self.dict
        filename = self.filename

        with open(filename, 'w') as outfile:
            json.dump(dict, outfile)

    def _get_checkbox_state(self, row=-1, column=-1):
        state = self.table_ui.cellWidget(row, column).children()[1].checkState()
        if state == Qt.Checked:
            return True
        return False

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

        # retrieve the key according to row
        o_util = Utilities(parent=self.parent)
        key = o_util.get_row_key_from_row_index(row=row)

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
        dict_element["MassDensity"]["UseMassDensity"] = self.parent.master_table_list_ui[key][element]['mass_density_infos']['mass_density']['selected']
        dict_element["MassDensity"]["NumberDensity"] = self.parent.master_table_list_ui[key][element]['mass_density_infos']['number_density']['value']
        dict_element["MassDensity"]["UseNumberDensity"] = self.parent.master_table_list_ui[key][element]['mass_density_infos']['number_density']['selected']
        dict_element["MassDensity"]["Mass"] = self.parent.master_table_list_ui[key][element]['mass_density_infos']['mass']['value']
        dict_element["MassDensity"]["UseMass"] = self.parent.master_table_list_ui[key][element]['mass_density_infos']['mass']['selected']

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
        if shape == 'cylindrical':
            height = str(self.parent.master_table_list_ui[key][element]['geometry']['height']['value'].text())
        elif shape == 'spherical':
            pass
        else:
            radius2 = str(self.parent.master_table_list_ui[key][element]['geometry']['radius2']['value'].text())

        dict_element["Geometry"]["Radius"] = radius
        dict_element["Geometry"]["Radius2"] = radius2
        dict_element["Geometry"]["Height"] = height

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

    def _retrieve_row_infos(self):
        '''this method retrieves the infos from the table using the master_table_list_ui'''

        facility = self.parent.facility
        instrument = self.parent.instrument["short_name"]
        cachedir = self.parent.cache_folder
        outputdir = self.parent.output_folder
        intermediate_grouping_file = self.parent.intermediate_grouping['filename']
        output_grouping_file = self.parent.output_grouping['filename']

        full_export_dictionary = OrderedDict()
        nbr_row = self.table_ui.rowCount()

        for _row in np.arange(nbr_row):

            activate = self._get_checkbox_state(row=_row, column=0)
            title = self._get_item_value(row=_row, column=1)
            _export_dictionary_sample = self._retrieve_element_infos(element='sample',
                                                                        row=_row)
            _export_dictionary_normalization = self._retrieve_element_infos(element='normalization',
                                                                            row=_row)
            _calibration = str(self.parent.ui.calibration_file.text())

            # force 3 digits index (to make sure loading back the table will be done in the same order)
            row = "{:03}".format(_row)
            full_export_dictionary[row] = {'Sample': _export_dictionary_sample,
                                           'Activate': activate,
                                           'Title': title,
                                           'Calibration': _calibration,
                                           'Normalization': _export_dictionary_normalization,
                                           'Facility': facility,
                                           'Instrument': instrument,
                                           'CacheDir': cachedir,
                                           'OutputDir': outputdir,
                                           "Merging": {"QBinning": [],
                                                       "SumBanks": [],
                                                       "Characterizations": "",
                                                       "Grouping": {"Initial": intermediate_grouping_file,
                                                                    "Output": output_grouping_file,
                                                                    },
                                                       },
                                           }

        return full_export_dictionary


