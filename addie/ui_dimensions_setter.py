# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/ui_dimensions_setter.ui'
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
        Dialog.resize(330, 451)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(200, 0))
        Dialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.radius_units = QtGui.QLabel(Dialog)
        self.radius_units.setObjectName(_fromUtf8("radius_units"))
        self.gridLayout.addWidget(self.radius_units, 0, 3, 1, 1)
        self.radius2_value = QtGui.QLineEdit(Dialog)
        self.radius2_value.setMinimumSize(QtCore.QSize(80, 0))
        self.radius2_value.setMaximumSize(QtCore.QSize(80, 16777215))
        self.radius2_value.setObjectName(_fromUtf8("radius2_value"))
        self.gridLayout.addWidget(self.radius2_value, 1, 2, 1, 1)
        self.radius2_label = QtGui.QLabel(Dialog)
        self.radius2_label.setObjectName(_fromUtf8("radius2_label"))
        self.gridLayout.addWidget(self.radius2_label, 1, 1, 1, 1)
        self.radius_value = QtGui.QLineEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radius_value.sizePolicy().hasHeightForWidth())
        self.radius_value.setSizePolicy(sizePolicy)
        self.radius_value.setMinimumSize(QtCore.QSize(80, 0))
        self.radius_value.setMaximumSize(QtCore.QSize(80, 16777215))
        self.radius_value.setObjectName(_fromUtf8("radius_value"))
        self.gridLayout.addWidget(self.radius_value, 0, 2, 1, 1)
        self.radius2_units = QtGui.QLabel(Dialog)
        self.radius2_units.setObjectName(_fromUtf8("radius2_units"))
        self.gridLayout.addWidget(self.radius2_units, 1, 3, 1, 1)
        self.height_label = QtGui.QLabel(Dialog)
        self.height_label.setObjectName(_fromUtf8("height_label"))
        self.gridLayout.addWidget(self.height_label, 2, 1, 1, 1)
        self.height_units = QtGui.QLabel(Dialog)
        self.height_units.setObjectName(_fromUtf8("height_units"))
        self.gridLayout.addWidget(self.height_units, 2, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 4, 1, 1)
        self.height_value = QtGui.QLineEdit(Dialog)
        self.height_value.setMinimumSize(QtCore.QSize(80, 0))
        self.height_value.setMaximumSize(QtCore.QSize(80, 16777215))
        self.height_value.setObjectName(_fromUtf8("height_value"))
        self.gridLayout.addWidget(self.height_value, 2, 2, 1, 1)
        self.radius_label = QtGui.QLabel(Dialog)
        self.radius_label.setObjectName(_fromUtf8("radius_label"))
        self.gridLayout.addWidget(self.radius_label, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.preview = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preview.sizePolicy().hasHeightForWidth())
        self.preview.setSizePolicy(sizePolicy)
        self.preview.setText(_fromUtf8(""))
        self.preview.setObjectName(_fromUtf8("preview"))
        self.horizontalLayout.addWidget(self.preview)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.cancel = QtGui.QPushButton(Dialog)
        self.cancel.setObjectName(_fromUtf8("cancel"))
        self.horizontalLayout_12.addWidget(self.cancel)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem4)
        self.ok = QtGui.QPushButton(Dialog)
        self.ok.setObjectName(_fromUtf8("ok"))
        self.horizontalLayout_12.addWidget(self.ok)
        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.reject)
        QtCore.QObject.connect(self.ok, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.accept)
        QtCore.QObject.connect(self.radius_value, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), Dialog.value_changed)
        QtCore.QObject.connect(self.radius2_value, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), Dialog.value_changed)
        QtCore.QObject.connect(self.height_value, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), Dialog.value_changed)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.radius_value, self.radius2_value)
        Dialog.setTabOrder(self.radius2_value, self.height_value)
        Dialog.setTabOrder(self.height_value, self.ok)
        Dialog.setTabOrder(self.ok, self.cancel)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Geometry Dimensions", None))
        self.radius_units.setText(_translate("Dialog", "cm", None))
        self.radius2_label.setText(_translate("Dialog", "Outer Radius", None))
        self.radius2_units.setText(_translate("Dialog", "cm", None))
        self.height_label.setText(_translate("Dialog", "Height", None))
        self.height_units.setText(_translate("Dialog", "cm", None))
        self.radius_label.setText(_translate("Dialog", "Inner Radius", None))
        self.cancel.setText(_translate("Dialog", "Cancel", None))
        self.ok.setText(_translate("Dialog", "Save", None))

