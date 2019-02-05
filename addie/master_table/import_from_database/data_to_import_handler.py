class DataToImportHandler:

    def __init__(self, parent=None):
        self.parent = parent

    def is_with_filter(self):
        if self.parent.ui.toolBox.currentIndex() == 0:
            return False
        return True

    def get_table_of_data_to_import(self):

        if self.is_with_filter():
            # work only with filtered runs
            list_of_rows_to_load = self.parent.list_of_rows_with_global_rule

        else:
            # work with entire stack of runs
            pass
