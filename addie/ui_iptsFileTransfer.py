# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/ui_iptsFileTransfer.ui'
#
# Created: Tue Dec 27 11:35:10 2016
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(476, 260)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.source_ipts_button = QtGui.QPushButton(self.groupBox)
        self.source_ipts_button.setMinimumSize(QtCore.QSize(150, 0))
        self.source_ipts_button.setMaximumSize(QtCore.QSize(150, 16777215))
        self.source_ipts_button.setObjectName(_fromUtf8("source_ipts_button"))
        self.gridLayout.addWidget(self.source_ipts_button, 0, 0, 1, 1)
        self.source_ipts_value = QtGui.QLabel(self.groupBox)
        self.source_ipts_value.setObjectName(_fromUtf8("source_ipts_value"))
        self.gridLayout.addWidget(self.source_ipts_value, 0, 1, 1, 1)
        self.source_autonom_button = QtGui.QPushButton(self.groupBox)
        self.source_autonom_button.setMinimumSize(QtCore.QSize(150, 0))
        self.source_autonom_button.setMaximumSize(QtCore.QSize(150, 16777215))
        self.source_autonom_button.setObjectName(_fromUtf8("source_autonom_button"))
        self.gridLayout.addWidget(self.source_autonom_button, 1, 0, 1, 1)
        self.source_autonom_value = QtGui.QLabel(self.groupBox)
        self.source_autonom_value.setObjectName(_fromUtf8("source_autonom_value"))
        self.gridLayout.addWidget(self.source_autonom_value, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.target_autonom_button = QtGui.QPushButton(self.groupBox_2)
        self.target_autonom_button.setMinimumSize(QtCore.QSize(150, 0))
        self.target_autonom_button.setMaximumSize(QtCore.QSize(150, 16777215))
        self.target_autonom_button.setObjectName(_fromUtf8("target_autonom_button"))
        self.gridLayout_2.addWidget(self.target_autonom_button, 0, 0, 1, 1)
        self.target_autonom_value = QtGui.QLabel(self.groupBox_2)
        self.target_autonom_value.setObjectName(_fromUtf8("target_autonom_value"))
        self.gridLayout_2.addWidget(self.target_autonom_value, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem = QtGui.QSpacerItem(20, 31, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cancel_button = QtGui.QPushButton(Dialog)
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.horizontalLayout.addWidget(self.cancel_button)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.transfer_button = QtGui.QPushButton(Dialog)
        self.transfer_button.setEnabled(False)
        self.transfer_button.setMinimumSize(QtCore.QSize(200, 0))
        self.transfer_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.transfer_button.setObjectName(_fromUtf8("transfer_button"))
        self.horizontalLayout.addWidget(self.transfer_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.cancel_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.cancel_clicked)
        QtCore.QObject.connect(self.source_ipts_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.source_ipts_clicked)
        QtCore.QObject.connect(self.source_autonom_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.source_autonom_clicked)
        QtCore.QObject.connect(self.target_autonom_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.target_autonom_clicked)
        QtCore.QObject.connect(self.transfer_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.transfer_clicked)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "IPTS File Transfer", None))
        self.groupBox.setTitle(_translate("Dialog", "Source", None))
        self.source_ipts_button.setText(_translate("Dialog", "IPTS ...", None))
        self.source_ipts_value.setText(_translate("Dialog", "N/A", None))
        self.source_autonom_button.setText(_translate("Dialog", "autoNOM ...", None))
        self.source_autonom_value.setText(_translate("Dialog", "N/A", None))
        self.groupBox_2.setTitle(_translate("Dialog", "Target", None))
        self.target_autonom_button.setText(_translate("Dialog", "autoNOM ...", None))
        self.target_autonom_value.setText(_translate("Dialog", "N/A", None))
        self.cancel_button.setText(_translate("Dialog", "Cancel", None))
        self.transfer_button.setText(_translate("Dialog", "Transfer Files", None))

