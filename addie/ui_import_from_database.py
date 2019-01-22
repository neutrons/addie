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
        Dialog.resize(453, 224)
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
        self.ipts_label = QtGui.QLabel(Dialog)
        self.ipts_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ipts_label.setObjectName(_fromUtf8("ipts_label"))
        self.horizontalLayout_2.addWidget(self.ipts_label)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.ipts_lineedit = QtGui.QLineEdit(Dialog)
        self.ipts_lineedit.setMinimumSize(QtCore.QSize(100, 0))
        self.ipts_lineedit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.ipts_lineedit.setObjectName(_fromUtf8("ipts_lineedit"))
        self.horizontalLayout_2.addWidget(self.ipts_lineedit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.run_radio_button = QtGui.QRadioButton(Dialog)
        self.run_radio_button.setObjectName(_fromUtf8("run_radio_button"))
        self.horizontalLayout.addWidget(self.run_radio_button)
        self.run_number_lineedit = QtGui.QLineEdit(Dialog)
        self.run_number_lineedit.setObjectName(_fromUtf8("run_number_lineedit"))
        self.horizontalLayout.addWidget(self.run_number_lineedit)
        self.run_number_label = QtGui.QLabel(Dialog)
        self.run_number_label.setObjectName(_fromUtf8("run_number_label"))
        self.horizontalLayout.addWidget(self.run_number_label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(20, 49, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_3.addWidget(self.pushButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.cancel_button = QtGui.QPushButton(Dialog)
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.horizontalLayout_3.addWidget(self.cancel_button)
        self.import_button = QtGui.QPushButton(Dialog)
        self.import_button.setObjectName(_fromUtf8("import_button"))
        self.horizontalLayout_3.addWidget(self.import_button)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.cancel_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.cancel_button_clicked)
        QtCore.QObject.connect(self.import_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.import_button_clicked)
        QtCore.QObject.connect(self.ipts_radio_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.radio_button_changed)
        QtCore.QObject.connect(self.run_radio_button, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.radio_button_changed)
        QtCore.QObject.connect(self.ipts_combobox, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), Dialog.ipts_selection_changed)
        QtCore.QObject.connect(self.run_number_lineedit, QtCore.SIGNAL(_fromUtf8("returnPressed()")), Dialog.run_number_return_pressed)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.change_user_clicked)
        QtCore.QObject.connect(self.ipts_lineedit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), Dialog.ipts_text_changed)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.import_button, self.ipts_combobox)
        Dialog.setTabOrder(self.ipts_combobox, self.ipts_lineedit)
        Dialog.setTabOrder(self.ipts_lineedit, self.run_number_lineedit)
        Dialog.setTabOrder(self.run_number_lineedit, self.cancel_button)
        Dialog.setTabOrder(self.cancel_button, self.pushButton)
        Dialog.setTabOrder(self.pushButton, self.run_radio_button)
        Dialog.setTabOrder(self.run_radio_button, self.ipts_radio_button)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.ipts_radio_button.setText(_translate("Dialog", "Select IPTS", None))
        self.ipts_label.setText(_translate("Dialog", "or", None))
        self.label_3.setText(_translate("Dialog", "IPTS-", None))
        self.run_radio_button.setText(_translate("Dialog", "Run(s) #", None))
        self.run_number_label.setText(_translate("Dialog", "1,3-5,10", None))
        self.pushButton.setText(_translate("Dialog", "Change User ...", None))
        self.cancel_button.setText(_translate("Dialog", "Cancel", None))
        self.import_button.setText(_translate("Dialog", "Import", None))

