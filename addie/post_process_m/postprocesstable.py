from qtpy.QtWidgets import QTableWidget
from qtpy.QtWidgets import QAction, QLabel
from qtpy.QtCore import Qt
import addie.post_process_m.event_handler as event


class PostProcessTable(QTableWidget):
    def __init__(self, parent):

        QTableWidget.__init__(self,parent)

        self._action_extract = QAction('Extract', self)
        self._action_extract.triggered.connect(self.extract)

        self.parent = parent
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.cellClicked.connect(self.on_click)
        self.selected_item = None
        self.main = None
        self.cur_row = None
        self.cur_col = 0
        self.cur_wks = None
        self.len_workspace = 0

    def extract(self):
        if self.main is not None:
            self.cur_wks = str(self.cellWidget(self.cur_row, self.cur_col).text())
            event.extract_button(self.main)

    def load(self, workspaces, main_window):
        self.main = main_window
        # clear rows
        self.setRowCount(0)

        # load the workspace table
        for workspace in workspaces:
            row_count = self.rowCount()
            self.insertRow(row_count)
            cell = QLabel(workspace)
            self.setCellWidget(row_count,0, cell)

        self.verticalHeader().hide()

    def on_click(self):
        self.cur_row = self.currentRow()

    def mousePressEvent(self, e):
        button = e.button()
        if button == 2:
            # override the response for right button
            QTableWidget.mousePressEvent(self, e)
            self.enable_disable_extract()
            self.pop_up_menu()
        else:
            # keep base method for other buttons
            QTableWidget.mousePressEvent(self, e)
            self.enable_disable_extract()

    def enable_disable_extract(self):
        indexes = self.selectedIndexes()
        if self.main is not None and len(indexes) == 1:
            self.main.postprocessing_ui_m.pushButton_extract.setEnabled(True)
            self.cur_row = self.currentRow()
            self.cur_wks = str(self.cellWidget(self.cur_row, self.cur_col).text())
        elif len(indexes) != 1:
            if self.main:
                self.main.postprocessing_ui_m.pushButton_extract.setDisabled(True)

    def pop_up_menu(self):
        indexes_selected = self.selectedIndexes()

        if len(indexes_selected) != 1:
            self.removeAction(self._action_extract)
        else:
            self.addAction(self._action_extract)

    def get_current_workspace(self):
        # if self.cur_wks is None:
        #     self.cur_row = self.currentRow()
        #     self.cur_wks = str(self.cellWidget(self.cur_row, self.cur_col).text())
        return self.cur_wks
