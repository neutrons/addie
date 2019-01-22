# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/ui_import_from_run_number.ui'
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
        Dialog.resize(466, 162)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.run_number_lineedit = QtGui.QLineEdit(Dialog)
        self.run_number_lineedit.setObjectName(_fromUtf8("run_number_lineedit"))
        self.horizontalLayout_2.addWidget(self.run_number_lineedit)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtGui.QSpacerItem(20, 49, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.cancel_button = QtGui.QPushButton(Dialog)
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.horizontalLayout_3.addWidget(self.cancel_button)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.import_button = QtGui.QPushButton(Dialog)
        self.import_button.setEnabled(False)
        self.import_button.setObjectName(_fromUtf8("import_button"))
        self.horizontalLayout_3.addWidget(self.import_button)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.cancel_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.cancel_button_clicked)
        QtCore.QObject.connect(self.import_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.import_button_clicked)
        QtCore.QObject.connect(self.run_number_lineedit, QtCore.SIGNAL(_fromUtf8("returnPressed()")), Dialog.run_number_return_pressed)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.change_user_clicked)
        QtCore.QObject.connect(self.run_number_lineedit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), Dialog.run_number_text_changed)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.pushButton.setText(_translate("Dialog", "Change User ...", None))
        self.label.setText(_translate("Dialog", "Run Number(s):", None))
        self.label_2.setText(_translate("Dialog", "1,3-5,10", None))
        self.cancel_button.setText(_translate("Dialog", "Cancel", None))
        self.import_button.setText(_translate("Dialog", "Import", None))

