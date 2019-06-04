from __future__ import (absolute_import, division, print_function)

from addie.utilities.file_handler import FileHandler
from qtpy.QtCore import Qt


class ExportTable(object):

    current_path = ''
    column_label = []
    data = []
    output_text = []

    def __init__(self, parent=None, filename=''):
        self.parent = parent
        self.filename = filename
        self.table_ui = self.parent.ui.h3_table

    def run(self):
        self.collect_data()
        self.format_data()
        self.export_data()

    def collect_data(self):
        nbr_row = self.table_ui.rowCount()

        # collect current folder
        _path = self.parent.current_folder
        self.current_path = "current_folder: %s" %_path

        return
        #FIXME

        _full_column_label = []
        nbr_column = self.table_ui.columnCount()
        for j in range(nbr_column):
            _column_label = str(self.parent.ui.table.horizontalHeaderItem(j).text())
            _full_column_label.append(_column_label)
        self.column_label = _full_column_label

        _data = []
        for i in range(nbr_row):

            _row = []

            # select flag
            _select_flag = self.retrieve_flag_state(row = i, column = 0)
            _row.append(_select_flag)

            # name
            _name_item = self.get_item_value(i, 1)
            _row.append(_name_item)

            # runs
            _run_item = self.get_item_value(i, 2)
            _row.append(_run_item)

            # sample formula
            _sample_formula = self.get_item_value(i, 3)
            _row.append(_sample_formula)

            # mass density
            _mass_density = self.get_item_value(i, 4)
            _row.append(_mass_density)

            # radius
            _radius = self.get_item_value(i, 5)
            _row.append(_radius)

            # packing fraction
            _packing_fraction = self.get_item_value(i, 6)
            _row.append(_packing_fraction)

            # sample shape
            _sample_shape = self.retrieve_sample_shape(row = i, column = 7)
            _row.append(_sample_shape)

            # do abs corr?
            _do_corr = self.retrieve_abs_corr_state(row = i, column = 8)
            _row.append(_do_corr)

            _data.append(_row)
        self.data = _data

    def get_item_value(self, row, column):
        if self.parent.ui.table.item(row, column) is None:
            return ''
        return str(self.parent.ui.table.item(row, column).text())

    def format_data(self):
        _current_path = self.current_path
        _column_label = self.column_label
        _data = self.data

        output_text = []
        output_text.append("#" + _current_path)

        _title = "|".join(_column_label)
        output_text.append("#" + _title)

        for _row in _data:
            _formatted_row = "|".join(_row)
            output_text.append(_formatted_row)

        self.output_text = output_text

    def export_data(self):
        _filename = self.filename
        if _filename == '':
            return
        _output_text = self.output_text
        _o_file = FileHandler(filename = _filename)
        _o_file.create_ascii(contain = _output_text)

    def retrieve_abs_corr_state(self, row=0, column=8):
        if self.parent.ui.table.cellWidget(row, 8) is None:
            return "False"
        _widget = self.parent.ui.table.cellWidget(row, 8).children()[1]
        if _widget.checkState() == Qt.Checked:
            return 'True'
        else:
            return 'False'

    def retrieve_sample_shape(self, row=0, column=7):
        _widget = self.parent.ui.table.cellWidget(row, column)
        if _widget is None:
            return 'Cylinder'
        _selected_index = _widget.currentIndex()
        _sample_shape = str(_widget.itemText(_selected_index))
        return _sample_shape

    def retrieve_flag_state(self, row=0, column=0):
        _widget = self.parent.ui.table.cellWidget(row, column).children()[1]
        if _widget is None:
            return "False"
        if _widget.checkState() == Qt.Checked:
            return "True"
        else:
            return "False"
