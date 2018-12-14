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

        nbr_row = self.table_ui.rowCount()
        for _row in np.arange(nbr_row):
            _row_infos = self._retrieve_row_infos(row=_row)


    def _get_checkbox_state(self, row=-1, column=-1):
        state = self.table_ui.cellWidget(row, column).children()[1].checkState()
        if state == Qt.Checked:
            return True
        return False

    def _get_item_value(self, row=-1, column=-1):
        item = str(self.table_ui.item(row, column).text())
        return item

    def _retrieve_row_infos(self, row=-1):
        '''this method retrieves the infos for the given row'''

        activate = self._get_checkbox_state(row=row, column=0)
        title = self._get_item_value(row=row, column=1)



        print("activate: {}".format(activate))
        print("title: {}".format(title))




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




