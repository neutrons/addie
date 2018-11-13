# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/ui_placzek.ui'
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
        MainWindow.resize(541, 359)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout.addWidget(self.checkBox)
        self.checkBox_2 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.verticalLayout.addWidget(self.checkBox_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.comboBox_2 = QtGui.QComboBox(self.centralwidget)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.comboBox_2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.q_range_group_box_3 = QtGui.QGroupBox(self.centralwidget)
        self.q_range_group_box_3.setObjectName(_fromUtf8("q_range_group_box_3"))
        self.horizontalLayout_32 = QtGui.QHBoxLayout(self.q_range_group_box_3)
        self.horizontalLayout_32.setObjectName(_fromUtf8("horizontalLayout_32"))
        self.label_46 = QtGui.QLabel(self.q_range_group_box_3)
        self.label_46.setMinimumSize(QtCore.QSize(35, 0))
        self.label_46.setMaximumSize(QtCore.QSize(35, 16777215))
        self.label_46.setObjectName(_fromUtf8("label_46"))
        self.horizontalLayout_32.addWidget(self.label_46)
        self.q_range_min_4 = QtGui.QLineEdit(self.q_range_group_box_3)
        self.q_range_min_4.setMinimumSize(QtCore.QSize(80, 0))
        self.q_range_min_4.setMaximumSize(QtCore.QSize(80, 16777215))
        self.q_range_min_4.setObjectName(_fromUtf8("q_range_min_4"))
        self.horizontalLayout_32.addWidget(self.q_range_min_4)
        self.label_70 = QtGui.QLabel(self.q_range_group_box_3)
        self.label_70.setMinimumSize(QtCore.QSize(30, 0))
        self.label_70.setObjectName(_fromUtf8("label_70"))
        self.horizontalLayout_32.addWidget(self.label_70)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_32.addItem(spacerItem2)
        self.label_47 = QtGui.QLabel(self.q_range_group_box_3)
        self.label_47.setMinimumSize(QtCore.QSize(40, 0))
        self.label_47.setMaximumSize(QtCore.QSize(40, 16777215))
        self.label_47.setObjectName(_fromUtf8("label_47"))
        self.horizontalLayout_32.addWidget(self.label_47)
        self.q_range_max_3 = QtGui.QLineEdit(self.q_range_group_box_3)
        self.q_range_max_3.setMinimumSize(QtCore.QSize(80, 0))
        self.q_range_max_3.setMaximumSize(QtCore.QSize(80, 16777215))
        self.q_range_max_3.setObjectName(_fromUtf8("q_range_max_3"))
        self.horizontalLayout_32.addWidget(self.q_range_max_3)
        self.label_73 = QtGui.QLabel(self.q_range_group_box_3)
        self.label_73.setMinimumSize(QtCore.QSize(30, 0))
        self.label_73.setObjectName(_fromUtf8("label_73"))
        self.horizontalLayout_32.addWidget(self.label_73)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_32.addItem(spacerItem3)
        self.label_74 = QtGui.QLabel(self.q_range_group_box_3)
        self.label_74.setMinimumSize(QtCore.QSize(35, 0))
        self.label_74.setMaximumSize(QtCore.QSize(35, 16777215))
        self.label_74.setTextFormat(QtCore.Qt.RichText)
        self.label_74.setObjectName(_fromUtf8("label_74"))
        self.horizontalLayout_32.addWidget(self.label_74)
        self.q_range_min_5 = QtGui.QLineEdit(self.q_range_group_box_3)
        self.q_range_min_5.setMinimumSize(QtCore.QSize(80, 0))
        self.q_range_min_5.setMaximumSize(QtCore.QSize(80, 16777215))
        self.q_range_min_5.setObjectName(_fromUtf8("q_range_min_5"))
        self.horizontalLayout_32.addWidget(self.q_range_min_5)
        self.label_79 = QtGui.QLabel(self.q_range_group_box_3)
        self.label_79.setMinimumSize(QtCore.QSize(25, 0))
        self.label_79.setObjectName(_fromUtf8("label_79"))
        self.horizontalLayout_32.addWidget(self.label_79)
        self.verticalLayout.addWidget(self.q_range_group_box_3)
        self.q_range_group_box_4 = QtGui.QGroupBox(self.centralwidget)
        self.q_range_group_box_4.setObjectName(_fromUtf8("q_range_group_box_4"))
        self.horizontalLayout_33 = QtGui.QHBoxLayout(self.q_range_group_box_4)
        self.horizontalLayout_33.setObjectName(_fromUtf8("horizontalLayout_33"))
        self.label_48 = QtGui.QLabel(self.q_range_group_box_4)
        self.label_48.setMinimumSize(QtCore.QSize(35, 0))
        self.label_48.setMaximumSize(QtCore.QSize(35, 16777215))
        self.label_48.setObjectName(_fromUtf8("label_48"))
        self.horizontalLayout_33.addWidget(self.label_48)
        self.q_range_min_6 = QtGui.QLineEdit(self.q_range_group_box_4)
        self.q_range_min_6.setMinimumSize(QtCore.QSize(80, 0))
        self.q_range_min_6.setMaximumSize(QtCore.QSize(80, 16777215))
        self.q_range_min_6.setObjectName(_fromUtf8("q_range_min_6"))
        self.horizontalLayout_33.addWidget(self.q_range_min_6)
        self.label_71 = QtGui.QLabel(self.q_range_group_box_4)
        self.label_71.setMinimumSize(QtCore.QSize(30, 0))
        self.label_71.setObjectName(_fromUtf8("label_71"))
        self.horizontalLayout_33.addWidget(self.label_71)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_33.addItem(spacerItem4)
        self.label_49 = QtGui.QLabel(self.q_range_group_box_4)
        self.label_49.setMinimumSize(QtCore.QSize(40, 0))
        self.label_49.setMaximumSize(QtCore.QSize(40, 16777215))
        self.label_49.setObjectName(_fromUtf8("label_49"))
        self.horizontalLayout_33.addWidget(self.label_49)
        self.q_range_max_4 = QtGui.QLineEdit(self.q_range_group_box_4)
        self.q_range_max_4.setMinimumSize(QtCore.QSize(80, 0))
        self.q_range_max_4.setMaximumSize(QtCore.QSize(80, 16777215))
        self.q_range_max_4.setObjectName(_fromUtf8("q_range_max_4"))
        self.horizontalLayout_33.addWidget(self.q_range_max_4)
        self.label_75 = QtGui.QLabel(self.q_range_group_box_4)
        self.label_75.setMinimumSize(QtCore.QSize(30, 0))
        self.label_75.setObjectName(_fromUtf8("label_75"))
        self.horizontalLayout_33.addWidget(self.label_75)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_33.addItem(spacerItem5)
        self.label_76 = QtGui.QLabel(self.q_range_group_box_4)
        self.label_76.setMinimumSize(QtCore.QSize(35, 0))
        self.label_76.setMaximumSize(QtCore.QSize(35, 16777215))
        self.label_76.setTextFormat(QtCore.Qt.RichText)
        self.label_76.setObjectName(_fromUtf8("label_76"))
        self.horizontalLayout_33.addWidget(self.label_76)
        self.q_range_min_7 = QtGui.QLineEdit(self.q_range_group_box_4)
        self.q_range_min_7.setMinimumSize(QtCore.QSize(80, 0))
        self.q_range_min_7.setMaximumSize(QtCore.QSize(80, 16777215))
        self.q_range_min_7.setObjectName(_fromUtf8("q_range_min_7"))
        self.horizontalLayout_33.addWidget(self.q_range_min_7)
        self.label_80 = QtGui.QLabel(self.q_range_group_box_4)
        self.label_80.setMinimumSize(QtCore.QSize(25, 0))
        self.label_80.setObjectName(_fromUtf8("label_80"))
        self.horizontalLayout_33.addWidget(self.label_80)
        self.verticalLayout.addWidget(self.q_range_group_box_4)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem6)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(80, 0))
        self.pushButton_2.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(100, 0))
        self.pushButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 541, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Placzek", None))
        self.label.setText(_translate("MainWindow", "Order:", None))
        self.comboBox.setItemText(0, _translate("MainWindow", "1st", None))
        self.checkBox.setText(_translate("MainWindow", "self", None))
        self.checkBox_2.setText(_translate("MainWindow", "Interference", None))
        self.label_2.setText(_translate("MainWindow", "Fit spectrum with:", None))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "Gauss Conv. Cubic Spline", None))
        self.q_range_group_box_3.setTitle(_translate("MainWindow", "Lambda Fit", None))
        self.label_46.setText(_translate("MainWindow", "min", None))
        self.q_range_min_4.setText(_translate("MainWindow", "0", None))
        self.label_70.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Å</p></body></html>", None))
        self.label_47.setText(_translate("MainWindow", "max", None))
        self.q_range_max_3.setText(_translate("MainWindow", "40", None))
        self.label_73.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Å</p></body></html>", None))
        self.label_74.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">∆</span></p></body></html>", None))
        self.q_range_min_5.setText(_translate("MainWindow", "0.02", None))
        self.label_79.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Å</p></body></html>", None))
        self.q_range_group_box_4.setTitle(_translate("MainWindow", "Lambda Calc.", None))
        self.label_48.setText(_translate("MainWindow", "min", None))
        self.q_range_min_6.setText(_translate("MainWindow", "0", None))
        self.label_71.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Å</p></body></html>", None))
        self.label_49.setText(_translate("MainWindow", "max", None))
        self.q_range_max_4.setText(_translate("MainWindow", "40", None))
        self.label_75.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Å</p></body></html>", None))
        self.label_76.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">∆</span></p></body></html>", None))
        self.q_range_min_7.setText(_translate("MainWindow", "0.02", None))
        self.label_80.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Å</p></body></html>", None))
        self.pushButton_2.setText(_translate("MainWindow", "Cancel", None))
        self.pushButton.setText(_translate("MainWindow", "OK", None))

