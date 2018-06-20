# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/ui_advanced_window.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(631, 244)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.instrument_comboBox = QtGui.QComboBox(self.centralwidget)
        self.instrument_comboBox.setObjectName(_fromUtf8("instrument_comboBox"))
        self.instrument_comboBox.addItem(_fromUtf8(""))
        self.instrument_comboBox.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.instrument_comboBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.mantid_post_processing_button = QtGui.QRadioButton(self.groupBox)
        self.mantid_post_processing_button.setObjectName(_fromUtf8("mantid_post_processing_button"))
        self.horizontalLayout_5.addWidget(self.mantid_post_processing_button)
        self.idl_post_processing_button = QtGui.QRadioButton(self.groupBox)
        self.idl_post_processing_button.setChecked(True)
        self.idl_post_processing_button.setObjectName(_fromUtf8("idl_post_processing_button"))
        self.horizontalLayout_5.addWidget(self.idl_post_processing_button)
        self.horizontalLayout.addWidget(self.groupBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setMinimumSize(QtCore.QSize(80, 0))
        self.label_2.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.cache_dir_button = QtGui.QPushButton(self.centralwidget)
        self.cache_dir_button.setMaximumSize(QtCore.QSize(80, 16777215))
        self.cache_dir_button.setObjectName(_fromUtf8("cache_dir_button"))
        self.horizontalLayout_3.addWidget(self.cache_dir_button)
        self.cache_dir_label = QtGui.QLabel(self.centralwidget)
        self.cache_dir_label.setObjectName(_fromUtf8("cache_dir_label"))
        self.horizontalLayout_3.addWidget(self.cache_dir_label)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setMinimumSize(QtCore.QSize(80, 0))
        self.label_4.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_4.addWidget(self.label_4)
        self.output_dir_button = QtGui.QPushButton(self.centralwidget)
        self.output_dir_button.setMaximumSize(QtCore.QSize(80, 16777215))
        self.output_dir_button.setObjectName(_fromUtf8("output_dir_button"))
        self.horizontalLayout_4.addWidget(self.output_dir_button)
        self.output_dir_label = QtGui.QLabel(self.centralwidget)
        self.output_dir_label.setObjectName(_fromUtf8("output_dir_label"))
        self.horizontalLayout_4.addWidget(self.output_dir_label)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        spacerItem2 = QtGui.QSpacerItem(20, 346, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 631, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.idl_post_processing_button, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.post_processing_clicked)
        QtCore.QObject.connect(self.mantid_post_processing_button, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.post_processing_clicked)
        QtCore.QObject.connect(self.instrument_comboBox, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), MainWindow.instrument_changed)
        QtCore.QObject.connect(self.cache_dir_button, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.cache_dir_button_clicked)
        QtCore.QObject.connect(self.output_dir_button, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.output_dir_button_clicked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Instrument:", None))
        self.instrument_comboBox.setItemText(0, _translate("MainWindow", "Nomad", None))
        self.instrument_comboBox.setItemText(1, _translate("MainWindow", "Powgen", None))
        self.groupBox.setTitle(_translate("MainWindow", "Post Processing", None))
        self.mantid_post_processing_button.setText(_translate("MainWindow", "Mantid", None))
        self.idl_post_processing_button.setText(_translate("MainWindow", "IDL", None))
        self.label_2.setText(_translate("MainWindow", "Cache Dir.:", None))
        self.cache_dir_button.setText(_translate("MainWindow", "Browse ...", None))
        self.cache_dir_label.setText(_translate("MainWindow", "N/A", None))
        self.label_4.setText(_translate("MainWindow", "Output Dir.:", None))
        self.output_dir_button.setText(_translate("MainWindow", "Browse ...", None))
        self.output_dir_label.setText(_translate("MainWindow", "N/A", None))

