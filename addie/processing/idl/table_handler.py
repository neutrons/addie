from __future__ import (absolute_import, division, print_function)
#import re
import glob
import os
import numpy as np
from qtpy.QtCore import (Qt)
from qtpy.QtGui import (QCursor)
from qtpy.QtWidgets import (QFileDialog, QMenu, QMessageBox, QTableWidgetSelectionRange)

import addie.processing.idl.populate_master_table
from addie.processing.idl.export_table import ExportTable
from addie.processing.idl.import_table import ImportTable
from addie.utilities.file_handler import FileHandler
from addie.processing.idl.populate_background_widgets import PopulateBackgroundWidgets
from addie.processing.idl.sample_environment_handler import SampleEnvironmentHandler
import addie.processing.idl.step2_gui_handler
from addie.widgets.filedialog import get_save_file

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm


class TableHandler(object):

    list_selected_row = None

    def __init__(self, parent=None):
        self.parent = parent

    def retrieve_list_of_selected_rows(self):
        self.list_selected_row = []
        for _row_index in range(self.parent.postprocessing_ui.table.rowCount()):
            _widgets = self.parent.postprocessing_ui.table.cellWidget(_row_index, 0).children()
            if len(_widgets) > 0:
                _selected_widget = self.parent.postprocessing_ui.table.cellWidget(_row_index, 0).children()[1]
                if _selected_widget.checkState() == Qt.Checked:
                    _entry = self._collect_metadata(row_index=_row_index)
                    self.list_selected_row.append(_entry)

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

    def _retrieve_sample_shape(self, row_index):
        _widget = self.parent.postprocessing_ui.table.cellWidget(row_index, 7)
        _selected_index = _widget.currentIndex()
        _sample_shape = _widget.itemText(_selected_index)
        return _sample_shape

    def _retrieve_do_abs_correction(self, row_index):
        _widget = self.parent.postprocessing_ui.table.cellWidget(row_index, 8).children()[1]
        if (_widget.checkState() == Qt.Checked):
            return 'go'
        else:
            return 'nogo'

    def current_row(self):
        _row = self.parent.postprocessing_ui.table.currentRow()
        return _row

    def right_click(self, position=None):
        _duplicate_row = -1
        _plot_sofq = -1
        _remove_row = -1
        _new_row = -1
        _copy = -1
        _paste = -1
        _cut = -1
        _refresh_table = -1
        _clear_table = -1
        # _import = -1
        # _export = -1
        _check_all = -1
        _uncheck_all = -1
        _undo = -1
        _redo = -1
        _plot_sofq_diff_first_run_row = -1
        _plot_sofq_diff_average_row = -1
        _plot_cryostat = -1
        _plot_furnace = -1
        _invert_selection = -1

        menu = QMenu(self.parent)

        if self.parent.table_selection_buffer == {}:
            paste_status = False
        else:
            paste_status = True

        if (self.parent.postprocessing_ui.table.rowCount() > 0):
            _undo = menu.addAction("Undo")
            _undo.setEnabled(self.parent.undo_button_enabled)
            _redo = menu.addAction("Redo")
            _redo.setEnabled(self.parent.redo_button_enabled)
            menu.addSeparator()
            _copy = menu.addAction("Copy")
            _paste = menu.addAction("Paste")
            self._paste_menu = _paste
            _paste.setEnabled(paste_status)
            _cut = menu.addAction("Clear")
            menu.addSeparator()
            _check_all = menu.addAction("Check All")
            _uncheck_all = menu.addAction("Unchecked All")
            menu.addSeparator()
            _invert_selection = menu.addAction("Inverse Selection")
            menu.addSeparator()

        _new_row = menu.addAction("Insert Blank Row")

        if (self.parent.postprocessing_ui.table.rowCount() > 0):
            _duplicate_row = menu.addAction("Duplicate Row")
            _remove_row = menu.addAction("Remove Row(s)")

            menu.addSeparator()
            _plot_menu = menu.addMenu('Plot')
            _plot_sofq = _plot_menu.addAction("S(Q) ...")
            _plot_sofq_diff_first_run_row = _plot_menu.addAction("S(Q) Diff (1st run)...")
            _plot_sofq_diff_average_row = _plot_menu.addAction("S(Q) Diff (Avg.)...")

            _temp_menu = _plot_menu.addMenu("Temperature")
            _plot_cryostat = _temp_menu.addAction("Cyrostat...")
            _plot_furnace = _temp_menu.addAction("Furnace...")

            menu.addSeparator()
            _refresh_table = menu.addAction("Refresh/Reset Table")
            _clear_table = menu.addAction("Clear Table")

        action = menu.exec_(QCursor.pos())
        self.current_row = self.current_row()

        if action == _undo:
            self.parent.action_undo_clicked()
        elif action == _redo:
            self.parent.action_redo_clicked()
        elif action == _copy:
            self._copy()
        elif action == _paste:
            self._paste()
        elif action == _cut:
            self._cut()
        elif action == _duplicate_row:
            self._duplicate_row()
        elif action == _plot_sofq:
            self._plot_sofq()
        elif action == _plot_sofq_diff_first_run_row:
            self._plot_sofq_diff_first_run_row()
        elif action == _plot_sofq_diff_average_row:
            self._plot_sofq_diff_average_row()
        elif action == _plot_cryostat:
            self._plot_temperature(samp_env_choice='cryostat')
        elif action == _plot_furnace:
            self._plot_temperature(samp_env_choice='furnace')
        elif action == _invert_selection:
            self._inverse_selection()
        elif action == _new_row:
            self._new_row()
        elif action == _remove_row:
            self._remove_selected_rows()
        elif action == _refresh_table:
            self._refresh_table()
        elif action == _clear_table:
            self._clear_table()
        elif action == _check_all:
            self.check_all()
        elif action == _uncheck_all:
            self.uncheck_all()

    def _import(self):
        _current_folder = self.parent.current_folder
        [_table_file, _] = QFileDialog.getOpenFileName(parent=self.parent,
                                                       caption="Select File",
                                                       directory=_current_folder,
                                                       filter=("text (*.txt);; All Files (*.*)"))

        if not _table_file:
            return
        if isinstance(_table_file, tuple):
            _table_file = _table_file[0]
        new_path = os.path.dirname(_table_file)
        self.parent.current_folder = new_path

        self._clear_table()

        _import_handler = ImportTable(filename=_table_file, parent=self.parent)
        _import_handler.run()

        _pop_back_wdg = PopulateBackgroundWidgets(main_window=self.parent)
        _pop_back_wdg.run()

        _o_gui = addie.processing.idl.step2_gui_handler.Step2GuiHandler(main_window=self.parent)
        _o_gui.check_gui()

    def _export(self):
        _current_folder = self.parent.current_folder
        _table_file, _ = get_save_file(parent=self.parent,
                                       caption="Select File",
                                       directory=_current_folder,
                                       filter={'text (*.txt)':'txt', 'All Files (*.*)':''})
        if not _table_file:
            return
        if isinstance(_table_file, tuple):
            _table_file = _table_file[0]

        _file_handler = FileHandler(filename=_table_file)
        _file_handler.check_file_extension(ext_requested='txt')
        _table_file = _file_handler.filename

        _export_handler = ExportTable(parent=self.parent,
                                      filename=_table_file)
        _export_handler.run()

    def _copy(self):
        _selection = self.parent.postprocessing_ui.table.selectedRanges()
        _selection = _selection[0]
        left_column = _selection.leftColumn()
        right_column = _selection.rightColumn()
        top_row = _selection.topRow()
        bottom_row = _selection.bottomRow()

        self.parent.table_selection_buffer = {'left_column': left_column,
                                              'right_column': right_column,
                                              'top_row': top_row,
                                              'bottom_row': bottom_row}
        self._paste_menu.setEnabled(True)

    def _paste(self, _cut=False):
        _copy_selection = self.parent.table_selection_buffer
        _copy_left_column = _copy_selection['left_column']

        # make sure selection start at the same column
        _paste_selection = self.parent.postprocessing_ui.table.selectedRanges()
        _paste_left_column = _paste_selection[0].leftColumn()

        if not (_copy_left_column == _paste_left_column):
            QMessageBox.warning(self.parent,
                                "Check copy/paste selection!",
                                "Check your selection!                   ")
            return

        _copy_right_column = _copy_selection["right_column"]
        _copy_top_row = _copy_selection["top_row"]
        _copy_bottom_row = _copy_selection["bottom_row"]

        _paste_top_row = _paste_selection[0].topRow()

        index = 0
        for _row in range(_copy_top_row, _copy_bottom_row+1):
            _paste_row = _paste_top_row + index
            for _column in range(_copy_left_column, _copy_right_column + 1):

                if _column in np.arange(1, 7):
                    if _cut:
                        _item_text = ''
                    else:
                        _item_text = self.retrieve_item_text(_row, _column)
                    self.paste_item_text(_paste_row, _column, _item_text)

                if _column == 7:
                    if _cut:
                        _widget_index = 0
                    else:
                        _widget_index = self.retrieve_sample_shape_index(_row)
                    self.set_widget_index(_widget_index, _paste_row)

                if _column == 8:
                    if _cut:
                        _widget_state = Qt.Unchecked
                    else:
                        _widget_state = self.retrieve_do_abs_correction_state(_row)
                    self.set_widget_state(_widget_state, _paste_row)

            index += 1

    def _inverse_selection(self):
        selected_range = self.parent.postprocessing_ui.table.selectedRanges()
        nbr_column = self.parent.postprocessing_ui.table.columnCount()

        self.select_all(status=True)

        # inverse selected rows
        for _range in selected_range:
            _range.leftColumn = 0
            _range.rightColun = nbr_column-1
            self.parent.postprocessing_ui.table.setRangeSelected(_range, False)

    def select_all(self, status=True):
        nbr_row = self.parent.postprocessing_ui.table.rowCount()
        nbr_column = self.parent.postprocessing_ui.table.columnCount()
        _full_range = QTableWidgetSelectionRange(0, 0, nbr_row-1, nbr_column-1)
        self.parent.postprocessing_ui.table.setRangeSelected(_full_range, status)

    def check_all(self):
        self.select_first_column(status=True)

    def uncheck_all(self):
        self.select_first_column(status=False)

    def select_row(self, row=-1, status=True):
        nbr_column = self.parent.postprocessing_ui.table.columnCount()
        _range = QTableWidgetSelectionRange(row, 0, row, nbr_column-1)
        self.parent.postprocessing_ui.table.setRangeSelected(_range, status)

    def check_row(self, row=-1, status=True):
        _widgets = self.parent.postprocessing_ui.table.cellWidget(row, 0).children()
        if len(_widgets) > 0:
            _selected_widget = self.parent.postprocessing_ui.table.cellWidget(row, 0).children()[1]
            _selected_widget.setChecked(status)

    def select_first_column(self, status=True):
        for _row in range(self.parent.postprocessing_ui.table.rowCount()):
            _widgets = self.parent.postprocessing_ui.table.cellWidget(_row, 0).children()
            if len(_widgets) > 0:
                _selected_widget = self.parent.postprocessing_ui.table.cellWidget(_row, 0).children()[1]
                _selected_widget.setChecked(status)

        _o_gui = addie.processing.idl.step2_gui_handler.Step2GuiHandler(main_window=self.parent)
        _o_gui.check_gui()

    def check_selection_status(self, state, row):
        list_ranges = self.parent.postprocessing_ui.table.selectedRanges()
        for _range in list_ranges:
            bottom_row = _range.bottomRow()
            top_row = _range.topRow()
            range_row = list(range(top_row, bottom_row + 1))

            for _row in range_row:
                _widgets = self.parent.postprocessing_ui.table.cellWidget(_row, 0).children()
                if len(_widgets) > 0:
                    _selected_widget = self.parent.postprocessing_ui.table.cellWidget(_row, 0).children()[1]
                    _selected_widget.setChecked(state)

        _o_gui = addie.processing.idl.step2_gui_handler.Step2GuiHandler(main_window=self.parent)
        _o_gui.check_gui()

    def _cut(self):
        self._copy()
        self._paste(_cut=True)

    def _duplicate_row(self):
        _row = self.current_row
        metadata_to_copy = self._collect_metadata(row_index=_row)
        o_populate = addie.processing.idl.populate_master_table.PopulateMasterTable(main_window=self.parent)
        o_populate.add_new_row(metadata_to_copy, row=_row)

    def _plot_fetch_files(self, file_type='SofQ'):
        if file_type == 'SofQ':
            search_dir = './SofQ'
            prefix = 'NOM_'
            suffix = 'SQ.dat'
        elif file_type == 'nexus':
            cwd = os.getcwd()
            search_dir = cwd[:cwd.find('shared')]+'/nexus'
            prefix = 'NOM_'
            suffix = '.nxs.h5'
            #ipts = int(re.search(r"IPTS-(\d*)\/", os.getcwd()).group(1))

        _row = self.current_row
        _row_runs = self._collect_metadata(row_index=_row)['runs'].split(',')

        output_list = list()
        file_list = [a_file for a_file in glob.glob(search_dir+'/'+prefix+'*')]
        for run in _row_runs:
            the_file = search_dir+'/'+prefix+str(run)+suffix
            if the_file in file_list:
                output_list.append({'file': the_file, 'run': run})

        return output_list

    def _plot_fetch_data(self):
        file_list = self._plot_fetch_files(file_type='SofQ')

        for data in file_list:
            with open(data['file'], 'r') as handle:
                x, y, e = np.loadtxt(handle, unpack=True)
                data['x'] = x
                data['y'] = y

        return file_list

    def _plot_datasets(self, datasets, shift_value=1.0, cmap_choice='inferno', title=None):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        # configure plot
        cmap = plt.get_cmap(cmap_choice)
        cNorm = colors.Normalize(vmin=0, vmax=len(datasets))
        scalarMap = cm.ScalarMappable(norm=cNorm, cmap=cmap)
        mrks = [0, -1]

        # plot data
        shifter = 0.0
        for idx, data in enumerate(datasets):
            data['y'] += shifter

            colorVal = scalarMap.to_rgba(idx)

            if 'linestyle' in data:
                ax.plot(data['x'], data['y'], data['linestyle']+'o', label=data['run'], color=colorVal, markevery=mrks,)
            else:
                ax.plot(data['x'], data['y'], label=data['run'], color=colorVal, markevery=mrks)
            shifter += shift_value
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1], title='Runs', loc='center left', bbox_to_anchor=(1, 0.5))
        if title:
            fig.suptitle(title)
        plt.show()

    def _plot_sofq(self):
        sofq_datasets = self._plot_fetch_data()
        self._plot_datasets(sorted(sofq_datasets, key=lambda k: int(k['run'])), title='S(Q)')

    def _plot_sofq_diff_first_run_row(self):
        sofq_datasets = self._plot_fetch_data()
        sofq_base = dict(sofq_datasets[0])

        for sofq in sorted(sofq_datasets, key=lambda k: int(k['run'])):
            sofq['y'] = sofq['y'] - sofq_base['y']

        self._plot_datasets(sofq_datasets, shift_value=0.2, title='S(Q) - S(Q) for run '+sofq_base['run'])

    def _plot_sofq_diff_average_row(self):
        sofq_datasets = self._plot_fetch_data()

        sofq_data = [sofq['y'] for sofq in sofq_datasets]
        sofq_avg = np.average(sofq_data, axis=0)
        for sofq in sorted(sofq_datasets, key=lambda k: int(k['run'])):
            sofq['y'] = sofq['y'] - sofq_avg

        self._plot_datasets(sofq_datasets, shift_value=0.2, title='S(Q) - <S(Q)>')

    def _plot_temperature(self, samp_env_choice=None):
        file_list = self._plot_fetch_files(file_type='nexus')
        samp_env = SampleEnvironmentHandler(samp_env_choice)

        datasets = list()
        for data in file_list:
            samp_x, samp_y = samp_env.getDataFromFile(data['file'], 'samp')
            envi_x, envi_y = samp_env.getDataFromFile(data['file'], 'envi')

            print(data['file'])
            datasets.append({'run': data['run'] + '_samp', 'x': samp_x, 'y': samp_y, 'linestyle': '-'})
            datasets.append({'run': None, 'x': envi_x, 'y': envi_y, 'linestyle': '--'})

        self._plot_datasets(sorted(datasets, key=lambda k: k['run']),
                            shift_value=0.0, title='Temperature: '+samp_env_choice)

    def _new_row(self):
        _row = self.current_row
        if _row == -1:
            _row = 0
        o_populate = addie.processing.idl.populate_master_table.PopulateMasterTable(main_window=self.parent)
        _metadata = o_populate.empty_metadata()
        o_populate.add_new_row(_metadata, row=_row)

    def _remove_selected_rows(self):
        selected_range = self.parent.postprocessing_ui.table.selectedRanges()
        _nbr_row_removed = 0
        _local_nbr_row_removed = 0
        for _range in selected_range:
            _top_row = _range.topRow()
            _bottom_row = _range.bottomRow()
            nbr_row = _bottom_row - _top_row + 1
            for i in np.arange(nbr_row):
                self._remove_row(row=_top_row - _nbr_row_removed)
                _local_nbr_row_removed += 1
            _nbr_row_removed = _local_nbr_row_removed

        _pop_back_wdg = PopulateBackgroundWidgets(main_window=self.parent)
        _pop_back_wdg.run()

    def _remove_row(self, row=-1):
        if row == -1:
            row = self.current_row
        self.parent.postprocessing_ui.table.removeRow(row)

        _o_gui = addie.processing.idl.step2_gui_handler.Step2GuiHandler(main_window=self.parent)
        _o_gui.check_gui()

    def _refresh_table(self):
        self.parent.populate_table_clicked()

        _o_gui = addie.processing.idl.step2_gui_handler.Step2GuiHandler(main_window=self.parent)
        _o_gui.check_gui()

    def _clear_table(self):
        _number_of_row = self.parent.postprocessing_ui.table.rowCount()
        self.parent.postprocessing_ui.table.setSortingEnabled(False)
        for _row in np.arange(_number_of_row):
            self.parent.postprocessing_ui.table.removeRow(0)
        self.parent.postprocessing_ui.background_line_edit.setText("")
        self.parent.postprocessing_ui.background_comboBox.clear()

        _o_gui = addie.processing.idl.step2_gui_handler.Step2GuiHandler(main_window=self.parent)
        _o_gui.check_gui()

    def set_widget_state(self, _widget_state, _row):
        _widget = self.parent.postprocessing_ui.table.cellWidget(_row, 8).children()[1]
        _widget.setCheckState(_widget_state)

    def retrieve_do_abs_correction_state(self, _row):
        _widget = self.parent.postprocessing_ui.table.cellWidget(_row, 8).children()[1]
        return _widget.checkState()

    def set_widget_index(self, _widget_index, _row):
        _widget = self.parent.postprocessing_ui.table.cellWidget(_row, 7)
        _widget.setCurrentIndex(_widget_index)

    def paste_item_text(self, _row, _column, _item_text):
        _item = self.parent.postprocessing_ui.table.item(_row, _column)
        _item.setText(_item_text)

    def retrieve_sample_shape_index(self, row_index):
        _widget = self.parent.postprocessing_ui.table.cellWidget(row_index, 7)
        _selected_index = _widget.currentIndex()
        return _selected_index

    def retrieve_item_text(self, row, column):
        _item = self.parent.postprocessing_ui.table.item(row, column)
        if _item is None:
            return ''
        else:
            return str(_item.text())

    def name_search(self):
        nbr_row = self.parent.postprocessing_ui.table.rowCount()
        if nbr_row == 0:
            return

        _string = str(self.parent.postprocessing_ui.name_search.text()).lower()
        if _string == '':
            self.select_all(status=False)
        else:
            for _row in range(nbr_row):
                _text_row = str(self.parent.postprocessing_ui.table.item(_row, 1).text()).lower()
                if _string in _text_row:
                    self.select_row(row=_row, status=True)
