from __future__ import (absolute_import, division, print_function)
import os
from qtpy.QtCore import Qt
from addie.processing.idl.step2_gui_handler import Step2GuiHandler
from addie.processing.mantid.master_table.periodic_table.material_handler import get_periodictable_formatted_element_and_number_of_atoms
import numpy as np
import re


class RunSumScans(object):

    output_file = ''
    # Variable for Jeorg's new routine, controlling maximum r one could get to.
    # For almost all situations, we don't need to change it, but it is good to
    # put the variable explicitly just in case we may need to change it for
    # whatever reason in the future.
    q_interval_min = 0.02

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
        collect_return = self.collect_runs_checked()
        self._runs = collect_return[0]
        self._runs_name = collect_return[1]
        self._sam_formula = collect_return[2]
        self._mass_den = collect_return[3]
        self._radius = collect_return[4]
        self._pack_frac = collect_return[5]
        self._geom = collect_return[6]
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

        # redpar file
        for _label in self._runs:
            f = open(self._runs_name[_label] + ".redpar", "w")
            chem_form_temp = self._sam_formula[_label]
            list_element = chem_form_temp.split(" ")
            formated_ele_list = []
            for _element in list_element:
                [formated_element, number_of_atoms, case] = get_periodictable_formatted_element_and_number_of_atoms(_element)
                formated_ele_list.append(formated_element)
            sample_form_str = ""
            for item in formated_ele_list:
                if case == 1:
                    to_append = item + "_"
                elif case == 2:
                    to_append = re.findall('[A-Z][a-z]*', item)[-1]
                    to_append += ("_" + re.findall('[0-9]+', item)[-1] + "_")
                else:
                    to_append = item.split("[")[1].split("]")[0] + item.split("[")[0] + "_" + item.split("]")[1] + "_"
                sample_form_str += to_append
            sample_form_str = sample_form_str[:-1]
            f.write("{0:13s}{1:<s}\n".format("formula", sample_form_str))
            f.write("{0:13s}{1:<s}\n".format("massdensity", self._mass_den[_label]))
            f.write("{0:13s}{1:<s}\n".format("radius", self._radius[_label]))
            f.write("{0:13s}{1:<s}\n".format("packfrac", self._pack_frac[_label]))
            f.write("{0:13s}{1:<s}\n".format("geometry", self._geom[_label]))
            [r_range_min, r_range_max] = o_gui_handler.get_r_range()
            r_max_possible = "{0:6.2F}".format(np.pi / self.q_interval_min)
            if r_range_min and r_range_max:
                f.write("{0:13s}{1:<s}\n".format("rfilter", r_range_min + "," + r_range_max + "," + r_max_possible))
            if q_range_min and q_range_max:
                f.write("{0:13s}{1:<s}\n".format("qfilter", q_range_min + "," + q_range_max))
            f.close()

    def collect_runs_checked(self):
        table = self.parent.table
        _runs_name = {}
        _runs = {}
        _sam_formula = {}
        _mass_den = {}
        _radius = {}
        _pack_frac = {}
        _geom = {}
        for _row_index in range(table.rowCount()):
            _selected_widget = table.cellWidget(_row_index, 0).children()[1]
            if (_selected_widget.checkState() == Qt.Checked):
                _runs = self.load_table(_runs, table, _row_index, 2)
                # for Joerg's new script.
                _runs_name = self.load_table(_runs_name, table, _row_index, 1)
                _sam_formula = self.load_table(_sam_formula, table, _row_index, 3)
                _mass_den = self.load_table(_mass_den, table, _row_index, 4)
                _radius = self.load_table(_radius, table, _row_index, 5)
                _pack_frac= self.load_table(_pack_frac, table, _row_index, 6)
                _geom = self.load_table(_geom, table, _row_index, 7)

        return [_runs, _runs_name, _sam_formula, _mass_den, _radius, _pack_frac, _geom]

    def collect_background_runs(self):
        if self.parent.background_no.isChecked():
            _background = str(self.parent.background_no_field.text())
        else:
            _background = str(self.parent.background_line_edit.text())
        return _background

    def load_table(self, dict_in, table_in, row, col):
        _label = str(table_in.item(row, 1).text())
        if col != 7:
            _value = str(table_in.item(row, col).text())
        else:
            _widget = table_in.cellWidget(row, col)
            _selected_index = _widget.currentIndex()
            _value = _widget.itemText(_selected_index)
        dict_in[_label] = _value

        return dict_in

