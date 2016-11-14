from PyQt4 import QtGui

from fastgr.ui_jobStatus import Ui_MainWindow as UiMainWindow


class JobMonitorInterface(QtGui.QMainWindow):
    
    column_width = [150, 100]
    
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
	for _row in range(self.ui.tableWidget.rowCount()):
	    self.ui.tableWidget.removeRow(0)