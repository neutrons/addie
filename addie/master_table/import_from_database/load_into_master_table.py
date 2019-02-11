from addie.master_table.import_from_database.conflicts_solver import ConflictsSolverHandler
from addie.master_table.table_row_handler import TableRowHandler

class LoadIntoMasterTable:

    def __init__(self, parent=None, json=None, with_conflict=False, ignore_conflicts=False):
        self.parent = parent
        self.json = json
        self.with_conflict = with_conflict

        if ignore_conflicts:
            self.load()
        else:
            if with_conflict:
                ConflictsSolverHandler(parent=self.parent, json_conflicts=self.json)
            else:
                self.load()

    def load(self):

        o_table = TableRowHandler(parent=self.parent)

        for _row, _key in enumerate(self.json.keys()):

            _entry = self.json[_key]

            run_number = _key
            title = _entry['title']
            chemical_formula = _entry['resolved_conflict']['chemical_formula']
            geometry = _entry['resolved_conflict']['geometry']
            mass_density = _entry['resolved_conflict']['mass_density']
            sample_env_device = _entry['resolved_conflict']['sample_env_device']

            o_table.insert_row(row=_row,
                               title=title,
                               sample_runs=run_number,
                               sample_mass_density=mass_density,
                               sample_chemical_formula=chemical_formula)






