from __future__ import (absolute_import, division, print_function)
from qtpy.QtCore import Qt
import os
import numpy as np
import glob
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm

from addie.processing.idl.sample_environment_handler import SampleEnvironmentHandler


class TablePlotHandler:

    def __init__(self, parent=None):
        self.parent = parent

    def plot_sofq(self):
        sofq_datasets = self._plot_fetch_data()
        self._plot_datasets(sorted(sofq_datasets,
                                   key=lambda k: int(k['run'])),
                            title='S(Q)')

    def plot_sofq_diff_first_run_row(self):
        sofq_datasets = self._plot_fetch_data()
        sofq_base  = dict(sofq_datasets[0])

        for sofq in sorted(sofq_datasets,
                           key=lambda k: int(k['run'])):
            sofq['y'] = sofq['y'] - sofq_base['y']

        self._plot_datasets(sofq_datasets,
                            shift_value=0.2,
                            title='S(Q) - S(Q) for run '+sofq_base['run'])

    def plot_sofq_diff_average_row(self):
        sofq_datasets = self._plot_fetch_data()

        sofq_data = [ sofq['y'] for sofq in sofq_datasets ]
        sofq_avg = np.average(sofq_data,axis=0)
        for sofq in sorted(sofq_datasets, key=lambda k: int(k['run'])):
            sofq['y'] = sofq['y'] - sofq_avg

        self._plot_datasets(sofq_datasets,
                            shift_value=0.2,
                            title='S(Q) - <S(Q)>')

    def _plot_temperature(self, samp_env_choice=None):
        file_list = self._plot_fetch_files(file_type='nexus')
        samp_env = SampleEnvironmentHandler(samp_env_choice)

        datasets = list()
        for data in file_list:
            samp_x, samp_y = samp_env.getDataFromFile(data['file'], 'samp')
            envi_x, envi_y = samp_env.getDataFromFile(data['file'], 'envi')

            datasets.append({'run': data['run'] + '_samp',
                             'x': samp_x,
                             'y': samp_y,
                             'linestyle': '-'})
            datasets.append({'run': None,
                             'x': envi_x,
                             'y': envi_y,
                             'linestyle': '--'})

        self._plot_datasets(sorted(datasets,
                                   key=lambda k: k['run']),
                            shift_value=0.0,
                            title='Temperature: ' + samp_env_choice)

    # utilities functions

    def _plot_fetch_data(self):
        file_list = self._plot_fetch_files(file_type='SofQ')

        for data in file_list:
            with open(data['file'], 'r') as handle:
                x, y, e = np.loadtxt(handle, unpack=True)
                data['x'] = x
                data['y'] = y

        return file_list

    def _plot_fetch_files(self, file_type='SofQ'):
        if file_type == 'SofQ':
            search_dir = './SofQ'
            prefix = 'NOM_'
            suffix = 'SQ.dat'
        elif file_type == 'nexus':
            cwd = os.getcwd()
            search_dir = cwd[:cwd.find('shared')] + '/nexus'
            prefix = 'NOM_'
            suffix = '.nxs.h5'
            # ipts = int(re.search(r"IPTS-(\d*)\/", os.getcwd()).group(1))

        _row = self.current_row
        _row_runs = self._collect_metadata(row_index=_row)['runs'].split(',')

        output_list = list()
        file_list = [a_file for a_file in glob.glob(search_dir + '/' + prefix + '*')]
        for run in _row_runs:
            the_file = search_dir + '/' + prefix + str(run) + suffix
            if the_file in file_list:
                output_list.append({'file': the_file, 'run': run})

        return output_list

    def _plot_datasets(self,datasets,shift_value=1.0,cmap_choice='inferno',title=None):
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)

        # configure plot
        cmap = plt.get_cmap(cmap_choice)
        cNorm = colors.Normalize(vmin=0, vmax=len(datasets) )
        scalarMap = cm.ScalarMappable(norm=cNorm, cmap=cmap)
        mrks=[0,-1]

        # plot data
        shifter = 0.0
        for idx, data in enumerate(datasets):
            data['y'] += shifter

            colorVal = scalarMap.to_rgba(idx)

            if 'linestyle' in data:
                ax.plot(data['x'],data['y'],data['linestyle']+'o',label=data['run'],color=colorVal,markevery=mrks,)
            else:
                ax.plot(data['x'],data['y'],label=data['run'],color=colorVal,markevery=mrks)
            shifter += shift_value
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1], title='Runs', loc='center left',bbox_to_anchor=(1,0.5))
        if title:
            fig.suptitle(title)
        plt.show()

    def _collect_metadata(self, row_index=-1):
        if row_index == -1:
            return []

        _name = self.retrieve_item_text(row_index, 1)
        _runs = self.retrieve_item_text(row_index, 2)
        _sample_formula = self.retrieve_item_text(row_index, 3)
        _mass_density = self.retrieve_item_text(row_index, 4)
        _radius = self.retrieve_item_text(row_index, 5)
        _packing_fraction = self.retrieve_item_text(row_index, 6)
        _sample_shape = self._retrieve_sample_shape(row_index)
        _do_abs_correction = self._retrieve_do_abs_correction(row_index)

        _metadata = {'name': _name,
                     'runs': _runs,
                     'sample_formula': _sample_formula,
                     'mass_density': _mass_density,
                     'radius': _radius,
                     'packing_fraction': _packing_fraction,
                     'sample_shape': _sample_shape,
                     'do_abs_correction': _do_abs_correction}

        return _metadata

    def retrieve_item_text(self, row, column):
        _item = self.parent.table.item(row, column)
        if _item is None:
            return ''
        else:
            return str(_item.text())

    def _retrieve_sample_shape(self, row_index):
        _widget = self.parent.table.cellWidget(row_index, 7)
        _selected_index = _widget.currentIndex()
        _sample_shape = _widget.itemText(_selected_index)
        return _sample_shape

    def _retrieve_do_abs_correction(self, row_index):
        _widget = self.parent.table.cellWidget(row_index, 8).children()[1]
        if (_widget.checkState() == Qt.Checked):
            return 'go'
        else:
            return 'nogo'
