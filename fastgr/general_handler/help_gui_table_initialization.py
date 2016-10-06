from PyQt4 import QtGui, QtCore

from fastgr.step1_handler.step1_utilities import Step1Utilities
from fastgr.step2_handler.step2_utilities import Step2Utilities


class HelpGuiTableInitialization(object):

    row_height = 50
    widget_bad = "color: rgb(255, 0, 0)"
    widget_ok = "color: rgb(33, 118, 0)"
    
    def __init__(self, parent=None, button_name='autonom'):
        self.parent = parent
        self.button_name = button_name
        print(button_name)
        
    def fill(self):
        if self.button_name == 'autonom':
            self.fill_autonom()
        elif self.button_name == 'ndabs':
            self.fill_ndabs()
            
    def refill(self):
        nbr_row = self.parent.ui.table_status.rowCount()
        for _row in range(nbr_row):
            self.parent.ui.table_status.removeRow(0)
        self.fill()
            
    def jump_to_step1_diamond(self):
        self.parent.parent.ui.tabWidget_2.setCurrentIndex(0)
        self.parent.parent.ui.diamond.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step1_diamond_background(self):
        self.parent.parent.ui.tabWidget_2.setCurrentIndex(0)
        self.parent.parent.ui.diamond_background.setFocus()
        self.parent.parent.activateWindow()
    
    def jump_to_step1_vanadium(self):
        self.parent.parent.ui.tabWidget_2.setCurrentIndex(0)
        self.parent.parent.ui.vanadium.setFocus()
        self.parent.parent.activateWindow()
    
    def jump_to_step1_vanadium_background(self):
        self.parent.parent.ui.tabWidget_2.setCurrentIndex(0)
        self.parent.parent.ui.vanadium_background.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step1_sample_background(self):
        self.parent.parent.ui.tabWidget_2.setCurrentIndex(0)
        self.parent.parent.ui.sample_background.setFocus()
        self.parent.parent.activateWindow()

    def jump_to_step1_create_folder(self):
        self.parent.parent.ui.tabWidget_2.setCurrentIndex(0)
        self.parent.parent.ui.manual_output_folder_field.setFocus()
        self.parent.parent.activateWindow()
        
    def fill_autonom(self):
        o_step1_handler = Step1Utilities(parent = self.parent.parent)

        # diamond
        self.parent.ui.table_status.insertRow(0)
        self.parent.ui.table_status.setRowHeight(0, self.row_height)       
        _widget = QtGui.QTextEdit()
        _text = "Diamond Field<br/><b>AutoNom>Diamond</b>"
        _widget.setHtml(_text)
        if o_step1_handler.is_diamond_text_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(0, 0, _widget)
        _widget_2 = QtGui.QPushButton()        
        _widget_2.setEnabled(o_step1_handler.is_diamond_text_empty())
        _widget_2.setText("Jump There!")
        QtCore.QObject.connect(_widget_2, QtCore.SIGNAL("clicked()"), self.jump_to_step1_diamond)
        self.parent.ui.table_status.setCellWidget(0, 1, _widget_2)

        # diamond background
        self.parent.ui.table_status.insertRow(1)
        self.parent.ui.table_status.setRowHeight(1, self.row_height)       
        _widget = QtGui.QTextEdit()
        _text = "Diamond Field<br/><b>AutoNom>Diamond Background</b>"
        _widget.setHtml(_text)
        if o_step1_handler.is_diamond_background_text_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(1, 0, _widget)
        _widget_2 = QtGui.QPushButton()        
        _widget_2.setEnabled(o_step1_handler.is_diamond_background_text_empty())
        _widget_2.setText("Jump There!")
        QtCore.QObject.connect(_widget_2, QtCore.SIGNAL("clicked()"), self.jump_to_step1_diamond_background)
        self.parent.ui.table_status.setCellWidget(1, 1, _widget_2)
        
        # vanadium
        self.parent.ui.table_status.insertRow(2)
        self.parent.ui.table_status.setRowHeight(2, self.row_height)       
        _widget = QtGui.QTextEdit()
        _text = "Diamond Field<br/><b>AutoNom>Vanadium</b>"
        _widget.setHtml(_text)
        if o_step1_handler.is_vanadium_text_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(2, 0, _widget)
        _widget_2 = QtGui.QPushButton()        
        _widget_2.setEnabled(o_step1_handler.is_vanadium_text_empty())
        _widget_2.setText("Jump There!")
        QtCore.QObject.connect(_widget_2, QtCore.SIGNAL("clicked()"), self.jump_to_step1_vanadium)
        self.parent.ui.table_status.setCellWidget(2, 1, _widget_2)

        # vanadium background
        self.parent.ui.table_status.insertRow(3)
        self.parent.ui.table_status.setRowHeight(3, self.row_height)       
        _widget = QtGui.QTextEdit()
        _text = "Diamond Field<br/><b>AutoNom>Vanadium Background</b>"
        _widget.setHtml(_text)
        if o_step1_handler.is_vanadium_background_text_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(3, 0, _widget)
        _widget_2 = QtGui.QPushButton()        
        _widget_2.setEnabled(o_step1_handler.is_vanadium_background_text_empty())
        _widget_2.setText("Jump There!")
        QtCore.QObject.connect(_widget_2, QtCore.SIGNAL("clicked()"), self.jump_to_step1_vanadium_background)
        self.parent.ui.table_status.setCellWidget(3, 1, _widget_2)

        # sample background
        self.parent.ui.table_status.insertRow(4)
        self.parent.ui.table_status.setRowHeight(4, self.row_height)       
        _widget = QtGui.QTextEdit()
        _text = "Diamond Field<br/><b>AutoNom>Sample Background</b>"
        _widget.setHtml(_text)
        if o_step1_handler.is_sample_background_text_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(4, 0, _widget)
        _widget_2 = QtGui.QPushButton()        
        _widget_2.setEnabled(o_step1_handler.is_sample_background_text_empty())
        _widget_2.setText("Jump There!")
        QtCore.QObject.connect(_widget_2, QtCore.SIGNAL("clicked()"), self.jump_to_step1_sample_background)
        self.parent.ui.table_status.setCellWidget(4, 1, _widget_2)
        
        # create folder button
        self.parent.ui.table_status.insertRow(5)
        self.parent.ui.table_status.setRowHeight(5, self.row_height + 20)       
        _widget = QtGui.QTextEdit()
        _text = "Diamond Field<br/><b>AutoNom>Create New AutoNom Folder</b>"
        _widget.setHtml(_text)
        if o_step1_handler.is_create_folder_button_status_ok():
            _widget.setStyleSheet(self.widget_ok)
        else:
            _widget.setStyleSheet(self.widget_bad)
        self.parent.ui.table_status.setCellWidget(5, 0, _widget)
        _widget_2 = QtGui.QPushButton()        
        _widget_2.setEnabled(not o_step1_handler.is_create_folder_button_status_ok())
        _widget_2.setText("Jump There!")
        QtCore.QObject.connect(_widget_2, QtCore.SIGNAL("clicked()"), self.jump_to_step1_create_folder)
        self.parent.ui.table_status.setCellWidget(5, 1, _widget_2)
        
    def jump_to_step2_table(self):
        self.parent.parent.ui.tabWidget_2.setCurrentIndex(1)
        self.parent.parent.ui.table.setFocus()
        self.parent.parent.activateWindow()
        
    def jump_to_step2_fourier_from(self):
        self.parent.parent.ui.tabWidget_2.setCurrentIndex(1)
        self.parent.parent.ui.fourier_filter_from.setFocus()
        self.parent.parent.activateWindow()
        
    def jump_to_step2_fourier_to(self):
        self.parent.parent.ui.tabWidget_2.setCurrentIndex(1)
        self.parent.parent.ui.fourier_filter_to.setFocus()
        self.parent.parent.activateWindow()
        
    def fill_ndabs(self):
        o_step2_handler = Step2Utilities(parent = self.parent.parent)
        
        # table status
        self.parent.ui.table_status.insertRow(0)
        self.parent.ui.table_status.setRowHeight(0, self.row_height)
        _widget = QtGui.QTextEdit()
        _text = "Main Table Empty?<br/><b>Post Processing>Table</b>"
        _widget.setHtml(_text)
        if o_step2_handler.is_table_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(0, 0, _widget)
        _widget_2 = QtGui.QPushButton()
        _widget_2.setEnabled(o_step2_handler.is_table_empty())
        _widget_2.setText("Jump There!")
        QtCore.QObject.connect(_widget_2, QtCore.SIGNAL("clicked()"), self.jump_to_step2_table)
        self.parent.ui.table_status.setCellWidget(0, 1, _widget_2)
        
        # at least one row checked
        self.parent.ui.table_status.insertRow(1)
        self.parent.ui.table_status.setRowHeight(1, self.row_height)
        _widget = QtGui.QTextEdit()
        _text = "Main Table Row Selected?<br/><b>Post Processing>Table</b>"
        _widget.setHtml(_text)
        if o_step2_handler.at_least_one_row_checked():
            _widget.setStyleSheet(self.widget_ok)
        else:
            _widget.setStyleSheet(self.widget_bad)
        self.parent.ui.table_status.setCellWidget(1, 0, _widget)
        _widget_2 = QtGui.QPushButton()
        _widget_2.setEnabled(not o_step2_handler.at_least_one_row_checked())
        _widget_2.setText("Jump There!")
        QtCore.QObject.connect(_widget_2, QtCore.SIGNAL("clicked()"), self.jump_to_step2_table)
        self.parent.ui.table_status.setCellWidget(1, 1, _widget_2)
        
        # any fourier filter from
        self.parent.ui.table_status.insertRow(2)
        self.parent.ui.table_status.setRowHeight(2, self.row_height)
        _widget = QtGui.QTextEdit()
        _text = "Is Fourier From Widgets Empty?<br/><b>Post Processing>Fourier Filter From</b>"
        _widget.setHtml(_text)
        if o_step2_handler.is_fourier_filter_from_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(2, 0, _widget)
        _widget_2 = QtGui.QPushButton()
        _widget_2.setEnabled(not o_step2_handler.is_fourier_filter_from_empty())
        _widget_2.setText("Jump There!")
        QtCore.QObject.connect(_widget_2, QtCore.SIGNAL("clicked()"), self.jump_to_step2_fourier_from)
        self.parent.ui.table_status.setCellWidget(2, 1, _widget_2)

        # any fourier filter to
        self.parent.ui.table_status.insertRow(3)
        self.parent.ui.table_status.setRowHeight(3, self.row_height)
        _widget = QtGui.QTextEdit()
        _text = "Is Fourier To Widgets Empty?<br/><b>Post Processing>Fourier Filter To</b>"
        _widget.setHtml(_text)
        if o_step2_handler.is_fourier_filter_to_empty():
            _widget.setStyleSheet(self.widget_bad)
        else:
            _widget.setStyleSheet(self.widget_ok)
        self.parent.ui.table_status.setCellWidget(3, 0, _widget)
        _widget_2 = QtGui.QPushButton()
        _widget_2.setEnabled(not o_step2_handler.is_fourier_filter_to_empty())
        _widget_2.setText("Jump There!")
        QtCore.QObject.connect(_widget_2, QtCore.SIGNAL("clicked()"), self.jump_to_step2_fourier_to)
        self.parent.ui.table_status.setCellWidget(3, 1, _widget_2)
        