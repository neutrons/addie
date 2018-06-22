from PyQt4 import QtGui, QtCore
import datetime

from addie.ui_make_calibration import Ui_MainWindow as UiMainWindow
from addie.utilities.gui_handler import TableHandler


class MakeCalibrationLauncher(object):

    def __init__(self, parent=None):
        self.parent = parent

        if self.parent.make_calibration_ui is None:
            _make = MakeCalibrationWindow(parent=self.parent)
            _make.show()
            self.parent.make_calibration_ui = _make
        else:
            self.parent.make_calibration_ui.setFocus()
            self.parent.make_calibration_ui.activateWindow()


class MakeCalibrationWindow(QtGui.QMainWindow):

    table_column_width = [50, 250, 250, 80, 300]
    table_row_height = 40
    entry_level =  0

    master_date = None  #QtCore.QDate()

    def __init__(self, parent=None):
        self.parent = parent

        QtGui.QMainWindow.__init__(self, parent=parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

        self.init_widgets()
        self.init_date()

    def init_date(self):
        """will initialize the master date using today's date"""
        now = datetime.datetime.now()
        day = now.day
        month = now.month
        year = now.year
        today = QtCore.QDate(year, month, day)
        self.master_date = today
        self.ui.master_date.setDate(today)

    def init_widgets(self):
        for index_col, col_size in enumerate(self.table_column_width):
            self.ui.tableWidget.setColumnWidth(index_col, col_size)

    def master_browse_button_clicked(self):
        _master_folder = QtGui.QFileDialog.getExistingDirectory(caption="Select Output Folder ...",
                                                                directory=self.parent.output_folder,
                                                                options=QtGui.QFileDialog.ShowDirsOnly)
        if _master_folder:
            self.ui.master_output_directory_label.setText(str(_master_folder))

    def remove_row_button_clicked(self):
        print("remove row")

    def add_row_button_clicked(self):
        o_gui = TableHandler(table_ui=self.ui.tableWidget)
        row_selected = o_gui.get_current_row()
        self.__insert_new_row(row=row_selected+1)

    def vanadium_browse_clicked(self, entry=-1):
        print("vanadium: {}".format(entry))

    def calibration_browse_clicked(self, entry=-1):
        print("calibration: {}".format(entry))

    def __insert_new_row(self, row=-1):
        self.ui.tableWidget.insertRow(row)
        self.ui.tableWidget.setRowHeight(row, self.table_row_height)

        button_width = 80

        #column0 - entry
        _name = str(self.entry_level+1)
        self.entry_level += 1
        label = QtGui.QLabel(_name)
        self.ui.tableWidget.setCellWidget(row, 0, label)

        #column 1 - calibration
        label = QtGui.QLabel("Run #:")
        value = QtGui.QLineEdit("")
        button = QtGui.QPushButton("Browse ...")
        button.setMinimumWidth(button_width)
        button.setMaximumWidth(button_width)
        button.clicked.connect(lambda state, entry=_name:  self.calibration_browse_clicked(entry))
        hori_layout = QtGui.QHBoxLayout()
        hori_layout.addWidget(label)
        hori_layout.addWidget(value)
        hori_layout.addWidget(button)
        col1_widget = QtGui.QWidget()
        col1_widget.setLayout(hori_layout)
        self.ui.tableWidget.setCellWidget(row, 1, col1_widget)

        #column 2 - Vanadium
        label = QtGui.QLabel("Run #:")
        value = QtGui.QLineEdit("")
        button = QtGui.QPushButton("Browse ...")
        button.setMinimumWidth(button_width)
        button.setMaximumWidth(button_width)
        button.clicked.connect(lambda state, entry=_name:  self.vanadium_browse_clicked(entry))
        hori_layout = QtGui.QHBoxLayout()
        hori_layout.addWidget(label)
        hori_layout.addWidget(value)
        hori_layout.addWidget(button)
        col1_widget = QtGui.QWidget()
        col1_widget.setLayout(hori_layout)
        self.ui.tableWidget.setCellWidget(row, 2, col1_widget)

        #column 3 - date
        date = QtGui.QDateEdit()
        self.ui.tableWidget.setCellWidget(row, 3, date)

        #column 4 - output dir
        label = QtGui.QLabel("N/A")
        button = QtGui.QPushButton("Browse...")
        button.setMinimumWidth(button_width)
        button.setMaximumWidth(button_width)
        hori_layout = QtGui.QHBoxLayout()
        hori_layout.addWidget(label)
        hori_layout.addWidget(button)
        col3_widget = QtGui.QWidget()
        col3_widget.setLayout(hori_layout)
        self.ui.tableWidget.setCellWidget(row, 4, col3_widget)

    def run_calibration_button_clicked(self):
        print("run calibration")

    def closeEvent(self, c):
        self.parent.make_calibration_ui = None

