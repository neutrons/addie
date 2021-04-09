from __future__ import (absolute_import, division, print_function)
import numpy as np


class DataToImportHandler:

    def __init__(self, parent=None):
        self.parent = parent

    def is_with_filter(self):
        if self.parent.ui.toolBox.currentIndex() == 0:
            return False
        return True

    def get_runs_from_row_number(self, list_of_rows_to_load):
        """looking at the tablewidget of all runs, this method will return the equivalent run numbers of the
        equivalent list of rows
        """
        list_of_runs = []
        for _row in list_of_rows_to_load:
            _run_for_row = str(self.parent.ui.tableWidget_all_runs.item(_row, 0).text())
            list_of_runs.append(_run_for_row)
        return list_of_runs

    def isolate_runs_from_json(self, json=None, list_of_runs=[]):
        clean_json_list = []
        for _entry in json:
            _run = str(_entry["indexed"]["run_number"])
            if _run in list_of_runs:
                clean_json_list.append(_entry)
        return clean_json_list

    def get_json_of_data_to_import(self):
        if self.is_with_filter():
            # work only with filtered runs
            list_of_rows_to_load = list(self.parent.list_of_rows_with_global_rule)
        elif self.parent.ui.name_search.text() is not None or self.parent.ui.name_search.text() != "":
            list_of_rows_to_load = self.parent.list_row_to_show
        else:
            # work with entire stack of runs
            nbr_rows = self.parent.ui.tableWidget_all_runs.rowCount()
            list_of_rows_to_load = np.arange(nbr_rows)

        list_of_runs = self.get_runs_from_row_number(list_of_rows_to_load)

        nexus_json_to_import = self.isolate_runs_from_json(json=self.parent.nexus_json_all_infos,
                                                           list_of_runs=list_of_runs)

        return nexus_json_to_import
