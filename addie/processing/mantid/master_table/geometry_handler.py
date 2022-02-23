from __future__ import (absolute_import, division, print_function)

from qtpy.QtWidgets import QDialog
from addie.utilities import load_ui
from qtpy import QtGui

from addie.processing.mantid.master_table.table_row_handler import TableRowHandler
from addie.utilities.math_tools import is_number

from addie.processing.mantid.master_table.tree_definition import INDEX_OF_COLUMNS_WITH_GEOMETRY_INFOS


def _sphere_csg_radius(value):
    value = 0.01 * value  # converts from cm -> m for CSG
    sphere_xml = " \
        <sphere id='some-sphere'> \
            <centre x='0.0'  y='0.0' z='0.0' /> \
            <radius val={radius} /> \
        </sphere> \
        <algebra val='some-sphere' /> \
    ".format(radius=value)
    return sphere_xml


_table2mantid_cylinder = {
    "Shape": {"Key": "Shape"},
    "Radius": {"Key": "Radius"},
    "Height": {"Key": "Height"}
}

_table2mantid_hollow_cylinder = {
    "Shape": {"Key": "Shape", "ValueProcessor": lambda x: "HollowCylinder"},
    "Radius": {"Key": "InnerRadius"},
    "Radius2": {"Key": "OuterRadius"},
    "Height": {"Key": "Height"}
}

_table2mantid_sphere = {
    "Shape": {"Key": "Shape", "ValueProcessor": lambda x: "CSG"},
    "Radius": {"Key": "Value", "ValueProcessor": _sphere_csg_radius}
}

table2mantid = {
    "Cylinder": _table2mantid_cylinder,
    "Hollow Cylinder": _table2mantid_hollow_cylinder,
    "Sphere": _table2mantid_sphere,
    "PAC03": _table2mantid_cylinder,
    "PAC06": _table2mantid_cylinder,
    "PAC08": _table2mantid_cylinder,
    "PAC10": _table2mantid_cylinder,
    "QuartzTube03": _table2mantid_cylinder
}


class DimensionsSetter(QDialog):

    shape_selected = 'Cylinder'
    column = 0

    def __init__(self, parent=None, key=None, data_type='sample'):
        self.parent = parent
        self.key = key
        self.data_type = data_type

        QDialog.__init__(self, parent=parent)
        self.ui = load_ui('dimensions_setter.ui', baseinstance=self)

        self.group_widgets()
        self.init_widgets_layout()
        self.init_widgets_content()

        if parent.geometry_ui_position:
            self.move(parent.geometry_ui_position)

        self.check_save_button()
        self.set_column_index()

    def set_column_index(self):
        self.column = INDEX_OF_COLUMNS_WITH_GEOMETRY_INFOS[0] if self.data_type == 'sample' else \
            INDEX_OF_COLUMNS_WITH_GEOMETRY_INFOS[1]

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
        return str(self.parent.master_table_list_ui[self.key]
                   [self.data_type]['geometry'][geometry_type]['value'].text())

    def __set_label_value(self, geometry_type, value):
        '''helper function to set value of label in master table.

        :argument:
        geometry_type being 'radius', 'radius2' or 'height'
        value: value to set
        '''
        self.parent.master_table_list_ui[self.key][self.data_type]['geometry'][geometry_type]['value'].setText(
            value)

    def init_widgets_content(self):
        '''populate the widgets using the value from the master table'''

        height = 'N/A'
        radius2 = 'N/A'

        cylinder_sam = ['cylinder', 'pac03', 'pac06', 'pac08', 'pac10',
                        'quartztube03']
        if self.shape_selected.lower() in cylinder_sam:
            radius = self.__get_label_value('radius')
            height = self.__get_label_value('height')
        elif self.shape_selected.lower() == 'sphere':
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
        cylinder_sam = ['cylinder', 'pac03', 'pac06', 'pac08', 'pac10',
                        'quartztube03']
        if self.shape_selected.lower() in cylinder_sam:
            # change label of first label
            self.ui.radius_label.setText("Radius")
            # hide radius 2 widgets
            for _widget in self.group['radius2']:
                _widget.setVisible(False)
            # display right image label
            self.ui.preview.setPixmap(QtGui.QPixmap(
                ":/preview/cylinder_reference.png"))
            self.ui.preview.setScaledContents(True)

        elif self.shape_selected.lower() == 'sphere':
            # change label of first label
            self.ui.radius_label.setText("Radius")
            # hide radius widgets
            for _widget in self.group['radius2']:
                _widget.setVisible(False)
            # hide radius 2 widgets
            for _widget in self.group['height']:
                _widget.setVisible(False)
            # display the right image label
            self.ui.preview.setPixmap(QtGui.QPixmap(
                ":/preview/sphere_reference.png"))
            self.ui.preview.setScaledContents(True)

        elif self.shape_selected.lower() == 'hollow cylinder':
            # display the right image label
            self.ui.preview.setPixmap(QtGui.QPixmap(
                ":/preview/hollow_cylinder_reference.png"))
            self.ui.preview.setScaledContents(True)

        # display value of radius1,2,height for this row

        return

    def value_changed(self, text):
        self.check_save_button()

    def check_save_button(self):
        save_button_status = False

        radius = str(self.ui.radius_value.text())
        radius2 = str(self.ui.radius2_value.text())
        height = str(self.ui.height_value.text())

        cylinder_sam = ['cylinder', 'pac03', 'pac06', 'pac08', 'pac10',
                        'quartztube03']
        if self.shape_selected.lower() in cylinder_sam:
            if is_number(radius) and is_number(height):
                save_button_status = True
        elif self.shape_selected.lower() == 'sphere':
            if is_number(radius):
                save_button_status = True
        else:
            if is_number(radius) and is_number(radius2) and is_number(height):
                save_button_status = True

        self.ui.ok.setEnabled(save_button_status)

    def accept(self):

        radius = str(self.ui.radius_value.text())
        radius2 = 'N/A'
        height = 'N/A'

        cylinder_sam = ['cylinder', 'pac03', 'pac06', 'pac08', 'pac10',
                        'quartztube03']
        if self.shape_selected.lower() in cylinder_sam:
            height = str(self.ui.height_value.text())
        elif self.shape_selected.lower() == 'sphere':
            pass
        else:
            radius2 = str(self.ui.radius2_value.text())
            height = str(self.ui.height_value.text())

        self.__set_label_value('radius', radius)
        self.__set_label_value('radius2', radius2)
        self.__set_label_value('height', height)

        o_table = TableRowHandler(main_window=self.parent)
        o_table.transfer_widget_states(
            from_key=self.key, data_type=self.data_type)

        self.parent.check_master_table_column_highlighting(column=self.column)

        self.close()

    def closeEvent(self, c):
        self.parent.geometry_ui_position = self.pos()
