from qtpy import QtGui


def run(main_window=None):
    main_window.processing_ui.search_logo_label.setPixmap(QtGui.QPixmap(":/MPL Toolbar/search_icon.png"))
    main_window.processing_ui.clear_search_button.setIcon(QtGui.QIcon(":/MPL Toolbar/clear_icon.png"))
    main_window.processing_ui.settings_table_button.setIcon(QtGui.QIcon(":/MPL Toolbar/settings_icon.png"))




