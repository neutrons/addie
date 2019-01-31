from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import (QMainWindow, QPushButton, QTableWidgetItem)  # noqa
import psutil
from addie.utilities import load_ui
from addie.utilities.job_monitor_thread import JobMonitorThread


class JobMonitorInterface(QMainWindow):

    column_width = [200, 250]

    def __init__(self, parent=None):
        self.parent = parent

        QMainWindow.__init__(self, parent=parent)
        self.ui = load_ui(__file__, '../../../designer/ui_jobStatus.ui', baseinstance=self)
        self.ui.setupUi(self)

        self.init_table()
        self.launch_table_update_thread()

    def launch_table_update_thread(self):
        _run_thread = self.parent.job_monitor_thread
        _run_thread.setup(parent=self.parent, job_monitor_interface=self)
        _run_thread.start()

    def init_table(self):
        for _index, _width in enumerate(self.column_width):
            self.ui.tableWidget.setColumnWidth(_index, _width)

    def closeEvent(self, event=None):
        self.parent.job_monitor_thread.stop()
        self.parent.job_monitor_interface = None

    def clear_table_clicked(self):
        self.parent.job_list = []
        for _row in range(self.ui.tableWidget.rowCount()):
            self.ui.tableWidget.removeRow(0)

    def launch_logbook_thread(self):
        self.parent.start_refresh_text_thread()

    def refresh_table(self, job_list):
        for _row in range(self.ui.tableWidget.rowCount()):
            self.ui.tableWidget.removeRow(0)

        nbr_row = len(job_list)
        for _row in range(nbr_row):
            _row_job = job_list[_row]

            self.ui.tableWidget.insertRow(_row)

            # job name
            _item = QTableWidgetItem(_row_job['job_name'])
            self.ui.tableWidget.setItem(_row, 0, _item)

            # time
            _item = QTableWidgetItem(_row_job['time'])
            self.ui.tableWidget.setItem(_row, 1, _item)

            # action
            _pid = _row_job['pid']
            process = psutil.Process(_pid)
            if not process.is_running():
                _item = QTableWidgetItem("Done!")
                self.ui.tableWidget.setItem(_row, 2, _item)
            else:
                if _row_job['status'] == 'processing':
                    _widget = QPushButton()
                    _widget.setText("Abort!")
                    _widget.clicked.connect(lambda row=_row:
                                            self.parent.kill_job(row))
                    self.ui.tableWidget.setCellWidget(_row, 2, _widget)
                else:
                    _item = QTableWidgetItem("Killed!")
                    self.ui.tableWidget.setItem(_row, 2, _item)
