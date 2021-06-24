from __future__ import (absolute_import, division, print_function)

import re
from qtpy.QtCore import QModelIndex
from qtpy.QtGui import QStandardItem, QStandardItemModel
from qtpy.QtWidgets import QAction
from addie.utilities import customtreeview as base
from addie.widgets.filedialog import get_save_file
from addie.rietveld import event_handler


class BankRegexException(Exception):
    """ Exception for bank regex not finding a match"""
    pass


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
        self._main_window = None
        self._workspaceNameList = None

        # set to parent
        if parent:
            self.set_main_window(parent)

        # reset
        self.reset_bragg_tree()

    def process_selected_nodes(self, selected_nodes):
        """
        Process selected nodes so that returned nodes will only
        contain main leaf but not any children.

        If both parent and children are selected from the tree, we want
        to get rid of children from the selected wks list. Meanwhile, we want
        to check the box corresponding to the selected children.

        Arguments:
            selected_nodes {list} -- List of selected nodes
        Return:
            selected_nodes_temp {list} -- List of nodes with all children removed.
        """

        leaf_dict_temp = self._main_window.rietveld_ui.treeWidget_braggWSList._leafDict
        for item_temp in selected_nodes:
            if item_temp not in list(leaf_dict_temp.keys()):
                parent_found = False
                for key, list_temp in leaf_dict_temp.items():
                    for item_temp_1 in list_temp:
                        if item_temp in item_temp_1:
                            bank_temp = list_temp.index(item_temp_1) + 1
                            self._main_window._braggBankWidgets[bank_temp].setChecked(True)
                            parent_found = True
                            parent_in_tree = key
                            break
                    if parent_found:
                        break
                if parent_in_tree not in selected_nodes:
                    selected_nodes.append(parent_in_tree)

        selected_nodes_temp = []
        for item_temp in selected_nodes:
            if item_temp in list(leaf_dict_temp.keys()):
                selected_nodes_temp.append(item_temp)

        return selected_nodes_temp

    def _get_bank_id(self, bank_wksp):
        """Get bank ID from a workspace name with the structure:
             Bank 1 - <float for theta angle>
        :param bank_wksp: Bank workspace name to strip out bank ID from
        :type bank_wksp: str
        :return: Bank ID as int
        """
        bank_regex = r"Bank\s+(\d+)\s+-"
        m = re.match(bank_regex, bank_wksp)
        if m:
            bank_id = m.group(1).strip()
        else:
            msg = "Did not find the bank ID in workspace name: {wksp} "
            msg += "when using regular expression: {regex}"
            msg = msg.format(wksp=bank_wksp, regex=bank_regex)
            raise BankRegexException(msg)
        return bank_id

    def _get_tree_structure(self, model=None, parent_index=QModelIndex(), spaces=""):
        """ Get the Bragg Tree structure information,
        such as node names, number of children for each node, etc.
        :param model: (optional) Model to print tree structure for
        :type model: QAbstractItemModel
        :param parent_index: (optional) Parent index to use for printing children of the Model
        :type parent_index: QModelIndex
        """
        if not model:
            model = self.model()

        if model.rowCount(parent_index) == 0:
            return

        for i in range(model.rowCount(parent_index)):
            index = model.index(i,0, parent_index)
            print("{}{}".format(spaces, model.data(index)))

            if model.hasChildren(index):
                self._get_tree_structure(model, index, spaces + "  |--")

    def add_bragg_ws_group(self, ws_group_name, bank_name_list):
        """
        Add a workspace group containing a list of bank names as a main node
        in the tree
        Parameters
        ----------
        ws_group_name
        bank_name_list

        Returns
        -------

        """
        # check inputs' validity
        msg = 'ws_group_name must be a string but not {}.'
        assert isinstance(ws_group_name, str), msg.format(type(ws_group_name))

        is_it_a_list = isinstance(bank_name_list, list)
        is_list_populated = len(bank_name_list) > 0
        is_a_list_and_populated = is_it_a_list and is_list_populated
        msg = 'Bank name list must be a non-empty list. Currently is: {}.'
        assert is_a_list_and_populated, msg.format(type(bank_name_list))
        # main node/leaf
        main_leaf_value = str(ws_group_name)
        self.add_main_item(main_leaf_value, True, True)

        for bank_name in bank_name_list:
            print("main_leaf_value:", main_leaf_value, "bank_name:", bank_name)
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
            msg = 'Current index is not QModelIndex instance, but {}.'
            return False, msg.format(type(current_index))

        assert (isinstance(current_index, QModelIndex))

        current_item = self.model().itemFromIndex(current_index)
        if isinstance(current_item, QStandardItem) is False:
            msg = 'Current item is not QStandardItem instance, but {}.'
            return False, msg.format(type(current_item))
        assert (isinstance(current_item, QStandardItem))

        ws_name = str(current_item.text())

        if ws_name == "workspaces":
            print("[Warning] No valid workspace selected.")
            return

        python_cmd = "ws = mtd['%s']" % ws_name

        if self._main_window is not None:
            self._main_window.set_ipython_script(python_cmd)

    def do_delete_gsas(self):
        """
        Delete a GSAS workspace and its split workspaces,
        and its item in the GSAS-tree as well.
        """
        # get selected nodes
        gsas_node_list = self.get_selected_items()
        for gsas_node in gsas_node_list:
            # delete the gsas group workspace (deletes sub-workspaces as well)
            gsas_name = str(gsas_node.text())
            gss_ws_name = gsas_name.split('_group')[0]
            if gss_ws_name == "workspaces":
                continue
            self._main_window.get_workflow().delete_workspace(gss_ws_name)

            # delete the node from the tree
            self.delete_node(gsas_node)
        if len(self._mainNodeDict) == 1:
            event_handler.do_clear_bragg_canvas(self._main_window)
            self._main_window._onCanvasGSSBankList = []
            event_handler.check_rietveld_widgets(self._main_window)

    def do_merge_to_gss(self):
        """
        Merge a selected GSAS workspace (with split workspaces)
        to a new GSAS file
        """
        # check prerequisite
        assert self._main_window is not None, 'Main window is not set up.'

        # get the selected GSAS node's name
        status, ret_obj = self.get_current_main_nodes()
        if not status:
            print('[Error] Get current main nodes: %s.' % str(ret_obj))
            return

        gss_node_list = ret_obj
        if len(gss_node_list) == 0:
            return

        elif len(gss_node_list) > 1:
            msg = '[Error] Only 1 GSS node can be selected.'
            msg += 'Current selected nodes are {}.'
            print(msg.format(gss_node_list))
            return

        if str(gss_node_list[0]) == "workspaces":
            print("[Warning] No valid workspace selected!")
            return

        # pop-out a file dialog for GSAS file's name
        file_ext = {'GSAS File (*.gsa)': 'gsa', 'Any File (*.*)': ''}
        new_gss_file_name, _ = get_save_file(
            self,
            caption='New GSAS file name',
            directory=self._main_window.get_default_data_dir(),
            filter=file_ext)

        if not new_gss_file_name:  # user pressed cancel
            return

        # emit the signal to the main window
        selected_node = self.get_selected_items()[0]
        bank_ws_list = self.get_child_nodes(selected_node, output_str=True)

        # write all the banks to a GSAS file
        self._main_window.get_workflow().write_gss_file(
            ws_name_list=bank_ws_list, gss_file_name=new_gss_file_name)

    def do_plot_ws(self):
        """
        Add selected runs
        :return:
        """
        # get the selected items of tree and sort them alphabetically
        item_list = self.get_selected_items()
        item_list = [str(item.text()) for item in item_list]
        # item_list.sort()

        item_list = self.process_selected_nodes(item_list)
        item_list.sort()

        # FIXME/LATER - replace this by signal
        if self._main_window is not None:
            print("do_plot_ws: item_list", item_list)
            ids = event_handler.get_bragg_banks_selected(self._main_window)
            print("do_plot_ws: ids -", ids)
            event_handler.plot_bragg(
                self._main_window,
                ws_list=item_list,
                bankIds=ids,
                clear_canvas=True)
        else:
            raise NotImplementedError('Main window has not been set up!')

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
            self.remove_gss_from_plot(self._main_window,
                                      gss_ws_name,
                                      gss_bank_names)

    def do_reset_gsas_tab(main_window):
        """
        Reset the GSAS-tab including
        1. deleting all the GSAS workspaces
        2. clearing the GSAS tree
        3. clearing GSAS canvas
        """
        bragg_list = main_window.rietveld_ui.treeWidget_braggWSList

        # delete all workspaces: get GSAS workspaces from tree
        gsas_group_node_list = bragg_list.get_main_nodes(output_str=False)
        for gsas_group_node in gsas_group_node_list:
            # skip if the workspace is 'workspaces'
            gss_node_name = str(gsas_group_node.text())
            if gss_node_name == 'workspaces':
                continue

            # guess for the main workspace and delete
            gss_main_ws = gss_node_name.split('_group')[0]
            main_window._myController.delete_workspace(
                gss_main_ws, no_throw=True)

        # reset the GSAS tree
        bragg_list.reset_bragg_tree()

        # clear checkboxes for banks
        main_window.clear_bank_checkboxes()

        # clear the canvas
        main_window.rietveld_ui.graphicsView_bragg.reset()
        main_window._onCanvasGSSBankList = []
        event_handler.check_rietveld_widgets(main_window)

    def do_select_gss_node(self):
        """
        Select a GSAS node such that this workspace (group)
        will be plotted to canvas
        Returns
        -------

        """
        # get selected nodes
        selected_nodes = self.get_selected_items()
        selected_nodes = [str(item.text()) for item in selected_nodes]

        selected_nodes = self.process_selected_nodes(selected_nodes)

        # set to plot
        for gss_group_node in selected_nodes:
            gss_group_name = str(gss_group_node)
            if gss_group_name == "workspaces":
                continue
            # self._main_window.set_bragg_ws_to_plot(gss_group_name)
            self._main_window.set_bragg_ws_to_plot(gss_group_node)

    def get_current_main_nodes(self):
        """
        Get the name of the current nodes that are selected
        The reason to put the method here is that it is assumed that the tree
        only has 2 level (main and leaf)
        Returns: 2-tuple: boolean, a list of strings as main nodes' names
        """
        # Get current index and item
        current_index = self.currentIndex()
        if isinstance(current_index, QModelIndex) is False:
            msg = 'Current index is not QModelIndex instance, but {}.'
            return False, msg.format(type(current_index))

        assert (isinstance(current_index, QModelIndex))

        # Get all selected indexes and get their main-node (or itself)'s name
        main_node_list = list()
        q_indexes = self.selectedIndexes()
        for q_index in q_indexes:
            # get item by QIndex
            this_item = self.model().itemFromIndex(q_index)
            # check
            if isinstance(this_item, QStandardItem) is False:
                msg = 'Current item is not QStandardItem instance, but {}.'
                return False,  msg.format(type(this_item))

            # get node name of parent's node name
            if this_item.parent() is not None:
                node_name = str(this_item.parent().text())
            else:
                node_name = str(this_item.text())
            main_node_list.append(node_name)

        return True, main_node_list

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

    def remove_gss_from_plot(self, main_window, gss_group_name, gss_wksps):
        """Remove a GSAS group from canvas if they exits
        :param gss_group_name: name of the GSS node, i.e.,
                               GSS workspace group's name
        :param gss_wksps: list of names of GSS single banks' workspace name
        :return:
        """
        # checks
        msg = 'GSS group workspace name must be a string but not {0}.'
        msg = msg.format(type(gss_group_name))
        assert isinstance(gss_group_name, str), msg

        msg = 'GSAS-single-bank workspace names {0} must be list, not {1}.'
        msg = msg.format(gss_wksps, type(gss_wksps))
        assert isinstance(gss_wksps, list),  msg

        if len(gss_wksps) == 0:
            print("[Warning] GSAS-single-bank workspace name list is empty!")
            return

        # get bank IDs
        bank_ids = list()
        for gss_bank_ws in gss_wksps:
            bank_id = self._get_bank_id(gss_bank_ws)
            bank_ids.append(bank_id)

        graphicsView_bragg = main_window.rietveld_ui.graphicsView_bragg

        # remove
        graphicsView_bragg.remove_gss_banks(gss_group_name, bank_ids)

        # check if there is no such bank's plot on figure
        # make sure the checkbox is unselected
        # turn on the mutex lock
        main_window._noEventBankWidgets = True

        for bank_id in range(1, 7):
            has_plot_on_canvas = len(
                graphicsView_bragg.get_ws_name_on_canvas(bank_id)) > 0
            main_window._braggBankWidgets[bank_id].setChecked(
                has_plot_on_canvas)

        # turn off the mutex lock
        main_window._noEventBankWidgets = False

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

        self._main_window = parent_window
