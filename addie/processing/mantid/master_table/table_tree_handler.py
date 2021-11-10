from __future__ import (absolute_import, division, print_function)

from collections import OrderedDict
import numpy as np
import os
import pickle

from qtpy.QtWidgets import QDialog, QTreeWidgetItem, QTableWidgetItem, QMenu, QFileDialog, QApplication
from addie.utilities import load_ui
from qtpy import QtCore, QtGui

from addie.utilities.file_handler import FileHandler
from addie.processing.mantid.master_table.tree_definition import TREE_DICT, COLUMN_DEFAULT_WIDTH, CONFIG_FILE
from addie.processing.mantid.master_table.tree_definition import h1_COLUMNS_WIDTH, h2_COLUMNS_WIDTH, h3_COLUMNS_WIDTH
from addie.processing.mantid.master_table.table_row_handler import TableRowHandler
from addie.processing.mantid.master_table.table_plot_handler import TablePlotHandler
from addie.processing.mantid.master_table.selection_handler import CellsHandler, RowsHandler
from addie.processing.mantid.master_table.master_table_loader import TableFileLoader
from addie.processing.mantid.master_table.master_table_exporter import TableFileExporter
from addie.widgets.filedialog import get_save_file
from addie.processing.mantid.master_table.selection_handler import rows_selected as rows_selected_valid
try:
    from addie.processing.mantid.master_table.import_from_database.oncat_authentication_handler import OncatAuthenticationHandler
    import pyoncat  # noqa
    ONCAT_ENABLED = True
except ImportError:
    print('pyoncat module not found. Functionality disabled')
    ONCAT_ENABLED = False


class TableInitialization:

    default_width = COLUMN_DEFAULT_WIDTH
    table_headers = {}
    table_width = {}

    def __init__(self, main_window=None):
        self.main_window = main_window
#        self.parent = parent
#        self.parent_ui = parent.processing_ui
        self.tree_dict = TREE_DICT

    def init_master_table(self):
        # set h1, h2 and h3 headers
        self.init_headers()
        self.init_table_header(
            table_ui=self.main_window.processing_ui.h1_table,
            list_items=self.table_headers['h1'])
        self.init_table_header(
            table_ui=self.main_window.processing_ui.h2_table,
            list_items=self.table_headers['h2'])
        self.init_table_header(
            table_ui=self.main_window.processing_ui.h3_table,
            list_items=self.table_headers['h3'])

        # set h1, h2 and h3 width
        self.init_table_dimensions()
        self.init_table_col_width(
            table_width=self.table_width['h1'],
            table_ui=self.main_window.processing_ui.h1_table)
        self.init_table_col_width(
            table_width=self.table_width['h2'],
            table_ui=self.main_window.processing_ui.h2_table)
        self.init_table_col_width(
            table_width=self.table_width['h3'],
            table_ui=self.main_window.processing_ui.h3_table)

        self.h1_header_table = self.main_window.processing_ui.h1_table.horizontalHeader()
        self.h2_header_table = self.main_window.processing_ui.h2_table.horizontalHeader()
        self.h3_header_table = self.main_window.processing_ui.h3_table.horizontalHeader()

        self.make_tree_of_column_references()
        self.save_parameters()

        _table_config = TableConfig(main_window=self.main_window)
        current_config = _table_config.get_current_config()

        inside_dict = OrderedDict()
        inside_dict['table'] = current_config
        inside_dict['active'] = False

        self.main_window.reset_config_dict = inside_dict

    def init_signals(self):
        self.main_window.h1_header_table.sectionResized.connect(
            self.main_window.resizing_h1)
        self.main_window.h2_header_table.sectionResized.connect(
            self.main_window.resizing_h2)
        self.main_window.h3_header_table.sectionResized.connect(
            self.main_window.resizing_h3)

        self.main_window.processing_ui.h1_table.horizontalScrollBar(
        ).valueChanged.connect(self.main_window.scroll_h1_table)
        self.main_window.processing_ui.h2_table.horizontalScrollBar(
        ).valueChanged.connect(self.main_window.scroll_h2_table)
        self.main_window.processing_ui.h3_table.horizontalScrollBar(
        ).valueChanged.connect(self.main_window.scroll_h3_table)

    def save_parameters(self):
        self.main_window.h1_header_table = self.h1_header_table
        self.main_window.h2_header_table = self.h2_header_table
        self.main_window.h3_header_table = self.h3_header_table

        self.main_window.table_columns_links = self.table_columns_links

        self.main_window.table_width = self.table_width
        self.main_window.table_headers = self.table_headers

        self.main_window.tree_dict = self.tree_dict

    def make_tree_of_column_references(self):
        """
        table_columns_links = {'h1': [], 'h2': [], 'h3': []}

        h1 = [0, 1, 2]  # number of h1 columns
        h2 = [[0], [1,2,3], [4]] link of h2 columns with h1
        h3 = [ [[0]], [[1,2], [3,4], [5]], [[6,7,8]] ]

        :return:
        None
        """

        h1 = []
        h2 = []
        h3 = []

        h2_index = 0
        h3_index = 0

        td = self.tree_dict
        for h1_index, _key_h1 in enumerate(td.keys()):

            h1.append(h1_index)

            if td[_key_h1]['children']:

                _h2 = []
                _h3_h2 = []
                for _key_h2 in td[_key_h1]['children']:

                    if td[_key_h1]['children'][_key_h2]['children']:

                        _h3_h3 = []
                        for _key_h3 in td[_key_h1]['children'][_key_h2]['children']:

                            _h3_h3.append(h3_index)
                            h3_index += 1

                        _h3_h2.append(_h3_h3)

                    else:
                        # h2 does not have any h3 children
                        _h3_h2.append([h3_index])
                        h3_index += 1

                    _h2.append(h2_index)
                    h2_index += 1

                h3.append(_h3_h2)
                h2.append(_h2)

            else:
                # h1 does not have any h2 children

                h2.append([h2_index])
                h3.append([[h3_index]])
                h2_index += 1
                h3_index += 1

        self.table_columns_links = {'h1': h1,
                                    'h2': h2,
                                    'h3': h3,
                                    }

    def init_table_col_width(self, table_width=[], table_ui=None):
        for _col in np.arange(table_ui.columnCount()):
            table_ui.setColumnWidth(_col, table_width[_col])

    def init_table_dimensions(self):
        table_width = {'h1': [], 'h2': [], 'h3': []}

        # Trying manual input of table dimensions
        table_width['h3'] = h3_COLUMNS_WIDTH
        table_width['h2'] = h2_COLUMNS_WIDTH
        table_width['h1'] = h1_COLUMNS_WIDTH
        self.table_width = table_width

    def init_headers(self):
        td = self.tree_dict

        table_headers = {'h1': [], 'h2': [], 'h3': []}
        for _key_h1 in td.keys():
            table_headers['h1'].append(td[_key_h1]['name'])
            if td[_key_h1]['children']:
                for _key_h2 in td[_key_h1]['children'].keys():
                    table_headers['h2'].append(
                        td[_key_h1]['children'][_key_h2]['name'])
                    if td[_key_h1]['children'][_key_h2]['children']:
                        for _key_h3 in td[_key_h1]['children'][_key_h2]['children'].keys(
                        ):
                            table_headers['h3'].append(
                                td[_key_h1]['children'][_key_h2]['children'][_key_h3]['name'])
                    else:
                        table_headers['h3'].append('')
            else:
                table_headers['h2'].append('')
                table_headers['h3'].append('')

        self.table_headers = table_headers

    def init_table_header(self, table_ui=None, list_items=None):
        table_ui.setColumnCount(len(list_items))
        for _index, _text in enumerate(list_items):
            item = QTableWidgetItem(_text)
            table_ui.setHorizontalHeaderItem(_index, item)


class TableTreeHandler:

    def __init__(self, parent=None):

        if parent.table_tree_ui is None:
            parent.table_tree_ui = TableTree(parent=parent)
            if parent.table_tree_ui_position:
                parent.table_tree_ui.move(parent.table_tree_ui_position)
            parent.table_tree_ui.show()
        else:
            parent.table_tree_ui.activateWindow()
            parent.table_tree_ui.setFocus()


class TableTree(QDialog):

    tree_column = 0

    def __init__(self, parent=None):
        self.parent = parent
        QDialog.__init__(self, parent=parent)
        self.ui = load_ui('table_tree.ui', baseinstance=self)

        self.init_tree()

    def init_tree(self):
        # fill the self.ui.treeWidget
        self.addItems(self.ui.treeWidget.invisibleRootItem())
        self.ui.treeWidget.itemChanged.connect(self.parent.tree_item_changed)

    def addParent(self, parent, title, name):
        item = QTreeWidgetItem(parent, [title])
        item.setData(self.tree_column, QtCore.Qt.UserRole, '')
        item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        item.setCheckState(self.tree_column, QtCore.Qt.Checked)
        item.setExpanded(True)
        return item

    def addChild(self, parent, title, name):
        item = QTreeWidgetItem(parent, [title])
        item.setData(self.tree_column, QtCore.Qt.UserRole, '')
        item.setCheckState(self.tree_column, QtCore.Qt.Checked)
        return item

    def addItems(self, parent):
        td = self.parent.tree_dict
        absolute_parent = parent

        tree_ui = {'h1': [],
                   'h2': [],
                   'h3': []}

        h1_index = 0
        h2_index = 0
        h3_index = 0

        def set_h_indexes(location, h1=None, h2=None, h3=None):
            location['h_index']['h1'] = h1
            location['h_index']['h2'] = h2
            location['h_index']['h3'] = h3

        for _key_h1 in td.keys():

            # if there are children, we need to use addParent
            if td[_key_h1]['children']:

                _h1_parent = self.addParent(absolute_parent,
                                            td[_key_h1]['name'],
                                            _key_h1)
                td[_key_h1]['ui'] = _h1_parent
                tree_ui['h1'].append(_h1_parent)

                for _key_h2 in td[_key_h1]['children'].keys():

                    # if there are children, we need to use addParent
                    if td[_key_h1]['children'][_key_h2]['children']:

                        _h2_parent = self.addParent(
                            _h1_parent, td[_key_h1]['children'][_key_h2]['name'], _key_h2)
                        td[_key_h1]['children'][_key_h2]['ui'] = _h2_parent
                        tree_ui['h2'].append(_h2_parent)

                        for _key_h3 in td[_key_h1]['children'][_key_h2]['children']:
                            _h3_child = self.addChild(
                                _h2_parent,
                                td[_key_h1]['children'][_key_h2]['children'][_key_h3]['name'],
                                _key_h3)
                            td[_key_h1]['children'][_key_h2]['children'][_key_h3]['ui'] = _h3_child

                            set_h_indexes(
                                td[_key_h1]['children'][_key_h2]['children'][_key_h3], h3=h3_index)
                            tree_ui['h3'].append(_h3_child)
                            h3_index += 1

                    else:  # key_h2 has no children, it's a leaf
                        _h3_child = self.addChild(
                            _h1_parent, td[_key_h1]['children'][_key_h2]['name'], _key_h2)
                        td[_key_h1]['children'][_key_h2]['ui'] = _h3_child
                        tree_ui['h2'].append(_h3_child)
                        tree_ui['h3'].append(None)
                        h3_index += 1

                    set_h_indexes(
                        td[_key_h1]['children'][_key_h2], h2=h2_index)
                    h2_index += 1

            else:  # _key_h1 has no children, using addChild
                _child = self.addChild(absolute_parent,
                                       td[_key_h1]['name'],
                                       _key_h1)
                td[_key_h1]['ui'] = _child
                tree_ui['h1'].append(_child)
                tree_ui['h2'].append(None)
                tree_ui['h3'].append(None)
                h2_index += 1

            set_h_indexes(td[_key_h1], h1=h1_index)
            h1_index += 1
            h3_index += 1

            self.tree_ui = tree_ui
            self.parent.tree_ui = tree_ui

    def closeEvent(self, c):
        self.parent.table_tree_ui = None
        self.parent.table_tree_ui_position = self.pos()


class SaveConfigInterface(QDialog):

    # config_dict = {}

    def __init__(self, parent=None, grand_parent=None):
        self.parent = parent
        self.grand_parent = grand_parent

        QDialog.__init__(self, parent=grand_parent)
        self.ui = load_ui('table_tree_save_config.ui', baseinstance=self)

        self.ui.save_as_value.setPlaceholderText("undefined")

    def get_defined_name_config(self):
        return str(self.ui.save_as_value.text())

    def ok_clicked(self):
        name_config = self.get_defined_name_config()
        if name_config:
            self.parent.save_as_config_name_selected(name=name_config)
            self.grand_parent.ui.statusbar.showMessage(
                "New configuration saved ({})".format(name_config), 8000)
            self.grand_parent.ui.statusbar.setStyleSheet("color: green")
            self.close()

    def cancel_clicked(self):
        self.close()


class ConfigHandler:
    '''This class takes care of the config dictionary manipulations'''

    @staticmethod
    def activate_this_config(key="", config={}):
        for _key in config:
            if _key == key:
                config[_key]['active'] = True
                break
        return config

    @staticmethod
    def deactivate_all_config(config={}):
        for _key in config:
            config[_key]['active'] = False
        return config

    @staticmethod
    def lazy_export_config(config_dict={}):
        with open(CONFIG_FILE, 'wb') as handle:
            full_config = {}
            full_config['configurations'] = config_dict
            pickle.dump(full_config,
                        handle,
                        protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def remove_this_config(key="", config={}):
        new_config = OrderedDict()
        for _key in config:
            if _key == key:
                pass
            else:
                new_config[_key] = config[_key]
        return new_config


class H3TableHandler:
    # object that takes care of handling the config object
    o_save_config = None
    config_dict = {}

    def __init__(self, main_window=None):
        self.main_window = main_window
        self.table_ui = main_window.processing_ui.h3_table

    def retrieve_previous_configurations(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'rb') as handle:
                _cfg = pickle.load(handle)

                try:
                    config_dict = _cfg['configurations']
                except KeyError:
                    return

            self.main_window.config_dict = config_dict

    def create_config_dict(self, name=''):
        if name == '':
            name = 'undefined'

        o_current_table_config = TableConfig(main_window=self.main_window)
        current_config = o_current_table_config.get_current_config()

        inside_dict = OrderedDict()
        inside_dict['table'] = current_config
        inside_dict['active'] = True

        # retrieve previous config file
        previous_config_dict = self.main_window.config_dict
        if previous_config_dict == {}:
            # first time
            new_full_config = OrderedDict()
            new_full_config[name] = inside_dict
        else:
            self.deactivate_all_config()
            old_full_config = self.main_window.config_dict
            # list_keys = old_full_config.keys()
            old_full_config[name] = inside_dict
            new_full_config = old_full_config

        self.config_dict = new_full_config

    def deactivate_all_config(self):
        old_full_config = self.main_window.config_dict
        for _key in old_full_config:
            old_full_config[_key]['active'] = False
        self.main_window.config_dict = old_full_config

    # Right click
    def right_click(self):
        self.retrieve_previous_configurations()
        previous_config = self.main_window.config_dict

        if previous_config == {}:
            list_configs = []
        else:
            list_configs = previous_config.keys()

        top_menu = QMenu(self.main_window)

        menu = top_menu.addMenu("Menu")

        # Selection
        activate = menu.addMenu("Activate")
        activate.setEnabled(
            self.main_window.master_table_right_click_buttons['activate']['status'])
        activate_check_all = activate.addAction("Check All")
        self.main_window.master_table_right_click_buttons[
            'activate_check_all']['ui'] = activate_check_all
        activate_uncheck_all = activate.addAction("Uncheck All")
        self.main_window.master_table_right_click_buttons[
            'activate_uncheck_all']['ui'] = activate_uncheck_all
        activate.addSeparator()
        activate_inverse = activate.addAction("Inverse")
        self.main_window.master_table_right_click_buttons['activate_inverse']['ui'] = activate_inverse

        menu.addSeparator()

        # Cells
        cells = menu.addMenu("Cell(s)")
        cells.setEnabled(
            self.main_window.master_table_right_click_buttons['cells']['status'])
        cells_copy = cells.addAction("Copy")
        self.main_window.master_table_right_click_buttons['cells_copy']['ui'] = cells_copy
        cells_paste = cells.addAction("Paste")
        self.main_window.master_table_right_click_buttons['cells_paste']['ui'] = cells_paste
        cells_paste.setEnabled(
            self.main_window.master_table_right_click_buttons['cells_paste']['status'])
        cells_clear = cells.addAction("Clear")
        self.main_window.master_table_right_click_buttons['cells_clear']['ui'] = cells_clear

        # Rows
        rows = menu.addMenu("Row")
        rows_copy = rows.addAction("Copy")
        self.main_window.master_table_right_click_buttons['rows_copy']['ui'] = rows_copy
        rows_copy.setEnabled(
            self.main_window.master_table_right_click_buttons['rows_copy']['status'])
        rows_paste = rows.addAction("Paste")
        rows_paste.setEnabled(
            self.main_window.master_table_right_click_buttons['rows_paste']['status'])
        self.main_window.master_table_right_click_buttons['rows_paste']['ui'] = rows_paste
        rows_duplicate = rows.addAction("Duplicate")
        self.main_window.master_table_right_click_buttons['rows_duplicate']['ui'] = rows_duplicate
        rows_duplicate.setEnabled(
            self.main_window.master_table_right_click_buttons['rows_duplicate']['status'])
        rows.addSeparator()
        rows_insert_blank = rows.addAction("Insert Blank")
        # rows_insert = rows.addMenu("Insert")
        # rows_insert_run_number = rows_insert.addAction("Via Run Number ...")
        #rows_insert_blank = rows_insert.addAction("Blank")
        rows_remove = rows.addAction("Remove")
        rows_remove.setEnabled(
            self.main_window.master_table_right_click_buttons['rows_remove']['status'])
        self.main_window.master_table_right_click_buttons['rows_remove']['ui'] = rows_remove

        # Table
        table = menu.addMenu("Table")

        if ONCAT_ENABLED:
            table_import_from_database = table.addMenu("Import from Database")
            table_import_from_database_replace = table_import_from_database.addAction(
                "Replace ...")
            table_import_from_database_append = table_import_from_database.addAction(
                "Append ...")
            table_import_from_database_append.setEnabled(
                self.main_window.master_table_right_click_buttons['import_from_database_append']['status'])
        else:
            table_import_from_database = None
            table_import_from_database_replace = None
            table_import_from_database_append = None

        table_import_from_config = table.addMenu("Import from Config. File")
        table_import_from_config_replace = table_import_from_config.addAction(
            "Replace ...")
        table_import_from_config_append = table_import_from_config.addAction(
            "Append ...")
        table_import_from_config_append.setEnabled(
            self.main_window.master_table_right_click_buttons['import_from_config_append']['status'])

        table_import_from_file = table.addMenu("Import from File(s)")
        table_import_from_file_replace = table_import_from_file.addAction(
            "Replace ...")
        table_import_from_file_append = table_import_from_file.addAction(
            "Append ...")
        table_import_from_file_append.setEnabled(
            self.main_window.master_table_right_click_buttons['import_from_file_append']['status'])

        table_export = table.addAction("Export ...")
        self.main_window.master_table_right_click_buttons['export']['ui'] = table_export
        table_export.setEnabled(
            self.main_window.master_table_right_click_buttons['export']['status'])
        table.addSeparator()
        table_clear = table.addAction("Clear")
        self.main_window.master_table_right_click_buttons['clear']['ui'] = table_clear
        table_clear.setEnabled(
            self.main_window.master_table_right_click_buttons['clear']['status'])

        # remove from now, waiting on user feedback to see if this is really
        # necessary
        table_reset = None
        #table_reset = table.addAction("Reset Format")
        #self.main_window.master_table_right_click_buttons['reset']['ui'] = table_reset
        # table_reset.setEnabled(self.main_window.master_table_right_click_buttons['reset']['status'])

        # configuration
        config = menu.addMenu("Columns Configuration")
        configuration_save = config.addAction("Save")
        configuration_save_as = config.addAction("Save As ...")
        list_signal_config_files = []
        list_signal_remove_config = []
        list_config_displayed = []
        save_state = False
        if not list_configs == []:
            config.addSeparator()
            for _label in list_configs:

                if _label == "FULL_RESET":
                    continue

                this_one_is_active = False

                if previous_config[_label]['active']:
                    self.main_window.active_config_name = _label
                    _full_label = u"\u2713 " + _label
                    save_state = True
                    this_one_is_active = True

                else:
                    _full_label = u"\u200b   \u200b " + _label

                list_config_displayed.append(_label)
                temp = config.addMenu(_full_label)
                if not this_one_is_active:
                    temp_select = temp.addAction("Select")
                else:
                    temp_select = temp.addAction("Reload")
                list_signal_config_files.append(temp_select)

                temp_remove = temp.addAction("Remove")
                list_signal_remove_config.append(temp_remove)

        # disable "save" button if we don't have any config activated
        configuration_save.setEnabled(save_state)
        self.main_window.list_config_displayed = list_config_displayed
        config.addSeparator()
        _reset = config.addAction("Show All Columns")

        menu.addSeparator()

        # Plot
        _plot_menu = menu.addMenu('Plot')
        self.main_window.master_table_right_click_buttons['plot']['ui'] = _plot_menu
        _plot_menu.setEnabled(
            self.main_window.master_table_right_click_buttons['plot']['status'])
        _plot_sofq = _plot_menu.addAction("S(Q) ...")
        _plot_sofq_diff_first_run_row = _plot_menu.addAction(
            "S(Q) Diff (1st run)...")
        _plot_sofq_diff_average_row = _plot_menu.addAction(
            "S(Q) Diff (Avg.)...")

        _temp_menu = _plot_menu.addMenu("Temperature")
        _plot_cryostat = _temp_menu.addAction("Cyrostat...")
        _plot_furnace = _temp_menu.addAction("Furnace...")

        action = menu.exec_(QtGui.QCursor.pos())

        # selection
        if not action:
            pass
        elif action == activate_check_all:
            self.check_all()
        elif action == activate_uncheck_all:
            self.uncheck_all()
        elif action == activate_inverse:
            self.inverse_activated_rows()

        # cells
        elif action == cells_copy:
            self.cells_copy()
        elif action == cells_paste:
            self.cells_paste()
        elif action == cells_clear:
            self.cells_clear()

        # rows
        elif action == rows_copy:
            self.rows_copy()
        elif action == rows_paste:
            self.rows_paste()
        elif action == rows_remove:
            self.rows_remove()
        elif action == rows_duplicate:
            self.rows_duplicate()

        # insert rows
        # elif action == rows_insert_run_number:
        #    self.insert_row_run_number()
        elif action == rows_insert_blank:
            self.insert_row_blank()

        # table
        elif action == table_reset:
            self.refresh_table()
        elif action == table_clear:
            self.clear_table()
        elif action == table_import_from_config_replace:
            self._import_table_from_config(clear_table=True)
        elif action == table_import_from_config_append:
            self._import_table_from_config(clear_table=False)
        elif action == table_import_from_database_replace:
            self._import_table_from_database(clear_table=True)
        elif action == table_import_from_database_append:
            self._import_table_from_database(clear_table=False)
        elif action == table_export:
            self._export_table()
        elif action == table_import_from_file_replace:
            self._import_table_from_file(clear_table=True)
        elif action == table_import_from_file_append:
            self._import_table_from_file(clear_table=False)

        # configuration
        if action == configuration_save_as:
            self.save_as_config()
        elif action == configuration_save:
            self.save_config()

        elif action == _reset:
            self.reset_table()

        # plot
        elif action == _plot_sofq:
            o_plot = TablePlotHandler(parent=self.main_window)
            o_plot.plot_sofq()
        elif action == _plot_sofq_diff_first_run_row:
            o_plot = TablePlotHandler(parent=self.main_window)
            o_plot.plot_sofq_diff_first_run_row()
        elif action == _plot_sofq_diff_average_row:
            o_plot = TablePlotHandler(parent=self.main_window)
            o_plot.plot_sofq_diff_average_row()

        # temperature
        elif action == _plot_cryostat:
            o_plot = TablePlotHandler(parent=self.main_window)
            o_plot.plot_temperature(samp_env_choice='cryostat')
        elif action == _plot_furnace:
            o_plot = TablePlotHandler(parent=self.main_window)
            o_plot.plot_temperature(samp_env_choice='furnace')

        if not (list_signal_config_files == []):

            # user clicked to select config
            for _index, _signal in enumerate(list_signal_config_files):
                if action == _signal:
                    self.activate_this_config(
                        config=list_config_displayed[_index])

        if not (list_signal_remove_config == []):

            # user clicked to remove config
            for _index, _signal in enumerate(list_signal_remove_config):
                if action == _signal:
                    self.remove_this_config(
                        config=list_config_displayed[_index])

    def check_all(self):
        '''Activate (check box in first column) all the selected rows'''
        self._set_checkbox_status()

    def uncheck_all(self):
        '''Deactivate (check box in first column) all the selected rows'''
        self._set_checkbox_status(QtCore.Qt.Unchecked)

    def _set_checkbox_status(self, status=QtCore.Qt.Checked):
        master_table_list_ui = self.main_window.master_table_list_ui
        for _key in master_table_list_ui.keys():
            _check_box_ui = master_table_list_ui[_key]['active']
            _check_box_ui.setCheckState(status)

    def inverse_activated_rows(self):
        '''Deactivate currently activated rows, and activate currently deactivated rows'''
        master_table_list_ui = self.main_window.master_table_list_ui
        for _key in master_table_list_ui.keys():
            _check_box_ui = master_table_list_ui[_key]['active']
            if _check_box_ui.checkState() == QtCore.Qt.Checked:
                _check_box_ui.setCheckState(QtCore.Qt.Unchecked)
            else:
                _check_box_ui.setCheckState(QtCore.Qt.Checked)

    def cells_copy(self):
        '''copy selected cells'''
        o_cells = CellsHandler(parent=self.main_window)
        o_cells.copy()
        self.check_status_of_right_click_buttons()

    def cells_paste(self):
        '''paste contain of cells in new selection (only if same number of cells per row'''
        o_cells = CellsHandler(parent=self.main_window)
        o_cells.paste()
        self.check_status_of_right_click_buttons()
        self.main_window.check_master_table_column_highlighting()

    def cells_clear(self):
        '''clear contain of selected cells'''
        o_cells = CellsHandler(parent=self.main_window)
        o_cells.clear()
        self.check_status_of_right_click_buttons()
        self.main_window.check_master_table_column_highlighting()

    def rows_copy(self):
        '''copy entire row'''
        o_rows = RowsHandler(parent=self.main_window)
        o_rows.parent.table_inserted_row = -1
        o_rows.parent.copied_row = -1
        o_rows.copy()
        self.check_status_of_right_click_buttons()

    def rows_paste(self):
        '''paste entire row'''
        o_rows = RowsHandler(parent=self.main_window)
        if o_rows.parent.table_inserted_row == -1:
            o_rows.paste()
        else:
            if o_rows.parent.table_inserted_row <= o_rows.parent.copied_row:
                o_rows.parent.master_table_cells_copy['row'] += 1
                o_rows.parent.copied_row += 1
            o_rows.paste()
        self.check_status_of_right_click_buttons()
        self.main_window.check_master_table_column_highlighting()

    def rows_remove(self):
        '''remove selected rows'''
        o_rows = RowsHandler(parent=self.main_window)
        o_rows.remove()
        self.check_status_of_right_click_buttons()
        self.main_window.check_master_table_column_highlighting()

    def rows_duplicate(self):
        '''duplicate currently selected rows'''
        o_row = RowsHandler(parent=self.main_window)
        row_selected = o_row.o_selection.top_row
        msg = "No row(s) selected. Highlight any cell(s) in row(s) to duplicate followed by right click."
        if not rows_selected_valid([row_selected], msg):
            self.main_window.ui.statusbar.setStyleSheet("color: red")
            self.main_window.ui.statusbar.showMessage(msg, self.main_window.statusbar_display_time)
            return
        else:
            o_table_row = TableRowHandler(main_window=self.main_window)
            o_table_row.insert_blank_row()
            o_row = RowsHandler(parent=self.main_window)
            row_selected = o_row.o_selection.top_row
            o_row.copy(row=row_selected)
            o_row.paste(row=row_selected - 1)
            self.check_status_of_right_click_buttons()
            self.main_window.check_master_table_column_highlighting()

    def refresh_table(self):
        '''reload the initial file'''
        self.check_status_of_right_click_buttons()

    def clear_table(self):
        '''clean up table'''
        nbr_row = self.main_window.processing_ui.h3_table.rowCount()
        for _ in np.arange(nbr_row):
            self.main_window.processing_ui.h3_table.removeRow(0)

        self.main_window.master_table_list_ui = {}
        self.check_status_of_right_click_buttons()

    def _import_table_from_database(self, clear_table=True):
        self.main_window.clear_master_table_before_loading = clear_table
        self.main_window.launch_import_from_database_handler()

#        OncatAuthenticationHandler(parent=self.parent, next_ui='from_database_ui')

    def _import_table_from_file(self, clear_table=True):
        _current_folder = self.main_window.current_folder
        [table_file,
         _] = QFileDialog.getOpenFileName(parent=self.main_window,
                                          caption='Select Table File ...',
                                          directory=_current_folder,
                                          filter="NeXus (*.nxsh5);; Raw (*.raw);; NeXus_old (*.nxs)")
        if table_file:
            new_path = os.path.dirname(table_file)
            self.main_window.current_folder = new_path
            if clear_table:
                self.clear_table()
            # fixme

    def _import_table_from_config(self, clear_table=True):
        _current_folder = self.main_window.current_folder
        [table_file,
         _] = QFileDialog.getOpenFileName(parent=self.main_window,
                                          caption='Select Table File ...',
                                          directory=_current_folder,
                                          filter="json (*.json);; Log (*.csv)")
        QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        if table_file:
            new_path = os.path.dirname(table_file)
            self.main_window.current_folder = new_path
            if clear_table:
                self.clear_table()

            try:
                o_dict = TableFileLoader(
                    parent=self.main_window, filename=table_file)
            except IOError as err:
                self.main_window.ui.statusbar.setStyleSheet("color: red")
                self.main_window.ui.statusbar.showMessage(
                    err.message, self.main_window.statusbar_display_time)
                QApplication.restoreOverrideCursor()
                return

            o_dict.display_dialog()
            QApplication.restoreOverrideCursor()

    def _export_table(self):
        _current_folder = self.main_window.current_folder
        _table_file, _ = get_save_file(parent=self.main_window,
                                       caption="Define Output File Name ...",
                                       directory=_current_folder,
                                       filter={'json (*.json)': 'json'})

        if _table_file:
            _file_handler = FileHandler(filename=_table_file)
            _file_handler.check_file_extension(ext_requested='json')
            _table_file = _file_handler.filename

            o_export = TableFileExporter(parent=self.main_window)
            o_export.export(_table_file)

            self.main_window.ui.statusbar.setStyleSheet("color: blue")
            self.main_window.ui.statusbar.showMessage(
                "Table has been exported in file {}".format(_table_file),
                self.main_window.statusbar_display_time)

    def insert_row_run_number(self):
        '''insert row using run number information and OnCat'''
        OncatAuthenticationHandler(
            parent=self.main_window,
            next_ui='from_run_number_ui')
        self.check_status_of_right_click_buttons()

    def insert_row_blank(self):
        '''insert a blank row'''
        o_row = TableRowHandler(main_window=self.main_window)
        o_row.insert_blank_row()
        self.main_window.table_inserted_row = o_row.inserted_row
        self.check_status_of_right_click_buttons()
        self.main_window.check_master_table_column_highlighting()

    def save_as_config(self):
        o_save_config = SaveConfigInterface(parent=self,
                                            grand_parent=self.main_window)
        o_save_config.show()
        self.o_save_config = o_save_config

    def save_as_config_name_selected(self, name=''):
        self.create_config_dict(name=name)
        self.export_config()

    def remove_this_config(self, config):
        config_dict = ConfigHandler.remove_this_config(
            config=self.main_window.config_dict, key=config)
        self.main_window.config_dict = config_dict
        ConfigHandler.lazy_export_config(config_dict=config_dict)

    def activate_this_config(self, config):
        config_dict = ConfigHandler.deactivate_all_config(
            config=self.main_window.config_dict)
        config_dict = ConfigHandler.activate_this_config(config=config_dict,
                                                         key=config)
        self.main_window.config_dict = config_dict
        ConfigHandler.lazy_export_config(config_dict=config_dict)
        self.main_window.load_this_config(key=config)

    def export_config(self):
        config_dict = self.config_dict
        with open(CONFIG_FILE, 'wb') as handle:
            full_config = {}
            full_config['configurations'] = config_dict
            pickle.dump(full_config,
                        handle,
                        protocol=pickle.HIGHEST_PROTOCOL)

    def save_config(self):
        active_config_name = self.main_window.active_config_name
        self.save_as_config_name_selected(name=active_config_name)

    def reset_table(self):
        config_dict = self.main_window.config_dict
        if not ("FULL_RESET" in config_dict):
            config_dict['FULL_RESET'] = self.main_window.reset_config_dict
            self.main_window.config_dict = config_dict

        ConfigHandler.lazy_export_config(
            config_dict=self.main_window.config_dict)
        self.main_window.load_this_config(key='FULL_RESET', resize=True)

    def check_status_of_right_click_buttons(self):
        '''check which of the right buttons can be disabled or not'''

        def _update_status(**kwargs):
            for _key in kwargs.keys():
                self.main_window.master_table_right_click_buttons[_key]['status'] = kwargs[_key]

        nbr_row = self.table_ui.rowCount()
        if nbr_row == 0:
            # table is empty
            _update_status(activate=False,
                           cells=False,
                           rows_paste=False,
                           rows_copy=False,
                           rows_duplicate=False,
                           rows_remove=False,
                           reset=False,
                           clear=False,
                           plot=False,
                           export=False,
                           import_from_config_append=False,
                           import_from_database_append=False,
                           import_from_file_append=False
                           )
        else:
            _update_status(activate=True,
                           cells=True,
                           cells_copy=True,
                           rows_copy=True,
                           rows_duplicate=True,
                           rows_remove=True,
                           reset=True,
                           clear=True,
                           export=True,
                           import_from_config_append=True,
                           import_from_database_append=True,
                           import_from_file_append=True
                           )

            if self.main_window.master_table_cells_copy['temp']:
                _update_status(cells_paste=True,
                               cells_clear=True)

            if self.main_window.master_table_cells_copy['row'] and (
                    self.main_window.master_table_cells_copy['temp'] == []):
                _update_status(rows_paste=True)

            # plot enabled if only user clicked a cell with runs


class TableConfig:
    '''This class will look at the h1, h2 and h3 table to create the config use width and visibility of each column'''

    def __init__(self, main_window=None):
        self.main_window = main_window

    def get_current_config(self):
        current_config_dict = {}
        current_config_dict['h1'] = self.__get_current_table_config(table='h1')
        current_config_dict['h2'] = self.__get_current_table_config(table='h2')
        current_config_dict['h3'] = self.__get_current_table_config(table='h3')
        return current_config_dict

    def __get_current_table_config(self, table='h1'):

        if table == 'h1':
            table_ui = self.main_window.processing_ui.h1_table
        elif table == 'h2':
            table_ui = self.main_window.processing_ui.h2_table
        else:
            table_ui = self.main_window.processing_ui.h3_table

        nbr_column = table_ui.columnCount()
        _dict = {}
        for _col in np.arange(nbr_column):
            _width = table_ui.columnWidth(_col)
            _visible = not table_ui.isColumnHidden(_col)
            _dict[_col] = {'width': _width,
                           'visible': _visible}

        return _dict

    def block_table_header_ui(self, block_all=True,
                              unblock_all=False,
                              block_h1=False,
                              block_h2=False,
                              block_h3=False):

        if block_all:
            block_h1 = True
            block_h2 = True
            block_h3 = True

        if unblock_all:
            block_h1 = False
            block_h2 = False
            block_h3 = False

        self.main_window.h1_header_table.blockSignals(block_h1)
        self.main_window.h2_header_table.blockSignals(block_h2)
        self.main_window.h3_header_table.blockSignals(block_h3)

    def disconnect_table_ui(self, block_all=True,
                            unblock_all=False,
                            block_h1=False,
                            block_h2=False,
                            block_h3=False):

        if block_all:
            block_h1 = True
            block_h2 = True
            block_h3 = True

        if unblock_all:
            block_h1 = False
            block_h2 = False
            block_h3 = False

        if block_h1:
            self.main_window.h1_header_table.sectionResized.disconnect(
                self.main_window.resizing_h1)
        else:
            self.main_window.h1_header_table.sectionResized.connect(
                self.main_window.resizing_h1)

        if block_h2:
            self.main_window.h2_header_table.sectionResized.disconnect(
                self.main_window.resizing_h2)
        else:
            self.main_window.h2_header_table.sectionResized.connect(
                self.main_window.resizing_h2)

        if block_h3:
            self.main_window.h3_header_table.sectionResized.disconnect(
                self.main_window.resizing_h3)
        else:
            self.main_window.h3_header_table.sectionResized.connect(
                self.main_window.resizing_h3)

    def get_h2_children_from_h1(self, h1=-1):
        if h1 == -1:
            return None

        table_columns_links = self.main_window.table_columns_links
        list_h2_values = table_columns_links['h2']

        return list_h2_values[h1]

    def get_last_h2_visible(self, list_h2=[]):
        if list_h2 == []:
            return None

        for _h2 in list_h2[::-1]:
            if self.main_window.processing_ui.h2_table.isColumnHidden(_h2):
                continue
            else:
                return _h2

        return None

    def get_h3_children_from_h2(self, h2=-1):
        if h2 == -1:
            return None

        table_columns_links = self.main_window.table_columns_links
        list_h3_values = table_columns_links['h3']
        list_h2_values = table_columns_links['h2']

        index_h2 = -1
        index_h1 = 0
        for h2_values in list_h2_values:
            if h2 in h2_values:
                index_h2 = h2_values.index(h2)
                break
            index_h1 += 1

        if index_h2 == -1:
            return []

        return list_h3_values[index_h1][index_h2]

    def get_last_h3_visible(self, list_h3=[]):
        if list_h3 == []:
            return None

        for _h3 in list_h3[::-1]:
            if self.main_window.processing_ui.h3_table.isColumnHidden(_h3):
                continue
            else:
                return _h3

        return None

    def get_size_column(self, h1=None, h2=None, h3=None):
        table_ui = self.get_table_ui(h1=h1, h2=h2, h3=h3)
        h = self.get_master_h(h1=h1, h2=h2, h3=h3)
        return table_ui.columnWidth(h)

    def get_table_ui(self, h1=None, h2=None, h3=None):
        '''h1, h2 or h3 are column indexes'''
        if h1 is not None:
            table_ui = self.main_window.processing_ui.h1_table
        elif h2 is not None:
            table_ui = self.main_window.processing_ui.h2_table
        elif h3 is not None:
            table_ui = self.main_window.processing_ui.h3_table
        else:
            table_ui = None
        return table_ui

    def get_master_h(self, h1=None, h2=None, h3=None):
        '''return the only defined column index from h1, h2 or h3 table'''
        if h1 is not None:
            return h1
        elif h2 is not None:
            return h2
        elif h3 is not None:
            return h3
        else:
            return None

    def set_size_column(self, h1=None, h2=None, h3=None, width=None):
        if width is None:
            return

        table_ui = self.get_table_ui(h1=h1, h2=h2, h3=h3)
        h = self.get_master_h(h1=h1, h2=h2, h3=h3)
        table_ui.setColumnWidth(h, width)

    def get_h1_parent_from_h2(self, h2=-1):
        if h2 == -1:
            return None

        table_columns_links = self.main_window.table_columns_links
        list_h2_values = table_columns_links['h2']

        h1_parent_index = 0
        for h2_values in list_h2_values:
            if h2 in h2_values:
                return h1_parent_index
            h1_parent_index += 1

        return None

    def resizing_h1_using_all_visible_h2(self, h1=None):
        '''automatically resize the h1 using all its h2 visible '''
        h2_children = self.get_h2_children_from_h1(h1=h1)
        list_visible_h2 = self.get_all_h2_visible(list_h2=h2_children)

        if list_visible_h2 is None:
            return

        full_size_h2 = 0
        for _h2 in list_visible_h2:
            full_size_h2 += self.get_size_column(h2=_h2)

        self.main_window.processing_ui.h1_table.setColumnWidth(
            h1, full_size_h2)

    def get_h_columns_from_item_name(self, item_name=None):
        # h_columns_affected = {'h1': [],
        #                       'h2': [],
        #                       'h3': [],
        #                       'list_tree_ui': [],
        #                       'list_parent_ui': []}

        if item_name is None:
            return

        h1_columns = []
        h2_columns = []
        h3_columns = []
        list_tree_ui = []
        list_parent_ui = []

        h1_global_counter = 0
        h2_global_counter = 0
        h3_global_counter = 0

        td = self.main_window.tree_dict
        for h1_global_counter, _key_h1 in enumerate(td.keys()):

            if item_name == _key_h1:
                # get all h2 and h3 of this h1

                if td[_key_h1]['children']:

                    for _key_h2 in td[_key_h1]['children']:

                        if td[_key_h1]['children'][_key_h2]['children']:

                            list_tree_ui.append(
                                td[_key_h1]['children'][_key_h2]['ui'])
                            for _key_h3 in td[_key_h1]['children'][_key_h2]['children'].keys(
                            ):
                                h3_columns.append(h3_global_counter)
                                list_tree_ui.append(
                                    td[_key_h1]['children'][_key_h2]['children'][_key_h3]['ui'])
                                h3_global_counter += 1

                        else:

                            h2_columns.append(h2_global_counter)
                            list_tree_ui.append(
                                td[_key_h1]['children'][_key_h2]['ui'])
                            h3_columns.append(h3_global_counter)

                            h2_global_counter += 1
                            h3_global_counter += 1

                    return {'h1': [h1_global_counter],
                            'h2': h2_columns,
                            'h3': h3_columns,
                            'list_tree_ui': list_tree_ui,
                            'list_parent_ui': list_parent_ui}

                else:

                    list_tree_ui.append(td[_key_h1]['ui'])
                    return {'h1': [h1_global_counter],
                            'h2': [h2_global_counter],
                            'h3': [h3_global_counter],
                            'list_tree_ui': list_tree_ui,
                            'list_parent_ui': list_parent_ui}

            else:
                # start looking into the h2 layer if it has children

                if td[_key_h1]['children']:

                    for _key_h2 in td[_key_h1]['children'].keys():

                        if item_name == _key_h2:
                            # get all h3 for this h2 and we are done

                            if td[_key_h1]['children'][_key_h2]['children']:
                                # if key_h2 has children

                                # list all h3 leaves for this h2
                                for _key_h3 in td[_key_h1]['children'][_key_h2]['children'].keys(
                                ):
                                    h3_columns.append(h3_global_counter)
                                    list_tree_ui.append(
                                        td[_key_h1]['children'][_key_h2]['children'][_key_h3]['ui'])
                                    h3_global_counter += 1

                            else:
                                h3_columns = [h3_global_counter]

                            list_tree_ui.append(
                                td[_key_h1]['children'][_key_h2]['ui'])
                            list_parent_ui.append(td[_key_h1]['ui'])
                            return {'h1': [],
                                    'h2': [h2_global_counter],
                                    'h3': h3_columns,
                                    'list_tree_ui': list_tree_ui,
                                    'list_parent_ui': list_parent_ui}

                        else:
                            # we did not find the item name yet

                            # start looking into all the h2 children (if any)
                            if td[_key_h1]['children'][_key_h2]['children']:

                                # loop through all the h3 and look for item_name. If found
                                # we are done
                                for _key_h3 in td[_key_h1]['children'][_key_h2]['children'].keys(
                                ):

                                    if item_name == _key_h3:
                                        # we found the item name at the h3 layer,
                                        # no leaf below, so we are done

                                        list_parent_ui.append(
                                            td[_key_h1]['ui'])
                                        list_parent_ui.append(
                                            td[_key_h1]['children'][_key_h2]['ui'])
                                        return {
                                            'h1': [],
                                            'h2': [],
                                            'h3': [h3_global_counter],
                                            'list_tree_ui': list_tree_ui,
                                            'list_parent_ui': list_parent_ui}

                                    else:

                                        h3_global_counter += 1

                                h2_global_counter += 1

                            else:
                                # no children, we just keep going to the next
                                # h2 (and h3)

                                h2_global_counter += 1
                                h3_global_counter += 1

                else:
                    # no children and item_name has not been found yet, so
                    # just keep going and move on to the next h1
                    h2_global_counter += 1
                    h3_global_counter += 1

        return {'h1': h1_columns,
                'h2': h2_columns,
                'h3': h3_columns,
                'list_tree_ui': list_tree_ui,
                'list_parent_ui': list_parent_ui}

    def get_item_name(self, item):
        td = self.main_window.tree_dict

        for _key_h1 in td.keys():

            if item == td[_key_h1]['ui']:
                return _key_h1

            if td[_key_h1]['children']:

                for _key_h2 in td[_key_h1]['children'].keys():

                    if item == td[_key_h1]['children'][_key_h2]['ui']:
                        return _key_h2

                    if td[_key_h1]['children'][_key_h2]['children']:

                        for _key_h3 in td[_key_h1]['children'][_key_h2]['children'].keys(
                        ):

                            if item == td[_key_h1]['children'][_key_h2]['children'][_key_h3]['ui']:
                                return _key_h3

        return None

    def change_state_tree(self, list_ui=[], list_parent_ui=[], state=0):
        """
        Will transfer the state of the parent to the children. We also need to make sure that if all the children
        are disabled, the parent gets disable as well.

        :param list_ui:
        :param list_parent_ui:
        :param state:
        :return:
        """

        # self.main_window.ui.treeWidget.blockSignals(True)

        for _ui in list_ui:
            _ui.setCheckState(0, state)

        # if the leaf is enabled, we need to make sure all the parents are
        # enabled as well.
        if state == QtCore.Qt.Checked:
            for _ui in list_parent_ui:
                _ui.setCheckState(0, state)

        self.update_full_tree_status()
        # self.main_window.ui.treeWidget.blockSignals(False)

    def update_full_tree_status(self):
        """this will update the tree_dict dictionary with the status of all the leaves"""
        td = self.main_window.tree_dict

        # clean tree
        # if all h3 of an h2 are disabled, h2 should be disabled
        # if all h2 of a h1 are disabled, h1 should be disabled
        for _key_h1 in td.keys():

            if td[_key_h1]['children']:

                all_h2_disabled = True

                for _key_h2 in td[_key_h1]['children'].keys():

                    if td[_key_h1]['children'][_key_h2]['children']:

                        all_h3_disabled = True
                        for _key_h3 in td[_key_h1]['children'][_key_h2]['children'].keys(
                        ):

                            if td[_key_h1]['children'][_key_h2]['children'][_key_h3]['ui'].checkState(
                                    0):
                                all_h3_disabled = False
                                all_h2_disabled = False
                                break

                        if all_h3_disabled:
                            # we need to make sure the h2 is disabled as well
                            td[_key_h1]['children'][_key_h2]['ui'].setCheckState(
                                0, QtCore.Qt.Unchecked)

                    else:

                        if td[_key_h1]['children'][_key_h2]['ui'].checkState(
                                0):
                            all_h2_disabled = False

                if all_h2_disabled:
                    # we need to make sure the h1 is disabled as well then
                    td[_key_h1]['ui'].setCheckState(0, QtCore.Qt.Unchecked)

        # record full tree state
        for _key_h1 in td.keys():

            td[_key_h1]['state'] = td[_key_h1]['ui'].checkState(0)

            if td[_key_h1]['children']:

                for _key_h2 in td[_key_h1]['children'].keys():

                    td[_key_h1]['children'][_key_h2]['state'] = td[_key_h1]['children'][_key_h2]['ui'].checkState(
                        0)

                    if td[_key_h1]['children'][_key_h2]['children']:

                        for _key_h3 in td[_key_h1]['children'][_key_h2]['children'].keys(
                        ):
                            td[_key_h1]['children'][_key_h2]['children'][_key_h3]['state'] = \
                                td[_key_h1]['children'][_key_h2]['children'][_key_h3]['ui'].checkState(0)

        self.main_window.tree_dict = td

    def update_table_columns_visibility(self):
        # will update the table by hiding or not the columns

        def set_column_visibility(column=-1, table_ui=None, visible=0):
            table_ui.setColumnHidden(column, not visible)

        def get_boolean_state(key=None):
            status = key['state']
            if status == QtCore.Qt.Checked:
                return True
            else:
                return False

        h2_counter = 0
        h3_counter = 0

        td = self.main_window.tree_dict

        for h1_counter, _key_h1 in enumerate(td.keys()):

            _h1_boolean_status = get_boolean_state(td[_key_h1])

            if td[_key_h1]['children']:

                for _key_h2 in td[_key_h1]['children'].keys():

                    _h2_boolean_status = get_boolean_state(
                        td[_key_h1]['children'][_key_h2])
                    set_column_visibility(
                        column=h2_counter,
                        table_ui=self.main_window.processing_ui.h2_table,
                        visible=_h2_boolean_status)

                    if td[_key_h1]['children'][_key_h2]['children']:

                        for _key_h3 in td[_key_h1]['children'][_key_h2]['children'].keys(
                        ):
                            _h3_boolean_status = get_boolean_state(
                                td[_key_h1]['children'][_key_h2]['children'][_key_h3])
                            set_column_visibility(
                                column=h3_counter,
                                table_ui=self.main_window.processing_ui.h3_table,
                                visible=_h3_boolean_status)
                            h3_counter += 1

                    else:

                        set_column_visibility(
                            column=h3_counter,
                            table_ui=self.main_window.processing_ui.h3_table,
                            visible=_h2_boolean_status)
                        h3_counter += 1

                    h2_counter += 1

            else:

                # h2 and h3 should have the same status as h1
                set_column_visibility(
                    column=h3_counter,
                    table_ui=self.main_window.processing_ui.h3_table,
                    visible=_h1_boolean_status)

                set_column_visibility(
                    column=h2_counter,
                    table_ui=self.main_window.processing_ui.h2_table,
                    visible=_h1_boolean_status)

                h2_counter += 1
                h3_counter += 1

            set_column_visibility(
                column=h1_counter,
                table_ui=self.main_window.processing_ui.h1_table,
                visible=_h1_boolean_status)

    def resizing_table(self, tree_dict={}, block_ui=True):
        '''updating the size of the columns using visibility of the various elements of the tree'''
        if tree_dict == {}:
            return

        if block_ui:
            self.disconnect_table_ui()

        # if user disabled or enabled at the h1 level, nothing to do as all the columns will be automatically
        # resized the right way
        h1 = tree_dict['h1']
        h2 = tree_dict['h2']
        h3 = tree_dict['h3']
        if not h1 == []:
            pass

        # if user clicked at the h2 level
        elif not h2 == []:

            h2 = h2[0]

            h1_parent = self.get_h1_parent_from_h2(h2=h2)
            is_h1_parent_visible = self.is_h_visible(h1=h1_parent)

            if is_h1_parent_visible:
                # resize h2 using all visible h3
                self.resizing_h2_using_all_visible_h3(h2=h2)

                # if h1 parent is visible, re-sized h1 parent using all visible
                # h2
                self.resizing_h1_using_all_visible_h2(h1=h1_parent)

            else:
                # if h1 parent is not visible, done !
                pass

        # if user clicked at the h3 level
        elif not h3 == []:

            h3 = h3[0]

            [h1_parent, h2_parent] = self.get_h1_h2_parent_from_h3(h3=h3)
            is_h2_parent_visible = self.is_h_visible(h2=h2_parent)

            if is_h2_parent_visible:
                # if we have more h3 siblings visible
                # - we need to resize h2_parent using visible h3 siblings
                # - we need to resize h1_parent using all visible h2
                self.resizing_h2_using_all_visible_h3(h2=h2_parent)
                self.resizing_h1_using_all_visible_h2(h1=h1_parent)

            else:
                # if there are no more h3 siblings then
                #      if h1_parent visible -> resize h1_parent using all h2 visible
                #      if h1_parent not visible -> Done !
                h2 = h2_parent

                h1_parent = self.get_h1_parent_from_h2(h2=h2)
                is_h1_parent_visible = self.is_h_visible(h1=h1_parent)

                if is_h1_parent_visible:
                    # if h1 parent is visible, resized h1 parent using all
                    # visible h2
                    self.resizing_h1_using_all_visible_h2(h1=h1_parent)

                else:
                    # if h1 parent is not visible, done !
                    pass

        if block_ui:
            self.disconnect_table_ui(unblock_all=True)

    def is_h_visible(self, h1=None, h2=None, h3=None):
        table_ui = self.get_table_ui(h1=h1, h2=h2, h3=h3)
        master_h = self.get_master_h(h1=h1, h2=h2, h3=h3)
        return not table_ui.isColumnHidden(master_h)

    def resizing_h2_using_all_visible_h3(self, h2=None):
        '''automatically resizing the h2 using all its h3 visible'''
        h3_children = self.get_h3_children_from_h2(h2=h2)
        list_visible_h3 = self.get_all_h3_visible(list_h3=h3_children)

        if list_visible_h3 is None:
            return

        full_size_h3 = 0
        for _h3 in list_visible_h3:
            full_size_h3 += self.get_size_column(h3=_h3)

        self.main_window.processing_ui.h2_table.setColumnWidth(
            h2, full_size_h3)

    def get_all_h2_visible(self, list_h2=[]):
        '''return the list of all the visible h2 from the list of h2 given'''
        if list_h2 == []:
            return None

        list_h2_visible = [
            _h2 for _h2 in list_h2 if not self.main_window.processing_ui.h2_table.isColumnHidden(_h2)]
        return list_h2_visible

    def get_all_h3_visible(self, list_h3=[]):
        '''return the list of all the visible h3 from the list of h3 given'''
        if list_h3 == []:
            return None

        list_h3_visible = [
            _h3 for _h3 in list_h3 if not self.main_window.processing_ui.h3_table.isColumnHidden(_h3)]
        return list_h3_visible

    def get_h1_h2_parent_from_h3(self, h3=-1):
        if h3 == -1:
            return [None, None]

        table_columns_links = self.main_window.table_columns_links
        list_h3_values = table_columns_links['h3']

        h1_parent_index = 0
        h2_parent_index = 0

        for h3_values in list_h3_values:
            for local_h3 in h3_values:
                if h3 in local_h3:
                    return [h1_parent_index, h2_parent_index]
                h2_parent_index += 1
            h1_parent_index += 1

        return [None, None]

    def update_tree_dict_and_tree(self, config_to_load={}):
        '''This method will update the tree_dict dictionary as well as the state of the tree'''

        if self.main_window.table_tree_ui is None:
            return

        if config_to_load == {}:
            return

        def from_boolean_to_ui_status(visible):
            if visible:
                return QtCore.Qt.Checked
            else:
                return QtCore.Qt.Unchecked

        def change_state_tree_widgets(list_tree_ui, list_h_columns):
            for _ui, _key in zip(list_tree_ui, list_h_columns):
                if _ui is None:
                    continue
                else:
                    _config = list_h_columns[_key]
                    _visibility = _config['visible']
                    _state = from_boolean_to_ui_status(_visibility)
                    _ui.setCheckState(0, _state)

        # self.main_window.ui.treeWidget.blockSignals(True)

        # print("config_to_load")
        # pprint.pprint(config_to_load)

        tree_ui = self.main_window.tree_ui

        # working with h1
        list_h1_columns = config_to_load['h1']
        list_h1_tree_ui = tree_ui['h1']
        change_state_tree_widgets(list_h1_tree_ui, list_h1_columns)

        # working with h2
        list_h2_columns = config_to_load['h2']
        list_h2_tree_ui = tree_ui['h2']
        change_state_tree_widgets(list_h2_tree_ui, list_h2_columns)

        # working with h3
        list_h3_columns = config_to_load['h3']
        list_h3_tree_ui = tree_ui['h3']
        change_state_tree_widgets(list_h3_tree_ui, list_h3_columns)

        # self.main_window.ui.treeWidget.blockSignals(False)

    def set_visibility_column(
            self,
            h1=None,
            h2=None,
            h3=None,
            visibility=True):
        table_ui = self.get_table_ui(h1=h1, h2=h2, h3=h3)
        h = self.get_master_h(h1=h1, h2=h2, h3=h3)
        table_ui.setColumnHidden(h, not visibility)

    def set_size_and_visibility_column(
            self,
            h1=None,
            h2=None,
            h3=None,
            width=None,
            visibility=True,
            resize=False):
        if resize:
            self.set_size_column(h1=h1, h2=h2, h3=h3, width=width)
        self.set_visibility_column(h1=h1, h2=h2, h3=h3, visibility=visibility)
