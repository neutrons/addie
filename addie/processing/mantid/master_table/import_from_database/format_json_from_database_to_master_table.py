from __future__ import (absolute_import, division, print_function)

import collections

from addie.processing.mantid.master_table.master_table_loader import FormatAsciiList
from addie.utilities.list_runs_parser import ListRunsParser
from addie.utilities.general import json_extractor

LIST_OF_METADATA_TO_CHECK = {"Mass Density": ["metadata", "entry", "sample", "mass_density"],
                             "Sample Env. Device": ["metadata", "entry", "daslogs", "bl1b:se:sampletemp",
                                                    "device_name"],
                             "Chemical Formula": ["metadata", "entry", "sample", "chemical_formula"],
                             "Geometry": ["metadata", "entry", "sample", "container_name"]}


class FormatJsonFromDatabaseToMasterTable:

    # list of runs and title simply retrieved from the input json
    list_of_runs = []
    list_of_title = []

    # list of runs and title after combining the title according to option selected
    final_list_of_runs = []
    final_list_of_title = []

    # json
    json = None  # list of json returned from ONCat
    reformated_json = None  # dictionary where key is run number and value is the appropriate json
    final_json = None
    """ dictionary of runs, with title and list of json for those runs
                        {'1-3'; {'list_of_json': [json1, json2, json3],
                                 'title': "this is title of 1-3"},
                          ..., }
    """

    any_conflict = False

    def __init__(self, parent=None):
        self.parent = parent

    def run(self, json=None, import_option=1):
        if json is None:
            return

        # isolate runs and titles
        self._isolate_runs_and_title(json=json)

        # create new json dictionary where the key is the run number and the value is the json item
        self._reformat_json(json=json)

        # combine according to option selected
        self._apply_loading_options(option=import_option)

        # making final json
        self._make_final_json()

    def _isolate_runs_and_title(self, json=None):
        """isolate the list of runs and title from the list of json returned by ONCat"""
        list_of_runs = []
        list_of_title = []

        for _entry in json:
            run = str(_entry["indexed"]["run_number"])
            title = str(_entry["metadata"]["entry"]["title"])
            list_of_runs.append(run)
            list_of_title.append(title)

        self.list_of_runs = list_of_runs
        self.list_of_title = list_of_title

    def _apply_loading_options(self, option=1):
        """using the ascii options, create the final list of runs and titles"""
        list_of_runs = self.list_of_runs
        list_of_title = self.list_of_title

        o_format = FormatAsciiList(list1=list_of_runs,
                                   list2=list_of_title)
        o_format.apply_option(option=option)

        self.final_list_of_runs = o_format.new_list1
        self.final_list_of_title = o_format.new_list2

    def _reformat_json(self, json=None):
        new_json = collections.OrderedDict()

        for _entry in json:
            run_number = _entry["indexed"]["run_number"]
            new_json[str(run_number)] = _entry

        self.reformated_json = new_json

    @staticmethod
    def check_conflict(list_json):
        """this method will check if all the metadata of interest are identical. If they are not,
        the method will return False"""

        o_conflict = ConflictHandler(list_json=list_json)
        is_conflict = o_conflict.is_conflict
        conflict = o_conflict.conflict

        return [is_conflict, conflict]

    def _create_resolved_conflict_dictionary(self, json=None):
        mass_density = str(json_extractor(json, LIST_OF_METADATA_TO_CHECK["Mass Density"]))
        sample_env_device = str(json_extractor(json, LIST_OF_METADATA_TO_CHECK["Sample Env. Device"]))
        chemical_formula = str(json_extractor(json, LIST_OF_METADATA_TO_CHECK["Chemical Formula"]))
        geometry = str(json_extractor(json, LIST_OF_METADATA_TO_CHECK["Geometry"]))

        return {'chemical_formula': chemical_formula,
                'geometry': geometry,
                'mass_density': mass_density,
                'sample_env_device': sample_env_device}

    def _make_final_json(self):
        """if runs are group together, those runs are regroup and final list of json is created"""
        json = self.reformated_json
        list_of_runs = self.final_list_of_runs
        list_of_title = self.final_list_of_title

        final_json = {}
        for _index, _combine_run in enumerate(list_of_runs):

            # get discrete list of the runs to isolate their json
            o_parser = ListRunsParser(current_runs=_combine_run)
            discrete_list_of_runs = o_parser.list_current_runs
            discrete_list_of_runs.sort()  # make sure the runs are in ascending order

            list_of_json_for_this_combine_run = []
            for _individual_run in discrete_list_of_runs:
                list_of_json_for_this_combine_run.append(json[str(_individual_run)])

            final_json[_combine_run] = {}
            final_json[_combine_run]['list_of_json'] = list_of_json_for_this_combine_run
            final_json[_combine_run]['title'] = list_of_title[_index]

            [is_conflict, conflict] = \
                FormatJsonFromDatabaseToMasterTable.check_conflict(list_of_json_for_this_combine_run)
            final_json[_combine_run]['any_conflict'] = is_conflict
            final_json[_combine_run]['conflict_dict'] = conflict

            if is_conflict:
                self.any_conflict = True
            else:
                # put inside a "resolved_conflict" key the result of the none conflicts values
                resolved_conflict = self._create_resolved_conflict_dictionary(json=list_of_json_for_this_combine_run[0])
                final_json[_combine_run]['resolved_conflict'] = resolved_conflict

        # final_json = {'1,2,5-10': {'list_of_json': [json1, json2, json5, json6, json7, ... json10],
        #                            'title': "title_1_1,2,5-10'},
        #               '20-30': {'list_of_json': [...',
        #                         'title': "title_20-30"},
        #               .... }

        self.final_json = final_json


class ConflictHandler:

    # LIST_OF_METADATA_TO_CHECK = {"Mass Density": ["metadata", "entry", "sample", "mass_density"],
    #                              "Sample Env. Device": ["metadata", "entry", "daslogs", "bl1b:se:sampletemp",
    #                                                     "device_name"],
    #                              "Chemical Formula": ["metadata", "entry", "sample", "chemical_formula"],
    #                              "Geometry": ["metadata", "entry", "sample", "container_name"]}

    run_number_path = ["indexed", "run_number"]

    is_conflict = False  # inform if there is a conflict or not
    conflict = {}
    """ this dictionary will inform of the conflict as defined here
                   # {"1,3-5": {'Sample Env. Device" : "N/A",
                   #            'Geometry": "N/A"},
                   #  "2": {"Sample Env. Device" : "yoyou",
                   #        "Geometry": "yaha"} }
    """

    def __init__(self, list_json=None):
        self.check(list_json)

    def check(self, list_json):
        """Check the conflict by creating a master dictionary defined as followed

        master_dict = {"0": {"Run Number": ["123", "124"],
                             "Sample Env. Device": "device 1",
                             "Geometry": "geometry 1",
                             ... },
                       "1": {"run Number": ["125"],
                             "Sample Env. Device": "device 2",
                             "Geometry": "geometry 1",
                             ... },
                       }
        """
        master_dict = {}
        master_key = 0
        for _json in list_json:
            run_number = str(json_extractor(_json, self.run_number_path))
            mass_density = str(json_extractor(_json, LIST_OF_METADATA_TO_CHECK["Mass Density"]))
            sample_env_device = str(json_extractor(_json, LIST_OF_METADATA_TO_CHECK["Sample Env. Device"]))
            chemical_formula = str(json_extractor(_json, LIST_OF_METADATA_TO_CHECK["Chemical Formula"]))
            geometry = str(json_extractor(_json, LIST_OF_METADATA_TO_CHECK["Geometry"]))

            if master_dict == {}:

                master_dict[master_key] = {"Run Number": [run_number],
                                           "sample_env_device": sample_env_device,
                                           "mass_density": mass_density,
                                           "chemical_formula": chemical_formula,
                                           "geometry": geometry}

            else:

                for _key in master_dict.keys():

                    if (mass_density == master_dict[_key]["mass_density"]) and \
                        (sample_env_device == master_dict[_key]["sample_env_device"]) and \
                        (chemical_formula == master_dict[_key]["chemical_formula"]) and \
                            (geometry == master_dict[_key]["geometry"]):
                        master_dict[_key]["Run Number"].append(run_number)
                        break
                else:
                    # we found a conflict
                    master_key += 1
                    master_dict[master_key] = {"Run Number": [run_number],
                                               "sample_env_device": sample_env_device,
                                               "mass_density": mass_density,
                                               "chemical_formula": chemical_formula,
                                               "geometry": geometry}
                    self.is_conflict = True

        self.conflict = master_dict
