# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/ui_list_of_scan_loader_dialog.ui'
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
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(705, 550)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans"))
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.option1 = QtGui.QRadioButton(Dialog)
        self.option1.setChecked(False)
        self.option1.setObjectName(_fromUtf8("option1"))
        self.verticalLayout_2.addWidget(self.option1)
        self.option2 = QtGui.QRadioButton(Dialog)
        self.option2.setChecked(True)
        self.option2.setObjectName(_fromUtf8("option2"))
        self.verticalLayout_2.addWidget(self.option2)
        self.option3 = QtGui.QRadioButton(Dialog)
        self.option3.setObjectName(_fromUtf8("option3"))
        self.verticalLayout_2.addWidget(self.option3)
        self.option4 = QtGui.QRadioButton(Dialog)
        self.option4.setObjectName(_fromUtf8("option4"))
        self.verticalLayout_2.addWidget(self.option4)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.groupBox = QtGui.QGroupBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.preview_label = QtGui.QLabel(self.groupBox)
        self.preview_label.setText(_fromUtf8(""))
        self.preview_label.setObjectName(_fromUtf8("preview_label"))
        self.verticalLayout.addWidget(self.preview_label)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QObject.connect(self.option1, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.radio_button_changed)
        QtCore.QObject.connect(self.option2, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.radio_button_changed)
        QtCore.QObject.connect(self.option3, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.radio_button_changed)
        QtCore.QObject.connect(self.option4, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.radio_button_changed)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Options to Load CSV File", None))
        self.label.setText(_translate("Dialog", "How do you want the program to populate the TITLE columns?", None))
        self.option1.setText(_translate("Dialog", "Using raw TITLE", None))
        self.option2.setText(_translate("Dialog", "Using raw TITLE but without DYNAMIC TEMPERATURE", None))
        self.option3.setText(_translate("Dialog", "Using raw TITLE and adding RUN_NUMBER information", None))
        self.option4.setText(_translate("Dialog", "Using raw TITLE, without DYNAMIC TEMPERATURE and adding RUN_NUMBER information", None))
        self.groupBox.setTitle(_translate("Dialog", "Preview", None))

import icons_rc
