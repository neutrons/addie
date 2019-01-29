import numpy as np

try:
    from PyQt4.QtGui import QDialog, QTableWidgetItem, QComboBox, QCheckBox, QSpacerItem, QSizePolicy, QHBoxLayout, \
        QWidget
    from PyQt4 import QtGui, QtCore
except:
    try:
        from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QComboBox, QCheckBox, QSpacerItem, QSizePolicy, \
            QHBoxLayout, QWidget
        from PyQt5 import QtGui, QtCore
    except:
        raise ImportError("Requires PyQt4 or PyQt5")

from addie.ui_filter_rule_editor import Ui_Dialog as UiDialog


class GlobalRuleHandler:

    def __init__(self, parent=None):
        o_global = GlobalRuleWindow(parent=parent)
        o_global.show()


class GlobalRuleWindow(QDialog):

    list_of_rule_names = []

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
        self.list_of_rule_names = list_of_rule_names
        for _col_index, _name in enumerate(list_of_rule_names):
            self.ui.tableWidget.insertColumn(_col_index+2)
            item_title = QTableWidgetItem(_name)
            self.ui.tableWidget.setHorizontalHeaderItem(_col_index+2, item_title)

    def check_widgets(self):
        nbr_row = self.ui.tableWidget.rowCount()
        enable_remove_widget = True
        if nbr_row == 0:
            enable_remove_widget = False
        self.ui.remove_group_button.setEnabled(enable_remove_widget)

    def define_unique_group_name(self, row):
        """this method makes sure that the name of the group defined is unique and does not exist already"""
        nbr_row = self.ui.tableWidget.rowCount()
        list_group_name = []
        for _row in np.arange(nbr_row):
            if self.ui.tableWidget.item(_row, 0):
                if self.ui.tableWidget.item(_row, 1):
                    _group_name = str(self.ui.tableWidget.item(_row, 1).text())
                    list_group_name.append(_group_name)

        offset = 0
        while True:
            if ("{}".format(offset+row)) in list_group_name:
                offset += 1
            else:
                return "{}".format(offset+row)

    def add_row(self, row=-1):
        self.ui.tableWidget.insertRow(row)
        list_of_widgets_to_unlock = []

        # group name
        _column = 0
        _group_name = self.define_unique_group_name(row)
        _item = QTableWidgetItem(_group_name)
        self.ui.tableWidget.setItem(row, _column, _item)

        # group to group rule
        list_options = ["and", "or"]
        _column += 1
        if row > 0:
            _widget = QComboBox()
            _widget.addItems(list_options)
            self.ui.tableWidget.setCellWidget(row, _column, _widget)
            _widget.blockSignals(True)
            list_of_widgets_to_unlock.append(_widget)
            QtCore.QObject.connect(_widget, QtCore.SIGNAL("currentIndexChanged(QString)"),
                                   lambda value=list_options[0]:
                                   self.combobox_changed(value))
        else:
            _item = QTableWidgetItem("N/A")
            self.ui.tableWidget.setItem(row, _column, _item)

        # rule columns
        _column += 1
        for _offset in np.arange(len(self.list_of_rule_names)):
            _row_layout = QHBoxLayout()
            _widget = QCheckBox()
            _widget.blockSignals(True)
            list_of_widgets_to_unlock.append(_widget)
            QtCore.QObject.connect(_widget, QtCore.SIGNAL("stateChanged(int)"),
                                   lambda value=0:
                                   self.checkbox_changed(value))
            _spacer1 = QSpacerItem(40,20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            _row_layout.addItem(_spacer1)
            _row_layout.addWidget(_widget)
            _spacer2 = QSpacerItem(40,20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            _row_layout.addItem(_spacer2)
            _rule_widget = QWidget()
            _rule_widget.setLayout(_row_layout)
            self.ui.tableWidget.setCellWidget(row, _column+_offset, _rule_widget)

        # inner group rule
        _column += len(self.list_of_rule_names)
        _widget = QComboBox()
        _widget.blockSignals(True)
        list_of_widgets_to_unlock.append(_widget)
        QtCore.QObject.connect(_widget, QtCore.SIGNAL("currentIndexChanged(QString)"),
                               lambda value=list_options[0]:
                               self.combobox_changed(value))
        list_options = ["and", "or"]
        _widget.addItems(list_options)
        self.ui.tableWidget.setCellWidget(row, _column, _widget)
        self.unlock_signals_ui(list_of_widgets_to_unlock)

    def unlock_signals_ui(self, list_ui=[]):
        if list_ui == []:
            return

        for _ui in list_ui:
            _ui.blockSignals(False)

    def checkbox_changed(self, value):
        self.refresh_global_rule()

    def combobox_changed(self, value):
        self.refresh_global_rule()

    def refresh_global_rule(self):
        print("refreshing global rule")


    # Event Handler
    def add_group(self):
        self.ui.remove_group_button.setEnabled(True)
        nbr_row = self.ui.tableWidget.rowCount()
        self.add_row(row=nbr_row)

    def remove_group(self):
        _select = self.ui.tableWidget.selectedRanges()
        if not _select:
            return
        row = _select[0].topRow()
        self.ui.tableWidget.removeRow(row)
        self.check_widgets()
        self.refresh_global_rule()

    def accept(self):
        print("do something")
        self.close()

