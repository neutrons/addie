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


class TransferH3TableWidgetState:

    def __init__(self, parent=None):
        self.parent = parent
        self.table_ui = self.parent.ui.h3_table

    def transfer_states(self, state=None):

        selection = self.parent.ui.h3_table.selectedRanges()[0]
        o_selection = SelectionHandler(selection)

        # enable or disable all other selected rows (if only first column selected)
        if (o_selection.nbr_column_selected() == 1):

            # activate row widget
            if (o_selection.first_column_selected() == 0):

                # get current state of button clicked
                range_row = o_selection.get_list_row()
                for _row in range_row:
                    ui = self.table_ui.cellWidget(_row, 0).children()[1]
                    ui.blockSignals(True)
                    ui.setCheckState(state)
                    ui.blockSignals(False)

            # sample or normalization, shape, abs. corr., mult. scat. corr or inelastic corr.
            elif (o_selection.first_column_selected() in [7, 10, 11, 12, 18, 21, 22, 23]):
                print("yes")

