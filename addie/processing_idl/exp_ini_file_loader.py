from __future__ import (absolute_import, division, print_function)


class ExpIniFileLoader(object):

    metadata = None

    def __init__(self, full_file_name=None):
        self.full_file_name = full_file_name
        self._retrieve_metadata()

    def _retrieve_metadata(self):
        _metadata = {}

        f = open(self.full_file_name, 'r')
        _file_contain = f.read()
        _file_array = _file_contain.split('\n')
        for _entry in _file_array:
            if not(_entry.strip() == ""):
                [key, value] = self.isolate_key_value(_entry)
                _metadata[key] = value

        self.metadata = _metadata

    def isolate_key_value(self, entry):
        _line_array = entry.split(' ')
        if len(_line_array) > 1:
            return [_line_array[0], _line_array[1]]
