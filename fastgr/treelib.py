#
# An extension on QTreeView for file system
#
import os

from PyQt4 import QtGui, QtCore
import customtreeview as base


class FileSystemTreeView(QtGui.QTreeView):
    """

    """
    def __init__(self, parent):
        """

        :param parent:
        :return:
        """
        QtGui.QTreeView.__init__(self, parent)

        # Selection mode
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        # Model
        cur_dir = os.path.expanduser('~')
        file_model = QtGui.QFileSystemModel()
        #file_model.setRootPath(QtCore.QString(cur_dir))
        file_model.setRootPath(str(cur_dir))

        self.setModel(file_model)

        return

    def set_root_path(self, root_path):
        """

        :param root_path: root path (i.e., no parent)
        :return:
        """
        # Root path: from model to TreeView
        self.model().setRootPath(root_path)
        idx = self.model().index(root_path)
        self.setRootIndex(idx)

        self.set_current_path(root_path)

        return

    def set_current_path(self, current_path):
        """

        :param current_path:
        :return:
        """
        # Set default path (i.e., current view)
        idx = self.model().index(current_path)
        self.setCurrentIndex(idx)

        return


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

        self.init_setup(['Bragg Workspaces'])

        # add actions
        # plot
        action_plot = QtGui.QAction('Plot', self)
        action_plot.triggered.connect(self.do_plot_ws)
        self.addAction(action_plot)
        # to python
        action_ipython = QtGui.QAction('To IPython', self)
        action_ipython.triggered.connect(self.do_copy_to_ipython)
        self.addAction(action_ipython)

        self._mainWindow = None

        return

    def add_bragg_ws_group(self, ws_group_name, bank_name_list):
        """
        Add a workspace group containing a list of bank names
        Parameters
        ----------
        ws_group_name
        bank_name_list

        Returns
        -------

        """
        # TODO/NOW - Doc & check

        # main node/leaf
        main_leaf_value = str(ws_group_name)
        # TODO/NOW - add check ...
        self.add_main_item(main_leaf_value, True)

        for bank_name in bank_name_list:
            self.add_child_main_item(main_leaf_value, bank_name)

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
        if isinstance(current_index, QtCore.QModelIndex) is False:
            return False, 'Current index is not QModelIndex instance, but %s.' % str(type(current_index))

        assert (isinstance(current_index, QtCore.QModelIndex))

        current_item = self.model().itemFromIndex(current_index)
        if isinstance(current_item, QtGui.QStandardItem) is False:
            return False, 'Current item is not QStandardItem instance, but %s.' % str(type(current_item))
        assert (isinstance(current_item, QtGui.QStandardItem))

        ws_name = str(current_item.text())

        python_cmd = "ws = mtd['%s']" % ws_name

        if self._mainWindow is not None:
            self._mainWindow.set_ipython_script(python_cmd)

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

    def get_current_main_node(self):
        """
        Get the name of the current nodes that are selected
        The reason to put the method here is that the 
        Returns:

        """
        # Get current index and item
        current_index = self.currentIndex()
        if isinstance(current_index, QtCore.QModelIndex) is False:
            return False, 'Current index is not QModelIndex instance, but %s.' % str(type(current_index))

        assert (isinstance(current_index, QtCore.QModelIndex))

        current_item = self.model().itemFromIndex(current_index)
        if isinstance(current_item, QtGui.QStandardItem) is False:
            return False, 'Current item is not QStandardItem instance, but %s.' % str(type(current_item))
        assert (isinstance(current_item, QtGui.QStandardItem))

        if current_item.parent() is None:
            # Top-level leaf, IPTS number
            node_name = str(current_item.parent().text())
        else:
            node_name = str(current_item.text())

        return node_name

    def set_main_window(self, parent_window):
        """

        Parameters
        ----------
        parent_window

        Returns
        -------

        """
        # TODO/NOW - Doc and check
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

        self.init_setup(['G(R) Workspaces'])

        # Add actions
        # plot
        action_plot = QtGui.QAction('Plot', self)
        action_plot.triggered.connect(self.do_plot_gr)
        self.addAction(action_plot)
        # to python
        action_ipython = QtGui.QAction('To IPython', self)
        action_ipython.triggered.connect(self.do_copy_to_ipython)
        self.addAction(action_ipython)

        self._mainWindow = None

        return

    def add_gr(self, gr_parameter, gr_ws_name):
        """
        Add runs of on IPTS
        :param ipts_number: it might an ipts number or a directory
        :param run_numbers:
        :return:
        """
        # TODO/DOC - check and etc.
        # Check

        # Create main leaf value
        main_leaf_value = str(gr_parameter)
        status, message = self.add_main_item(main_leaf_value, False)
        if status is False:
            print '[Log] %s' % message

        # Add workspace name as a leaf
        child_value = gr_ws_name
        self.add_child_main_item(main_leaf_value, child_value)

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

    def do_copy_to_ipython(self):
        """

        Returns
        -------

        """
        # TODO/NOW - Doc and check

        # Get current index and item
        current_index = self.currentIndex()
        if isinstance(current_index, QtCore.QModelIndex) is False:
            return False, 'Current index is not QModelIndex instance, but %s.' % str(type(current_index))

        assert (isinstance(current_index, QtCore.QModelIndex))

        current_item = self.model().itemFromIndex(current_index)
        if isinstance(current_item, QtGui.QStandardItem) is False:
            return False, 'Current item is not QStandardItem instance, but %s.' % str(type(current_item))
        assert (isinstance(current_item, QtGui.QStandardItem))

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

    def do_plot_gr(self):
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
            self._mainWindow.plot_gr(leaf_list)
        else:
            raise NotImplementedError('Main windown has not been set up!')

        # print '[DB...BAT] selected leaves: ', leaf_list

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
        if isinstance(current_index, QtCore.QModelIndex) is False:
            return False, 'Current index is not QModelIndex instance, but %s.' % str(type(current_index))

        assert(isinstance(current_index, QtCore.QModelIndex))

        current_item = self.model().itemFromIndex(current_index)
        if isinstance(current_item, QtGui.QStandardItem) is False:
            return False, 'Current item is not QStandardItem instance, but %s.' % str(type(current_item))
        assert(isinstance(current_item, QtGui.QStandardItem))

        if current_item.parent() is None:
            # Top-level leaf, IPTS number
            return False, 'Top-level leaf for IPTS number'

        try:
            value_str = str(current_item.text())
            run = int(value_str)
        except ValueError:
            return False, 'Unable to convert %s to run number as integer.' % value_str

        return True, run

    def mouseDoubleClickEvent(self, e):
        """ Override event handling method
        """
        status, current_run = self.get_current_run()

        if self._mainWindow is not None:
            self._mainWindow.set_run(current_run)

        return

    def set_main_window(self, main_window):
        """

        :param main_window:
        :return:
        """
        self._mainWindow = main_window

        return

