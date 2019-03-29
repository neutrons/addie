from __future__ import (absolute_import, division, print_function)
from qtpy import QtCore
from qtpy.QtWidgets import QApplication

from addie.processing.mantid.master_table.import_from_database.conflicts_solver import ConflictsSolverHandler
from addie.processing.mantid.master_table.table_row_handler import TableRowHandler
from addie.utilities.gui_handler import TableHandler


class LoadIntoMasterTable:

    def __init__(self, parent=None, json=None, with_conflict=False, ignore_conflicts=False):
        self.parent = parent
        self.json = json
        self.with_conflict = with_conflict
        self.table_ui = parent.processing_ui.h3_table

        if ignore_conflicts:
            self.load()
        else:
            if with_conflict:
                ConflictsSolverHandler(parent=self.parent,
                                       json_conflicts=self.json)
            else:
                self.load()

    def load(self):

        QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        o_table = TableRowHandler(main_window=self.parent)

        if self.parent.clear_master_table_before_loading:
            TableHandler.clear_table(self.table_ui)

        for _row, _key in enumerate(self.json.keys()):

            _entry = self.json[_key]

            run_number = _key
            title = _entry['title']
            chemical_formula = _entry['resolved_conflict']['chemical_formula']
            # geometry = _entry['resolved_conflict']['geometry']
            mass_density = _entry['resolved_conflict']['mass_density']
            # sample_env_device = _entry['resolved_conflict']['sample_env_device']

            o_table.insert_row(row=_row,
                               title=title,
                               sample_runs=run_number,
                               sample_mass_density=mass_density,
                               sample_chemical_formula=chemical_formula)

        QApplication.restoreOverrideCursor()
