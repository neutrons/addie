import copy
import numpy as np
import random

try:
    from PyQt4.QtGui import QCheckBox, QSpacerItem, QSizePolicy, QTableWidgetItem, QLabel, QPushButton, \
        QComboBox, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QDialog, QLineEdit
    from PyQt4.QtGui import QFileDialog
    from PyQt4 import QtCore, QtGui
except ImportError:
    try:
        from PyQt5.QtWidgets import QCheckBox, QSpacerItem, QSizePolicy, QTableWidgetItem, QLabel, QPushButton, \
            QWidget, QComboBox, QGridLayout, QVBoxLayout, QHBoxLayout, QDialog, QLineEdit
        from PyQt5.QtWidgets import QFileDialog
        from PyQt5 import QtCore, QtGui
    except ImportError:
        raise ImportError("Requires PyQt4 or PyQt5")

# from qtpy.QWidgets import QCheckBox, QSpacerItem, QSizePolicy, QTableWidgetItem, QLabel, QPushButton, QWidget, QComboBox
# from qtpy import QtCore, QtGui
from addie.master_table.table_row_handler import TableRowHandler
from addie.master_table.placzek_handler import PlaczekHandler
from addie.master_table.selection_handler import TransferH3TableWidgetState
from addie.master_table.tree_definition import COLUMN_DEFAULT_HEIGHT

from addie.ui_dimensions_setter import Ui_Dialog as UiDialog


class DimensionsSetter(QDialog):

    shape_selected = 'cylindrical'

    def __init__(self, parent=None, key=None, data_type='sample'):
        self.parent = parent
        self.key = key
        self.data_type =  data_type

        QDialog.__init__(self, parent=parent)
        self.ui = UiDialog()
        self.ui.setupUi(self)

        self.group_widgets()
        self.init_widgets_layout()
        self.init_widgets_content()

    def group_widgets(self):
        self.group = {'radius': [self.ui.radius_label,
                                 self.ui.radius_value,
                                 self.ui.radius_units],
                      'radius2': [self.ui.radius2_label,
                                  self.ui.radius2_value,
                                  self.ui.radius2_units],
                      'height': [self.ui.height_label,
                                 self.ui.height_value,
                                 self.ui.height_units]}

    def __get_label_value(self, geometry_type):
        '''helper function to retrieve value of labels from master table.

        :argument:
        geometry_type being 'radius', 'radius2' or 'height'
        '''
        return str(self.parent.master_table_list_ui[self.key][self.data_type]['geometry'][geometry_type]['value'].text())

    def __set_label_value(self, geometry_type, value):
        '''helper function to set value of label in master table.

        :argument:
        geometry_type being 'radius', 'radius2' or 'height'
        value: value to set
        '''
        self.parent.master_table_list_ui[self.key][self.data_type]['geometry'][geometry_type]['value'].setText(value)

    def init_widgets_content(self):
        '''populate the widgets using the value from the master table'''

        height = 'N/A'
        radius2 = 'N/A'

        if self.shape_selected.lower() == 'cylindrical':
            radius = self.__get_label_value('radius')
            height = self.__get_label_value('height')
        elif self.shape_selected.lower() == 'spherical':
            radius = self.__get_label_value('radius')
        else:
            radius = self.__get_label_value('radius')
            radius2 = self.__get_label_value('radius2')
            height = self.__get_label_value('height')

        self.ui.radius_value.setText(radius)
        self.ui.radius2_value.setText(radius2)
        self.ui.height_value.setText(height)

    def init_widgets_layout(self):
        '''using the shape defined for this row, will display the right widgets and will populate
        them with the right values'''

        # which shape are we working on
        table_row_ui = self.parent.master_table_list_ui[self.key][self.data_type]
        shape_ui = table_row_ui['shape']
        self.shape_selected = shape_ui.currentText()

        # hide/show widgets according to shape selected
        if self.shape_selected.lower() == 'cylindrical':
            # change label of first label
            self.ui.radius_label.setText("Radius")
            # hide radius 2 widgets
            for _widget in self.group['radius2']:
                _widget.setVisible(False)
            # display right image label
            self.ui.preview.setPixmap(QtGui.QPixmap(":/preview/cylindrical_reference.png"))
            self.ui.preview.setScaledContents(True)

        elif self.shape_selected.lower() == 'spherical':
            # change label of first label
            self.ui.radius_label.setText("Radius")
            # hide radius widgets
            for _widget in self.group['radius2']:
                _widget.setVisible(False)
            # hide radius 2 widgets
            for _widget in self.group['height']:
                _widget.setVisible(False)
            # display the right image label
            self.ui.preview.setPixmap(QtGui.QPixmap(":/preview/spherical_reference.png"))
            self.ui.preview.setScaledContents(True)

        elif self.shape_selected.lower() == 'hollow cylinder':
            # display the right image label
            self.ui.preview.setPixmap(QtGui.QPixmap(":/preview/hollow_cylindrical_reference.png"))
            self.ui.preview.setScaledContents(True)

        # display value of radius1,2,height for this row

        return

    def accept(self):

        radius = str(self.ui.radius_value.text())
        radius2 = 'N/A'
        height = 'N/A'

        if self.shape_selected.lower() == 'cylindrical':
            height = str(self.ui.height_value.text())
        elif self.shape_selected.lower() == 'spherical':
            pass
        else:
            radius2 = str(self.ui.radius2_value.text())
            height = str(self.ui.height_value.text())

        self.__set_label_value('radius', radius)
        self.__set_label_value('radius2', radius2)
        self.__set_label_value('height', height)

        o_table = TableRowHandler(parent=self.parent)
        o_table.transfer_widget_states(from_key=self.key, data_type=self.data_type)

        self.close()

