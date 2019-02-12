from __future__ import (absolute_import, division, print_function)
import numpy as np
from h5py import File


class SampleEnvironmentHandler(object):

    # Specify paths in NeXus files for different sample environments
    _dict_samp_env = dict()

    _dict_samp_env['cryostat'] = {'samp': {'path_to_time': '/entry/DASlogs/BL1B:SE:SampleTemp/time',
                                           'path_to_value': '/entry/DASlogs/BL1B:SE:SampleTemp/value'},
                                  'envi': {'path_to_time': '/entry/DASlogs/BL1B:SE:Cryo:TempActual/time',
                                           'path_to_value': '/entry/DASlogs/BL1B:SE:Cryo:TempActual/value'}
                                  }

    _dict_samp_env['furnace'] = {'samp': {'path_to_time': '/entry/DASlogs/BL1B:SE:SampleTemp/time',
                                          'path_to_value': '/entry/DASlogs/BL1B:SE:SampleTemp/value'},
                                 'envi': {'path_to_time': '/entry/DASlogs/BL1B:SE:ND1:Loop1:SP/time',
                                          'path_to_value': '/entry/DASlogs/BL1B:SE:ND1:Loop1:SP/value'}
                                 }

    def __init__(self, samp_env):
        self._data = dict()
        self._data['samp'] = dict()
        self._data['envi'] = dict()

        self._data['envi']['lastTime'] = 0.0
        self._data['samp']['lastTime'] = 0.0

        if samp_env in self._dict_samp_env:
            self._data['samp'].update(self._dict_samp_env[samp_env]['samp'])
            self._data['envi'].update(self._dict_samp_env[samp_env]['envi'])
        else:
            raise KeyError('The sample environment '+samp_env+' is not available')

    def getDataFromFile(self, filename, data_type):
        _data = self._data[data_type]
        nf = File(filename, 'r')
        _data['time'] = np.array(nf[_data['path_to_time']])
        _data['value'] = np.array(nf[_data['path_to_value']])
        _data['time'] = np.add(_data['lastTime'], _data['time'])
        _data['lastTime'] = _data['time'][-1]
        return _data['time'], _data['value']
