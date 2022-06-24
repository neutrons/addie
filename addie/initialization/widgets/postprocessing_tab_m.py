# from qtpy.QtCore import Qt
# from qtpy.QtWidgets import QVBoxLayout
def run(main_window=None):
    main_window.postprocessing_ui_m.splitter.setStyleSheet("""
    QSplitter::handle {
       image: url(':/MPL Toolbar/vertical_splitter_icon.png');
    }
    """)
