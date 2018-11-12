class TableRowHandler:

    def __init__(self, parent=None):
        self.parent = parent

    def insert_blank_row(self):
        insert_row = self._calculate_insert_row()

        print("insert row here {}".format(insert_row))


    def _calculate_insert_row(self):
        selection = self.parent.ui.h3_table.selectedRanges()

        # no row selected, new row will be the first row
        if selection == []:
            return 0

        first_selection = selection[0]
        return first_selection.topRow()



