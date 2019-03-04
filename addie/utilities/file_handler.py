from __future__ import (absolute_import, division, print_function)
import os
import configparser
import numpy as np


class FileHandler(object):

    file_contain = []

    def __init__(self, filename=None):
        self.filename = filename

    @staticmethod
    def is_file_correct_extension(filename='', ext_requested='csv'):
        [_, _ext] = os.path.splitext(filename)
        if _ext == ".{}".format(ext_requested):
            return True
        return False

    def csv_parser(self):
        data = np.genfromtxt(self.filename,dtype='str',delimiter=',',comments=None)
        headers = data[0,:]
        obj = dict()
        for col_id, col_name in enumerate(headers):
            obj[col_name] = data[1:,col_id]
        return obj

    def retrieve_contain(self):
        file_contain = []
        with open(self.filename, 'r') as f:
            file_contain = f.read()
        self.file_contain = file_contain

    def check_file_extension(self, ext_requested='txt'):
        file_parsed = self.filename.split(".")
        if len(file_parsed) > 1:
            _ext = file_parsed[-1]
            if _ext != ext_requested:
                self.filename = self.filename + "." + ext_requested
        else:
            self.filename = self.filename + "." + ext_requested

    def create_ascii(self, contain=None, carriage_return=True):
        _filename = self.filename
        f = open(_filename, 'w')
        for _line in contain:
            if carriage_return:
                f.write(_line + "\n")
            else:
                f.write(_line)

        f.close()

    def create_config_parser(self, section_name='Configuration', dictionary=None):
        config = configparser.ConfigParser()
        cfgfile = open(self.filename, 'w')

        config.add_section(section_name)
        for key, value in dictionary.items():
            config.set(section_name, key, value)

        config.write(cfgfile)
        cfgfile.close()

    def is_file_writable(self):
        if os.path.exists(self.filename):
            if os.path.isfile(self.filename):
                return os.access(self.filename, os.W_OK)
            else:
                return False
        pdir = os.path.dirname(self.filename)
        if not pdir:
            pdir = '.'
        return os.access(pdir, os.W_OK)
