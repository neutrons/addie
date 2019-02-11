from addie.master_table.import_from_database.conflicts_solver import ConflictsSolverHandler


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
        print("importing all runs. No conflicts found!")

