import numpy as np


class SelectionHandler:

    right_column = -1
    left_column = -2
    top_row = -1
    bottom_row = -2

    def __init__(self, selection_range):

        if len(selection_range) == 0:
            return

        # only considering the first selection in this class
        selection_range = selection_range[0]

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

    def transfer_states(self, state=None, value=''):

        selection = self.parent.ui.h3_table.selectedRanges()
        o_selection = SelectionHandler(selection)

        # enable or disable all other selected rows (if only first column selected)
        if (o_selection.nbr_column_selected() == 1):

            range_row = o_selection.get_list_row()
            column_selected = o_selection.first_column_selected()

            # activate row widget
            if (column_selected == 0):

                # apply state to all the widgets
                for _row in range_row:
                    ui = self.table_ui.cellWidget(_row, 0).children()[1]
                    ui.blockSignals(True)
                    ui.setCheckState(state)
                    ui.blockSignals(False)

            # sample or normalization, shape, abs. corr., mult. scat. corr or inelastic corr.
            elif (column_selected in [7, 10, 11, 12, 18, 21, 22, 23]):

                for _row in range_row:
                    ui = self.table_ui.cellWidget(_row, column_selected).children()[1]
                    index = ui.findText(value)
                    # we found the text
                    if index > -1:
                        if not column_selected in [7, 18]:
                            ui.blockSignals(True)
                        ui.setCurrentIndex(index)
                        if not column_selected in [7, 18]:
                            ui.blockSignals(False)
