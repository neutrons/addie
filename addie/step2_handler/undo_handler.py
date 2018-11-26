from addie.step2_handler.export_table import ExportTable
from addie.step2_handler.import_table import ImportTable
from addie.step2_handler.table_handler import TableHandler
from addie.step2_handler.populate_background_widgets import PopulateBackgroundWidgets


class UndoHandler(object):

    def __init__(self, parent=None):
        self.parent = parent

    def save_table(self, first_save=False):

        if not first_save:
            self.parent.undo_button_enabled = True

        # retrieve table settings
        o_export_table = ExportTable(parent=self.parent)
        o_export_table.collect_data()
        o_export_table.format_data()
        _new_entry = o_export_table.output_text

        self.add_new_entry_to_table(new_entry=_new_entry)

    def add_new_entry_to_table(self, new_entry=''):
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

        _pop_back_wdg = PopulateBackgroundWidgets(parent=self.parent)
        _pop_back_wdg.run()

        self.parent.ui.table.blockSignals(False)

    def check_undo_widgets(self):
        _undo_index = self.parent.undo_index

        if _undo_index == 0:
            _undo_status = False
            _redo_status = True
        elif _undo_index == 10:
            _undo_status = True
            _redo_status = False
        elif not (str(_undo_index-1) in self.parent.undo_table.keys()):
            _undo_status = False
            _redo_status = True
        else:
            _undo_status = True
            _redo_status = True

        # buttons in main gui (Edit menu bar) removed for now !
        # self.parent.ui.actionRedo.setEnabled(redo_status)
        # self.parent.ui.actionUndo.setEnabled(undo_status)

        self.parent.undo_button_enabled = _undo_status
        self.parent.redo_button_enabled = _redo_status
