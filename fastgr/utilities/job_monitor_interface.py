from PyQt4 import QtGui, QtCore

from fastgr.ui_jobStatus import Ui_MainWindow as UiMainWindow


class JobMonitorInterface(QtGui.QMainWindow):
    
    column_width = [200, 250]
    
    def __init__(self, parent=None):
        self.parent = parent
        
        QtGui.QMainWindow.__init__(self, parent = parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)
	
	self.init_table()
	
    def init_table(self):
	for _index, _width in enumerate (self.column_width):
	    self.ui.tableWidget.setColumnWidth(_index, _width)
        
    def closeEvent(self, event=None):
	self.parent.job_monitor_interface = None
	
    def clear_table_clicked(self):
	self.parent.job_list = []
	for _row in range(self.ui.tableWidget.rowCount()):
	    self.ui.tableWidget.removeRow(0)
	    
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
	    if _row_job['status'] == 'processing':
		_widget = QtGui.QPushButton()
		_widget.setText("Aboard")
		QtCore.QObject.connect(_widget, QtCore.SIGNAL("clicked()"), lambda row=_row:
		                       self.parent.kill_job(row))
		self.ui.tableWidget.setCellWidget(_row, 2, _widget)
	    else:
		_item = QtGui.QTableWidgetItem("Killed!")
		self.ui.tableWidget.setItem(_row, 2, _item)