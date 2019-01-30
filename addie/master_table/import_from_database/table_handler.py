import numpy as np


class TableHandler:

    def __init__(self, table_ui=None):
        self.table_ui = table_ui

    def show_all_rows(self):
        self.set_row_visibility(visibility=True, all_rows=True)

    def hide_all_rows(self):
        self.set_row_visibility(visibility=False, all_rows=True)

    def set_row_visibility(self, visibility=True, list_of_rows=[], all_rows=False):
        if all_rows:
            list_of_rows = np.arange(self.table_ui.rowCount())

        for _row in list_of_rows:
            self.table_ui.setRowHidden(_row, not visibility)

    def show_list_of_rows(self, list_of_rows):
        self.hide_all_rows()
        self.set_row_visibility(visibility=True, list_of_rows=list_of_rows)

