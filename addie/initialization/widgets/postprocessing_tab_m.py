# from qtpy.QtCore import Qt
from qtpy.QtWidgets import QVBoxLayout, QHeaderView
from qtpy.QtCore import Qt
from addie.post_process_m.postprocesstable import PostProcessTable
from addie.post_process_m.filelisttree import FileListTree
from addie.post_process_m.ppmview import PPMView


def run(main_window=None):
    main_window.postprocessing_ui_m.pushButton_extract.setEnabled(False)
    main_window.postprocessing_ui_m.pushButton_savemc.setEnabled(False)
    main_window.postprocessing_ui_m.pushButton_savesc.setEnabled(False)
    main_window.postprocessing_ui_m.pushButton_loadmc.setEnabled(False)
    main_window.postprocessing_ui_m.pushButton_loadsc.setEnabled(False)
    main_window.postprocessing_ui_m.comboBox_pdfform.addItems(['g(r)', 'G(r)'])

   # setup the plot view
    graphics_view = QVBoxLayout()
    main_window.postprocessing_ui_m.frame_ppm_view.setLayout(graphics_view)
    main_window.postprocessing_ui_m.ppm_view = PPMView(main_window)
    graphics_view.addWidget(main_window.postprocessing_ui_m.ppm_view)

   # setup the workspaces table
    temp_layout = QVBoxLayout()
    main_window.postprocessing_ui_m.frame_workspaces_table.setLayout(temp_layout)
    main_window.postprocessing_ui_m.frame_workspaces_table = PostProcessTable(main_window)
    temp_layout.addWidget(main_window.postprocessing_ui_m.frame_workspaces_table)
    main_window.postprocessing_ui_m.frame_workspaces_table.setColumnCount(1)
    header_label = ['Workspaces']
    main_window.postprocessing_ui_m.frame_workspaces_table.setHorizontalHeaderLabels(header_label)

    header = main_window.postprocessing_ui_m.frame_workspaces_table.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.Stretch)
    header.setDefaultAlignment(Qt.AlignLeft)

   # setup the files tree
    temp_layout = QVBoxLayout()
    main_window.postprocessing_ui_m.frame_filelist_tree.setLayout(temp_layout)
    main_window.postprocessing_ui_m.frame_filelist_tree = FileListTree(main_window)
    temp_layout.addWidget(main_window.postprocessing_ui_m.frame_filelist_tree)
    tree = main_window.postprocessing_ui_m.frame_filelist_tree
    tree.header().setStretchLastSection(True)

    main_window.postprocessing_ui_m.frame_filelist_tree.setStyleSheet("""
    FileListTree {
       alternate-background-color: yellow;
    }
    """)

    main_window.postprocessing_ui_m.splitter.setStyleSheet("""
    QSplitter::handle {
       image: url(':/MPL Toolbar/vertical_splitter_icon.png');
    }
    """)
