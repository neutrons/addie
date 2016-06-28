import autoNOM
import numpy as np
import os
from PyQt4 import QtCore, QtGui
import sys

class MyApp(QtGui.QMainWindow, autoNOM.Ui_MainWindow):

    def __init__(self):
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
        QtGui.QMainWindow.__init__(self)
        autoNOM.Ui_MainWindow.__init__(self)
        self.setupUi(self)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
