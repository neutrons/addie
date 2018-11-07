import numpy as np

try:
    from PyQt4.QtGui import QDialog, QTreeWidgetItem, QTableWidgetItem
    from PyQt4 import QtCore
except ImportError:
    try:
        from PyQt5.QtWidgets import QDialog, QTreeWidgetItem, QTableWidgetItem
        from PyQt5 import QtCore
    except ImportError:
        raise ImportError("Requires PyQt4 or PyQt5")

from addie.ui_table_tree import Ui_Dialog as UiDialog
from addie.master_table.tree_definition import tree_dict, column_default_width


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
            table_tree_ui = TableTree(parent=parent)
            table_tree_ui.show()
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
        self.ui.treeWidget.itemChanged.connect(self.tree_item_changed)

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

    def tree_item_changed(self, item, _):
        pass


    def closeEvent(self):
        self.parent.table_tree_ui = None

