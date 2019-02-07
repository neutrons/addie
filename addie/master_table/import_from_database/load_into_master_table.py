from addie.master_table.import_from_database.conflicts_solver import ConflictsSolverHandler


class LoadIntoMasterTable:

    def __init__(self, parent=None, json=None, with_conflict=False):
        self.parent = parent
        self.json = json
        self.with_conflict = with_conflict

        self.run()

    def run(self):
        print("loading json into master table now")

        if self.with_conflict:
            ConflictsSolverHandler(parent=self.parent, json_conflicts=self.json)

