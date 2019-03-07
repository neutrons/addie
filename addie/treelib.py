from __future__ import (absolute_import, division, print_function)

from qtpy.QtCore import (QModelIndex)
from qtpy.QtGui import (QStandardItem, QStandardItemModel)
from qtpy.QtWidgets import (QAction, QFileDialog)
from addie.utilities import customtreeview as base

#
# An extension of QTreeView for file system
#


class BraggTree(base.CustomizedTreeView):
    """ Tree widget to store Bragg workspace """

    def __init__(self, parent):
        """
        Initialize
        Parameters
        ----------
        parent
        """
        base.CustomizedTreeView.__init__(self, parent)

        # set up actions
        self._action_plot = QAction('Plot', self)
        self._action_plot.triggered.connect(self.do_plot_ws)

        # to python
        self._action_ipython = QAction('To IPython', self)
        self._action_ipython.triggered.connect(self.do_copy_to_ipython)

        # to delete
        self._action_delete = QAction('Delete workspace', self)
        self._action_delete.triggered.connect(self.do_delete_gsas)

        # to merge GSAS file
        self._action_merge_gss = QAction('Merge to GSAS', self)
        self._action_merge_gss.triggered.connect(self.do_merge_to_gss)

        # to select
        self._action_select_node = QAction('Plot', self)
        self._action_select_node.triggered.connect(self.do_select_gss_node)

        # to de-select
        self._action_deselect_node = QAction('Remove from plotting', self)
        self._action_deselect_node.triggered.connect(self.do_remove_from_plot)

        # class variables
        self._mainWindow = None
        self._workspaceNameList = None

        # reset
        self.reset_bragg_tree()

        return

    def reset_bragg_tree(self):
        """
        Clear the leaves of the tree only leaving the main node 'workspaces'
        Returns
        -------

        """
        # clear all
        if self.model() is not None:
            self.model().clear()

        # reset workspace names list
        self._workspaceNameList = list()
        self._myHeaderList = list()
        self._leafDict.clear()

        # re-initialize the model
        self._myNumCols = 1
        model = QStandardItemModel()
        model.setColumnCount(self._myNumCols)
        self.setModel(model)

        self.init_setup(['Bragg Workspaces'])
        self.add_main_item('workspaces', append=True, as_current_index=False)

        return

    # override
    def mousePressEvent(self, e):
        """
        Over ride mouse press event
        Parameters
        ----------
        e :: event

        Returns
        -------

        """
        button_pressed = e.button()
        if button_pressed == 2:
            # override the response for right button
            self.pop_up_menu()
        else:
            # keep base method for other buttons
            base.CustomizedTreeView.mousePressEvent(self, e)

        return

    def pop_up_menu(self):
        """

        Parameters
        ----------

        Returns
        -------

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
            self.removeAction(self._action_plot)
            self.addAction(self._action_select_node)
            self.addAction(self._action_ipython)
            self.addAction(self._action_merge_gss)
            self.addAction(self._action_deselect_node)
            self.addAction(self._action_delete)
        elif leaf_level == 2:
            self.addAction(self._action_plot)
            self.removeAction(self._action_select_node)
            self.removeAction(self._action_merge_gss)
            self.addAction(self._action_ipython)
            self.removeAction(self._action_deselect_node)
            self.removeAction(self._action_delete)

        return

    def add_bragg_ws_group(self, ws_group_name, bank_name_list):
        """
        Add a workspace group containing a list of bank names as a main node in the tree
        Parameters
        ----------
        ws_group_name
        bank_name_list

        Returns
        -------

        """
        # check inputs' validity
        assert isinstance(ws_group_name, str), 'ws_group_name must be a string but not %s.' % str(type(ws_group_name))
        assert isinstance(bank_name_list, list) and len(bank_name_list) > 0, 'Bank name list must be a non-empty list' \
                                                                             ' but not %s.' % str(type(bank_name_list))
        # main node/leaf
        main_leaf_value = str(ws_group_name)
        self.add_main_item(main_leaf_value, True, True)

        for bank_name in bank_name_list:
            # add the tree
            self.add_child_main_item(main_leaf_value, bank_name)
            # register
            self._workspaceNameList.append(bank_name)

        return

    def add_temp_ws(self, ws_name):
        """

        Parameters
        ----------
        ws_name

        Returns
        -------

        """
        self.add_child_main_item('workspaces', ws_name)

        return

    def do_copy_to_ipython(self):
        """

        Returns
        -------

        """
        # TO/NOW - Doc and check

        # Get current index and item
        current_index = self.currentIndex()
        if isinstance(current_index, QModelIndex) is False:
            return False, 'Current index is not QModelIndex instance, but %s.' % str(type(current_index))

        assert (isinstance(current_index, QModelIndex))

        current_item = self.model().itemFromIndex(current_index)
        if isinstance(current_item, QStandardItem) is False:
            return False, 'Current item is not QStandardItem instance, but %s.' % str(type(current_item))
        assert (isinstance(current_item, QStandardItem))

        ws_name = str(current_item.text())

        python_cmd = "ws = mtd['%s']" % ws_name

        if self._mainWindow is not None:
            self._mainWindow.set_ipython_script(python_cmd)

        return

    def do_remove_from_plot(self):
        """
        Remove a node's plot if it is plot on canvas
        Returns
        -------

        """
        # get the selected gsas node
        selected_nodes = self.get_selected_items()
        if len(selected_nodes) == 0:
            return

        # remove it from canvas
        for gss_node in selected_nodes:
            gss_ws_name = str(gss_node.text())
            gss_bank_names = self.get_child_nodes(gss_node, output_str=True)
            self._mainWindow.remove_gss_from_plot(gss_ws_name, gss_bank_names)

        return

    def do_delete_gsas(self):
        """
        Delete a GSAS workspace and its split workspaces, and its item in the GSAS-tree as well.
        Returns:
        None
        """
        # get selected nodes
        gsas_node_list = self.get_selected_items()

        for gsas_node in gsas_node_list:
            # delete a gsas workspace and the workspaces split from it
            gsas_name = str(gsas_node.text())
            gss_ws_name = gsas_name.split('_group')[0]
            self._mainWindow.get_workflow().delete_workspace(gss_ws_name)

            # get the sub nodes and delete the workspaces
            sub_leaves = self.get_child_nodes(parent_node=gsas_node, output_str=True)
            for ws_name in sub_leaves:
                self._mainWindow.get_workflow().delete_workspace(ws_name)
                try:
                    self._mainWindow.remove_gss_from_plot(gss_group_name=gsas_name, gss_bank_ws_name_list=[ws_name])
                except AssertionError:
                    print('Workspace %s is not on canvas.' % ws_name)

            # delete the node from the tree
            self.delete_node(gsas_node)
        # END-FOR

        return

    def do_merge_to_gss(self):
        """
        Merge a selected GSAS workspace (with split workspaces) to a new GSAS file
        Returns:

        """
        # check prerequisite
        assert self._mainWindow is not None, 'Main window is not set up.'

        # get the selected GSAS node's name
        status, ret_obj = self.get_current_main_nodes()
        if not status:
            print('[Error] Get current main nodes: %s.' % str(ret_obj))
            return

        gss_node_list = ret_obj
        if len(gss_node_list) == 0:
            return
        elif len(gss_node_list) > 1:
            print('[Error] Only 1 GSS node can be selected.  Current selected nodes are %s.' % str(gss_node_list))
            return

        # pop-out a file dialog for GSAS file's name
        file_ext = 'GSAS File (*.gsa);;Any File (*.*)'
        new_gss_file_name = str(QFileDialog.getSaveFileName(self, 'New GSAS file name',
                                                                  self._mainWindow.get_default_data_dir(), file_ext))

        # quit
        if new_gss_file_name is None or len(new_gss_file_name) == 0:
            return

        # emit the signal to the main window
        selected_node = self.get_selected_items()[0]
        bank_ws_list = self.get_child_nodes(selected_node, output_str=True)

        #out_gss_ws = os.path.basename(new_gss_file_name).split('.')[0]
        # write all the banks to a GSAS file
        self._mainWindow.get_workflow().write_gss_file(ws_name_list=bank_ws_list, gss_file_name=new_gss_file_name)

        return

    def do_plot_ws(self):
        """
        Add selected runs
        :return:
        """
        item_list = self.get_selected_items()
        leaf_list = list()

        for item in item_list:
            leaf = str(item.text())
            leaf_list.append(leaf)
        # END-FOR

        # sort
        leaf_list.sort()

        # FIXME/LATER - replace this by signal
        if self._mainWindow is not None:
            self._mainWindow.plot_bragg(leaf_list)
        else:
            raise NotImplementedError('Main window has not been set up!')

        return

    def do_select_gss_node(self):
        """
        Select a GSAS node such that this workspace (group) will be plotted to canvas
        Returns
        -------

        """
        # get selected nodes
        selected_nodes = self.get_selected_items()

        # set to plot
        for gss_group_node in selected_nodes:
            gss_group_name = str(gss_group_node.text())
            self._mainWindow.set_bragg_ws_to_plot(gss_group_name)

    def get_current_main_nodes(self):
        """
        Get the name of the current nodes that are selected
        The reason to put the method here is that it is assumed that the tree only has 2 level (main and leaf)
        Returns: 2-tuple: boolean, a list of strings as main nodes' names

        """
        # Get current index and item
        current_index = self.currentIndex()
        if isinstance(current_index, QModelIndex) is False:
            return False, 'Current index is not QModelIndex instance, but %s.' % str(type(current_index))

        assert (isinstance(current_index, QModelIndex))

        # Get all selected indexes and get their main-node (or itself)'s name
        main_node_list = list()
        q_indexes = self.selectedIndexes()
        for q_index in q_indexes:
            # get item by QIndex
            this_item = self.model().itemFromIndex(q_index)
            # check
            if isinstance(this_item, QStandardItem) is False:
                return False, 'Current item is not QStandardItem instance, but %s.' % str(type(this_item))

            # get node name of parent's node name
            if this_item.parent() is not None:
                node_name = str(this_item.parent().text())
            else:
                node_name = str(this_item.text())
            main_node_list.append(node_name)
        # END-FOR

        return True, main_node_list

    def set_main_window(self, parent_window):
        """
        Set the main window (parent window) to this tree
        Parameters
        ----------
        parent_window

        Returns
        -------

        """
        # check
        assert parent_window is not None, 'Parent window cannot be None'

        self._mainWindow = parent_window

        return


class GofRTree(base.CustomizedTreeView):
    """ Tree to record G(R) workspaces
    """

    def __init__(self, parent):
        """

        :param parent:
        :return:
        """
        base.CustomizedTreeView.__init__(self, parent)

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

        return

    # override
    def mousePressEvent(self, e):
        """
        Over ride mouse press event
        Parameters
        ----------
        e :: event

        Returns
        -------

        """
        button_pressed = e.button()
        if button_pressed == 2:
            # override the response for right button
            self.pop_up_menu()
        else:
            # keep base method for other buttons
            base.CustomizedTreeView.mousePressEvent(self, e)

        return

    def pop_up_menu(self):
        """

        Parameters
        ----------

        Returns
        -------

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
        # END-FOR

        if leaf_level == 1:
            self.addAction(self._action_plot)
            self.addAction(self._action_ipython)
            self.addAction(self._action_delete)
        elif leaf_level == 2:
            self.addAction(self._action_plot)
            self.addAction(self._action_ipython)
            self.addAction(self._action_remove_plot)
            self.addAction(self._action_delete)

        return

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

        return

    def add_arb_gr(self, ws_name, is_gr=True):
        """
        Add a G(r) workspace that is not belonged to any S(Q) and add it under 'workspaces'
        Parameters
        ----------
        ws_name
        is_gr

        Returns
        -------

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

        return

    def add_sq(self, sq_ws_name):
        """
        Add an SofQ workspace
        Args:
            sq_ws_name:

        Returns:

        """
        # check
        assert isinstance(sq_ws_name, str)

        # add
        self.add_child_main_item('SofQ', sq_ws_name)

        return

    def reset_gr_tree(self):
        """
        Clear the leaves of the tree only leaving the main node 'workspaces'
        Returns
        -------

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

        return

    def do_copy_to_ipython(self):
        """
        Copy the selected item to an iPython command
        Returns
        -------

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

        return

    def do_delete_selected_items(self):
        """
        Delete the workspaces assigned to the selected items
        Returns:

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
                raise RuntimeError('Nodes of different levels are selected. It is not supported for deletion.')
        # END-FOR

        # get item and delete
        if curr_level == 0:
            # delete node
            for item in selected_items:
                self._delete_main_node(item)
        else:
            # delete leaf
            for item in selected_items:
                self._delete_ws_node(item, None, check_gr_sq=True)
        # END-IF-ELSE

        return

    def _delete_main_node(self, node_item):
        """
        Delete a main node
        Args:
            node_item:

        Returns:

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
        # END-FOR

        # delete this node
        if not keep_main_node:
            self.delete_node(node_item)

        return

    def _delete_ws_node(self, ws_item, is_gr, check_gr_sq):
        """
        Delete a level-2 item
        Args:
            ws_item:

        Returns:

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
                self._mainWindow.remove_gr_from_plot(leaf_node_name)
            else:
                self._mainWindow.remove_sq_from_plot(leaf_node_name)
        except AssertionError as ass_err:
            print('Unable to remove %s from canvas due to %s.' % (leaf_node_name, str(ass_err)))
        # delete node
        self.delete_node(ws_item)

        return

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
        # END-FOR

        # sort
        sq_list.sort()
        gr_list.sort()

        # FIXME/LATER - replace this by signal
        if self._mainWindow is None:
            raise NotImplementedError('Main window has not been set up!')

        if len(gr_list) > 0:
            self._mainWindow.plot_gr(gr_list, None, None, None, auto=True)

        for sq_name in sq_list:
            self._mainWindow.plot_sq(sq_name, None, False)

        return

    def do_remove_from_plot(self):
        """
        Remove the selected item from plot if it is plotted
        Returns:

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
                self._mainWindow.remove_sq_from_plot(leaf_name)
            else:
                self._mainWindow.remove_gr_from_plot(leaf_name)
            # END-IF
        # END-FOR

        return

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
        # END-TRY

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
        print('[INFO] Status = {0}; Current run number = {1}'.format(status, current_run))

        # if self._mainWindow is not None:
        #     self._mainWindow.set_run(current_run)

        return

    def set_main_window(self, main_window):
        """

        :param main_window:
        :return:
        """
        self._mainWindow = main_window

        return
