class UndoHandler(object):
    
    def __init__(self, parent=None):
        self.parent = parent
        
    def save_table(self):
        print("save table")
        self.parent.ui.actionUndo.setEnabled(True)
        #work here to add table into list of table saved
        
    def undo_table(self):
        if self.parent.undo_index == 0:
            return
        
        #work here
        print("UNDO with current index is {}".format(self.parent.undo_index))
        
        self.parent.undo_index -= 1
        self.check_undo_widgets()
            
    def redo_table(self):
        if self.parent.undo_index == self.parent.max_undo_list:
            return
        
        #work here
        print("REDO with current index is {}".format(self.parent.undo_index))
        
        self.parent.undo_index += 1
        self.check_undo_widgets()

    def check_undo_widgets(self):
        _undo_index = self.parent.undo_index
        if _undo_index == 0:
            self.parent.ui.actionUndo.setEnabled(False)
            self.parent.ui.actionRedo.setEnabled(True)
        elif _undo_index == 10:
            self.parent.ui.actionRedo.setEnabled(False)
            self.parent.ui.actionUndo.setEnabled(True)
        else:
            self.parent.ui.actionRedo.setEnabled(True)
            self.parent.ui.actionUndo.setEnabled(True)
            
            
            
        

        