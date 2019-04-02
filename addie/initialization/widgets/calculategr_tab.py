from qtpy import QtGui
from qtpy.QtWidgets import QVBoxLayout

from addie.calculate_gr.gofrtree import GofRTree
from addie.calculate_gr.gofrview import GofRView
from addie.calculate_gr.sofqview import SofQView


def run(main_window=None):

    # frame_graphicsView_sq
    graphicsView_layout = QVBoxLayout()
    main_window.calculategr_ui.frame_graphicsView_sq.setLayout(graphicsView_layout)
    main_window.calculategr_ui.graphicsView_sq = SofQView(main_window)
    graphicsView_layout.addWidget(main_window.calculategr_ui.graphicsView_sq)

    # frame_graphicsView_gr
    graphicsView_layout = QVBoxLayout()
    main_window.calculategr_ui.frame_graphicsView_gr.setLayout(graphicsView_layout)
    main_window.calculategr_ui.graphicsView_gr = GofRView(main_window)
    graphicsView_layout.addWidget(main_window.calculategr_ui.graphicsView_gr)

    # frame_treeWidget_grWsList
    temp_layout = QVBoxLayout()
    main_window.calculategr_ui.frame_treeWidget_grWsList.setLayout(temp_layout)
    main_window.calculategr_ui.treeWidget_grWsList = GofRTree(main_window)
    temp_layout.addWidget(main_window.calculategr_ui.treeWidget_grWsList)


