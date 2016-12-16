from fastgr.step2_handler.export_table import ExportTable
from fastgr.step2_handler.import_table import ImportTable
from fastgr.step2_handler.table_handler import TableHandler
from fastgr.step2_handler.populate_background_widgets import PopulateBackgroundWidgets


class UndoHandler(object):
    
    def __init__(self, parent=None):
        self.parent = parent
        
    def save_table(self):
        self.parent.ui.actionUndo.setEnabled(True)
        
        # retrieve table settings
        o_export_table = ExportTable(parent=self.parent)
        o_export_table.collect_data()
        o_export_table.format_data()
        _new_entry = o_export_table.output_text
        
        self.add_new_entry_to_table(new_entry = _new_entry)
        
    def add_new_entry_to_table(self, new_entry = ''):
        undo_table = self.parent.undo_table
        new_dict = {}
        if not undo_table == {}:
            for key in undo_table.keys():
                _new_key = str(int(key) - 1)
                new_dict[_new_key] = undo_table[key]
            undo_table = new_dict
        undo_table[str(self.parent.max_undo_list)] = new_entry

        self.parent.undo_table = undo_table
        
    def undo_table(self):
        if self.parent.undo_index == 0:
            return        
        self.parent.undo_index -= 1
        self.load_table()
        self.check_undo_widgets()
            
    def redo_table(self):
        if self.parent.undo_index == self.parent.max_undo_list:
            return
        self.parent.undo_index += 1
        self.load_table()
        self.check_undo_widgets()
        
    def load_table(self):
        self.parent.ui.table.blockSignals(True)
    
        _table_to_reload = self.parent.undo_table[str(self.parent.undo_index)]
    
        o_table = TableHandler(parent=self.parent)
        o_table._clear_table()
        
        o_import = ImportTable(parent=self.parent)
        o_import._list_row = _table_to_reload
        o_import.parser()
        o_import.populate_gui()
        
        _pop_back_wdg = PopulateBackgroundWidgets(parent = self.parent)
        _pop_back_wdg.run()        
    
        self.parent.ui.table.blockSignals(False)
    
    def check_undo_widgets(self):
        _undo_index = self.parent.undo_index
        if _undo_index == 0:
            self.parent.ui.actionUndo.setEnabled(False)
            self.parent.ui.actionRedo.setEnabled(True)
        elif _undo_index == 10:
            self.parent.ui.actionRedo.setEnabled(False)
            self.parent.ui.actionUndo.setEnabled(True)
        elif not (str(_undo_index) in self.parent.undo_table.keys()):
            self.parent.ui.actionUndo.setEnabled(False)
        else:
            self.parent.ui.actionRedo.setEnabled(True)
            self.parent.ui.actionUndo.setEnabled(True)
            
            
            
        

        