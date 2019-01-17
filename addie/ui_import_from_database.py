# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/ui_import_from_database.ui'
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
        Dialog.resize(514, 169)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.ipts_radio_button = QtGui.QRadioButton(Dialog)
        self.ipts_radio_button.setChecked(True)
        self.ipts_radio_button.setObjectName(_fromUtf8("ipts_radio_button"))
        self.horizontalLayout_2.addWidget(self.ipts_radio_button)
        self.ipts_combobox = QtGui.QComboBox(Dialog)
        self.ipts_combobox.setMinimumSize(QtCore.QSize(150, 0))
        self.ipts_combobox.setMaximumSize(QtCore.QSize(150, 16777215))
        self.ipts_combobox.setObjectName(_fromUtf8("ipts_combobox"))
        self.horizontalLayout_2.addWidget(self.ipts_combobox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.run_radio_button = QtGui.QRadioButton(Dialog)
        self.run_radio_button.setObjectName(_fromUtf8("run_radio_button"))
        self.horizontalLayout.addWidget(self.run_radio_button)
        self.run_number_lineedit = QtGui.QLineEdit(Dialog)
        self.run_number_lineedit.setObjectName(_fromUtf8("run_number_lineedit"))
        self.horizontalLayout.addWidget(self.run_number_lineedit)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
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
        self.import_button.setObjectName(_fromUtf8("import_button"))
        self.horizontalLayout_3.addWidget(self.import_button)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.ipts_radio_button.setText(_translate("Dialog", "IPTS #", None))
        self.run_radio_button.setText(_translate("Dialog", "Run #", None))
        self.label_2.setText(_translate("Dialog", "1,3-5,10", None))
        self.cancel_button.setText(_translate("Dialog", "Cancel", None))
        self.import_button.setText(_translate("Dialog", "Import", None))

