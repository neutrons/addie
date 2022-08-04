from qtpy.QtWidgets import QAction
from qtpy.QtGui import QStandardItemModel
from addie.utilities import customtreeview as base
from addie.post_process_m import event_handler


class FileListTree(base.CustomizedTreeView):

    def __init__(self, parent):
        base.CustomizedTreeView.__init__(self, parent)
        self._action_plot = QAction('Plot', self)
        self._action_plot.triggered.connect(self.do_plot)
        self._main_window = None
        self._current_workspace = None
        if parent:
            self.set_main_window(parent)
        self.reset_files_tree()

    def load_data(self, files, workspace):
        self._current_workspace = workspace
        for extracted_file in files:
            self.add_child_current_item(extracted_file)

    def reset_files_tree(self):
        if self.model() is not None:
            self.model().clear()

        self._myHeaderList = list()
        self._leafDict.clear()
        self._myNumCols = 1

        model = QStandardItemModel()
        model.setColumnCount(self._myNumCols)
        self.setModel(model)
        self.init_setup(['File List'])
        self.add_main_item('Raw Data', append=True, as_current_index=True)
        self.add_main_item('Merged Data', append=True, as_current_index=False)
        self.add_main_item('StoG Data', append=True, as_current_index=False)

    def do_plot(self):
        item_list = self.get_selected_items()
        item_list = [str(item.text()) for item in item_list]

        if self._main_window is not None:
            print("do_plot: banks", item_list)
            bank_indexes = self.selectedIndexes()
            event_handler.plot(
                self._main_window,
                item_list,
                bank_indexes,
                self._current_workspace
            )

    def mousePressEvent(self, e):
        button_pressed = e.button()
        if button_pressed == 2:
            base.CustomizedTreeView.mousePressEvent(self, e)
            self.pop_up_menu()
        else:
            base.CustomizedTreeView.mousePressEvent(self, e)

    def pop_up_menu(self):
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
            if leaf_level == 2:
                self.addAction(self._action_plot)

    def set_main_window(self, parent):
        assert parent is not None, 'Parent window cannot be None'
        self._main_window = parent
