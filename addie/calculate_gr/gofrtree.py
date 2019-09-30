from __future__ import (absolute_import, division, print_function)

from qtpy.QtCore import QModelIndex
from qtpy.QtGui import QStandardItem, QStandardItemModel
from qtpy.QtWidgets import QAction

from addie.utilities import customtreeview as base
from addie.calculate_gr import event_handler


class GofRTree(base.CustomizedTreeView):
    """ Tree to record G(R) workspaces
    """

    def __init__(self, parent):
        """

        :param parent:
        :return:
        """
        base.CustomizedTreeView.__init__(self, parent)
        self.parent = parent

        # define actions
        self._action_plot = QAction('Plot', self)
        self._action_plot.triggered.connect(self.do_plot)

        # to python
        self._action_ipython = QAction('To IPython', self)
        self._action_ipython.triggered.connect(self.do_copy_to_ipython)

        # remove from plot
        self._action_remove_plot = QAction('Remove from plot', self)
        self._action_remove_plot.triggered.connect(self.do_remove_from_plot)

        # delete workspace/data
        self._action_delete = QAction('Delete data', self)
        self._action_delete.triggered.connect(self.do_delete_selected_items)

        self._mainWindow = None
        self._workspaceNameList = None

        self.reset_gr_tree()

    # override
    def mousePressEvent(self, e):
        """
        Over ride mouse press event
        Parameters
        ----------
        e :: event
        """
        button_pressed = e.button()
        if button_pressed == 2:
            # override the response for right button
            self.pop_up_menu()
        else:
            # keep base method for other buttons
            base.CustomizedTreeView.mousePressEvent(self, e)

    def pop_up_menu(self):
        """

        Parameters
        ----------
        """
        selected_items = self.get_selected_items()
        if len(selected_items) == 0:
            return

        leaf_level = -1
        for item in selected_items:
            if item.parent() is None and leaf_level == -1:
                leaf_level = 1
            elif item.parent() is not None and leaf_level == -1:
                leaf_level = 2
            elif item.parent() is None and leaf_level != 1:
                print('[Error] Nodes of different levels are selected.')
            elif item.parent() is None and leaf_level != 2:
                print('[Error] Nodes of different levels are selected.')

        if leaf_level == 1:
            self.addAction(self._action_plot)
            self.addAction(self._action_ipython)
            self.addAction(self._action_delete)
        elif leaf_level == 2:
            self.addAction(self._action_plot)
            self.addAction(self._action_ipython)
            self.addAction(self._action_remove_plot)
            self.addAction(self._action_delete)

    def add_gr(self, gr_parameter, gr_ws_name):
        """
        Add a G(r) workspace with given Qmin and Qmax
        :param gr_parameter: the leaf name for the G(r) in the tree.
        :param gr_ws_name:
        :return:
        """
        # Check
        assert isinstance(gr_parameter, str), 'G(r) parameters must be a string but not a %s.' \
                                              '' % str(type(gr_parameter))
        assert isinstance(gr_ws_name, str)

        # Create main leaf value if it does not exist
        main_leaf_value = str(gr_parameter)
        status, message = self.add_main_item(main_leaf_value, False, True)
        if status is False:
            print('[Log] %s' % message)

        # Add workspace name as a leaf
        child_value = gr_ws_name
        self.add_child_main_item(main_leaf_value, child_value)

        # register workspace
        self._workspaceNameList.append(gr_ws_name)

    def add_arb_gr(self, ws_name, is_gr=True):
        """
        Add a G(r) workspace that is not belonged to any S(Q) and add it under 'workspaces'
        Parameters
        ----------
        ws_name
        is_gr
        """
        # check
        assert isinstance(ws_name, str)

        # add leaf
        if is_gr:
            self.add_child_main_item('workspaces', ws_name)
        else:
            self.add_child_main_item('SofQ', ws_name)

        # register workspace
        self._workspaceNameList.append(ws_name)

    def add_sq(self, sq_ws_name):
        """
        Add an SofQ workspace
        Args:
            sq_ws_name:
        """
        # check
        assert isinstance(sq_ws_name, str)

        # add
        self.add_child_main_item('SofQ', sq_ws_name)

    def reset_gr_tree(self):
        """
        Clear the leaves of the tree only leaving the main node 'workspaces'
        """
        # clear all
        if self.model() is not None:
            self.model().clear()

        # reset workspace data structures
        self._workspaceNameList = list()
        self._myHeaderList = list()
        self._leafDict.clear()

        # re-initialize the model
        self._myNumCols = 1
        model = QStandardItemModel()
        model.setColumnCount(self._myNumCols)
        self.setModel(model)

        self.init_setup(['G(R) Workspaces'])
        self.add_main_item('workspaces', append=True, as_current_index=False)
        self.add_main_item('SofQ', append=False, as_current_index=False)

    def do_copy_to_ipython(self):
        """
        Copy the selected item to an iPython command
        """
        # Get current index and item
        current_index = self.currentIndex()
        if isinstance(current_index, QModelIndex) is False:
            return False, 'Current index is not QModelIndex instance, but %s.' % str(type(current_index))

        assert (isinstance(current_index, QModelIndex))

        current_item = self.model().itemFromIndex(current_index)
        if isinstance(current_item, QStandardItem) is False:
            return False, 'Current item is not QStandardItem instance, but %s.' % str(type(current_item))
        assert (isinstance(current_item, QStandardItem))

        # get the workspace name.  if it is on main node, then use its child's value
        if current_item.parent() is None:
            # main node.  access its child and use child's name
            only_child = current_item.child(0)
            ws_name = only_child.text()
        else:
            # workspace name node.
            ws_name = str(current_item.text())

        python_cmd = "ws = mtd['%s']" % ws_name

        if self._mainWindow is not None:
            self._mainWindow.set_ipython_script(python_cmd)

    def is_gr_empty(self):
        """ Checks if there is a G(r) workspace and returns True if empty
        """
        gr_exists = False
        for key in self._leafDict.keys():
            if key.startswith('G(r)'):
                gr_exists = True
        return not gr_exists

    def is_sofq_empty(self):
        if self._leafDict['SofQ'] == []:
            return True
        return False

    def do_delete_selected_items(self):
        """
        Delete the workspaces assigned to the selected items
        """
        # get selected item
        selected_items = self.get_selected_items()
        if len(selected_items) == 0:
            return

        # check that all the items should be of the same level
        curr_level = -1
        for item in selected_items:
            # get this level
            if item.parent() is None:
                temp_level = 0
            else:
                temp_level = 1
            if curr_level == -1:
                curr_level = temp_level
            elif curr_level != temp_level:
                raise RuntimeError(
                    'Nodes of different levels are selected. It is not supported for deletion.')

        # get item and delete
        if curr_level == 0:
            # delete node
            for item in selected_items:
                self._delete_main_node(item)
        else:
            # delete leaf
            for item in selected_items:
                self._delete_ws_node(item, None, check_gr_sq=True)

        self.check_widgets_status()

    def check_widgets_status(self):
        is_gr_empty = self.is_gr_empty()
        event_handler.gr_widgets_status(self.parent, not is_gr_empty)

        is_sofq_empty = self.is_sofq_empty()
        event_handler.sofq_widgets_status(self.parent, not is_sofq_empty)

    def _delete_main_node(self, node_item):
        """
        Delete a main node
        Args:
            node_item:
        """
        # Check
        assert node_item.parent() is None

        # check item
        item_name = str(node_item.text())
        keep_main_node = False
        is_gr = True
        if item_name == 'workspaces':
            keep_main_node = True
        elif item_name == 'SofQ':
            keep_main_node = True
            is_gr = False

        # node workspaces and SofQ cannot be deleted
        sub_leaves = self.get_child_nodes(node_item, output_str=False)
        for leaf_node in sub_leaves:
            # delete a leaf
            self._delete_ws_node(leaf_node, is_gr, check_gr_sq=False)

        # delete this node
        if not keep_main_node:
            self.delete_node(node_item)

    def _delete_ws_node(self, ws_item, is_gr, check_gr_sq):
        """
        Delete a level-2 item
        Args:
            ws_item:
        """
        # check
        assert ws_item.parent() is not None

        if check_gr_sq:
            parent_node = ws_item.parent()
            if str(parent_node.text()) == 'SofQ':
                is_gr = False
            else:
                is_gr = True

        # get leaf node name
        leaf_node_name = str(ws_item.text())
        # delete workspace
        self._mainWindow.get_workflow().delete_workspace(leaf_node_name)
        # remove from canvas
        try:
            if is_gr:
                event_handler.remove_gr_from_plot(self.parent, leaf_node_name)
            else:
                event_handler.remove_sq_from_plot(self.parent, leaf_node_name)
        except AssertionError as ass_err:
            print('Unable to remove %s from canvas due to %s.' %
                  (leaf_node_name, str(ass_err)))
        # delete node
        self.delete_node(ws_item)

    def do_plot(self):
        """
        Add selected runs
        :return:
        """
        # get list of the items that are selected
        item_list = self.get_selected_items_of_level(target_item_level=2, excluded_parent=None,
                                                     return_item_text=False)

        gr_list = list()
        sq_list = list()

        for item in item_list:
            leaf = str(item.text())

            parent_i = item.parent()
            if str(parent_i.text()) == 'SofQ':
                sq_list.append(leaf)
            else:
                gr_list.append(leaf)

        # sort
        sq_list.sort()
        gr_list.sort()

        # FIXME/LATER - replace this by signal
        if self._mainWindow is None:
            raise NotImplementedError('Main window has not been set up!')

        if len(gr_list) > 0:
            for gr_name in gr_list:
                event_handler.plot_gr(
                    self._mainWindow, gr_name,
                    None, None, None, None, None,
                    auto=True)

        for sq_name in sq_list:
            event_handler.plot_sq(self._mainWindow, sq_name, None, False)

    def do_remove_from_plot(self):
        """
        Remove the selected item from plot if it is plotted
        """
        # get selected items
        item_list = self.get_selected_items()

        # remove the selected items from plotting
        for tree_item in item_list:
            # get its name and its parent's name
            leaf_name = str(tree_item.text())
            node_name = str(tree_item.parent().text())

            # remove from canvas by calling parents
            if node_name == 'SofQ':
                event_handler.remove_sq_from_plot(self._mainWindow, leaf_name)
            else:
                event_handler.remove_gr_from_plot(self._mainWindow, leaf_name)

    def get_current_run(self):
        """ Get current run selected by mouse
        note: if multiple items are selected,
          (1) currentIndex() returns the first selected item
          (2) selectedIndexes() returns all the selected items
        :return: status, run number in integer
        """
        # Get current index and item
        current_index = self.currentIndex()
        if isinstance(current_index, QModelIndex) is False:
            return False, 'Current index is not QModelIndex instance, but %s.' % str(type(current_index))

        assert(isinstance(current_index, QModelIndex))

        current_item = self.model().itemFromIndex(current_index)
        if isinstance(current_item, QStandardItem) is False:
            return False, 'Current item is not QStandardItem instance, but %s.' % str(type(current_item))
        assert(isinstance(current_item, QStandardItem))

        if current_item.parent() is None:
            # Top-level leaf, IPTS number
            return False, 'Top-level leaf for IPTS number'

        try:
            value_str = str(current_item.text())
            run = int(value_str)
        except ValueError as value_error:
            return False, 'Unable to convert {0} to run number as integer due to {1}.' \
                          ''.format(current_item.text(), value_error)

        return True, run

    def get_workspaces(self):
        """
        Get workspaces controlled by GSAS tree.
        Returns
        -------

        """
        return self._workspaceNameList

    def mouseDoubleClickEvent(self, e):
        """ Override event handling method
        """
        status, current_run = self.get_current_run()
        print('[INFO] Status = {0}; Current run number = {1}'.format(
            status, current_run))

    def set_main_window(self, main_window):
        """

        :param main_window:
        :return:
        """
        self._mainWindow = main_window
