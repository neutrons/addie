try:
    from PyQt4.QtGui import QComboBox, QApplication, QMainWindow
    from PyQt4 import QtGui, QtCore
except:
    try:
        from PyQt5.QtWidgets import QComboBox, QApplication, QMainWindow
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

