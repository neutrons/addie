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

    main_window.calculategr_ui.splitter_4.setStyleSheet("""
                                                        QSplitter::handle {
                                                           image: url(':/MPL Toolbar/splitter_icon.png');
                                                        }
                                                        """)

    # main_window.calculategr_ui.splitter.setStyleSheet("""
    #                                                     QSplitter::handle {
    #                                                        image: url(':/MPL Toolbar/vertical_splitter_icon.png');
    #                                                     }
    #                                                     """)
    #main_window.calculategr_ui.splitter.setSizes([1000, 1])

    main_window.calculategr_ui.treeWidget_grWsList.set_main_window(main_window)
    main_window.calculategr_ui.treeWidget_grWsList.add_main_item('workspaces',
                                                                 append=True,
                                                                 as_current_index=False)
    main_window.calculategr_ui.treeWidget_grWsList.add_main_item('SofQ',
                                                                 append=True,
                                                                 as_current_index=False)

    main_window.calculategr_ui.comboBox_SofQType.clear()
    main_window.calculategr_ui.comboBox_SofQType.addItem('S(Q)')
    main_window.calculategr_ui.comboBox_SofQType.addItem('S(Q)-1')
    main_window.calculategr_ui.comboBox_SofQType.addItem('Q[S(Q)-1]')
    main_window.calculategr_ui.comboBox_SofQType.setCurrentIndex(0)

    main_window.calculategr_ui.comboBox_pdfType.addItems(['G(r)', 'g(r)', 'RDF(r)'])

    # some starting value
    main_window.calculategr_ui.doubleSpinBoxDelR.setValue(0.01)

    # set a constant item to combobox Sq
    main_window.calculategr_ui.comboBox_SofQ.addItem('All')

    # PDF filter
    main_window.calculategr_ui.comboBox_pdfCorrection.clear()
    main_window.calculategr_ui.comboBox_pdfCorrection.addItem('No Modification')
    main_window.calculategr_ui.comboBox_pdfCorrection.addItem('Lorch')

    # set the lower limit on Qmin
    main_window.calculategr_ui.doubleSpinBoxQmin.setDecimals(6)
    main_window.calculategr_ui.doubleSpinBoxQmin.setMinimum(1.E-10)
