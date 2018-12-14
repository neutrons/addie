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

    def _retrieve_element_infos(self, element='sample', row_entry=None):

        _element_dict = OrderedDict()

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
        master_table_list_ui = self.parent.master_table_list_ui

        index = 0
        for _key in master_table_list_ui.keys():

            _row_entry = master_table_list_ui[_key]

            _export_dictionary_sample = self._retrieve_element_infos(element='sample',
                                                                        row_entry=_row_entry)
            _export_dictionary_normalization = self._retrieve_element_infos(element='normalization',
                                                                               row_entry=_row_entry)

            full_export_dictionary[index] = {'sample': _export_dictionary_sample,
                                             'normalization': _export_dictionary_normalization}

        return full_export_dictionary


        # activate = self._get_checkbox_state(row=row, column=0)
        # title = self._get_item_value(row=row, column=1)
        #
        # # sample
        # sample_element = self._retrieve_element_infos(element='sample')
        # runs = self._get_item_value(row=row, column=2)
        # background_runs = self._get_item_value(row=row, column=3)
        # background_background = self._get_item_value(row=row, column=4)
        # material = self._get_item_value(row=row, column=5)
        # packing_fraction =  self._get_item_value(row=row, column=6)
        # shape = self._get_selected_value(row=row, column=7)
        # radius = self._get_item_value(row=row, column=8)
        # height = self._get_item_value(row=row, column=9)
        # abs_correction = self._get_selected_value(row=row,column=10)
        # multiple_scattering_correction = self._get_selected_value(row=row, column=11)
        # inelastic_correction = self._get_selected_value(row=row,column=12)
        # if inelastic_correction.lower() == 'placzek':
        #     pass
        #order
        #self
        #interference
        #fit_spectrum_width
        #lambda_binning_for_fit
        #lambda_binning_for_calc


        #input_grouping
        #output_grouping

        # if row==0:
        #     print(" activate: {}".format(activate))
        #     print(" title: {}".format(title))
        #     print(" runs: {}".format(runs))
        #     print(" background_runs: {}".format(background_runs))
        #     print(" background_background: {}".format(background_background))
        #     print(" material: {}".format(material))
        #     print(" packing_fraction: {}".format(packing_fraction))




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




