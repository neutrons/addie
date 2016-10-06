from PyQt4 import QtGui, QtCore

from fastgr.step1_handler.step1_utilities import Step1Utilities


class HelpGuiTableInitialization(object):

    row_height = 50
    widget_bad = "color: rgb(255, 0, 0)"
    widget_ok = "color: rgb(33, 118, 0)"
    
    def __init__(self, parent=None, button_name='autonom'):
        self.parent = parent
        self.button_name = button_name
        
    def fill(self):
        if self.button_name == 'autonom':
            self.fill_autonom()
            
    def refill(self):
        if self.button_name == 'autonom':
            self.refill_autonom()
            
    def refill_autonom(self):
        nbr_row = self.parent.ui.table_status.rowCount()
        for _row in range(nbr_row):
            self.parent.ui.table_status.removeRow(0)
        self.fill_autonom()
    
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
        