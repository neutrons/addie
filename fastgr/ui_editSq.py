# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_editSq.ui'
#
# Created: Wed May  3 18:36:38 2017
#      by: PyQt4 UI code generator 4.10.4
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
        Dialog.resize(402, 250)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.comboBox_workspaces = QtGui.QComboBox(Dialog)
        self.comboBox_workspaces.setObjectName(_fromUtf8("comboBox_workspaces"))
        self.comboBox_workspaces.addItem(_fromUtf8(""))
        self.comboBox_workspaces.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.comboBox_workspaces)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_scaleFactor = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_scaleFactor.setObjectName(_fromUtf8("lineEdit_scaleFactor"))
        self.gridLayout.addWidget(self.lineEdit_scaleFactor, 1, 2, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_shift = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_shift.setObjectName(_fromUtf8("lineEdit_shift"))
        self.gridLayout.addWidget(self.lineEdit_shift, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.pushButton_saveNewSq = QtGui.QPushButton(Dialog)
        self.pushButton_saveNewSq.setObjectName(_fromUtf8("pushButton_saveNewSq"))
        self.verticalLayout.addWidget(self.pushButton_saveNewSq)
        self.pushButton_quit = QtGui.QPushButton(Dialog)
        self.pushButton_quit.setObjectName(_fromUtf8("pushButton_quit"))
        self.verticalLayout.addWidget(self.pushButton_quit)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.comboBox_workspaces.setItemText(0, _translate("Dialog", "workspace 1", None))
        self.comboBox_workspaces.setItemText(1, _translate("Dialog", "workspace 2", None))
        self.groupBox.setTitle(_translate("Dialog", "Edit S(Q)", None))
        self.label_2.setText(_translate("Dialog", "Scale", None))
        self.lineEdit_scaleFactor.setText(_translate("Dialog", "1", None))
        self.label.setText(_translate("Dialog", "Shift", None))
        self.lineEdit_shift.setText(_translate("Dialog", "0", None))
        self.pushButton_saveNewSq.setText(_translate("Dialog", "Save As", None))
        self.pushButton_quit.setText(_translate("Dialog", "Quit", None))

