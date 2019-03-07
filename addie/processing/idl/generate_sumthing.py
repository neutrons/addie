# -*- coding: utf-8 -*-
"""
reads in a los.txt file, writes out auto_sum.inp file
"""
from __future__ import (absolute_import, division, print_function)
from collections import defaultdict
import os.path
import re
from qtpy.QtWidgets import QMessageBox

from addie.utilities.file_handler import FileHandler


class GenerateSumthing(object):

    input_file_old_format = 'los.txt'
    input_file_new_format = 'los.csv'
    output_inp_file = 'auto_sum.inp'

    def __init__(self, parent=None, folder=None):
        self.parent = parent
        self.folder = folder

    def create_sum_inp_file(self):

        # try new format (csv) with comma separated and scan column
        full_input_file_name_new_format = os.path.join(self.folder, self.input_file_new_format)
        if os.path.isfile(full_input_file_name_new_format):
            self.create_sum_inp_file_from_new_format(full_input_file_name_new_format)
            if self.is_sum_inp_file_not_empty():
                return

        # try old format with space separated columns
        full_input_file_name_old_format = os.path.join(self.folder, self.input_file_old_format)
        if os.path.isfile(full_input_file_name_old_format):
            self.create_sum_inp_file_from_old_format(full_input_file_name_old_format)
            if not self.is_sum_inp_file_not_empty():
                raise ValueError("Format of file not compatible!")

        else:
            raise IOError("lost.* file does not exist!")

    def is_sum_inp_file_not_empty(self):
        full_output_file_name = os.path.join(self.folder, self.output_inp_file)
        _o_file = FileHandler(filename=full_output_file_name)
        _o_file.retrieve_contain()
        _file_contain = _o_file.file_contain
        if len(_file_contain) == 12:
            return False
        return True

    def open_output_file_if_writable(self, full_output_file_name):
        _o_file = FileHandler(filename=full_output_file_name)
        if _o_file.is_file_writable():
            outfile = open(full_output_file_name, "w")
        else:
            title = "No write permissions!"
            error_msg = "Unable to write cached table. " + \
                        "Will not be able to write output files to this directory. " + \
                        "\n\nCheck file and directory for write permissions!"
            QMessageBox.warning(self.parent, title, error_msg)
            outfile = None
        return outfile

    def write_outfile(self, outfile, run_nums):
        outfile.write("background \n")
        for key in sorted(run_nums.keys()):
            outbit = str(run_nums[key])
            outbit = outbit.replace("[", "")
            outbit = outbit.replace("]", "")
            outbit = outbit.replace(" ", "")
            outfile.write(key + " " + outbit+"\n")

        outfile.close()

    def create_sum_inp_file_from_new_format(self,  full_input_file_name):

        #        print("]LOG]  Format: comma separated, no scan infos")
        #        print("[LOG] Reading %s" %full_input_file_name)
        name_list = []
        run_nums = defaultdict(list)

        with open(full_input_file_name, "r") as myfile:
            data = myfile.readlines()

        data = data[1:]
        for _row in data:
            _row_split = _row.split(',')

            if len(_row_split) == 8:
                temp_range = _row_split[7].replace("K", "").split('to')
                from_temp = round(float(temp_range[0]))
                temp_name = str(from_temp).replace(".0", "")

                word = _row_split[-2].strip()
                word = word.replace(":", "_")
                word = word.replace(" ", "_")

                word = word + "_" + temp_name + "K"

            else:
                word = _row_split[-1].strip()

                # stripping "at temperature" if True
                if self.parent.remove_dynamic_temperature_flag:
                    word = re.sub(" at temperature.*$", "", word)
                word = word.replace(":", "_")
                word = word.replace(" ", "_")

            run_num = int(_row_split[0])

            run_nums[word].append(run_num)
            if not (word in name_list):
                name_list.append(word)

        full_output_file_name = os.path.join(self.folder, self.output_inp_file)
        outfile = self.open_output_file_if_writable(full_output_file_name)

        if outfile:
            self.write_outfile(outfile, run_nums)

    def create_sum_inp_file_from_old_format(self, full_input_file_name):

        #        print("]LOG]  Format: space separated, with scan infos")
        #        print("[LOG] Reading %s" %full_input_file_name)
        name_list = []
        run_nums = defaultdict(list)

        with open(full_input_file_name, "r") as myfile:
            data = myfile.readlines()

        for i in range(0, len(data)):
            if len(data[i].split()) == 9:
                if data[i].split()[7] == "scan":
                    word = data[i].split()[6]
                    run_num = int(data[i].split()[0])
                    temp_name = round(float(data[i].split()[8].replace("K", "")))
                    temp_name = str(temp_name).replace(".0", "")
                    word = word.replace("(", "")
                    word = word.replace(")", "_")
                    word = word+"_"+temp_name+"K"
                    if word in name_list:
                        run_nums[word].append(run_num)
                    else:
                        name_list.append(word)
                        run_nums[word].append(run_num)

        full_output_file_name = os.path.join(self.folder, self.output_inp_file)

        full_output_file_name = os.path.join(self.folder, self.output_inp_file)
        outfile = self.open_output_file_if_writable(full_output_file_name)

        if outfile:
            self.write_outfile(outfile, run_nums)

        outfile = open(full_output_file_name, "w")
        outfile.write("background \n")
