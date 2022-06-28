from qtpy.QtWidgets import QTreeWidget, QTreeWidgetItem
from qtpy.QtWidgets import QAction, QLabel
from qtpy.QtCore import Qt

class FileListTree(QTreeWidget):
    def __init__(self, parent):
        QTreeWidget.__init__(self, parent)


    def load_raw_data(self, main_window, files):
        file_list = main_window.postprocessing_ui_m.frame_filelist_tree
        raw_data_root = QTreeWidgetItem(file_list, ['Raw Data'])
        file_list.addTopLevelItem(raw_data_root)

        for extracted_file in files:
            to_add = QTreeWidgetItem()
            to_add.setText([extracted_file])
            raw_data_root.addChild(to_add)
