from PyQt4 import QtGui

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

    table_column_width = [200, 200, 60, 300]
    table_row_height = 40

    def __init__(self, parent=None):
        self.parent = parent

        QtGui.QMainWindow.__init__(self, parent=parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

        self.init_widgets()

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

    def __insert_new_row(self, row=-1):
        self.ui.tableWidget.insertRow(row)
        self.ui.tableWidget.setRowHeight(row, self.table_row_height)

        #column 1
        label = QtGui.QLabel("Run #:")
        value = QtGui.QLineEdit("")
        button = QtGui.QPushButton("Browse ...")
        hori_layout = QtGui.QHBoxLayout()
        hori_layout.addWidget(label)
        hori_layout.addWidget(value)
        hori_layout.addWidget(button)
        col1_widget = QtGui.QWidget()
        col1_widget.setLayout(hori_layout)
        self.ui.tableWidget.setCellWidget(row, 0, col1_widget)


    def run_calibration_button_clicked(self):
        print("run calibration")

    def closeEvent(self, c):
        self.parent.make_calibration_ui = None

