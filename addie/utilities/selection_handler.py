class SelectionHandler:

    def __init__(self, selection_range):
        self.selection_range = selection_range
        self.left_column = self.selection_range.leftColumn()
        self.right_column = self.selection_range.rightColumn()

    def nbr_column_selected(self):
        return (self.right_column - self.left_column) + 1

    def first_column_selected(self):
        return self.left_column