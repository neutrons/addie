# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/ui_make_calibration.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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
        MainWindow.resize(1619, 515)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setMinimumSize(QtCore.QSize(40, 0))
        self.label.setMaximumSize(QtCore.QSize(40, 16777215))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.master_date = QtGui.QDateEdit(self.groupBox)
        self.master_date.setObjectName(_fromUtf8("master_date"))
        self.horizontalLayout_2.addWidget(self.master_date)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setMaximumSize(QtCore.QSize(120, 16777215))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.master_output_directory_button = QtGui.QPushButton(self.groupBox)
        self.master_output_directory_button.setMaximumSize(QtCore.QSize(80, 16777215))
        self.master_output_directory_button.setObjectName(_fromUtf8("master_output_directory_button"))
        self.horizontalLayout.addWidget(self.master_output_directory_button)
        self.master_output_directory_label = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.master_output_directory_label.sizePolicy().hasHeightForWidth())
        self.master_output_directory_label.setSizePolicy(sizePolicy)
        self.master_output_directory_label.setObjectName(_fromUtf8("master_output_directory_label"))
        self.horizontalLayout.addWidget(self.master_output_directory_label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.tableWidget = QtGui.QTableWidget(self.centralwidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setHighlightSections(False)
        self.tableWidget.verticalHeader().setSortIndicatorShown(True)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.remove_row_button = QtGui.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.remove_row_button.setFont(font)
        self.remove_row_button.setObjectName(_fromUtf8("remove_row_button"))
        self.horizontalLayout_3.addWidget(self.remove_row_button)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.add_row_button = QtGui.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.add_row_button.setFont(font)
        self.add_row_button.setObjectName(_fromUtf8("add_row_button"))
        self.horizontalLayout_3.addWidget(self.add_row_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.run_calibration_button = QtGui.QPushButton(self.centralwidget)
        self.run_calibration_button.setObjectName(_fromUtf8("run_calibration_button"))
        self.horizontalLayout_4.addWidget(self.run_calibration_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1619, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.master_output_directory_button, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.master_browse_button_clicked)
        QtCore.QObject.connect(self.remove_row_button, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.remove_row_button_clicked)
        QtCore.QObject.connect(self.add_row_button, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.add_row_button_clicked)
        QtCore.QObject.connect(self.run_calibration_button, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.run_calibration_button_clicked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Make Calibration", None))
        self.groupBox.setTitle(_translate("MainWindow", "Master", None))
        self.label.setText(_translate("MainWindow", "Date:", None))
        self.label_2.setText(_translate("MainWindow", "Output Directory:", None))
        self.master_output_directory_button.setText(_translate("MainWindow", "Browse ...", None))
        self.master_output_directory_label.setText(_translate("MainWindow", "N/A", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Entry #", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Calibration", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Vanadium", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Date", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Output Dir.", None))
        self.remove_row_button.setText(_translate("MainWindow", "-", None))
        self.add_row_button.setText(_translate("MainWindow", "+", None))
        self.run_calibration_button.setText(_translate("MainWindow", "Run Calibration", None))
