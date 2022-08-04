from __future__ import (absolute_import, division, print_function)
import os
from qtpy.QtCore import Qt
from addie.processing.idl.step2_gui_handler import Step2GuiHandler
from addie.processing.mantid.master_table.periodic_table.material_handler \
    import get_periodictable_formatted_element_and_number_of_atoms as format_ele
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
        self.script = '/usr/bin/python ' + self.script_path
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
            f.write("%s %s\n" % (_label, self._runs[_label]["runs"]))
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
        r_max_possible = "{0:6.2F}".format(np.pi / self.q_interval_min)
        r_range = o_gui_handler.get_r_range(r_max_possible)
        self._runs["r_range"] = r_range
        self._runs["q_range"] = [q_range_min, q_range_max]
        if self.validate_table(self._runs):
            for _label in self._runs:
                if _label != "r_range" and _label != "q_range":
                    self._runs = self.collect_info_for_redpar(self._runs, _label)
                    self.write_redpar(self._runs, _label)

    def collect_info_for_redpar(self, runs_info, _label):
        chem_form_temp = runs_info[_label]["sam_formula"]
        list_element = chem_form_temp.split(" ")
        formated_ele_list = []
        for _element in list_element:
            [formated_element, number_of_atoms, case] = format_ele(_element)
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
        runs_info[_label]["sam_form_used"] = sample_form_str[:-1]

        return runs_info

    def write_redpar(self, runs_info, _label):
        file_name = runs_info[_label]["sam_name"] + ".redpar"
        with open(file_name, 'w') as f:
            f.write("{0:13s}{1:<s}\n".format("formula", runs_info[_label]["sam_form_used"]))
            f.write("{0:13s}{1:<s}\n".format("massdensity", runs_info[_label]["mass_density"]))
            f.write("{0:13s}{1:<s}\n".format("radius", runs_info[_label]["radius"]))
            f.write("{0:13s}{1:<s}\n".format("packfrac", runs_info[_label]["packing_fraction"]))
            f.write("{0:13s}{1:<s}\n".format("geometry", runs_info[_label]["geometry"]))
            if None not in runs_info["r_range"]:
                f.write("{0:13s}{1:<s}\n".format("rfilter", ",".join(runs_info["r_range"])))
            if None not in runs_info["q_range"]:
                f.write("{0:13s}{1:<s}\n".format("qfilter", ",".join(runs_info["q_range"])))
        print("[LOG] created redpar file {}".format(file_name))

    def collect_runs_checked(self):
        table = self.parent.table
        _runs = {}
        for _row_index in range(table.rowCount()):
            _selected_widget = table.cellWidget(_row_index, 0).children()[1]
            _label = str(table.item(_row_index, 1).text())
            if (_selected_widget.checkState() == Qt.Checked):
                _runs[_label] = {}
                # for Joerg's new script.
                for i in range(7):
                    _runs = self.load_table(_runs, table, _label, _row_index, i + 1)

        return _runs

    def collect_background_runs(self):
        if self.parent.background_no.isChecked():
            _background = str(self.parent.background_no_field.text())
        else:
            _background = str(self.parent.background_line_edit.text())
        return _background

    def load_table(self, dict_in, table_in, _label, row, col):
        if col != 7:
            _value = str(table_in.item(row, col).text())
            if col == 1:
                dict_in[_label]["sam_name"] = _value
            elif col == 2:
                dict_in[_label]["runs"] = _value
            elif col == 3:
                dict_in[_label]["sam_formula"] = _value
            elif col == 4:
                dict_in[_label]["mass_density"] = _value
            elif col == 5:
                dict_in[_label]["radius"] = _value
            elif col == 6:
                dict_in[_label]["packing_fraction"] = _value
        else:
            _widget = table_in.cellWidget(row, col)
            _selected_index = _widget.currentIndex()
            _value = _widget.itemText(_selected_index)
            dict_in[_label]["geometry"] = _value

        return dict_in

    def validate_table(self, runs_in):
        for _label in runs_in:
            if _label == "r_range":
                if any(runs_in[_label]) == "":
                    print("[Warning] R range info not provided and thus redpar file will not be created.")
                    return False
            elif _label == "q_range":
                if any(runs_in[_label]) == "":
                    print("[Warning] Q range info not provided and thus redpar file will not be created.")
                    return False
            else:
                for _label_1 in runs_in[_label]:
                    if runs_in[_label][_label_1] == "":
                        print("[Warning] {0:s} info not provided for {1:s}".format(_label_1, _label))
                        print("[Warning] Hence the redpar file will not be created.")
                        return False

        return True
