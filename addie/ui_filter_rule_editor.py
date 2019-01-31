# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/ui_filter_rule_editor.ui'
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
        Dialog.resize(728, 373)
        Dialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.remove_group_button = QtGui.QPushButton(Dialog)
        self.remove_group_button.setEnabled(False)
        self.remove_group_button.setMinimumSize(QtCore.QSize(180, 0))
        self.remove_group_button.setMaximumSize(QtCore.QSize(180, 30))
        self.remove_group_button.setObjectName(_fromUtf8("remove_group_button"))
        self.horizontalLayout_3.addWidget(self.remove_group_button)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.add_group_button = QtGui.QPushButton(Dialog)
        self.add_group_button.setEnabled(True)
        self.add_group_button.setMinimumSize(QtCore.QSize(200, 0))
        self.add_group_button.setMaximumSize(QtCore.QSize(200, 30))
        self.add_group_button.setObjectName(_fromUtf8("add_group_button"))
        self.horizontalLayout_3.addWidget(self.add_group_button)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.rule_result = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rule_result.sizePolicy().hasHeightForWidth())
        self.rule_result.setSizePolicy(sizePolicy)
        self.rule_result.setObjectName(_fromUtf8("rule_result"))
        self.horizontalLayout.addWidget(self.rule_result)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 26, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.cancel = QtGui.QPushButton(Dialog)
        self.cancel.setObjectName(_fromUtf8("cancel"))
        self.horizontalLayout_2.addWidget(self.cancel)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.ok = QtGui.QPushButton(Dialog)
        self.ok.setObjectName(_fromUtf8("ok"))
        self.horizontalLayout_2.addWidget(self.ok)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.reject)
        QtCore.QObject.connect(self.ok, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.accept)
        QtCore.QObject.connect(self.remove_group_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.remove_group)
        QtCore.QObject.connect(self.add_group_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.add_group)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Group Name", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Btw. Groups", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Inner Group", None))
        self.remove_group_button.setText(_translate("Dialog", "Remove Selected Group", None))
        self.add_group_button.setText(_translate("Dialog", "Add a Group", None))
        self.label.setText(_translate("Dialog", "Global Rule:", None))
        self.rule_result.setText(_translate("Dialog", "N/A", None))
        self.cancel.setText(_translate("Dialog", "Cancel", None))
        self.ok.setText(_translate("Dialog", "OK", None))

