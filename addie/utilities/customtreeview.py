# Modified from vdriverunmanagertree.py
# Note: Child cannot be in the same column as parent
# Note: In TreeView, QModelIndex and QStandardItem points to the same leaf.
#       But QModelIndex.data() and QStandardItem.data() are different!
#       The variable set to QStandardItem can be only retrieved by QModelIndex.data()
from __future__ import (absolute_import, division, print_function)
from qtpy.QtCore import (Qt, QModelIndex, QVariant)
from qtpy.QtWidgets import (QAbstractItemView, QHeaderView, QScrollBar, QTreeView)
from qtpy.QtGui import (QStandardItem, QStandardItemModel)


class CustomizedTreeView(QTreeView):
    """ Customized TreeView for data management
    """

    def __init__(self, parent=None):
        """ Initialization
        :param parent: parent window
        :return:
        """
        QTreeView.__init__(self, parent)
        self._myParent = parent

        # Enabled to select multiple items with shift key
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.setHorizontalScrollBar(QScrollBar())
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.setContextMenuPolicy(Qt.ActionsContextMenu)

        # Data structure to control the items
        self._leafDict = dict()  # dictionary for the name each leaf and its child. key is string only!
        self._mainNodeDict = dict()  # dictionary for each main node
        self._myHeaderList = list()
        self._childrenInOrder = True

    def _add_child_item(self, parent_item, child_item_value, append):
        """
        Add a child item
        :param parent_item:
        :param child_item_value:
        :param append:
        :return:
        """
        # Check
        assert(isinstance(parent_item, QStandardItem))
        assert(isinstance(child_item_value, str))
        assert(child_item_value != '')
        assert(isinstance(append, bool))

        parent_value = str(parent_item.text())
        if parent_value not in self._leafDict:
            raise RuntimeError('No parent leaf with key value %s' % parent_value)
        elif child_item_value in self._leafDict[parent_value]:
            raise RuntimeError('Child item %s has existed in parent %s. '
                               'Unable to add duplicate item!' % (child_item_value, parent_value))

        # New item
        # child_item = QStandardItem(child_item_value)
        child_item = QStandardItem(str(child_item_value))
        self._leafDict[parent_value].append(child_item_value)
        if append is False:
            self._leafDict[parent_value].sort()

        if append is True:
            # Append
            num_children = parent_item.rowCount()
            parent_item.setChild(num_children, 0, child_item)
        else:
            # Insert
            row_number = self._leafDict[parent_value].index(child_item_value)
            parent_item.insertRow(row_number, [child_item])

    def add_child_current_item(self, child_value):
        """

        :param child_value:
        :return:
        """
        current_index = self.currentIndex()
        assert(isinstance(current_index, QModelIndex))
        current_row = current_index.row()
        print('[DEV] Current Index of Row = %d ' % current_row)

        # Get model
        my_model = self.model()
        assert(isinstance(my_model, QStandardItemModel))
        current_item = my_model.itemFromIndex(current_index)
        if current_item is None:
            print('[INFO] Current item has not been set up.')
            return

        self._add_child_item(current_item, child_value, False)

    def add_child_main_item(self, main_item_value, child_value):
        """ Add a child under a main item with given name
        :return: boolean. True: add the child item successfully. False: unable to add child due to being duplicate.
        """
        main_item_value = str(main_item_value)
        child_value = str(child_value)

        # find the main item value
        if main_item_value not in self._mainNodeDict:
            raise KeyError('Main node item %s does not exist in the tree.' % main_item_value)

        # get the model of the tree
        my_model = self.model()
        assert(isinstance(my_model, QStandardItemModel))

        # check whether the child item (value) has exist
        if child_value in self._leafDict[main_item_value]:
            return False

        # add the child item to main item
        main_node_item = self._mainNodeDict[main_item_value]
        self._add_child_item(main_node_item, child_value, not self._childrenInOrder)
        return True

    def add_main_item(self, item_value, append, as_current_index):
        """
        Append a new main leaf item to
        :param item_value: value or name of the node
        :param append: appending mode?
        :param as_current_index: if it is set to true, then the newly added main node is set to be current
        :return: If true, then append new item; otherwise, insert in increasing order
        """
        # Check requirements
        assert isinstance(item_value, str), 'Item value (i.e., node name) %s must be an integer but not' \
                                            '%s.' % (str(item_value), str(type(item_value)))
        assert isinstance(append, bool), 'Parameter append must be a boolean but not %s.' % str(type(bool))

        # whether the main node with the same value exists. It is a key!
        if item_value in self._leafDict:
            return False, 'Item %s has been in Tree already.' % str(item_value)

        # Create QStandardItem and add to data manager))
        main_node_item = QStandardItem(str(item_value))
        self._leafDict[item_value] = []
        self._mainNodeDict[item_value] = main_node_item

        # Get current number of row
        model = self.model()
        assert(isinstance(model, QStandardItemModel))
        if append is True:
            # append
            num_rows = self.model().rowCount()
            model.setItem(num_rows, 0, main_node_item)
        else:
            # insert
            leaf_value_list = sorted(self._leafDict.keys())
            try:
                row_number = leaf_value_list.index(item_value)
                model.insertRow(row_number, [main_node_item])
            except ValueError as e:
                raise RuntimeError('Impossible to have a ValueError as %s' % str(e))

        # set to current index
        if as_current_index:
            num_rows = self.model().rowCount()
            self.setCurrentIndex(model.index(num_rows-1, 0))

        return True, ''

    def clear_tree(self):
        """
        Clear the items in the tree
        :return:
        """
        self.model().clear()

        # model.clear() removes the header too
        self.model().setHeaderData(0, Qt.Horizontal, 'IPTS')

        # clear all the fast access data structure
        self._mainNodeDict.clear()
        self._leafDict.clear()

    def delete_node(self, node_item):
        """ Delete a node in the tree
        """
        # check input
        assert isinstance(node_item, QStandardItem)

        # Get current item
        node_index = self.model().indexFromItem(node_item)
        assert node_index is not None

        # get row number and node value
        row_number = node_index.row()
        node_value = str(node_item.text())

        # delete by using parent
        the_parent = node_item.parent()
        if the_parent is None:
            # top main item: remove the item and delete from the leaf dictionary
            self.model().removeRows(row_number, 1)
            del self._leafDict[node_value]
            del self._mainNodeDict[node_value]
        else:
            # it is a child
            parent_index = self.model().indexFromItem(the_parent)
            self.model().removeRows(row_number, 1, parent_index)
            parent_value = str(the_parent.text())

            if parent_value in self._leafDict:
                self._leafDict[parent_value].remove(node_value)

    def init_setup(self, header_list):
        """
        To set up customized header
        :param header_list:
        :param header_list:
        :return:
        """
        assert(isinstance(header_list, list))
        assert(len(header_list) == self._myNumCols)

        # Set up header
        for i_col in range(self._myNumCols):
            header = header_list[i_col]
            self.model().setHeaderData(0, Qt.Horizontal, header)

        self._myHeaderList = header_list[:]

        # Enable scroll bar
        header = self.header()
        assert isinstance(header, QHeaderView), 'Header must be a QHeaderView instance.'
        # header.setHorizontalScrollBar(QScrollBar())

        header.setHorizontalScrollMode(QAbstractItemView.ScrollPerItem)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(False)

        return

    def do_show_info(self):
        """
        :return:
        """
        # Get current item
        current_index = self.currentIndex()
        assert(isinstance(current_index, QModelIndex))
        current_row = current_index.row()

        current_data = current_index.data()
        assert(isinstance(current_data, QVariant))
        current_int_value, is_int = current_data.toInt()

        print('[DEV] Current Index of Row = %d ' % current_row, end=' ')
        if is_int is True:
            print('with integer value %d' % current_int_value)
        else:
            print('with a value other than integer %s' % str(current_data.toString()))

        current_item = self.model().itemFromIndex(current_index)
        assert(isinstance(current_item, QStandardItem))
        print('Current item has %d rows; ' % current_item.rowCount(), end=' ')
        print('Current item has child = %s; ' % str(current_item.hasChildren()), end=' ')

    def get_main_nodes(self, output_str=True):
        """
        Get all name of all main nodes
        Returns:
        A list of strings as names of main nodes
        """
        # return with list of main nodes' names
        if output_str:
            return list(self._leafDict.keys())

        return list(self._mainNodeDict.values())

    def get_selected_items(self):
        """
        Get selected items
        :return: list of QModelItems
        """
        qindex_list = self.selectedIndexes()

        item_list = list()
        error_message = ''

        for qindex in qindex_list:
            # check
            if isinstance(qindex, QModelIndex) is True:
                # get item and check
                qitem = self.model().itemFromIndex(qindex)
                if isinstance(qitem, QStandardItem) is True:
                    assert isinstance(qitem, QStandardItem)
                    item_list.append(qitem)
                else:
                    error_message += 'Found index %s is not a QModelIndex instance, ' \
                        'but of type %s.' % (str(qindex), str(type(qindex)))
            else:
                error_message += 'Item of index %s not a QStandardItem instance, ' \
                                 'but of type %s.' % (str(qindex), str(type(qitem)))

        if len(error_message) > 0:
            print('[Error] %s' % error_message)

        return item_list

    def get_selected_items_of_level(self, target_item_level, excluded_parent, return_item_text):
        """
        Get the selected items in a specified level
        Args:
            target_item_level: root is 0.
            excluded_parent: (1) parent nodes' name to be excluded or (2) None for nothing to exclude
            return_item_text: if True, the return the item text; otherwise, QItem
        Returns: list of q-items

        """
        # check
        assert isinstance(target_item_level, int) and target_item_level >= 1, \
            'Level %s is not allowed. It must be larger than 0.' % str(target_item_level)
        assert isinstance(return_item_text, bool)
        assert isinstance(excluded_parent, str) or excluded_parent is None

        # get selected QIndexes
        selected_items = self.get_selected_items()

        return_list = list()

        # remove the items of different levels
        for item in selected_items:
            item_level = self.get_item_level(item)
            if item_level != target_item_level:
                continue
            if excluded_parent is not None and self.has_ancestor(item, excluded_parent):
                continue
            if return_item_text:
                return_list.append(str(item.text()))
            else:
                return_list.append(item)

        return return_list

    @staticmethod
    def get_child_nodes(parent_node, output_str=False):
        """
        Get a list of children nodes
        Args:
            parent_node:
            output_str: if True, then output list of item's text instead of QStandardItem

        Returns:

        """
        assert isinstance(parent_node, QStandardItem), 'Parent node %s must be a QStandardItem but not ' \
            'of type %s.' % (str(parent_node), str(type(parent_node)))
        child_count = parent_node.rowCount()

        child_item_list = list()
        for i_child in range(child_count):
            child_item = parent_node.child(i_child)
            if output_str:
                child_item_list.append(str(child_item.text()))
            else:
                child_item_list.append(child_item)

        return child_item_list

    @staticmethod
    def get_item_level(q_item):
        """
        Get the level of a QItem in the tree
        Args:
            q_item:

        Returns:
            integer as level
        """

        level = 0
        while q_item is not None:
            q_item = q_item.parent()
            level += 1

        return level

    @staticmethod
    def has_ancestor(q_item, ancestor_name):
        """
        Check whether a node has an ancestor with similar name
        Args:
            q_item:
            ancestor_name:

        Returns:

        """
        has = False

        while not has and q_item is not None:
            if q_item.text() == ancestor_name:
                has = True
            else:
                q_item = q_item.parent()

        return has

    def insert_child_current_item(self, child_value):
        """
        Insert a child item to currently selected item
        Args:
            child_value:

        Returns:

        """
        current_index = self.currentIndex()
        assert(isinstance(current_index, QModelIndex))
        current_row = current_index.row()
        print('[DEV] Current Index of Row = %d ' % current_row)

        # Get model
        my_model = self.model()
        assert(isinstance(my_model, QStandardItemModel))
        current_item = my_model.itemFromIndex(current_index)

        assert(isinstance(current_item, QStandardItem))

        print('Add Child Value ', child_value)
        # child_item = QStandardItem(child_value)
        child_item = QStandardItem(str(child_value))
        current_item.insertRow(0, [child_item])

        return
