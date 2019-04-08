from __future__ import (absolute_import, division, print_function)

from collections import defaultdict
import numpy as np

from qtpy.QtWidgets import QMainWindow, QTableWidget, QRadioButton, QTableWidgetItem
from addie.utilities import load_ui

from addie.utilities.list_runs_parser import ListRunsParser

#from addie.ui_solve_import_conflicts import Ui_MainWindow as UiMainWindow


class ConflictsSolverHandler:

    def __init__(self, parent=None, json_conflicts={}):
        o_solver = ConflictsSolverWindow(parent=parent, json_conflicts=json_conflicts)
        if parent.conflicts_solver_ui_position:
            o_solver.move(parent.conflicts_solver_ui_position)
        o_solver.show()


class ConflictsSolverWindow(QMainWindow):

    list_table = [] # name of table in each of the tabs
    table_width_per_character = 20
    table_header_per_character = 15

    list_keys = ["Run Number", 'chemical_formula', 'geometry', 'mass_density', 'sample_env_device']
    columns_label = ["Run Number", "Chemical Formula", "Geometry", "Mass Density", "Sample Env. Device"]

    list_of_keys_with_conflicts = []

    def __init__(self, parent=None, json_conflicts={}):
        self.parent = parent
        self.json_conflicts = json_conflicts

        QMainWindow.__init__(self, parent=parent)
        self.ui = load_ui('solve_import_conflicts.ui', baseinstance=self)
        #self.ui = UiMainWindow()
        #self.ui.setupUi(self)

        self.init_widgets()

    def init_widgets(self):
        json_conflicts = self.json_conflicts

        for _key in json_conflicts.keys():
            if json_conflicts[_key]['any_conflict']:
                self.list_of_keys_with_conflicts.append(_key)
                self._add_tab(json=json_conflicts[_key]['conflict_dict'])

    def _calculate_columns_width(self, json=None):
        """will loop through all the conflict keys to figure out which one, for each column label, the string
        is the longest"""
        list_key = self.list_keys

        columns_width = defaultdict(list)
        for _key in list_key:
            for _conflict_index in json.keys():
                columns_width[_key].append(self.table_width_per_character * len(json[_conflict_index][_key]))

        final_columns_width = []
        for _key in list_key:
            _max_width = np.max([np.array(columns_width[_key]).max(), len(_key)* self.table_header_per_character])
            final_columns_width.append(_max_width)

        return final_columns_width

    def _add_tab(self, json=None):
        """will look at the json and will display the values in conflicts in a new tab to allow the user
        to fix the conflicts"""

        number_of_tabs = self.ui.tabWidget.count()

        _table = QTableWidget()

        # initialize each table
        columns_width = self._calculate_columns_width(json=json)
        for _col in np.arange(len(json[0])):
            _table.insertColumn(_col)
            _table.setColumnWidth(_col, columns_width[_col])
        for _row in np.arange(len(json)):
            _table.insertRow(_row)
        self.list_table.append(_table)

        _table.setHorizontalHeaderLabels(self.columns_label)

        for _row in np.arange(len(json)):

            # run number
            _col = 0
            list_runs = json[_row]["Run Number"]
            o_parser = ListRunsParser()
            checkbox = QRadioButton(o_parser.new_runs(list_runs=list_runs))
            if _row == 0:
                checkbox.setChecked(True)
            # QtCore.QObject.connect(checkbox, QtCore.SIGNAL("clicked(bool)"),
            #                        lambda bool, row=_row, table_id=_table:
            #                        self._changed_conflict_checkbox(bool, row, table_id))
            _table.setCellWidget(_row, _col, checkbox)

            _col += 1
            # chemical formula
            item = QTableWidgetItem(json[_row]["chemical_formula"])
            _table.setItem(_row, _col, item)

            _col += 1
            # geometry
            item = QTableWidgetItem(json[_row]["geometry"])
            _table.setItem(_row, _col, item)

            _col += 1
            # mass_density
            item = QTableWidgetItem(json[_row]["mass_density"])
            _table.setItem(_row, _col, item)

            _col += 1
            # sample_env_device
            item = QTableWidgetItem(json[_row]["sample_env_device"])
            _table.setItem(_row, _col, item)

        self.ui.tabWidget.insertTab(number_of_tabs, _table, "Conflict #{}".format(number_of_tabs))

    # def _changed_conflict_checkbox(self, state, row, table_id):
    #     print("state is {} in row {} from table_id {}".format(state, row, table_id))

    def save_resolved_conflict(self, tab_index=0, key=None):
        """Using the radio button checked, will save the chemical_formula, geometry... into the final json"""

        def _get_checked_row(table_ui=None):
            """returns the first row where the radio button (column 0) is checked"""
            if table_ui is None:
                return -1

            nbr_row = table_ui.rowCount()
            for _row in np.arange(nbr_row):
                is_radio_button_checked = table_ui.cellWidget(_row, 0).isChecked()
                if is_radio_button_checked:
                    return _row

            return -1

        table_ui = self.list_table[tab_index]
        json_conflicts = self.json_conflicts

        this_json = json_conflicts[key]

        # row checked (which row to use to fix conflict
        _row = _get_checked_row(table_ui=table_ui)

        this_json['any_conflict'] = False

        # chemical_formula, geometry, etc.
        chemical_formula = str(table_ui.item(_row, 1).text())
        geometry = str(table_ui.item(_row, 2).text())
        mass_density = str(table_ui.item(_row, 3).text())
        sample_env_device = str(table_ui.item(_row, 4).text())

        this_json['resolved_conflict'] = {'chemical_formula': chemical_formula,
                                          'geometry': geometry,
                                          'mass_density': mass_density,
                                          'sample_env_device': sample_env_device}

        self.json_conflicts = json_conflicts

    def accept(self):
        for _conflict_index, _key in enumerate(self.list_of_keys_with_conflicts):
            self.save_resolved_conflict(tab_index=_conflict_index, key=_key)

        self.parent.from_oncat_to_master_table(json=self.json_conflicts,
                                               with_conflict=False)
        self.close()

    def reject(self):
        self.parent.from_oncat_to_master_table(json=self.json_conflicts,
                                               ignore_conflicts=True)
        self.close()

    def closeEvent(self, c):
        pass
