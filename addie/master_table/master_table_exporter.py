from collections import OrderedDict
import copy
import numpy as np

try:
    from PyQt4.QtCore import Qt
except ImportError:
    try:
        from PyQt5.QtCore import Qt
    except ImportError:
        raise ImportError("Requires PyQt4 or PyQt5")

from addie.master_table.tree_definition import sample_first_column, normalization_first_column
from addie.master_table.utilities import Utilities

_export_dictionary = OrderedDict()

_element= {"Runs": "",
           "Background": {"Runs": "",
                          "Background": {"Runs": "",
                                         },
                          },
           "Material": "",
           "MassDensity": np.NaN,
           "PackingFraction": np.NaN,
           "Geometry": {"Radius": np.NaN,
                        "Radius1": np.NaN,
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
                                   "LambdaBinningForCAlc": "",
                                   },
           }

_data = {"Facility": "SNS",
         "Instrument": "NOM",
         "Title" : "",
         "Sample": copy.deepcopy(_element),
         "Vanadium": copy.deepcopy(_element),
         "Calibration": "",
         "HighQLinearFitRange": np.NaN,
         "Merging": {"QBinning": [],
                     "SumBanks": [],
                     "Characterizations": "",
                     "Grouping": {"Initial": "",
                                  "Output": "",
                                  },
                     "CacheDir": "./tmp",
                     "OutputDir": "./output"},
         }

_empty_row = {'activate': True,
              'data': copy.deepcopy(_data)}


class TableFileExporter:

    def __init__(self, parent=None, filename=''):
        self.parent = parent
        self.table_ui = parent.ui.h3_table
        self.filename = filename

    def create_dictionary(self):
        '''using the general infos, and the one from each row, this method creates the master
        dictionary that will be saved into a json file'''

        general_infos = self._retrieve_general_infos()
        _row_infos = self._retrieve_row_infos()

    def _get_checkbox_state(self, row=-1, column=-1):
        state = self.table_ui.cellWidget(row, column).children()[1].checkState()
        if state == Qt.Checked:
            return True
        return False

    def _get_item_value(self, row=-1, column=-1):
        item = str(self.table_ui.item(row, column).text())
        return item

    def _get_selected_value(self, row=-1, column=-1):
        widget = self.table_ui.cellWidget(row, column).children()[1]
        return str(widget.currentText())

    def _retrieve_element_infos(self, element='sample', row=-1):
        '''form the given row, and the given element (sample or normalization) will
        retrieve the widgets values'''

        _element_dict = OrderedDict()

        if element == 'sample':
            column = sample_first_column
        else:
            column = normalization_first_column

        runs = self._get_item_value(row=row, column=column)

        column += 1
        background_runs = self._get_item_value(row=row, column=column)

        column += 1
        background_background = self._get_item_value(row=row, column=column)

        column += 1
        material = self._get_item_value(row=row, column=column)

        column += 1
        mass_density = self._get_item_value(row=row, column=column)

        column += 1
        packing_fraction =  self._get_item_value(row=row, column=6)

        column += 1
        shape = self._get_selected_value(row=row, column=column)

        column += 1
        radius = self._get_item_value(row=row, column=column)

        column += 1
        radius2 = self._get_item_value(row=row, column=column)

        column += 1
        height = self._get_item_value(row=row, column=column)

        column += 1
        abs_correction = self._get_selected_value(row=row, column=column)

        column += 1
        multiple_scattering_correction = self._get_selected_value(row=row, column=column)

        column += 1
        inelastic_correction = self._get_selected_value(row=row,column=column)
        #if inelastic_correction.lower() == 'placzek':

        # retrieve the key according to row
        o_util = Utilities(parent=self.parent)
        key = o_util.get_row_key_from_row_index(row=row)

        # for debugging and testing, printing the value of title of this key/row
        master_table_list_ui = self.parent.master_table_list_ui
        widget = master_table_list_ui[key]['title']
        print("row: {} has a title of: {}".format(row, str(widget.text())))


        # order
        # self
        # interference
        # fit_spectrum_width
        # lambda_binning_for_fit
        # lambda_binning_for_calc
        #
        # input_grouping
        # output_grouping

        # if row==0:
        #     print(" activate: {}".format(activate))
        #     print(" title: {}".format(title))
        #     print(" runs: {}".format(runs))
        #     print(" background_runs: {}".format(background_runs))
        #     print(" background_background: {}".format(background_background))
        #     print(" material: {}".format(material))
        #     print(" packing_fraction: {}".format(packing_fraction))
        #     print(" shape: {}".format(shape))



        _element_dict['Runs'] = None
        _element_dict['Background'] = OrderedDict()
        _element_dict['Background']['Runs'] = None
        _element_dict['Background']['Background'] = None
        _element_dict['Material'] = None
        #FIXME




        return _element_dict

    def _retrieve_row_infos(self):
        '''this method retrieves the infos from the table using the master_table_list_ui'''

        full_export_dictionary = OrderedDict()
        nbr_row = self.table_ui.rowCount()
        #master_table_list_ui = self.parent.master_table_list_ui

        #index = 0
        for _row in np.arange(nbr_row):

            activate = self._get_checkbox_state(row=_row, column=0)
            title = self._get_item_value(row=_row, column=1)
            _export_dictionary_sample = self._retrieve_element_infos(element='sample',
                                                                        row=_row)
            _export_dictionary_normalization = self._retrieve_element_infos(element='normalization',
                                                                            row=_row)

            full_export_dictionary[_row] = {'sample': _export_dictionary_sample,
                                             'normalization': _export_dictionary_normalization}

        return full_export_dictionary







    def _retrieve_general_infos(self):
        '''this method collects the general information (such as facility, instrument'''

        facility = self.parent.facility
        instrument = self.parent.instrument["short_name"]
        cachedir = self.parent.cache_folder
        outputdir = self.parent.output_folder

        return {'facility': facility,
                'instrument': instrument,
                'cachedir': cachedir,
                'outputdir': outputdir}




