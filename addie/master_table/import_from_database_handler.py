try:
    from PyQt4.QtGui import QDialog, QComboBox, QLineEdit, QPushButton, QWidget, QHBoxLayout, QLabel, QTableWidgetItem
    from PyQt4 import QtGui, QtCore
except:
    try:
        from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit, QPushButton, QWidget, QHBoxLayout, QLabel, QTableWidgetItem
        from PyQt5 import QtGui, QtCore
    except:
        raise ImportError("Requires PyQt4 or PyQt5")

from addie.master_table.oncat_authentication_handler import OncatAuthenticationHandler
from addie.utilities.oncat import pyoncatGetIptsList
from addie.master_table.tree_definition import LIST_SEARCH_CRITERIA
from addie.master_table.periodic_table.material_handler import MaterialHandler

from addie.utilities.general import generate_random_key

from addie.ui_import_from_database import Ui_Dialog as UiDialog


class ImportFromDatabaseHandler:

    def __init__(self, parent=None):
        if parent.import_from_database_ui is None:
            o_import = ImportFromDatabaseWindow(parent=parent)
            o_import.show()
            parent.import_from_database_ui = o_import
            if parent.import_from_database_ui_position:
                parent.import_from_database_ui.move(parent.import_from_database_ui_position)
        else:
            parent.import_from_database_ui.setFocus()
            parent.import_from_database_ui.activateWindow()


class ImportFromDatabaseWindow(QDialog):

    column_widths = [10, 200, 100, 300]
    row_height = 40

    button_height = 30
    button_width = 150

    list_ui = {}

    def __init__(self, parent=None):
        self.parent = parent

        QDialog.__init__(self, parent=parent)
        self.ui = UiDialog()
        self.ui.setupUi(self)

        self.init_widgets()
        self.radio_button_changed()

    def init_widgets(self):
        if self.parent.oncat is None:
            return

        self.ui.tableWidget.setColumnHidden(0, True)

        self.ui.error_message.setStyleSheet("color: red")
        self.ui.error_message.setVisible(False)

        # retrieve list of IPTS for this user
        instrument = self.parent.instrument['short_name']
        facility = self.parent.facility

        list_ipts = pyoncatGetIptsList(oncat=self.parent.oncat,
                                       instrument=instrument,
                                       facility=facility)
        self.list_ipts = list_ipts

        self.ui.ipts_combobox.addItems(list_ipts)

        self.ui.clear_ipts.setIcon(QtGui.QIcon(":/MPL Toolbar/clear_icon.png"))
        self.ui.clear_run.setIcon(QtGui.QIcon(":/MPL Toolbar/clear_icon.png"))

        for _col, _width in enumerate(self.column_widths):
            self.ui.tableWidget.setColumnWidth(_col, _width)

    def change_user_clicked(self):
        OncatAuthenticationHandler(parent=self.parent)

    def radio_button_changed(self):
        ipts_widgets_status = False
        run_widgets_status = True
        if self.ui.ipts_radio_button.isChecked():
            ipts_widgets_status = True
            run_widgets_status = False
            self.ipts_text_changed(str(self.ui.ipts_lineedit.text()))
        else:
            self.ui.error_message.setVisible(False)

        self.ui.ipts_combobox.setEnabled(ipts_widgets_status)
        self.ui.ipts_lineedit.setEnabled(ipts_widgets_status)
        self.ui.ipts_label.setEnabled(ipts_widgets_status)
        self.ui.clear_ipts.setEnabled(ipts_widgets_status)

        self.ui.run_number_lineedit.setEnabled(run_widgets_status)
        self.ui.run_number_label.setEnabled(run_widgets_status)
        self.ui.clear_run.setEnabled(run_widgets_status)

    def clear_ipts(self):
        self.ui.ipts_lineedit.setText("")

    def clear_run(self):
        self.ui.run_number_lineedit.setText("")

    def ipts_selection_changed(self, ipts_selected):
        self.ui.ipts_lineedit.setText("")

    def ipts_text_changed(self, ipts_text):
        if ipts_text.strip() != "":
            str_ipts = "IPTS-{}".format(ipts_text.strip())

            ipts_exist = False
            if str_ipts in self.list_ipts:
                ipts_exist = True
        else:
            ipts_exist = True

        self.ui.error_message.setVisible(not ipts_exist)
        self.ui.import_button.setEnabled(ipts_exist)

    def run_number_return_pressed(self):
        pass

    def import_button_clicked(self):
        pass

    def cancel_button_clicked(self):
        self.close()

    def add_criteria_clicked(self):
        nbr_row = self.ui.tableWidget.rowCount()
        self._add_row(row=nbr_row)

    def chemical_formula_pressed(self, key):
        MaterialHandler(parent=self.parent,
                        database_window=self,
                        key=key,
                        data_type='database')

    def list_criteria_changed(self, value, key):
        if value == 'Chemical Formula':
            show_label = True
            show_button = True
            show_lineedit = False
        else:
            show_label = False
            show_button = False
            show_lineedit = True

        self.list_ui[key]['value_lineedit'].setVisible(show_lineedit)
        self.list_ui[key]['value_label'].setVisible(show_label)
        self.list_ui[key]['value_button'].setVisible(show_button)

    def _add_row(self, row=-1):

        _random_key = generate_random_key()

        _list_ui_for_this_row = {}

        self.ui.tableWidget.insertRow(row)
        self.ui.tableWidget.setRowHeight(row, self.row_height)

        # key
        _item = QTableWidgetItem("{}".format(_random_key))
        self.ui.tableWidget.setItem(row, 0, _item)

        # search argument
        _widget = QComboBox()
        _list_ui_for_this_row['list_items'] = _widget
        list_items = LIST_SEARCH_CRITERIA[self.parent.instrument['short_name'].lower()]
        _widget.addItems(list_items)
        self.ui.tableWidget.setCellWidget(row, 1, _widget)
        QtCore.QObject.connect(_widget, QtCore.SIGNAL("currentIndexChanged(QString)"),
                               lambda value=list_items[0],
                               key = _random_key:
                               self.list_criteria_changed(value, key))

        # criteria
        list_criteria = ['is', 'contains']
        _widget = QComboBox()
        _list_ui_for_this_row['list_criteria'] = _widget
        _widget.addItems(list_criteria)
        self.ui.tableWidget.setCellWidget(row, 2, _widget)

        # argument
        _layout = QHBoxLayout()
        _lineedit = QLineEdit()
        _lineedit.setVisible(False)
        _label = QLabel()
        _label.setVisible(True)
        _button = QPushButton("Define Formula")
        _button.setFixedHeight(self.button_height)
        _button.setFixedWidth(self.button_width)
        QtCore.QObject.connect(_button, QtCore.SIGNAL("pressed()"),
                                lambda key=_random_key:
                               self.chemical_formula_pressed(key))
        _button.setVisible(True)

        _list_ui_for_this_row['value_lineedit'] = _lineedit
        _list_ui_for_this_row['value_label'] = _label
        _list_ui_for_this_row['value_button'] = _button

        _layout.addWidget(_lineedit)
        _layout.addWidget(_label)
        _layout.addWidget(_button)
        _widget = QWidget()
        _widget.setLayout(_layout)
        self.ui.tableWidget.setCellWidget(row, 3, _widget)

        self.list_ui[_random_key] = _list_ui_for_this_row
        self.check_remove_widget()

    def remove_criteria_clicked(self):
        _select = self.ui.tableWidget.selectedRanges()
        if not _select:
            return
        row = _select[0].topRow()
        _randome_key = str(self.ui.tableWidget.item(row, 0).text())
        self.list_ui.pop(_randome_key, None)
        self.ui.tableWidget.removeRow(row)
        self.check_remove_widget()

    def check_remove_widget(self):
        nbr_row = self.ui.tableWidget.rowCount()
        if nbr_row > 0:
            self.ui.remove_criteria_button.setEnabled(True)
        else:
            self.ui.remove_criteria_button.setEnabled(False)

    def closeEvent(self, c):
        self.parent.import_from_database_ui = None
        self.parent.import_from_database_ui_position = self.pos()