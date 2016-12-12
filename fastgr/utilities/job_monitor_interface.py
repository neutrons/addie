from PyQt4 import QtGui, QtCore
import psutil

from fastgr.ui_jobStatus import Ui_MainWindow as UiMainWindow
from fastgr.ui_logbook import Ui_MainWindow as logbookUiMainWindow
from fastgr.utilities.job_monitor_thread import JobMonitorThread

class JobMonitorInterface(QtGui.QMainWindow):
    
    column_width = [200, 250]
    
    def __init__(self, parent=None):
        self.parent = parent
        
        QtGui.QMainWindow.__init__(self, parent = parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)
	
	self.init_table()
	self.launch_table_update_thread()
	
    def launch_table_update_thread(self):
	_run_thread = self.parent.job_monitor_thread
	_run_thread.setup(parent = self.parent, job_monitor_interface=self)
	_run_thread.start()	
	
    def init_table(self):
	for _index, _width in enumerate (self.column_width):
	    self.ui.tableWidget.setColumnWidth(_index, _width)
        
    def closeEvent(self, event=None):
	self.parent.job_monitor_thread	.stop()
	self.parent.job_monitor_interface = None
	
    def clear_table_clicked(self):
	self.parent.job_list = []
	for _row in range(self.ui.tableWidget.rowCount()):
	    self.ui.tableWidget.removeRow(0)
	    
    def logbook_clicked(self):
	if self.parent.logbook_interface is None:
	    job_ui = LogbookInterface(parent = self.parent)
	    job_ui.show()
	    self.parent.logbook_interface = job_ui
	else:
	    self.parent.logbook_inteface.activateWindow()
	    job_ui = self.parent.logbook_interface

    def refresh_table(self, job_list):
	for _row in range(self.ui.tableWidget.rowCount()):
	    self.ui.tableWidget.removeRow(0)

	nbr_row = len(job_list)
	for _row in range(nbr_row):
	    _row_job = job_list[_row]

	    self.ui.tableWidget.insertRow(_row)
	    
	    #job name
	    _item = QtGui.QTableWidgetItem(_row_job['job_name'])
	    self.ui.tableWidget.setItem(_row, 0, _item)
	    
	    #time
	    _item = QtGui.QTableWidgetItem(_row_job['time'])
	    self.ui.tableWidget.setItem(_row, 1, _item)

	    #action
	    _pid = _row_job['pid']
	    process = psutil.Process(_pid)
	    if not process.is_running():
		_item = QtGui.QTableWidgetItem("Done!")
		self.ui.tableWidget.setItem(_row, 2, _item)
	    else:
		if _row_job['status'] == 'processing':
		    _widget = QtGui.QPushButton()
		    _widget.setText("Abort!")
		    QtCore.QObject.connect(_widget, QtCore.SIGNAL("clicked()"), lambda row=_row:
			                   self.parent.kill_job(row))
		    self.ui.tableWidget.setCellWidget(_row, 2, _widget)
		else:
		    _item = QtGui.QTableWidgetItem("Killed!")
		    self.ui.tableWidget.setItem(_row, 2, _item)
		    
class LogbookInterface(QtGui.QMainWindow):
    
    
    def __init__(self, parent=None):
        self.parent = parent
        
        QtGui.QMainWindow.__init__(self, parent = parent)
        self.ui = logbookUiMainWindow()
        self.ui.setupUi(self)

	self.start_refresh_text_thread()

    def start_refresh_text_thread(self):
	_run_thread = self.parent.logbook_thread
	_run_thread.setup(parent = self.parent, logbook_interface=self)
	_run_thread.start()	
	
    def closeEvent(self, event=None):
	self.parent.logbook_interface = None
		    