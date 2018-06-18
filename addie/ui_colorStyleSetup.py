# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/ui_colorStyleSetup.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(425, 228)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox_lines = QtWidgets.QComboBox(Dialog)
        self.comboBox_lines.setObjectName("comboBox_lines")
        self.gridLayout.addWidget(self.comboBox_lines, 0, 0, 1, 3)
        self.comboBox_color = QtWidgets.QComboBox(Dialog)
        self.comboBox_color.setObjectName("comboBox_color")
        self.gridLayout.addWidget(self.comboBox_color, 1, 0, 1, 3)
        self.comboBox_style = QtWidgets.QComboBox(Dialog)
        self.comboBox_style.setObjectName("comboBox_style")
        self.gridLayout.addWidget(self.comboBox_style, 2, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(222, 24, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.pushButton_apply = QtWidgets.QPushButton(Dialog)
        self.pushButton_apply.setObjectName("pushButton_apply")
        self.gridLayout.addWidget(self.pushButton_apply, 3, 1, 1, 1)
        self.pushButton_quit = QtWidgets.QPushButton(Dialog)
        self.pushButton_quit.setObjectName("pushButton_quit")
        self.gridLayout.addWidget(self.pushButton_quit, 3, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_apply.setText(_translate("Dialog", "Apply"))
        self.pushButton_quit.setText(_translate("Dialog", "Quit"))

