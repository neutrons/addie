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
        Dialog.resize(224, 378)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.radius_label = QtGui.QLabel(Dialog)
        self.radius_label.setObjectName(_fromUtf8("radius_label"))
        self.gridLayout.addWidget(self.radius_label, 0, 0, 1, 1)
        self.radius_value = QtGui.QLineEdit(Dialog)
        self.radius_value.setObjectName(_fromUtf8("radius_value"))
        self.gridLayout.addWidget(self.radius_value, 0, 1, 1, 1)
        self.radius_units = QtGui.QLabel(Dialog)
        self.radius_units.setObjectName(_fromUtf8("radius_units"))
        self.gridLayout.addWidget(self.radius_units, 0, 2, 1, 1)
        self.radius2_label = QtGui.QLabel(Dialog)
        self.radius2_label.setObjectName(_fromUtf8("radius2_label"))
        self.gridLayout.addWidget(self.radius2_label, 1, 0, 1, 1)
        self.radius2_value = QtGui.QLineEdit(Dialog)
        self.radius2_value.setObjectName(_fromUtf8("radius2_value"))
        self.gridLayout.addWidget(self.radius2_value, 1, 1, 1, 1)
        self.radius2_units = QtGui.QLabel(Dialog)
        self.radius2_units.setObjectName(_fromUtf8("radius2_units"))
        self.gridLayout.addWidget(self.radius2_units, 1, 2, 1, 1)
        self.height_label = QtGui.QLabel(Dialog)
        self.height_label.setObjectName(_fromUtf8("height_label"))
        self.gridLayout.addWidget(self.height_label, 2, 0, 1, 1)
        self.height_value = QtGui.QLineEdit(Dialog)
        self.height_value.setObjectName(_fromUtf8("height_value"))
        self.gridLayout.addWidget(self.height_value, 2, 1, 1, 1)
        self.height_units = QtGui.QLabel(Dialog)
        self.height_units.setObjectName(_fromUtf8("height_units"))
        self.gridLayout.addWidget(self.height_units, 2, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.preview = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preview.sizePolicy().hasHeightForWidth())
        self.preview.setSizePolicy(sizePolicy)
        self.preview.setText(_fromUtf8(""))
        self.preview.setObjectName(_fromUtf8("preview"))
        self.verticalLayout.addWidget(self.preview)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Geometry Dimensions", None))
        self.radius_label.setText(_translate("Dialog", "Radius:", None))
        self.radius_units.setText(_translate("Dialog", "cm", None))
        self.radius2_label.setText(_translate("Dialog", "Radius:", None))
        self.radius2_units.setText(_translate("Dialog", "cm", None))
        self.height_label.setText(_translate("Dialog", "Height", None))
        self.height_units.setText(_translate("Dialog", "cm", None))

