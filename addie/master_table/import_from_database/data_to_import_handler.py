import numpy as np


class DataToImportHandler:

    def __init__(self, parent=None):
        self.parent = parent

    def is_with_filter(self):
        if self.parent.ui.toolBox.currentIndex() == 0:
            return False
        return True

    def get_table_of_data_to_import(self):

        import pprint

        if self.is_with_filter():
            # work only with filtered runs
            list_of_rows_to_load = list(self.parent.list_of_rows_with_global_rule)

        else:
            # work with entire stack of runs
            nbr_rows = self.parent.ui.tableWidget_all_runs.rowCount()
            list_of_rows_to_load = np.arange(nbr_rows)


        pprint.pprint(list_of_rows_to_load)
        pprint.pprint(list_of_rows_to_load[0])
