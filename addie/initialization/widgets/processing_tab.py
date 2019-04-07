from qtpy import QtGui

from addie.processing.mantid.master_table.table_tree_handler import TableInitialization


def run(main_window=None):

    # widgets
    main_window.processing_ui.search_logo_label.setPixmap(QtGui.QPixmap(":/MPL Toolbar/search_icon.png"))
    main_window.processing_ui.clear_search_button.setIcon(QtGui.QIcon(":/MPL Toolbar/clear_icon.png"))
    main_window.processing_ui.settings_table_button.setIcon(QtGui.QIcon(":/MPL Toolbar/settings_icon.png"))

    # table
    # TODO should look for ~/.mantid/addie.json and load it
    o_table = TableInitialization(main_window=main_window)
    o_table.init_master_table()
    o_table.init_signals()
