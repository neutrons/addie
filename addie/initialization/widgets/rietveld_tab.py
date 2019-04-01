from qtpy.QtCore import Qt
from qtpy.QtWidgets import QVBoxLayout

from addie.rietveld.braggview import BraggView
from addie.rietveld.braggtree import BraggTree


def run(main_window=None):
    # frame_graphicsView_bragg
    graphicsView_layout = QVBoxLayout()
    main_window.rietveld_ui.frame_graphicsView_bragg.setLayout(graphicsView_layout)
    main_window.rietveld_ui.graphicsView_bragg = BraggView(main_window)
    graphicsView_layout.addWidget(main_window.rietveld_ui.graphicsView_bragg)

    # frame_treeWidget_braggWSList
    temp_layout = QVBoxLayout()
    main_window.rietveld_ui.frame_treeWidget_braggWSList.setLayout(temp_layout)
    main_window.rietveld_ui.treeWidget_braggWSList = BraggTree(main_window)
    temp_layout.addWidget(main_window.rietveld_ui.treeWidget_braggWSList)

    main_window.rietveld_ui.splitter_2.setStyleSheet("""
        QSplitter::handle {
           image: url(':/MPL Toolbar/vertical_splitter_icon.png');
        }
        """)
    main_window.rietveld_ui.splitter_2.setSizes([1000, 1])

    main_window.rietveld_ui.comboBox_xUnit.clear()
    main_window.rietveld_ui.comboBox_xUnit.addItems(['TOF', 'dSpacing', 'Q'])
    index = main_window.rietveld_ui.comboBox_xUnit.findText('dSpacing', Qt.MatchFixedString)
    main_window.rietveld_ui.comboBox_xUnit.setCurrentIndex(index)

    main_window.rietveld_ui.treeWidget_braggWSList.set_main_window(main_window)
    main_window.rietveld_ui.treeWidget_braggWSList.add_main_item('workspaces',
                                                                 append=True,
                                                                 as_current_index=False)

    main_window.rietveld_ui.radioButton_multiBank.setChecked(True)

    # organize widgets group
    main_window._braggBankWidgets = {1: main_window.rietveld_ui.checkBox_bank1,
                                     2: main_window.rietveld_ui.checkBox_bank2,
                                     3: main_window.rietveld_ui.checkBox_bank3,
                                     4: main_window.rietveld_ui.checkBox_bank4,
                                     5: main_window.rietveld_ui.checkBox_bank5,
                                     6: main_window.rietveld_ui.checkBox_bank6}
    main_window._braggBankWidgetRecords = dict()
    for bank_id in main_window._braggBankWidgets:
        checked = main_window._braggBankWidgets[bank_id].isChecked()
        main_window._braggBankWidgetRecords[bank_id] = checked

    # some controlling variables
    main_window._currBraggXUnit = str(main_window.rietveld_ui.comboBox_xUnit.currentText())
    if main_window._currBraggXUnit == 'Q':
        main_window._currBraggXUnit = 'MomentumTransfer'
    main_window._onCanvasGSSBankList = list()
