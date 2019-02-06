import collections

from addie.master_table.master_table_loader import FormatAsciiList
from addie.utilities.list_runs_parser import ListRunsParser


class MasterTableLoaderFromDatabaseUi:

    # list of runs and title simply retrieved from the input json
    list_of_runs = []
    list_of_title = []

    # list of runs and title after combining the title according to option selected
    final_list_of_runs = []
    final_list_of_title = []

    # json
    json = None  # list of json returned from ONCat
    reformated_json = None  # dictionary where key is run number and value is the appropriate json

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
            new_json[run_number] = _entry

        self.reformated_json = new_json

    def _make_final_json(self):
        """if runs are group together, those runs are regroup and final list of json is created"""
        json = self.json
        list_of_runs = self.final_list_of_runs
        list_of_title = self.final_list_of_title

        import pprint

        final_json = []
        for _index, _run in enumerate(list_of_runs):

            # get discrete list of the runs to isolate their json
            o_parser = ListRunsParser(current_runs=_run)
            discrete_list_of_runs = o_parser.list_current_runs
            discrete_list_of_runs.sort() # make sure the runs are in ascending order

            pprint.pprint("from {} to {}".format(_run, discrete_list_of_runs))
