# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/ui_iptsFileTransfer.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(476, 260)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.source_ipts_button = QtWidgets.QPushButton(self.groupBox)
        self.source_ipts_button.setMinimumSize(QtCore.QSize(150, 0))
        self.source_ipts_button.setMaximumSize(QtCore.QSize(150, 16777215))
        self.source_ipts_button.setObjectName("source_ipts_button")
        self.gridLayout.addWidget(self.source_ipts_button, 0, 0, 1, 1)
        self.source_ipts_value = QtWidgets.QLabel(self.groupBox)
        self.source_ipts_value.setObjectName("source_ipts_value")
        self.gridLayout.addWidget(self.source_ipts_value, 0, 1, 1, 1)
        self.source_autonom_button = QtWidgets.QPushButton(self.groupBox)
        self.source_autonom_button.setMinimumSize(QtCore.QSize(150, 0))
        self.source_autonom_button.setMaximumSize(QtCore.QSize(150, 16777215))
        self.source_autonom_button.setObjectName("source_autonom_button")
        self.gridLayout.addWidget(self.source_autonom_button, 1, 0, 1, 1)
        self.source_autonom_value = QtWidgets.QLabel(self.groupBox)
        self.source_autonom_value.setObjectName("source_autonom_value")
        self.gridLayout.addWidget(self.source_autonom_value, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.target_autonom_button = QtWidgets.QPushButton(self.groupBox_2)
        self.target_autonom_button.setMinimumSize(QtCore.QSize(150, 0))
        self.target_autonom_button.setMaximumSize(QtCore.QSize(150, 16777215))
        self.target_autonom_button.setObjectName("target_autonom_button")
        self.gridLayout_2.addWidget(self.target_autonom_button, 0, 0, 1, 1)
        self.target_autonom_value = QtWidgets.QLabel(self.groupBox_2)
        self.target_autonom_value.setObjectName("target_autonom_value")
        self.gridLayout_2.addWidget(self.target_autonom_value, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem = QtWidgets.QSpacerItem(20, 31, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cancel_button = QtWidgets.QPushButton(Dialog)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.transfer_button = QtWidgets.QPushButton(Dialog)
        self.transfer_button.setEnabled(False)
        self.transfer_button.setMinimumSize(QtCore.QSize(200, 0))
        self.transfer_button.setMaximumSize(QtCore.QSize(200, 16777215))
        self.transfer_button.setObjectName("transfer_button")
        self.horizontalLayout.addWidget(self.transfer_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        self.cancel_button.clicked.connect(Dialog.cancel_clicked)
        self.source_ipts_button.clicked.connect(Dialog.source_ipts_clicked)
        self.source_autonom_button.clicked.connect(Dialog.source_autonom_clicked)
        self.target_autonom_button.clicked.connect(Dialog.target_autonom_clicked)
        self.transfer_button.clicked.connect(Dialog.transfer_clicked)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "IPTS File Transfer"))
        self.groupBox.setTitle(_translate("Dialog", "Source"))
        self.source_ipts_button.setText(_translate("Dialog", "IPTS ..."))
        self.source_ipts_value.setText(_translate("Dialog", "N/A"))
        self.source_autonom_button.setText(_translate("Dialog", "autoNOM ..."))
        self.source_autonom_value.setText(_translate("Dialog", "N/A"))
        self.groupBox_2.setTitle(_translate("Dialog", "Target"))
        self.target_autonom_button.setText(_translate("Dialog", "autoNOM ..."))
        self.target_autonom_value.setText(_translate("Dialog", "N/A"))
        self.cancel_button.setText(_translate("Dialog", "Cancel"))
        self.transfer_button.setText(_translate("Dialog", "Transfer Files"))

