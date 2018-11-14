import numpy as np


class SelectionHandler:

    def __init__(self, selection_range):
        self.selection_range = selection_range
        self.left_column = self.selection_range.leftColumn()
        self.right_column = self.selection_range.rightColumn()
        self.top_row = self.selection_range.topRow()
        self.bottom_row = self.selection_range.bottomRow()

    def nbr_column_selected(self):
        return (self.right_column - self.left_column) + 1

    def first_column_selected(self):
        return self.left_column

    def get_list_row(self):
        return np.arange(self.top_row, self.bottom_row+1)

