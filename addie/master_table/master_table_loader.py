import os

from collections import OrderedDict
import copy

try:
    from PyQt4 import QtCore
except ImportError:
    try:
        from PyQt5 import QtCore
    except ImportError:
        raise ImportError("Requires PyQt4 or PyQt5")

from addie.master_table.table_row_handler import TableRowHandler

# init test dictionary (to test loader
_dictionary_test = OrderedDict()
_default_empty_row = {"activate": True,
                      "title": "",
                      "sample": {"runs": "",
                                 "background": {"runs": "",
                                                "background": "",
                                                },
                                 "material": "",
                                 "packing_fraction": "",
                                 "geometry": {"shape": "cylindrical",
                                              "radius_cm": "",
                                              "height_cm": "",
                                              },
                                 "abs_correction": "",
                                 "multi_scattering_correction": "",
                                 "inelastic_correction": ""},
                      "normalization": {"runs": "",
                                 "background": {"runs": "",
                                                "background": "",
                                                },
                                 "material": "",
                                 "packing_fraction": "",
                                 "geometry": {"shape": "cylindrical",
                                              "radius_cm": "",
                                              "height_cm": "",
                                              },
                                 "abs_correction": "",
                                 "multi_scattering_correction": "",
                                 "inelastic_correction": ""},
                      "input_grouping": "",
                      "output_grouping": "",
                      }
# for debugging, faking a 2 row dictionary
# _dictionary_test[0] = copy.deepcopy(_default_empty_row)
# _dictionary_test[0]["activate"] = False
# _dictionary_test[0]["title"] = "this is row 0"
# _dictionary_test[0]["sample"]["run"] = "1,2,3,4,5"
# _dictionary_test[0]["sample"]["background"]["runs"] = "10,20"
# _dictionary_test[0]["sample"]["background"]["background"] = "100:300"
# _dictionary_test[0]["sample"]["material"] = "material 1"
# _dictionary_test[0]["sample"]["packing_fraction"] = "fraction 1"
# _dictionary_test[0]["sample"]["geometry"]["shape"] = "spherical"
# _dictionary_test[0]["sample"]["geometry"]["radius_cm"] = "5"
# _dictionary_test[0]["sample"]["geometry"]["height_cm"] = "15"
# _dictionary_test[0]["sample"]["abs_correction"] = "Monte Carlo"
# _dictionary_test[0]["sample"]["multi_scattering_correction"] = "None"
# _dictionary_test[0]["sample"]["inelastic_correction"] = "Placzek"
#
# _dictionary_test[1] = copy.deepcopy(_default_empty_row)

class TableFileLoader:
    '''This class will take a table config file and will return a dictionary the program can use to
     populate the table

     For now, this loader will take 2 different file format, the old ascii and a new json file format.
     This json file format will be format used when exporting the table
     '''

    def __init__(self, parent=None, filename=''):
        if not os.path.exists(filename):
            raise IOError("{} does not exist!".format(filename))





class FromDictionaryToTableUi:
    '''This class will take a dictionary especially designed for the master table to fill all the rows and cells'''

    def __init__(self, parent=None):
        self.parent = parent
        self.table_ui = self.parent.ui.h3_table

    def fill(self, input_dictionary={}):
        if input_dictionary == {}:
            # # use for debugging
            # input_dictionary = _dictionary_test
            return

        o_table = TableRowHandler(parent=self.parent)

        for _row_entry in _dictionary_test.keys():
            o_table.insert_row(row=_row_entry)
            self.populate_row(row=_row_entry, entry=_dictionary_test[_row_entry])

    def __fill_data_type(self, data_type="sample", starting_col=1, row=0, entry={}):

        col=starting_col

        # sample - run
        self.table_ui.item(row, col).setText(entry[data_type]["runs"])

        # sample - background - runs
        self.table_ui.item(row, col+1).setText(entry[data_type]["background"]["runs"])

        # sample - background - background
        self.table_ui.item(row, col+2).setText(entry[data_type]["background"]["background"])

        # sample - material
        self.table_ui.item(row, col+3).setText(entry[data_type]["material"])

        # sample - packing_fraction
        self.table_ui.item(row, col+4).setText(entry[data_type]["packing_fraction"])

        # sample - geometry - shape
        _requested_shape = entry[data_type]["geometry"]["shape"]
        self.__set_combobox(requested_value=_requested_shape, row=row, col=col+5)

        # sample - geometry - radius
        self.table_ui.item(row, col+6).setText(entry[data_type]["geometry"]["radius_cm"])

        # sample - geometry - height
        self.table_ui.item(row, col+7).setText(entry[data_type]["geometry"]["height_cm"])

        # abs correction
        _requested_correction = entry[data_type]["abs_correction"]
        self.__set_combobox(requested_value=_requested_correction, row=row, col=col+8)

        # multi scattering correction
        _requested_scattering = entry[data_type]["multi_scattering_correction"]
        self.__set_combobox(requested_value=_requested_scattering, row=row, col=col+9)

        # inelastic correction
        _requested_inelastic = entry[data_type]["inelastic_correction"]
        self.__set_combobox(requested_value=_requested_inelastic, row=row, col=col+10)

    def __set_combobox(self, requested_value="", row=-1, col=-1):
        _widget = self.table_ui.cellWidget(row, col).children()[1]
        _index = _widget.findText(requested_value)
        _widget.setCurrentIndex(_index)

    def populate_row(self, row=-1, entry=None):

        # activate
        _status = QtCore.Qt.Checked if entry["activate"] else QtCore.Qt.Unchecked
        _widget = self.table_ui.cellWidget(row, 0).children()[1]
        _widget.setCheckState(_status)

        # title
        self.table_ui.item(row, 1).setText(entry["title"])

        # sample
        self.__fill_data_type(data_type='sample', starting_col=2, row=row, entry=entry )

        # normalization
        self.__fill_data_type(data_type='normalization', starting_col=13, row=row, entry=entry )





