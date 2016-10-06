# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/ui_helpGui.ui'
#
# Created: Thu Oct  6 09:34:06 2016
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(381, 560)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.table_status = QtGui.QTableWidget(self.centralwidget)
        self.table_status.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed|QtGui.QAbstractItemView.DoubleClicked)
        self.table_status.setAlternatingRowColors(True)
        self.table_status.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.table_status.setObjectName(_fromUtf8("table_status"))
        self.table_status.setColumnCount(2)
        self.table_status.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.table_status.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table_status.setHorizontalHeaderItem(1, item)
        self.table_status.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.table_status)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 381, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.hide_button_clicked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Button Status", None))
        item = self.table_status.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Fields/Widgets", None))
        item = self.table_status.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Status", None))
        self.pushButton.setText(_translate("MainWindow", "Hide", None))

