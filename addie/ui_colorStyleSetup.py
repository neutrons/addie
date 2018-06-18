# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/ui_colorStyleSetup.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(425, 228)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.comboBox_lines = QtGui.QComboBox(Dialog)
        self.comboBox_lines.setObjectName(_fromUtf8("comboBox_lines"))
        self.gridLayout.addWidget(self.comboBox_lines, 0, 0, 1, 3)
        self.comboBox_color = QtGui.QComboBox(Dialog)
        self.comboBox_color.setObjectName(_fromUtf8("comboBox_color"))
        self.gridLayout.addWidget(self.comboBox_color, 1, 0, 1, 3)
        self.comboBox_style = QtGui.QComboBox(Dialog)
        self.comboBox_style.setObjectName(_fromUtf8("comboBox_style"))
        self.gridLayout.addWidget(self.comboBox_style, 2, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(222, 24, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.pushButton_apply = QtGui.QPushButton(Dialog)
        self.pushButton_apply.setObjectName(_fromUtf8("pushButton_apply"))
        self.gridLayout.addWidget(self.pushButton_apply, 3, 1, 1, 1)
        self.pushButton_quit = QtGui.QPushButton(Dialog)
        self.pushButton_quit.setObjectName(_fromUtf8("pushButton_quit"))
        self.gridLayout.addWidget(self.pushButton_quit, 3, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.pushButton_apply.setText(_translate("Dialog", "Apply", None))
        self.pushButton_quit.setText(_translate("Dialog", "Quit", None))

