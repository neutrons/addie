from qtpy import QtGui

SMALL_FIELD_WIDTH = 120
COLUMN_WIDTHS = [60, 250, 250, SMALL_FIELD_WIDTH, SMALL_FIELD_WIDTH + 30,
                 SMALL_FIELD_WIDTH, SMALL_FIELD_WIDTH,
                 SMALL_FIELD_WIDTH, SMALL_FIELD_WIDTH, 80]


def run(main_window=None):

    main_window.postprocessing_ui.splitter.setStyleSheet("""
        QSplitter::handle {
           image: url(':/MPL Toolbar/splitter_icon.png');
        }
        """)

    main_window.postprocessing_ui.label_21.setPixmap(QtGui.QPixmap(":/MPL Toolbar/search_icon.png"))

    main_window.postprocessing_ui.run_rmc_groupbox.setVisible(False)
    for _index, _width in enumerate(COLUMN_WIDTHS):
        main_window.postprocessing_ui.table.setColumnWidth(_index, _width)

    # q range
    _q_range_title = "Q range (\u212B\u207B\u00b9)"
    main_window.postprocessing_ui.q_range_group_box.setTitle(_q_range_title)

    # fourier filter
    _fourier_filter_title = "Fourier filter (\u212B)"
    main_window.postprocessing_ui.fourier_filter_group_box.setTitle(_fourier_filter_title)
