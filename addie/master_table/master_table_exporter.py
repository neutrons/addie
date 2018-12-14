from collections import OrderedDict
import copy
import numpy as np

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
        '''this method collects the general information (such as facility, instrument) as well as
        the data from each row'''

        # general infos
        facility = self.parent.facility
        instrument = self.parent.instrument["short_name"]
        #cachedir =



        nbr_row = self.table_ui.rowCount()




