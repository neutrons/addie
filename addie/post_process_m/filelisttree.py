from qtpy.QtWidgets import QAction
from qtpy.QtGui import QStandardItemModel
from addie.utilities import customtreeview as base
from addie.post_process_m import event_handler


class FileListTree(base.CustomizedTreeView):

    def __init__(self, parent):
        base.CustomizedTreeView.__init__(self, parent)
        self._action_plot = QAction('Plot', self)
        self._action_plot.triggered.connect(self.do_plot)
        self._action_save_merge = QAction('Save', self)
        self._action_save_merge.triggered.connect(self.save_merge)
        self._action_save_raw = QAction('Save', self)
        self._action_save_raw.triggered.connect(self.save_raw)
        self._action_save_stog = QAction('Save', self)
        self._action_save_stog.triggered.connect(self.save_stog)
        self._main_window = None
        self._current_workspace = None
        self._selected_items = None
        if parent:
            self.set_main_window(parent)
        self.reset_files_tree()

    def set_workspace(self, workspace):
        self._current_workspace = workspace

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
        mode = ''
        if item_list[0].parent().text() == 'Raw Data':
            item_list = [str(item.text()) for item in item_list]
            mode = 'Raw'
        elif item_list[0].parent().text() == 'Merged Data':
            item_list = [str(item.text()) for item in item_list]
            mode = 'Merged'
        elif item_list[0].parent().text() == 'StoG Data':
            item_list = [str(item.text()) for item in item_list]
            mode = 'StoG'
        if self._main_window is not None:
            bank_indexes = self.selectedIndexes()
            event_handler.plot(
                self._main_window,
                item_list,
                bank_indexes,
                self._current_workspace,
                mode
            )

    def mousePressEvent(self, e):
        button_pressed = e.button()
        if button_pressed == 2:
            base.CustomizedTreeView.mousePressEvent(self, e)
            self.pop_up_menu()
        else:
            base.CustomizedTreeView.mousePressEvent(self, e)

    def pop_up_menu(self):
        self._selected_items = self.get_selected_items()
        if len(self._selected_items) == 0:
            return
        leaf_level = -1
        for item in self._selected_items:
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
                if item.parent().text() == 'Merged Data':
                    self.addAction(self._action_save_merge)
                    self.removeAction(self._action_save_raw)
                    self.removeAction(self._action_save_stog)
                elif item.parent().text() == 'Raw Data':
                    self.addAction(self._action_save_raw)
                    self.removeAction(self._action_save_merge)
                    self.removeAction(self._action_save_stog)
                elif item.parent().text() == 'StoG Data':
                    self.addAction(self._action_save_stog)
                    self.removeAction(self._action_save_raw)
                    self.removeAction(self._action_save_merge)

    def set_main_window(self, parent):
        assert parent is not None, 'Parent window cannot be None'
        self._main_window = parent

    def add_merged_data(self, merged_banks_ref):
        self.add_child_main_item('Merged Data', merged_banks_ref)
        # save the merged data file with the automated mode set true
        event_handler.save_file_merged(self._main_window, auto=True)

    def save_merge(self):
        # save the merged data file with the automated mode set false
        if len(self._selected_items) > 1:
            return
        event_handler.save_file_merged(self._main_window)

    def save_raw(self):
        if len(self._selected_items) > 1:
            return
        event_handler.save_file_raw(self._main_window, self._selected_items[0].text())

    def save_stog(self):
        if len(self._selected_items) > 1:
            return
        event_handler.save_file_stog(self._main_window, self._selected_items[0].text())

    def add_stog_data(self, file_name):
        # output = self._main_window.output_folder
        self.add_child_main_item('StoG Data', file_name)

    def add_raw_data(self, banks):
        for bank in banks:
            self.add_child_main_item('Raw Data', bank)
