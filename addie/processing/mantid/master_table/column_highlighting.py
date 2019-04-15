from addie.processing.mantid.master_table.tree_definition import LIST_COLUMNS_TO_SEARCH_FOR_FULL_HIGHLIGTHING


class ColumnHighlighting:

    def __init__(self, main_window=None):
        self.main_window = main_window

    def check(self):
        print("checking columns")
