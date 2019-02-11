import pprint

try:
    from PyQt4.QtGui import QComboBox, QApplication, QMainWindow, QWidget
    from PyQt4 import QtGui, QtCore
except:
    try:
        from PyQt5.QtWidgets import QComboBox, QApplication, QMainWindow, QWidget
        from PyQt5 import QtGui, QtCore
    except:
        raise ImportError("Requires PyQt4 or PyQt5")

from addie.ui_solve_import_conflicts import Ui_MainWindow as UiMainWindow


class ConflictsSolverHandler:

    def __init__(self, parent=None, json_conflicts={}):
        o_solver = ConflictsSolverWindow(parent=parent, json_conflicts=json_conflicts)
        o_solver.show()
        if parent.conflicts_solver_ui_position:
            o_solver.move(parent.conflicts_solver_ui_position)


class ConflictsSolverWindow(QMainWindow):

    def __init__(self, parent=None, json_conflicts={}):
        self.parent = parent
        self.json_conflicts = json_conflicts

        QMainWindow.__init__(self, parent=parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

        self.init_widgets()

    def init_widgets(self):
        json_conflicts = self.json_conflicts

        for _key in json_conflicts.keys():
            if json_conflicts[_key]['any_conflict']:
                self._add_tab(json=json_conflicts[_key])

    def _add_tab(self, json=None):
        """will look at the json and will display the values in conflicts in a new tab to allow the user
        to fix the conflicts"""

        number_of_tabs = self.ui.tabWidget.count()
        widget = QWidget()
        self.ui.tabWidget.insertTab(number_of_tabs, widget, "tab #{}".format(number_of_tabs))


    def accept(self):
        self.parent.from_oncat_to_master_table(json=self.json_conflicts,
                                               with_conflict=False)

    def reject(self):
        self.parent.from_oncat_to_master_table(json=self.json_conflicts,
                                               ignore_conflicts=True)
        self.close()

    def closeEvent(self, c):
        pass