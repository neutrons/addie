from __future__ import (absolute_import, division, print_function)
import os
from qtpy.QtCore import Qt
from addie.processing.idl.step2_gui_handler import Step2GuiHandler


class RunSumScans(object):

    output_file = ''

    def __init__(self, parent=None):
        self.parent = parent.ui.postprocessing_ui
        self.parent_no_ui = parent
        self.o_gui_handler = Step2GuiHandler(main_window=self.parent_no_ui)
        self.folder = os.getcwd()
        self.set_sum_scans_script()

    def set_sum_scans_script(self):
        self.script_path = self.o_gui_handler.get_sum_scans_script()
        self.script = 'python ' + self.script_path
        print("SumScans: ", self.script)

    def run(self):
        self._background = self.collect_background_runs()
        self._runs = self.collect_runs_checked()
        self.create_output_file()
        self.run_script()

    def run_script(self):
        _script_to_run = self.add_script_flags()
        _script_to_run += ' -f ' + self.full_output_file_name + ' &'

        self.parent_no_ui.launch_job_manager(job_name="SumScans",
                                             script_to_run=_script_to_run)

        print("[LOG] " + _script_to_run)

    def add_script_flags(self):
        self.set_sum_scans_script()
        _script = self.script

        if not self.parent.interactive_mode_checkbox.isChecked():
            _script += " -n True "
        if self.parent_no_ui._is_sum_scans_python_checked:
            _script += " -u True "

        qmax_list = str(self.parent.pdf_qmax_line_edit.text()).strip()
        if not (qmax_list == ""):
            _script += ' -q ' + qmax_list

        return _script

    def create_output_file(self):
        _output_file_name = "sum_" + self.parent.sum_scans_output_file_name.text() + ".inp"
        # print("_output_file_name: {}".format(_output_file_name))
        _full_output_file_name = os.path.join(self.folder, _output_file_name)
        # print("_full_output_file_name: {}".format(_full_output_file_name))
        self.full_output_file_name = _full_output_file_name

        f = open(_full_output_file_name, 'w')

        for _label in self._runs:
            f.write("%s %s\n" % (_label, self._runs[_label]))
        f.write("endsamples\n")
        f.write("Background %s\n" % self._background)

        o_gui_handler = Step2GuiHandler(main_window=self.parent_no_ui)

        # hydrogen flag
        plattype_flag = 0
        if o_gui_handler.is_hydrogen_clicked():
            plattype_flag = 2
        f.write("platype {}\n".format(plattype_flag))

        # platrange
        [plarange_min, plarange_max] = o_gui_handler.get_plazcek_range()
        if plarange_min and plarange_max:
            f.write("plarange {},{}\n".format(plarange_min, plarange_max))

        # poly degree
        poly_degree = str(self.parent.ndeg.value())
        f.write("ndeg {}\n".format(poly_degree))

        # qrangeft
        [q_range_min, q_range_max] = o_gui_handler.get_q_range()
        if q_range_min and q_range_max:
            f.write("qrangeft {},{}\n".format(q_range_min, q_range_max))

        # rmax
        rmax = str(self.parent.sum_scans_rmax.text()).strip()
        if not (rmax == ""):
            f.write("rmax {}\n".format(rmax))

        f.close()
        print("[LOG] created file %s" % _full_output_file_name)

    def collect_runs_checked(self):
        table = self.parent.table
        _runs = {}
        for _row_index in range(table.rowCount()):
            _selected_widget = table.cellWidget(_row_index, 0).children()[1]
            if (_selected_widget.checkState() == Qt.Checked):
                _label = str(table.item(_row_index, 1).text())
                _value = str(table.item(_row_index, 2).text())
                _runs[_label] = _value

        return _runs

    def collect_background_runs(self):
        if self.parent.background_no.isChecked():
            _background = str(self.parent.background_no_field.text())
        else:
            _background = str(self.parent.background_line_edit.text())
        return _background
