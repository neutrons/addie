from __future__ import (absolute_import, division, print_function)

from qtpy.QtCore import QModelIndex
from qtpy.QtGui import QStandardItem, QStandardItemModel
from qtpy.QtWidgets import QAction
from addie.utilities import customtreeview as base
from addie.calculate_gr.event_handler import remove_gss_from_plot
from addie.widgets.filedialog import get_save_file


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

    def add_temp_ws(self, ws_name):
        """

        Parameters
        ----------
        ws_name
        """
        self.add_child_main_item('workspaces', ws_name)

    def do_copy_to_ipython(self):
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
            remove_gss_from_plot(self._mainWindow,
                                 gss_ws_name,
                                 gss_bank_names)

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
                    remove_gss_from_plot(self._mainWindow,
                                         gss_group_name=gsas_name,
                                         gss_bank_ws_name_list=[ws_name])
                except AssertionError:
                    print('Workspace %s is not on canvas.' % ws_name)

            # delete the node from the tree
            self.delete_node(gsas_node)

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
        file_ext = {'GSAS File (*.gsa)':'gsa', 'Any File (*.*)':''}
        new_gss_file_name, _ = get_save_file(self, caption='New GSAS file name',
                                             directory=self._mainWindow.get_default_data_dir(),
                                             filter=file_ext)

        if not new_gss_file_name:  # user pressed cancel
            return

        # emit the signal to the main window
        selected_node = self.get_selected_items()[0]
        bank_ws_list = self.get_child_nodes(selected_node, output_str=True)

        # write all the banks to a GSAS file
        self._mainWindow.get_workflow().write_gss_file(ws_name_list=bank_ws_list, gss_file_name=new_gss_file_name)

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
