# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/ui_table_tree_save_config.ui'
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
        Dialog.resize(401, 89)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.save_as_value = QtGui.QLineEdit(Dialog)
        self.save_as_value.setToolTip(_fromUtf8(""))
        self.save_as_value.setStatusTip(_fromUtf8(""))
        self.save_as_value.setPlaceholderText(_fromUtf8(""))
        self.save_as_value.setObjectName(_fromUtf8("save_as_value"))
        self.horizontalLayout.addWidget(self.save_as_value)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.cancel_button = QtGui.QPushButton(Dialog)
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.horizontalLayout_2.addWidget(self.cancel_button)
        self.save_button = QtGui.QPushButton(Dialog)
        self.save_button.setObjectName(_fromUtf8("save_button"))
        self.horizontalLayout_2.addWidget(self.save_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label.setBuddy(self.label)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.cancel_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.cancel_clicked)
        QtCore.QObject.connect(self.save_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.ok_clicked)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.save_as_value, self.save_button)
        Dialog.setTabOrder(self.save_button, self.cancel_button)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Configuration Name:", None))
        self.cancel_button.setText(_translate("Dialog", "Cancel", None))
        self.save_button.setText(_translate("Dialog", "Save", None))

