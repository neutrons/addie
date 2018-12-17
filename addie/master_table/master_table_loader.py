import os
import numpy as np
from collections import OrderedDict
import copy

try:
    from PyQt4 import QtCore, QtGui
    from PyQt4.QtGui import QDialog
except ImportError:
    try:
        from PyQt5 import QtCore, QtGui
        from PyQt5.QtWidgets import QDialog
    except ImportError:
        raise ImportError("Requires PyQt4 or PyQt5")

from addie.utilities.file_handler import FileHandler
from addie.utilities.list_runs_parser import ListRunsParser
from addie.master_table.table_row_handler import TableRowHandler

from addie.ui_list_of_scan_loader_dialog import Ui_Dialog as UiDialog

# init test dictionary (to test loader
_dictionary_test = OrderedDict()
_default_empty_row = {"activate": True,
                      "title": "",
                      "sample": {"runs": "",
                                 "background": {"runs": "",
                                                "background": "",
                                                },
                                 "material": "",
                                 "mass_density": "",
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
                                 "mass_density": "",
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

class AsciiLoaderOptions(QDialog):

    def __init__(self, parent=None, filename=''):
        self.parent = parent
        self.filename = filename
        QDialog.__init__(self, parent=parent)
        self.ui = UiDialog()
        self.ui.setupUi(self)
        self.init_widgets()

        short_filename = os.path.basename(filename)
        self.setWindowTitle("Options to load {}".format(short_filename))

        self.parent.ascii_loader_option = None

    def init_widgets(self):
        self.radio_button_changed()

    def __get_option_selected(self):
        if self.ui.option1.isChecked():
            return 1
        elif self.ui.option2.isChecked():
            return 2
        elif self.ui.option3.isChecked():
            return 3
        else:
            return 4

    def radio_button_changed(self):
        option_selected = self.__get_option_selected()
        image = ":/preview/load_csv_case{}.png".format(option_selected)
        self.ui.preview_label.setPixmap(QtGui.QPixmap(image))

    def accept(self):
        self.parent.ascii_loader_option = self.__get_option_selected()
        self.parent._load_ascii(filename=self.filename)
        self.close()


class AsciiLoader:

    filename = ''
    file_contain = [] # raw file contain
    table_dictionary = {}

    def __init__(self, parent=None, filename=''):
        self.filename = filename
        self.parent = parent

    def show_dialog(self):
        o_dialog = AsciiLoaderOptions(parent=self.parent, filename=self.filename)
        o_dialog.show()

    def load(self):
        # options selected by user
        options = self.parent.ascii_loader_option
        if options is None:
            return

        filename = self.filename
        o_file = FileHandler(filename=filename)
        o_table = o_file.pandas_parser()

        list_runs = o_table['#Scan']
        list_titles = o_table['title']

        o_format = FormatAsciiList(list1=list_runs,
                                   list2=list_titles)
        # option 1
        # keep raw title and merge lines with exact same title
        if options == 1:
            o_format.option1()

        # option 2
        # remove temperature part of title and merge lines with exact same title
        elif options == 2:
            o_format.option2()
        # option 3
        # keep raw title, append run number
        elif options == 3:
            o_format.option3()

        # option 4
        # take raw title, remove temperature part, add run number
        elif options == 4:
            o_format.option4()

        else:
            raise ValueError("Options nos implemented yet!")

        list_runs = o_format.new_list1
        list_titles = o_format.new_list2

        _table_dictionary = {}
        runs_titles = zip(list_runs, list_titles)
        _index = 0
        for [_run, _title] in runs_titles:
            _entry = copy.deepcopy(_default_empty_row)
            _entry['title'] = str(_title)
            _entry['sample']['runs'] = str(_run)
            _table_dictionary[_index] = _entry
            _index += 1

        self.table_dictionary = _table_dictionary
        self.parent.ascii_loader_dictionary = _table_dictionary

        o_table_ui_loader = FromDictionaryToTableUi(parent=self.parent)
        o_table_ui_loader.fill(input_dictionary=_table_dictionary)

        self.parent.ui.statusbar.setStyleSheet("color: blue")
        self.parent.ui.statusbar.showMessage("File {} has been imported".format(self.filename),
                                            self.parent.statusbar_display_time)


class FormatAsciiList:
    ''' This class takes 2 list as input. According to the option selected, the list2 will be
    modified. Once it has been modified, if two element are equal, the runs coming from the list1 will
    be combined using a compact version

    ex: list1 = ["1","2","3","4"]
        list2 = ["sampleA at temperature 10C",
                 "sampleA at temperature 5C",
                 "sampleA at temperature 15C",
                 "sampleA at temperature 15C"]

        options1:  keep raw title and merge lines with exact same title
        list1 = ["1", "2", "3,4"]
        list2 = ["sampleA at temperature 10C",
                 "sampleA at temperature 5C",
                 "sampleA at temperature 15C"]

        options2: remove temperature part of title and merge lines with exact same title
        list1 = ["1-4"]
        list2 = ["sampleA"]

        options3: keep raw title, append run number
        list1 = ["1", "2", "3,4"]
        list2 = ["sampleA at temperature 10C_1",
                 "sampleA at temperature 5C_2",
                 "sampleA at temperature 15C_3,4"]

        options4: take raw title, remove temperature part, add run number
        list1 = ["1", "2", "3", "4"]
        list2 = ["sampleA at temperature 10C_1",
                 "sampleA at temperature 5C_2",
                 "sampleA at temperature 15C_3",
                 "sampleA at temperature 15C_4"]
    '''

    new_list1 = []
    new_list2 = []

    def __init__(self, list1=[], list2=[]):
        self.list1 = list1
        self.list2 = list2

    def __combine_identical_elements(self, check_list=[], combine_list=[]):
        '''This method will combine the element of the combine_list according to the
        similitude of the check_list

        for example:
        check_list = ["sampleA", "sampleB", "sampleB"]
        combine_list = ["1", "2", "3"]

        new_check_list = ["sampleA", "sampleB"]
        new_combine_list = ["1", "2,3"]
        '''
        list2 = list(check_list)
        list1 = list(combine_list)

        final_list1 = []
        final_list2 = []
        while (list2):

            element_list2 = list2.pop(0)
            str_element_to_merge = str(list1.pop(0))

            # find all indexes where element_list2 are identical
            indices = [i for i, x in enumerate(list2) if x==element_list2]
            if not (indices == []):

                # remove all element already treated
                for _index in indices:
                    list2[_index] = ''

                clean_list2 = []
                for _entry in list2:
                    if not (_entry == ''):
                        clean_list2.append(_entry)
                list2 = clean_list2

                list_element_to_merge = [str(list1[i]) for i in indices]
                str_element_to_merge += "," + (",".join(list_element_to_merge))
                o_combine = ListRunsParser(current_runs=str_element_to_merge)
                str_element_to_merge = o_combine.new_runs()

                for _index in indices:
                    list1[_index] = ''

                clean_list1 = []
                for _entry in list1:
                    if not (_entry == ''):
                        clean_list1.append(_entry)
                list1 = clean_list1

            final_list2.append(element_list2)
            final_list1.append(str_element_to_merge)

        return [final_list1, final_list2]

    def __keep_string_before(self, list=[], splitter_string=""):
        '''this function will split each element by the given splitter_string and will
        only keep the string before that splitter

        ex:
        list = ["sampleA at temperature 150C", "sampleB at temperature 160C"]
        splitter_string = "at temperature"

        :return
        ["sampleA", "sampleB"]
        '''
        new_list = []
        for _element in list:
            split_element = _element.split(splitter_string)
            element_to_keep = split_element[0].strip()
            new_list.append(element_to_keep)
        return new_list

    def __convert_list_to_combine_version(self, list=[]):
        '''this method is to make sure we are working on the combine version of the list of runs

        examples:
        list = ["1", "2,3,4,5"]

        return:
        ["1", "2-5"]
        '''
        new_list = []
        for _element in list:
            o_parser = ListRunsParser(current_runs=str(_element))
            _combine_element = o_parser.new_runs()
            new_list.append(_combine_element)
        return new_list

    def __append_list1_to_list2(self, list1=[], list2=[]):
        '''will append to the end of each list2 element, the value of the list1, with the same index

        examples:
        list1 = ["1", "2", "3", "4-6"]
        list2 = ["Sample A", "Sample B", "Sample C", "Sample D"]

        :returns
        ["Sample A_1", "Sample B_2", "Sample C_3", "Sample D_4-6"]
        '''
        new_list2 = [_ele2 + "_" + str(_ele1) for _ele1, _ele2 in zip(list1, list2)]

        # new_list2 = []
        # for element1, element2 in zip(list1, list2):
        #     new_list2.append(list2 + "_" + str(element1))

        return new_list2

    def option1(self):
        # keep raw title and merge lines with exact same title
        [self.new_list1, self.new_list2] = self.__combine_identical_elements(check_list=self.list2,
                                                                             combine_list=self.list1)

    def option2(self):
        # remove temperature part of title and merge lines with exact same title
        clean_list2 = self.__keep_string_before(list=self.list2,
                                                splitter_string=" at temperature")
        [self.new_list1, self.new_list2] = self.__combine_identical_elements(check_list=clean_list2,
                                                                             combine_list=self.list1)

    def option3(self):
        # keep raw title, append run number
        combine_list1 = self.__convert_list_to_combine_version(list=self.list1)
        list2_with_run_number = self.__append_list1_to_list2(list1=combine_list1, list2=self.list2)

        [self.new_list1, self.new_list2] = self.__combine_identical_elements(check_list=list2_with_run_number,
                                                                             combine_list=self.list1)

    def option4(self):
        # take raw title, remove temperature part, add run number
        clean_list2 = self.__keep_string_before(list=self.list2,
                                                splitter_string=" at temperature")
        combine_list1 = self.__convert_list_to_combine_version(list=self.list1)
        list2_with_run_number = self.__append_list1_to_list2(list1=combine_list1, list2=clean_list2)

        [self.new_list1, self.new_list2] = self.__combine_identical_elements(check_list=list2_with_run_number,
                                                                             combine_list=self.list1)


class TableFileLoader:
    '''This class will take a table config file and will return a dictionary the program can use to
     populate the table

     For now, this loader will take 2 different file format, the old ascii and a new json file format.
     This json file format will be format used when exporting the table
     '''

    def __init__(self, parent=None, filename=''):
        if not os.path.exists(filename):
            raise IOError("{} does not exist!".format(filename))

        self.parent = parent
        self.filename = filename

    def display_dialog(self):
        # trying to load first using ascii loader
        o_loader = AsciiLoader(parent=self.parent, filename=self.filename)
        o_loader.show_dialog()


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

        for _row_entry in input_dictionary.keys():
            o_table.insert_row(row=_row_entry)
            self.populate_row(row=_row_entry, entry=input_dictionary[_row_entry])

    def __fill_data_type(self, data_type="sample", starting_col=1, row=0, entry={}):

        column=starting_col

        # sample - run
        self.table_ui.item(row, column).setText(entry[data_type]["runs"])

        # sample - background - runs
        column += 1
        self.table_ui.item(row, column).setText(entry[data_type]["background"]["runs"])

        # sample - background - background
        column += 1
        self.table_ui.item(row, column).setText(entry[data_type]["background"]["background"])

        # sample - material
        column += 1
        self.table_ui.item(row, column).setText(entry[data_type]["material"])

        # sample - mass density
        column += 1
        self.table_ui.item(row, column).setText(entry[data_type]["mass_density"])

        # sample - packing_fraction
        column +=1
        self.table_ui.item(row, column).setText(entry[data_type]["packing_fraction"])

        # sample - geometry - shape
        column += 1
        _requested_shape = entry[data_type]["geometry"]["shape"]
        self.__set_combobox(requested_value=_requested_shape, row=row, col=column)

        # sample - geometry - radius
        column += 1
        self.table_ui.item(row, column).setText(entry[data_type]["geometry"]["radius_cm"])

        # sample - geometry - height
        column += 1
        self.table_ui.item(row, column).setText(entry[data_type]["geometry"]["height_cm"])

        # abs correction
        column += 1
        _requested_correction = entry[data_type]["abs_correction"]
        self.__set_combobox(requested_value=_requested_correction, row=row, col=column)

        # multi scattering correction
        column += 1
        _requested_scattering = entry[data_type]["multi_scattering_correction"]
        self.__set_combobox(requested_value=_requested_scattering, row=row, col=column)

        # inelastic correction
        column += 1
        _requested_inelastic = entry[data_type]["inelastic_correction"]
        self.__set_combobox(requested_value=_requested_inelastic, row=row, col=column)

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
        self.__fill_data_type(data_type='normalization', starting_col=14, row=row, entry=entry )





