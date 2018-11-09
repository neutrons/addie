import numpy as np
import os
import pickle


try:
    from PyQt4.QtGui import QDialog, QTreeWidgetItem, QTableWidgetItem, QMenu
    from PyQt4 import QtCore, QtGui
except ImportError:
    try:
        from PyQt5.QtWidgets import QDialog, QTreeWidgetItem, QTableWidgetItem, QMenu
        from PyQt5 import QtCore, QtGui
    except ImportError:
        raise ImportError("Requires PyQt4 or PyQt5")

from addie.ui_table_tree import Ui_Dialog as UiDialog
from addie.master_table.tree_definition import tree_dict, column_default_width, CONFIG_FILE


class TableInitialization:

    default_width = column_default_width

    def __init__(self, parent=None):
        self.parent = parent
        self.tree_dict = tree_dict
#        self.parent.tree_dict = tree_dict

    def init_master_table(self):
        # set h1, h2 and h3 headers
        self.init_headers()
        self.init_table_header(table_ui=self.parent.ui.h1_table,
                               list_items=self.table_headers['h1'])
        self.init_table_header(table_ui=self.parent.ui.h2_table,
                               list_items=self.table_headers['h2'])
        self.init_table_header(table_ui=self.parent.ui.h3_table,
                               list_items=self.table_headers['h3'])

        # set h1, h2 and h3 width
        self.init_table_dimensions()
        self.init_table_col_width(table_width=self.table_width['h1'],
                                  table_ui=self.parent.ui.h1_table)
        self.init_table_col_width(table_width=self.table_width['h2'],
                                  table_ui=self.parent.ui.h2_table)
        self.init_table_col_width(table_width=self.table_width['h3'],
                                  table_ui=self.parent.ui.h3_table)

        self.h1_header_table = self.parent.ui.h1_table.horizontalHeader()
        self.h2_header_table = self.parent.ui.h2_table.horizontalHeader()
        self.h3_header_table = self.parent.ui.h3_table.horizontalHeader()

        self.make_tree_of_column_references()

        self.save_parameters()

    def init_signals(self):
        self.parent.h1_header_table.sectionResized.connect(self.parent.resizing_h1)
        self.parent.h2_header_table.sectionResized.connect(self.parent.resizing_h2)
        self.parent.h3_header_table.sectionResized.connect(self.parent.resizing_h3)

        self.parent.ui.h1_table.horizontalScrollBar().valueChanged.connect(self.parent.scroll_h1_table)
        self.parent.ui.h2_table.horizontalScrollBar().valueChanged.connect(self.parent.scroll_h2_table)
        self.parent.ui.h3_table.horizontalScrollBar().valueChanged.connect(self.parent.scroll_h3_table)

    def save_parameters(self):

        self.parent.h1_header_table = self.h1_header_table
        self.parent.h2_header_table = self.h2_header_table
        self.parent.h3_header_table = self.h3_header_table

        self.parent.table_columns_links = self.table_columns_links

        self.parent.table_width = self.table_width
        self.parent.table_headers = self.table_headers

        self.parent.tree_dict = self.tree_dict


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

        h2_index=0
        h3_index=0

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
        td = self.tree_dict

        table_width = {'h1': [], 'h2': [], 'h3': []}

        # check all the h1 headers
        for _key_h1 in td.keys():

            # if h1 header has children
            if td[_key_h1]['children']:

                absolute_nbr_h3_for_this_h1 = 0

                # loop through list of h2 header for this h1 header
                for _key_h2 in td[_key_h1]['children'].keys():

                    # if h2 has children, just count how many children
                    if td[_key_h1]['children'][_key_h2]['children']:
                        nbr_h3 = len(td[_key_h1]['children'][_key_h2]['children'])

                        for _ in np.arange(nbr_h3):
                            table_width['h3'].append(self.default_width)

                        ## h2 header will be as wide as the number of h3 children
                        table_width['h2'].append(nbr_h3 * self.default_width)

                        ## h1 header will be += the number of h3 children
                        absolute_nbr_h3_for_this_h1 += nbr_h3

                    # if h2 has no children
                    else:

                        ## h2 header is 1 wide
                        table_width['h2'].append(self.default_width)
                        table_width['h3'].append(self.default_width)

                        ## h2 header will be += 1
                        absolute_nbr_h3_for_this_h1 += 1

                table_width['h1'].append(absolute_nbr_h3_for_this_h1 * self.default_width)

            # if h1 has no children
            else:
                # h1, h2 and h3 are 1 wide
                table_width['h1'].append(self.default_width)
                table_width['h2'].append(self.default_width)
                table_width['h3'].append(self.default_width)

        self.table_width = table_width

    def init_headers(self):
        td = self.tree_dict

        table_headers = {'h1': [], 'h2': [], 'h3': []}
        for _key_h1 in td.keys():
            table_headers['h1'].append(td[_key_h1]['name'])
            if td[_key_h1]['children']:
                for _key_h2 in td[_key_h1]['children'].keys():
                    table_headers['h2'].append(td[_key_h1]['children'][_key_h2]['name'])
                    if td[_key_h1]['children'][_key_h2]['children']:
                        for _key_h3 in td[_key_h1]['children'][_key_h2]['children'].keys():
                            table_headers['h3'].append(td[_key_h1]['children'][_key_h2]['children'][_key_h3]['name'])
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

        if parent.table_tree_ui == None:
            parent.table_tree_ui = TableTree(parent=parent)
            parent.table_tree_ui.show()
            if parent.table_tree_ui_position:
                parent.table_tree_ui.move(parent.table_tree_ui_position)
        else:
            parent.table_tree_ui.activateWindow()
            parent.table_tree_ui.setFocus()

class TableTree(QDialog):

    tree_column = 0

    def __init__(self, parent=None):
        self.parent = parent
        QDialog.__init__(self, parent=parent)
        self.ui = UiDialog()
        self.ui.setupUi(self)

        self.init_tree()

    def init_tree(self):
        # fill the self.ui.treeWidget
        # self.addItems(self.ui.treeWidget.invisibleRootItem())
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

                        _h2_parent = self.addParent(_h1_parent,
                                                    td[_key_h1]['children'][_key_h2]['name'],
                                                    _key_h2)
                        td[_key_h1]['children'][_key_h2]['ui'] = _h2_parent
                        tree_ui['h2'].append(_h2_parent)

                        for _key_h3 in td[_key_h1]['children'][_key_h2]['children']:
                            _h3_child = self.addChild(_h2_parent,
                                                      td[_key_h1]['children'][_key_h2]['children'][_key_h3]['name'],
                                                      _key_h3)
                            td[_key_h1]['children'][_key_h2]['children'][_key_h3]['ui'] = _h3_child

                            set_h_indexes(td[_key_h1]['children'][_key_h2]['children'][_key_h3], h3=h3_index)
                            tree_ui['h3'].append(_h3_child)
                            h3_index += 1

                    else: # key_h2 has no children, it's a leaf
                        _h3_child = self.addChild(_h1_parent,
                                                  td[_key_h1]['children'][_key_h2]['name'],
                                                  _key_h2)
                        td[_key_h1]['children'][_key_h2]['ui'] = _h3_child
                        tree_ui['h2'].append(_h3_child)
                        tree_ui['h3'].append(None)
                        h3_index += 1

                    set_h_indexes(td[_key_h1]['children'][_key_h2], h2=h2_index)
                    h2_index += 1

            else: #_key_h1 has no children, using addChild
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
        self.ui = UiDialogSave()
        self.ui.setupUi(self)

        self.ui.save_as_value.setPlaceholderText("undefined")

    def get_defined_name_config(self):
        return str(self.ui.save_as_value.text())

    def ok_clicked(self):
        name_config = self.get_defined_name_config()
        if name_config:
            self.parent.save_as_config_name_selected(name=name_config)
            self.grand_parent.ui.statusbar.showMessage("New configuration saved ({})".format(name_config), 8000)
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

    def __init__(self, parent=None):
        self.parent = parent

    def retrieve_previous_configurations(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'rb') as handle:
                _cfg = pickle.load(handle)

                try:
                    config_dict = _cfg['configurations']
                except KeyError:
                    return

            self.parent.config_dict = config_dict

    def save_as_config(self):
        o_save_config = SaveConfigInterface(parent=self,
                                            grand_parent=self.parent)
        o_save_config.show()
        self.o_save_config = o_save_config

    def save_as_config_name_selected(self, name=''):
        self.create_config_dict(name=name)
        self.export_config()

    def create_config_dict(self, name=''):
        if name == '':
            name = 'undefined'

        o_current_table_config = TableConfig(parent=self.parent)
        current_config = o_current_table_config.get_current_config()

        inside_dict = OrderedDict()
        inside_dict['table'] = current_config
        inside_dict['active'] = True

        # retrieve previous config file
        previous_config_dict = self.parent.config_dict
        if previous_config_dict == {}:
            # first time
            new_full_config = OrderedDict()
            new_full_config[name] = inside_dict
        else:
            self.deactivate_all_config()
            old_full_config = self.parent.config_dict
            # list_keys = old_full_config.keys()
            old_full_config[name] = inside_dict
            new_full_config = old_full_config

        self.config_dict = new_full_config

    def deactivate_all_config(self):
        old_full_config = self.parent.config_dict
        for _key in old_full_config:
            old_full_config[_key]['active'] = False
        self.parent.config_dict = old_full_config

    def export_config(self):
        config_dict = self.config_dict
        with open(CONFIG_FILE, 'wb') as handle:
            full_config = {}
            full_config['configurations'] = config_dict
            pickle.dump(full_config,
                        handle,
                        protocol=pickle.HIGHEST_PROTOCOL)

    def save_config(self):
        active_config_name = self.parent.active_config_name
        self.save_as_config_name_selected(name=active_config_name)

    def reset_table(self):
        config_dict = self.parent.config_dict
        if not ("FULL_RESET" in config_dict):
            config_dict['FULL_RESET'] = self.parent.reset_config_dict
            self.parent.config_dict = config_dict

        ConfigHandler.lazy_export_config(config_dict=self.parent.config_dict)
        self.parent.load_this_config(key='FULL_RESET', resize=True)

    def right_click(self):
        self.retrieve_previous_configurations()
        previous_config = self.parent.config_dict

        if previous_config == {}:
            list_configs = []
        else:
            list_configs = previous_config.keys()

        top_menu = QMenu(self.parent)

        menu = top_menu.addMenu("Menu")
        config = menu.addMenu("Configuration ...")

        _save = config.addAction("Save")

        _save_as = config.addAction("Save As ...")

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
                    self.parent.active_config_name = _label
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
        _save.setEnabled(save_state)

        self.parent.list_config_displayed = list_config_displayed
        menu.addSeparator()
        _reset = menu.addAction("Full Reset Table/Tree")

        action = menu.exec_(QtGui.QCursor.pos())

        if action == _save_as:
            self.save_as_config()
            return

        elif action == _save:
            self.save_config()
            return

        elif action == _reset:
            self.reset_table()
            return

        if not (list_signal_config_files == []):

            # user clicked to select config
            for _index, _signal in enumerate(list_signal_config_files):
                if action == _signal:
                    self.activate_this_config(config=list_config_displayed[_index])

        if not (list_signal_remove_config == []):

            # user clicked to remove config
            for _index, _signal in enumerate(list_signal_remove_config):
                if action == _signal:
                    self.remove_this_config(config=list_config_displayed[_index])

    def remove_this_config(self, config):
        config_dict = ConfigHandler.remove_this_config(config=self.parent.config_dict,
                                                       key=config)
        self.parent.config_dict = config_dict
        # import pprint
        # pprint.pprint(config_dict)
        ConfigHandler.lazy_export_config(config_dict=config_dict)

    def activate_this_config(self, config):
        config_dict = ConfigHandler.deactivate_all_config(config=self.parent.config_dict)
        config_dict = ConfigHandler.activate_this_config(config=config_dict,
                                                         key=config)
        self.parent.config_dict = config_dict
        ConfigHandler.lazy_export_config(config_dict=config_dict)
        self.parent.load_this_config(key=config)


class TableConfig:
    '''This class will look at the h1, h2 and h3 table to create the config use width and visibility of each column'''

    def __init__(self, parent=None):
        self.parent = parent

    def get_current_config(self):
        current_config_dict = {}
        current_config_dict['h1'] = self.__get_current_table_config(table='h1')
        current_config_dict['h2'] = self.__get_current_table_config(table='h2')
        current_config_dict['h3'] = self.__get_current_table_config(table='h3')
        return current_config_dict

    def __get_current_table_config(self, table='h1'):

        if table == 'h1':
            table_ui = self.parent.ui.h1_table
        elif table == 'h2':
            table_ui = self.parent.ui.h2_table
        else:
            table_ui = self.parent.ui.h3_table

        nbr_column = table_ui.columnCount()
        _dict = {}
        for _col in np.arange(nbr_column):
            _width = table_ui.columnWidth(_col)
            _visible = not table_ui.isColumnHidden(_col)
            _dict[_col] = {'width': _width,
                           'visible': _visible}

        return _dict

    def block_table_ui(self, block_all=True,
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
            self.parent.h1_header_table.sectionResized.disconnect(self.parent.resizing_h1)
        else:
            self.parent.h1_header_table.sectionResized.connect(self.parent.resizing_h1)

        if block_h2:
            self.parent.h2_header_table.sectionResized.disconnect(self.parent.resizing_h2)
        else:
            self.parent.h2_header_table.sectionResized.connect(self.parent.resizing_h2)

        if block_h3:
            self.parent.h3_header_table.sectionResized.disconnect(self.parent.resizing_h3)
        else:
            self.parent.h3_header_table.sectionResized.connect(self.parent.resizing_h3)







