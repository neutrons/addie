from __future__ import (absolute_import, division, print_function)

import numpy as np


class TableSearchEngine:

    def __init__(self, table_ui=None):
        self.table_ui = table_ui

    def locate_string(self, string_to_locate):
        nbr_row = self.table_ui.rowCount()
        nbr_column = self.table_ui.columnCount()

        list_of_row_to_show = []

        for _row in np.arange(nbr_row):
            for _col in np.arange(nbr_column):
                _text = str(self.table_ui.item(_row, _col).text())
                if string_to_locate in _text:
                    list_of_row_to_show.append(_row)
                    break

        return list_of_row_to_show
