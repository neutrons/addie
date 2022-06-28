from qtpy.QtWidgets import QTableWidget
from qtpy.QtWidgets import QAction, QLabel
from qtpy.QtCore import Qt


class PostProcessTable(QTableWidget):
    def __init__(self, parent):

        QTableWidget.__init__(self,parent)

        self._action_extract = QAction('Extract', self)
        self._action_extract.triggered.connect(self.extract)
        # self.clicked.connect(self.on_click)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.cellClicked.connect(self.on_click)
        self.selected_item = None
        self.main = None
        self.cur_row = None
        self.cur_col = 0
        self.cur_wks = None
        self.len_workspace = 0


    def extract(self):
        pass

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
        self.cur_wks = self.itemAt(self.cur_row, self.cur_col)


    def mousePressEvent(self, e):
        button = e.button()
        if button == 2:
            # override the response for right button
            QTableWidget.mousePressEvent(self, e)
            self.pop_up_menu()
        else:
            # keep base method for other buttons
            self.enable_extract()
            QTableWidget.mousePressEvent(self, e)


    def enable_extract(self):
        if self.main is not None:
            self.main.postprocessing_ui_m.pushButton_extract.setEnabled(True)


    def pop_up_menu(self):

        rows = self.selectedItems()

        if len(rows) > 1 or len(rows) < 1:
            self.addAction(self._action_extract)
            self._action_extract.setDisabled(True)

        else:
            self.addAction(self._action_extract)
            self._action_extract.setEnabled(True)
