import os
import platform
import sys
#import helpform
#import newimagedlg
#import qrc_resources

import ui_mainWindow

from PyQt4.QtCore import *
import PyQt4.QtCore
from PyQt4.QtGui import *

__version__ = "1.0.0"

class MainWindow(PyQt4.QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.ui = ui_mainWindow.Ui_MainWindow()
        self.ui.setupUi(self)


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Qtrac Ltd.")
    app.setOrganizationDomain("qtrac.eu")
    app.setApplicationName("Image Changer")
    app.setWindowIcon(QIcon(":/icon.png"))
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
