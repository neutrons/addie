from __future__ import (absolute_import, division, print_function)
import os
import numpy as np
from collections import OrderedDict
import copy
import simplejson

from qtpy.QtWidgets import QDialog
from addie.utilities import load_ui
from qtpy import QtCore, QtGui

from addie.utilities.file_handler import FileHandler
from addie.utilities.list_runs_parser import ListRunsParser
from addie.utilities.set import Set
from addie.processing.mantid.master_table.table_row_handler import TableRowHandler
from addie.processing.mantid.master_table.utilities import LoadGroupingFile

# init test dictionary (to test loader)
_dictionary_test = OrderedDict()
_density_dict = {"mass_density": {"value": "N/A",
                                  "selected": True},
                 "number_density": {"value": "N/A",
                                    "selected": False},
                 "mass": {"value": "N/A",
                          "selected": False},
                 }
_default_empty_row = {
    "activate": True,
    "title": "",
    "sample": {
        "runs": "",
        "background": {
            "runs": "",
            "background": "",
        },
        "material": "",
        "density": copy.deepcopy(_density_dict),
        "packing_fraction": "",
        "geometry": {
            "shape": "Cylinder",
            "radius": "N/A",
            "radius2": "N/A",
            "height": "N/A",
        },
        "abs_correction": "",
        "multi_scattering_correction": "",
        "inelastic_correction": {},
        "resonance": {
            "axis": "None",
            "lower": "N/A",
            "upper": "N/A"}
    },
    "normalization": {
        "runs": "",
        "background": {
            "runs": "",
            "background": "",
        },
        "material": "",
        "density": copy.deepcopy(_density_dict),
        "packing_fraction": "",
        "geometry": {
                            "shape": "Cylinder",
                            "radius": "N/A",
                            "radius2": "N/A",
                            "height": "N/A",
        },
        "abs_correction": "",
        "multi_scattering_correction": "",
        "inelastic_correction": "",
        "placzek": {},
    },
    "input_grouping": "",
    "output_grouping": "",
    "AlignAndFocusArgs": {},
    "self_scattering_level": {
        "lower": "",
        "upper": ""
        }
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
# _dictionary_test[0]["sample"]["geometry"]["shape"] = "Sphere"
# _dictionary_test[0]["sample"]["geometry"]["radius_cm"] = "5"
# _dictionary_test[0]["sample"]["geometry"]["height_cm"] = "15"
# _dictionary_test[0]["sample"]["abs_correction"] = "Monte Carlo"
# _dictionary_test[0]["sample"]["multi_scattering_correction"] = "None"
# _dictionary_test[0]["sample"]["inelastic_correction"] = "Placzek"
#
# _dictionary_test[1] = copy.deepcopy(_default_empty_row)


class LoaderOptionsInterface(QDialog):

    real_parent = None

    def __init__(self, parent=None, is_parent_main_ui=True, real_parent=None):
        """
        This class can be called from different level of ui. In the case of the import from database ui,
        real_parent parameter is needed to be able to close this ui and the ui above it as well as running a function
        in the parent ui before closing.

        :param parent:
        :param is_parent_main_ui:
        :param real_parent:
        """

        if is_parent_main_ui:
            self.parent = parent
        else:
            self.real_parent = real_parent
            self.parent = parent.parent

        QDialog.__init__(self, parent=parent)
        self.ui = load_ui('list_of_scan_loader_dialog.ui', baseinstance=self)
        self.init_widgets()
        self.setWindowTitle("Options to load list of runs selected")
        self.parent.ascii_loader_option = None

    def init_widgets(self):
        self.radio_button_changed()

    def get_option_selected(self):
        if self.ui.option1.isChecked():
            return 1
        elif self.ui.option2.isChecked():
            return 2
        elif self.ui.option3.isChecked():
            return 3
        else:
            return 4

    def radio_button_changed(self):
        option_selected = self.get_option_selected()
        image = ":/preview/load_csv_case{}.png".format(option_selected)
        self.ui.preview_label.setPixmap(QtGui.QPixmap(image))


class AsciiLoaderOptionsInterface(LoaderOptionsInterface):

    def __init__(self, parent=None, filename=''):
        self.filename = filename
        self.parent = parent

        QDialog.__init__(self, parent=parent)
        self.ui = load_ui('list_of_scan_loader_dialog.ui', baseinstance=self)
        self.init_widgets()

        short_filename = os.path.basename(filename)
        self.setWindowTitle("Options to load {}".format(short_filename))

        self.parent.ascii_loader_option = None


class AsciiLoaderOptions(AsciiLoaderOptionsInterface):

    def accept(self):
        self.parent.ascii_loader_option = self.get_option_selected()
        self.parent.load_ascii(filename=self.filename)
        self.close()


class JsonLoader:

    filename = ''

    def __init__(self, parent=None, filename=''):
        self.filename = filename
        self.parent = parent

    def _retrieve_element_dict(self, element='Sample', source_row_entry={}):
        _target_row_entry = {}
        _source_entry = source_row_entry[element]

        if 'Runs' in _source_entry:
            _target_row_entry["runs"] = _source_entry['Runs']
        else:
            _target_row_entry["runs"] = ''
        _target_row_entry["background"] = {}
        if 'Background' in _source_entry:
            _target_row_entry["background"]["runs"] = _source_entry['Background']["Runs"]
            if "Background" in _source_entry["Background"]:
                _target_row_entry["background"]["background"] = _source_entry["Background"]["Background"]["Runs"]
            else:
                _target_row_entry["background"]["background"] = ''
        else:
            _target_row_entry["background"]["runs"] = ''
            _target_row_entry["background"]["background"] = ''
        if "Material" in _source_entry:
            _target_row_entry["material"] = _source_entry["Material"]
        else:
            _target_row_entry["material"] = ''
        _target_row_entry["mass_density"] = copy.deepcopy(_density_dict)
        if _source_entry["Density"]["UseMassDensity"]:
            if "MassDensity" in _source_entry["Density"]:
                _target_row_entry["mass_density"]["mass_density"]["value"] = _source_entry["Density"]["MassDensity"]
            else:
                _target_row_entry["mass_density"]["mass_density"]["value"] = "N/A"
            _target_row_entry["mass_density"]["mass_density"]["selected"] = True
        else:
            _target_row_entry["mass_density"]["mass_density"]["value"] = 'N/A'
            _target_row_entry["mass_density"]["mass_density"]["selected"] = False
        if _source_entry["Density"]["UseNumberDensity"]:
            _target_row_entry["mass_density"]["number_density"]["value"] = _source_entry["Density"]["NumberDensity"]
            _target_row_entry["mass_density"]["number_density"]["selected"] = True
        else:
            _target_row_entry["mass_density"]["number_density"]["value"] = 'N/A'
            _target_row_entry["mass_density"]["number_density"]["selected"] = False
        if _source_entry["Density"]["UseMass"]:
            _target_row_entry["mass_density"]["mass"]["value"] = _source_entry["Density"]["Mass"]
            _target_row_entry["mass_density"]["mass"]["selected"] = True
        else:
            _target_row_entry["mass_density"]["mass"]["value"] = 'N/A'
            _target_row_entry["mass_density"]["mass"]["selected"] = False
        if "PackingFraction" in _source_entry:
            _target_row_entry["packing_fraction"] = _source_entry["PackingFraction"]
        else:
            _target_row_entry["packing_fraction"] = ''
        _target_row_entry["geometry"] = {}
        _target_row_entry["geometry"]["shape"] = _source_entry["Geometry"]["Shape"]
        if "Radius" in _source_entry["Geometry"]:
            _target_row_entry["geometry"]["radius"] = _source_entry["Geometry"]["Radius"]
        else:
            _target_row_entry["geometry"]["radius"] = "N/A"

        if "Height" in _source_entry["Geometry"]:
            _target_row_entry["geometry"]["height"] = _source_entry["Geometry"]["Height"]
        else:
            _target_row_entry["geometry"]["height"] = "N/A"
        if "AbsorptionCorrection" in _source_entry:
            _target_row_entry["abs_correction"] = _source_entry["AbsorptionCorrection"]["Type"]
        else:
            _target_row_entry["abs_correction"] = "None"
        if "MultipleScatteringCorrection" in _source_entry:
            _target_row_entry["multi_scattering_correction"] = _source_entry["MultipleScatteringCorrection"]["Type"]
        else:
            _target_row_entry["multi_scattering_correction"] = "None"
        _target_row_entry["inelastic_correction"] = copy.deepcopy(self.parent.placzek_default)
        if "InelasticCorrection" in _source_entry:
            _target_row_entry["inelastic_correction"]["is_self"] = _source_entry["InelasticCorrection"]["Self"]
            _target_row_entry["inelastic_correction"]["is_interference"] = \
                _source_entry["InelasticCorrection"]["Interference"]
            _target_row_entry["inelastic_correction"]["sample_t"] = \
                _source_entry["InelasticCorrection"]["SampleTemperature"]
            _target_row_entry["inelastic_correction"]["fit_spectrum_with"]["text"] = \
                _source_entry["InelasticCorrection"]["FitSpectrumWith"]

            lambda_binning_for_fit = _source_entry["InelasticCorrection"]["LambdaBinningForFit"].split(
                ",")
            if len(lambda_binning_for_fit) == 3:
                _target_row_entry["inelastic_correction"]["lambda_binning_for_fit"]["min"] = lambda_binning_for_fit[0]
                _target_row_entry["inelastic_correction"]["lambda_binning_for_fit"]["delta"] = lambda_binning_for_fit[1]
                _target_row_entry["inelastic_correction"]["lambda_binning_for_fit"]["max"] = lambda_binning_for_fit[2]
            else:
                default_placzek = self.parent.placzek_default["lambda_binning_for_fit"]
                _target_row_entry["inelastic_correction"]["lambda_binning_for_fit"]["min"] = default_placzek["min"]
                _target_row_entry["inelastic_correction"]["lambda_binning_for_fit"]["delta"] = default_placzek["delta"]
                _target_row_entry["inelastic_correction"]["lambda_binning_for_fit"]["max"] = default_placzek["max"]
        else:
            _target_row_entry['inelastic_correction'] = None
        if element == 'Sample':
            _target_row_entry["resonance"] = {}
            if "Resonance" in _source_entry:
                _target_row_entry["resonance"]["axis"] = _source_entry["Resonance"]["Axis"]
                if isinstance(_source_entry["Resonance"]["LowerLimits"], list):
                    lower_tmp = ",".join([str(item) for item in _source_entry["Resonance"]["LowerLimits"]])
                else:
                    lower_tmp = _source_entry["Resonance"]["LowerLimits"]
                if isinstance(_source_entry["Resonance"]["UpperLimits"], list):
                    upper_tmp = ",".join([str(item) for item in _source_entry["Resonance"]["UpperLimits"]])
                else:
                    upper_tmp = _source_entry["Resonance"]["UpperLimits"]
                _target_row_entry["resonance"]["lower"] = lower_tmp
                _target_row_entry["resonance"]["upper"] = upper_tmp

        return _target_row_entry

    def load(self):

        # load json
        with open(self.filename) as f:
            data = simplejson.load(f)

        # convert into UI dictionary
        list_keys = sorted([_key for _key in data.keys()])

        table_dictionary = {}
        first_entry = True
        for _row in list_keys:

            _source_row_entry = data[str(_row)]

            _row = np.int(_row)
            _target_row_entry = copy.deepcopy(_default_empty_row)

            # _target_row_entry["activate"] = _source_row_entry['Activate']
            _target_row_entry["title"] = _source_row_entry['Title']
            _target_row_entry["sample"] = self._retrieve_element_dict(
                element='Sample', source_row_entry=_source_row_entry)
            _target_row_entry["runs"] = _source_row_entry['Sample']['Runs']
            _target_row_entry["normalization"] = self._retrieve_element_dict(
                element='Normalization', source_row_entry=_source_row_entry)

            _target_row_entry["align_and_focus_args"] = _source_row_entry.get(
                "AlignAndFocusArgs", {})

            _target_row_entry["SelfScatteringLevelCorrection"] = _source_row_entry.get(
                "SelfScatteringLevelCorrection", {})

            table_dictionary[_row] = _target_row_entry

            # load general settings of first entry only
            if first_entry:
                o_set = Set(parent=self.parent)

                # short name of instrument (ex: NOM)
                short_instrument_name = str(_source_row_entry['Instrument'])
                o_set.set_instrument(short_name=short_instrument_name)

                # name of facility (not used yet)
                facility = str(_source_row_entry["Facility"])
                self.parent.facility = facility

                # cache and output dir
                cache_folder = str(_source_row_entry["CacheDir"])
                self.parent.cache_folder = cache_folder

                output_dir = str(_source_row_entry["OutputDir"])
                self.parent.output_folder = output_dir

                if "Filename" in _source_row_entry["Calibration"]:
                    calibration_file = str(
                        _source_row_entry["Calibration"]["Filename"])
                else:
                    calibration_file = "N/A"
                self.parent.processing_ui.calibration_file.setText(
                    calibration_file)

                if "Grouping" in _source_row_entry["Merging"]:
                    if "Initial" in _source_row_entry["Merging"]["Grouping"]:
                        intermediate_grouping_file = str(
                            _source_row_entry["Merging"]["Grouping"]["Initial"])
                    else:
                        intermediate_grouping_file = ''
                    if "Output" in _source_row_entry["Merging"]["Grouping"]:
                        output_grouping_file = str(
                            _source_row_entry["Merging"]["Grouping"]["Output"])
                    else:
                        output_grouping_file = ''
                else:
                    intermediate_grouping_file = ''
                    output_grouping_file = ''

                if not (intermediate_grouping_file == ''):
                    self.parent.intermediate_grouping['filename'] = intermediate_grouping_file
                    self.parent.intermediate_grouping['enabled'] = True
                    o_grouping = LoadGroupingFile(
                        filename=intermediate_grouping_file)
                    nbr_groups = o_grouping.get_number_of_groups()
                    self.parent.intermediate_grouping['nbr_groups'] = nbr_groups
                if not (output_grouping_file == ''):
                    self.parent.output_grouping['filename'] = output_grouping_file
                    self.parent.output_grouping['enabled'] = True
                    o_grouping = LoadGroupingFile(
                        filename=output_grouping_file)
                    nbr_groups = o_grouping.get_number_of_groups()
                    self.parent.output_grouping['nbr_groups'] = nbr_groups

                if "AbsMSParameters" in _source_row_entry["Sample"]:
                    ele_size_val = _source_row_entry["Sample"]["AbsMSParameters"]["ElementSize"]
                    if type(ele_size_val) == list:
                        ele_size_val = ",".join([str(item) for item in ele_size_val])
                    else:
                        ele_size_val = str(ele_size_val)
                    self.parent.advanced_dict["ele_size"] = ele_size_val

                first_entry = False

        o_table_ui_loader = FromDictionaryToTableUi(parent=self.parent)
        o_table_ui_loader.fill(input_dictionary=table_dictionary)

        self.parent.ui.statusbar.setStyleSheet("color: blue")
        self.parent.ui.statusbar.showMessage(
            "File {} has been imported".format(
                self.filename), self.parent.statusbar_display_time)


class AsciiLoader:

    filename = ''
    file_contain = []  # raw file contain
    table_dictionary = {}

    def __init__(self, parent=None, filename=''):
        self.filename = filename
        self.parent = parent

    def show_dialog(self):
        o_dialog = AsciiLoaderOptions(
            parent=self.parent, filename=self.filename)
        o_dialog.show()

    def load(self):
        # options selected by user
        options = self.parent.ascii_loader_option
        if options is None:
            return

        filename = self.filename
        o_file = FileHandler(filename=filename)
        o_table = o_file.csv_parser()

        list_runs = o_table['#Scan']
        list_titles = o_table['title']

        o_format = FormatAsciiList(list1=list_runs,
                                   list2=list_titles)
        # option 1
        # keep raw title and merge lines with exact same title
        if options == 1:
            o_format.option1()

        # option 2
        # remove temperature part of title and merge lines with exact same
        # title
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
        self.parent.ui.statusbar.showMessage(
            "File {} has been imported".format(
                self.filename), self.parent.statusbar_display_time)


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
            indices = [i for i, x in enumerate(list2) if x == element_list2]
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
        new_list2 = [_ele2 + "_" + str(_ele1)
                     for _ele1, _ele2 in zip(list1, list2)]

        # new_list2 = []
        # for element1, element2 in zip(list1, list2):
        #     new_list2.append(list2 + "_" + str(element1))

        return new_list2

    def option1(self):
        # keep raw title and merge lines with exact same title
        [self.new_list1, self.new_list2] = self.__combine_identical_elements(
            check_list=self.list2, combine_list=self.list1)

    def option2(self):
        # remove temperature part of title and merge lines with exact same
        # title
        clean_list2 = self.__keep_string_before(
            list=self.list2, splitter_string=" at temperature")
        [self.new_list1, self.new_list2] = self.__combine_identical_elements(
            check_list=clean_list2, combine_list=self.list1)

    def option3(self):
        # keep raw title, append run number
        combine_list1 = self.__convert_list_to_combine_version(list=self.list1)
        list2_with_run_number = self.__append_list1_to_list2(
            list1=combine_list1, list2=self.list2)

        [self.new_list1, self.new_list2] = self.__combine_identical_elements(
            check_list=list2_with_run_number, combine_list=self.list1)

    def option4(self):
        # take raw title, remove temperature part, add run number
        clean_list2 = self.__keep_string_before(
            list=self.list2, splitter_string=" at temperature")
        combine_list1 = self.__convert_list_to_combine_version(list=self.list1)
        list2_with_run_number = self.__append_list1_to_list2(
            list1=combine_list1, list2=clean_list2)

        [self.new_list1, self.new_list2] = self.__combine_identical_elements(
            check_list=list2_with_run_number, combine_list=self.list1)

    def apply_option(self, option=1):
        if option == 1:
            return self.option1()
        elif option == 2:
            return self.option2()
        elif option == 3:
            return self.option3()
        elif option == 4:
            return self.option4()
        else:
            raise NotImplementedError


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
        self.init_raw_dict()

    def init_raw_dict(self):
        _default_empty_row['sample']['inelastic_correction'] = self.parent.placzek_default
        _default_empty_row['normalization']['inelastic_correction'] = self.parent.placzek_default

    def display_dialog(self):

        try:
            # if extension is csv, use ascii loader
            if FileHandler.is_file_correct_extension(
                    filename=self.filename, ext_requested='csv'):  # ascii file
                o_loader = AsciiLoader(
                    parent=self.parent, filename=self.filename)
                o_loader.show_dialog()
            # json file
            elif FileHandler.is_file_correct_extension(filename=self.filename, ext_requested='json'):
                o_loader = JsonLoader(
                    parent=self.parent, filename=self.filename)
                o_loader.load()
            else:
                raise IOError(
                    "File format not supported for {}!".format(
                        self.filename))

            self.parent.check_master_table_column_highlighting()

        except ValueError:
            self.parent.ui.statusbar.setStyleSheet("color: red")
            self.parent.ui.statusbar.showMessage(
                "Unable to load configuration file {}!".format(
                    self.filename), self.parent.statusbar_display_time)
        except TypeError:
            self.parent.ui.statusbar.setStyleSheet("color: red")
            self.parent.ui.statusbar.showMessage(
                "Error while trying to load file {}!".format(
                    self.filename), self.parent.statusbar_display_time)


class FromDictionaryToTableUi:
    '''This class will take a dictionary especially designed for the master table to fill all the rows and cells'''

    def __init__(self, parent=None):
        self.parent = parent
        self.table_ui = self.parent.processing_ui.h3_table

    def fill(self, input_dictionary={}):

        if input_dictionary == {}:
            # # use for debugging
            # input_dictionary = _dictionary_test
            return

        o_table = TableRowHandler(main_window=self.parent)

        for _row_entry in input_dictionary.keys():

            # insert row but also initialize the hidden arguments such as
            # placzek settings
            o_table.insert_row(
                row=_row_entry,
                align_and_focus_args=input_dictionary[_row_entry]['align_and_focus_args'],
                normalization_placzek_arguments=input_dictionary[_row_entry]['normalization']['inelastic_correction'],
                sample_placzek_arguments=input_dictionary[_row_entry]['sample']['inelastic_correction'])

            self.populate_row(row=_row_entry,
                              entry=input_dictionary[_row_entry],
                              key=o_table.key)

    def __fill_data_type(
            self,
            data_type="sample",
            starting_col=1,
            row=0,
            entry={},
            key=None):

        column = starting_col
        #print("ran")
        # run
        #print(self.table_ui.item(row,column))
        self.table_ui.item(row, column).setText(entry[data_type]["runs"])

        # background - runs
        column += 1
        self.table_ui.item(
            row, column).setText(
            entry[data_type]["background"]["runs"])

        # background - background
        column += 1
        self.table_ui.item(
            row, column).setText(
            entry[data_type]["background"]["background"])

        # material
        column += 1
        self.parent.master_table_list_ui[key][data_type]['material']['text'].setText(
            entry[data_type]["material"])

        # mass density
        column += 1
        self.parent.master_table_list_ui[key][data_type]['mass_density']['text'].setText(
            entry[data_type]["mass_density"]["mass_density"]["value"])

        # packing_fraction
        column += 1
        self.table_ui.item(
            row, column).setText(str(entry[data_type]["packing_fraction"]))

        # geometry - shape
        column += 1
        _requested_shape = entry[data_type]["geometry"]["shape"]
        self.__set_combobox(
            requested_value=_requested_shape,
            row=row,
            col=column)

        # geometry
        column += 1
        self.parent.master_table_list_ui[key][data_type]['geometry']['radius']['value'].setText(
            str(entry[data_type]['geometry']['radius']))
        self.parent.master_table_list_ui[key][data_type]['geometry']['height']['value'].setText(
            str(entry[data_type]['geometry']['height']))

        # abs correction
        column += 1
        _requested_correction = entry[data_type]["abs_correction"]
        self.__set_combobox(
            requested_value=_requested_correction,
            row=row,
            col=column)

        # multi scattering correction
        column += 1
        _requested_scattering = entry[data_type]["multi_scattering_correction"]
        self.__set_combobox(
            requested_value=_requested_scattering,
            row=row,
            col=column)

        # inelastic correction
        column += 1
        _requested_inelastic = entry[data_type]["inelastic_correction"]
        if _requested_inelastic is not None:
            _requested_inelastic = "Placzek"
        else:
            _requested_inelastic = "None"
        self.__set_combobox(
            requested_value=_requested_inelastic,
            row=row,
            col=column)
        #print(entry[data_type])
        #resonance filter
        try:
            if data_type == "sample":
                column += 1
                if 'resonance' in entry[data_type].keys():
                    text1_tmp = str(entry[data_type]['resonance']['axis'])
                    text2_tmp = str(entry[data_type]['resonance']['lower'])
                    text3_tmp = str(entry[data_type]['resonance']['upper'])
                else:
                    text1_tmp = 'N/A'
                    text2_tmp = 'N/A'
                    text3_tmp = 'N/A'
                self.parent.master_table_list_ui[key][data_type]['resonance']['axis']['value'].setText(text1_tmp)
                self.parent.master_table_list_ui[key][data_type]['resonance']['lower']['value'].setText(text2_tmp)
                self.parent.master_table_list_ui[key][data_type]['resonance']['upper']['value'].setText(text3_tmp)
                if text2_tmp == 'N/A':
                    self.parent.master_table_list_ui[key][data_type]['resonance']['lower']['lim_list'] = []
                else:
                    list_tmp = list(map(float, text2_tmp.split(",")))
                    self.parent.master_table_list_ui[key][data_type]['resonance']['lower']['lim_list'] = list_tmp
                if text3_tmp == "N/A":
                    self.parent.master_table_list_ui[key][data_type]['resonance']['upper']['lim_list'] = []
                else:
                    list_tmp = list(map(float, text3_tmp.split(",")))
                    self.parent.master_table_list_ui[key][data_type]['resonance']['upper']['lim_list'] = list_tmp
        except:
            pass

    def __set_combobox(self, requested_value="", row=-1, col=-1):
        _widget = self.table_ui.cellWidget(row, col).children()[1]
        _index = _widget.findText(requested_value)
        if _index == -1:
            _index = 0
        _widget.setCurrentIndex(_index)

    def populate_row(self, row=-1, entry=None, key=None):

        # activate
        _status = QtCore.Qt.Checked if entry["activate"] else QtCore.Qt.Unchecked
        _widget = self.table_ui.cellWidget(row, 0).children()[1]
        _widget.setCheckState(_status)

        # title
        self.table_ui.item(row, 1).setText(entry["title"])

        # sample
        self.__fill_data_type(
            data_type='sample',
            starting_col=2,
            row=row,
            entry=entry,
            key=key)

        # normalization
        self.__fill_data_type(
            data_type='normalization',
            starting_col=14,
            row=row,
            entry=entry,
            key=key)

        if "SelfScatteringLevelCorrection" in entry.keys():
            if entry["SelfScatteringLevelCorrection"]:
                lower_list = []
                upper_list = []
                for i in range(6):
                    key_tmp = "Bank" + str(i + 1)
                    lower_list.append(entry["SelfScatteringLevelCorrection"][key_tmp][0])
                    upper_list.append(entry["SelfScatteringLevelCorrection"][key_tmp][1])
                lower_text = ",".join(list(map(str, lower_list)))
                upper_text = ",".join(list(map(str, upper_list)))
            else:
                lower_list = []
                upper_list = []
                lower_text = ""
                upper_text = ""
        else:
            lower_list = []
            upper_list = []
            lower_text = ""
            upper_text = ""

        self.parent.master_table_list_ui[key]["self_scattering_level"]["lower"]["value"].setText(lower_text)
        self.parent.master_table_list_ui[key]["self_scattering_level"]["upper"]["value"].setText(upper_text)
        self.parent.master_table_list_ui[key]["self_scattering_level"]["lower"]["val_list"] = lower_list
        self.parent.master_table_list_ui[key]["self_scattering_level"]["upper"]["val_list"] = upper_list
