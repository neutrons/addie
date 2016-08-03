# Modified from vdriverunmanagertree.py
# Note: Child cannot be in the same column as parent
# Note: In TreeView, QModelIndex and QStandardItem points to the same leaf.
#       But QModelIndex.data() and QStandardItem.data() are different!
#       The variable set to QStandardItem can be only retrieved by QModelIndex.data()

from PyQt4 import QtGui, QtCore


class CustomizedTreeView(QtGui.QTreeView):
    """
    """
    def __init__(self, parent=None):
        """

        :param parent:
        :return:
        """
        QtGui.QTreeView.__init__(self, parent)
        self._myParent = parent

        # Enabled to select multiple items with shift key
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        # Set up model
        # self._myNumCols = 1
        # model = QtGui.QStandardItemModel()
        # model.setColumnCount(self._myNumCols)
        # self.setModel(model)

        # Set up tree
        # ... ... self.setDragEnabled(True)
        # ... ... self.setColumnWidth(0, 90)
        # ... ... self.setColumnWidth(1, 60)

        # Add action menu: to use right mouse operation for pop-up sub menu
        """
        action_del = QtGui.QAction('Delete', self)
        action_del.triggered.connect(self.do_delete_leaf)
        self.addAction(action_del)

        action_info = QtGui.QAction('Info', self)
        action_info.triggered.connect(self.do_show_info)
        self.addAction(action_info)
        """

        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        # Data structure to control the items
        self._leafDict = dict()  # dictionary for each leaf and its child. key is string only!
        self._myHeaderList = list()
        self._childrenInOrder = True

        return

    def delete_node(self, node_item):
        """
        """
        # TODO/NOW/ISSUE 3: Documentation!
        # check input
        assert isinstance(node_item, QtGui.QStandardItem)

        # Get current item
        node_index = self.model().indexFromItem(node_item)
        assert node_index is not None

        # get row number and node value
        row_number = node_index.row()
        node_value = str(node_item.text())

        # delete by using parent
        the_parent = node_item.parent()
        if the_parent is None:
            # top main item
            self.model().removeRows(row_number, 1)
            children = self._leafDict.pop(node_value)
            print '[INFO] Remove leaf %s with children %s.' % (node_value, str(children))
        else:
            # it is a child
            parent_index = self.model().indexFromItem(the_parent)
            self.model().removeRows(row_number, 1, parent_index)
            parent_value = str(the_parent.text())

            if self._leafDict.has_key(parent_value):
                self._leafDict[parent_value].remove(node_value)
                print '[INFO] Remove child %s from leaf %s.' % (node_value, parent_value)
            else:
                print '[INFO] Remove child %s from non-leaf parent %s.' % (node_value, parent_value)

        return

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
        for i_col in xrange(self._myNumCols):
            header = header_list[i_col]
            self.model().setHeaderData(0, QtCore.Qt.Horizontal, header)
        self._myHeaderList = header_list[:]

        return

    def do_delete_leaf(self):
        """
        Delete a run under an IPTS from tree
        :return:
        """
        # Get current item
        current_index = self.currentIndex()
        assert(isinstance(current_index, QtCore.QModelIndex))
        current_item = self.model().itemFromIndex(current_index)
        assert(isinstance(current_item, QtGui.QStandardItem))
        row_number = current_index.row()
        current_value = str(current_item.text())

        the_parent = current_item.parent()
        if the_parent is None:
            # top main item
            self.model().removeRows(row_number, 1)
            children = self._leafDict.pop(current_value)
            print '[INFO] Remove leaf %s with children %s.' % (current_value, str(children))
        else:
            # it is a child
            parent_index = self.model().indexFromItem(the_parent)
            self.model().removeRows(row_number, 1, parent_index)
            parent_value = str(the_parent.text())

            if self._leafDict.has_key(parent_value):
                self._leafDict[parent_value].remove(current_value)
                print '[INFO] Remove child %s from leaf %s.' % (current_value, parent_value)
            else:
                print '[INFO] Remove child %s from non-leaf parent %s.' % (current_value, parent_value)

        return

    def do_show_info(self):
        """
        :return:
        """
        # Get current item
        current_index = self.currentIndex()
        assert(isinstance(current_index, QtCore.QModelIndex))
        current_row = current_index.row()

        current_data = current_index.data()
        assert(isinstance(current_data, QtCore.QVariant))
        current_int_value, is_int = current_data.toInt()

        print '[DEV] Current Index of Row = %d ' % current_row,
        if is_int is True:
            print 'with integer value %d' % current_int_value
        else:
            print 'with a value other than integer %s' % str(current_data.toString())

        current_item = self.model().itemFromIndex(current_index)
        assert(isinstance(current_item, QtGui.QStandardItem))
        print 'Current item has %d rows; ' % current_item.rowCount(),
        print 'Current item has child = %s; ' % str(current_item.hasChildren()),
        print 'Current item has parent = %s; ' % str(current_item.parent()),
        print 'Current item has text = %s. ' % str(current_item.text())

        return

    def add_main_item(self, item_value, append, as_current_index):
        """
        Append a new main leaf item to
        :param item_value:
        :param append:
        :param as_current_index: if it is set to true, then the newly added main node is set to be current
        :return: If true, then append new item; otherwise, insert in increasing order
        """
        # Check
        assert(isinstance(item_value, str))

        if self._leafDict.has_key(item_value) is True:
            return False, 'Item %s has been in Tree already.' % str(item_value)
        assert(isinstance(append, bool))

        # Create QStandardItem and add to data manager
        # new_item = QtGui.QStandardItem(QtCore.QString(item_value))
        new_item = QtGui.QStandardItem(str(item_value))
        self._leafDict[item_value] = []

        # Get current number of row
        model = self.model()
        assert(isinstance(model, QtGui.QStandardItemModel))
        if append is True:
            # append
            num_rows = self.model().rowCount()
            model.setItem(num_rows, 0, new_item)
        else:
            # insert
            leaf_value_list = sorted(self._leafDict.keys())
            try:
                row_number = leaf_value_list.index(item_value)
                model.insertRow(row_number, [new_item])
            except ValueError as e:
                raise RuntimeError('Impossible to have a ValueError as %s' % str(e))

        # set to current index
        if as_current_index:
            num_rows = self.model().rowCount()
            self.setCurrentIndex(model.index(num_rows-1, 0))

        return True, ''

    def add_child_current_item(self, child_value):
        """

        :param child_value:
        :return:
        """
        current_index = self.currentIndex()
        assert(isinstance(current_index, QtCore.QModelIndex))
        current_row = current_index.row()
        print '[DEV] Current Index of Row = %d ' % current_row

        # Get model
        my_model = self.model()
        assert(isinstance(my_model, QtGui.QStandardItemModel))
        current_item = my_model.itemFromIndex(current_index)
        if current_item is None:
            print '[INFO] Current item has not been set up.'
            return

        self._add_child_item(current_item, child_value, False)

        return

    def add_child_main_item(self, main_item_value, child_value):
        """ Add a child with main item
        :return:
        """
        my_model = self.model()
        assert(isinstance(my_model, QtGui.QStandardItemModel))

        leaf_found = False
        num_rows = my_model.rowCount()
        # found_item = my_model.findItems(QtCore.QString(main_item_value))
        my_model.findItems(str(main_item_value))

        for i_row in xrange(num_rows):
            # Get item per line:
            temp_item = my_model.item(i_row)
            assert(isinstance(temp_item, QtGui.QStandardItem))

            # Use text() to match the target value
            temp_value = str(temp_item.text())
            if temp_value != main_item_value:
                continue

            # Add child
            self._add_child_item(temp_item, child_value, not self._childrenInOrder)

            break
        # END-FOR

        if leaf_found is False:
            return False

        return True

    def insert_child_current_item(self, child_value):
        current_index = self.currentIndex()
        assert(isinstance(current_index, QtCore.QModelIndex))
        current_row = current_index.row()
        print '[DEV] Current Index of Row = %d ' % current_row

        # Get model
        my_model = self.model()
        assert(isinstance(my_model, QtGui.QStandardItemModel))
        current_item = my_model.itemFromIndex(current_index)

        assert(isinstance(current_item, QtGui.QStandardItem))

        print 'Add Child Value ', child_value
        # child_item = QtGui.QStandardItem(QtCore.QString(child_value))
        child_item = QtGui.QStandardItem(str(child_value))
        current_item.insertRow(0, [child_item])

        return

    def clear_tree(self):
        """
        Clear the items in the tree
        :return:
        """
        self.model().clear()

        # model.clear() removes the header too
        self.model().setHeaderData(0, QtCore.Qt.Horizontal, 'IPTS')

        return

    def _add_child_item(self, parent_item, child_item_value, append):
        """
        Add a child item
        :param parent_item:
        :param child_item_value:
        :param append:
        :return:
        """
        # Check
        assert(isinstance(parent_item, QtGui.QStandardItem))
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
        # child_item = QtGui.QStandardItem(QtCore.QString(child_item_value))
        child_item = QtGui.QStandardItem(str(child_item_value))
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

        return

    def get_main_nodes(self):
        """
        Get all name of all main nodes
        Returns:
        A list of strings as names of main nodes
        """
        return self._leafDict.keys()

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
            if isinstance(qindex, QtCore.QModelIndex) is True:
                # get item and check
                qitem = self.model().itemFromIndex(qindex)
                if isinstance(qitem, QtGui.QStandardItem) is True:
                    assert isinstance(qitem, QtGui.QStandardItem)
                    item_list.append(qitem)
                else:
                    error_message += 'Found index %s is not a QModelIndex instance, ' \
                                 'but of type %s.' % (str(qindex), str(type(qindex)))
            else:
                error_message += 'Item of index %s not a QStandardItem instance, ' \
                                 'but of type %s.' % (str(qindex), str(type(qitem)))
            # END-IF-ELSE
        # END-FOR

        if len(error_message) > 0:
            print '[Error] %s' % error_message

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
            # END-IF
        # END-FOR

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
        assert isinstance(parent_node, QtGui.QStandardItem), 'Parent node %s must be a QStandardItem but not ' \
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
