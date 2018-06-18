# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/ui_launchMantid.ui'
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
        Dialog.resize(413, 98)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setModal(False)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cancel_button = QtGui.QPushButton(Dialog)
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.horizontalLayout.addWidget(self.cancel_button)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.view_jobs_button = QtGui.QPushButton(Dialog)
        self.view_jobs_button.setObjectName(_fromUtf8("view_jobs_button"))
        self.horizontalLayout.addWidget(self.view_jobs_button)
        self.launch_jobs_button = QtGui.QPushButton(Dialog)
        self.launch_jobs_button.setObjectName(_fromUtf8("launch_jobs_button"))
        self.horizontalLayout.addWidget(self.launch_jobs_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.cancel_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.cancel_clicked)
        QtCore.QObject.connect(self.view_jobs_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.view_jobs_clicked)
        QtCore.QObject.connect(self.launch_jobs_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.launch_jobs_clicked)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "You are about to launch x Mantid Reductions", None))
        self.cancel_button.setText(_translate("Dialog", "Cancel", None))
        self.view_jobs_button.setText(_translate("Dialog", "View Jobs ...", None))
        self.launch_jobs_button.setText(_translate("Dialog", "Launch Jobs", None))

