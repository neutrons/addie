
class Utilities:

    def __init__(self, parent=None):
        self.parent = parent
        self.table_ui = parent.ui.h3_table

    def get_row_key_from_row_index(self, row=-1):
        if row == -1:
            return None

        master_table_row_ui = self.parent.master_table_list_ui

        for _key in master_table_row_ui.keys():

            _activate_ui = master_table_row_ui[_key]["active"]

            _activate_ui_of_given_row = self.table_ui.cellWidget(row, 0).children()[1]

            if _activate_ui == _activate_ui_of_given_row:
                return _key
