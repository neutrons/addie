import numpy as np

try:
    from PyQt4.QtGui import QDialog, QTableWidgetItem
    from PyQt4 import QtGui, QtCore
except:
    try:
        from PyQt5.QtWidgets import QDialog, QTableWidgetItem
        from PyQt5 import QtGui, QtCore
    except:
        raise ImportError("Requires PyQt4 or PyQt5")

from addie.ui_filter_rule_editor import Ui_Dialog as UiDialog


class GlobalRuleHandler:

    def __init__(self, parent=None):
        o_global = GlobalRuleWindow(parent=parent)
        o_global.show()


class GlobalRuleWindow(QDialog):

    def __init__(self, parent=None):
        self.parent = parent

        QDialog.__init__(self, parent=parent)
        self.ui = UiDialog()
        self.ui.setupUi(self)

        self.init_widgets()

    def get_list_of_rule_names(self):
        """make the list of rule name defined in the previous ui"""
        table_widget = self.parent.ui.tableWidget
        nbr_row = table_widget.rowCount()
        list_of_rule_names = []
        for _row in np.arange(nbr_row):
            _name = str(table_widget.item(_row, 1).text())
            list_of_rule_names.append(_name)
        return list_of_rule_names

    def init_widgets(self):
        list_of_rule_names = self.get_list_of_rule_names()
        for _col_index, _name in enumerate(list_of_rule_names):
            self.ui.tableWidget.insertColumn(_col_index+2)
            item_title = QTableWidgetItem(_name)
            self.ui.tableWidget.setHorizontalHeaderItem(_col_index+2, item_title)

    def check_widgets(self):
        nbr_row = self.ui.tableWidget.rowCount()
        enable_remove_widget = True
        if nbr_row == 1:
            enable_remove_widget = False
        self.ui.remove_group_button.setEnabled(enable_remove_widget)


    # Event Handler
    def add_group(self):
        self.ui.remove_group_button.setEnabled(True)

    def remove_group(self):
        self.check_widgets()

    def accept(self):
        print("do something")
        self.close()

