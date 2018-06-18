# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/ui_launchMantid.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(413, 98)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setModal(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cancel_button = QtWidgets.QPushButton(Dialog)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.view_jobs_button = QtWidgets.QPushButton(Dialog)
        self.view_jobs_button.setObjectName("view_jobs_button")
        self.horizontalLayout.addWidget(self.view_jobs_button)
        self.launch_jobs_button = QtWidgets.QPushButton(Dialog)
        self.launch_jobs_button.setObjectName("launch_jobs_button")
        self.horizontalLayout.addWidget(self.launch_jobs_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        self.cancel_button.clicked.connect(Dialog.cancel_clicked)
        self.view_jobs_button.clicked.connect(Dialog.view_jobs_clicked)
        self.launch_jobs_button.clicked.connect(Dialog.launch_jobs_clicked)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "You are about to launch x Mantid Reductions"))
        self.cancel_button.setText(_translate("Dialog", "Cancel"))
        self.view_jobs_button.setText(_translate("Dialog", "View Jobs ..."))
        self.launch_jobs_button.setText(_translate("Dialog", "Launch Jobs"))

