from qtpy import QtGui


def run(main_window=None):
    main_window.processing_ui.clear_search_button.clicked.connect(main_window.table_search_clear)
    main_window.processing_ui.settings_table_button.clicked.connect(main_window.personalization_table_clicked)



