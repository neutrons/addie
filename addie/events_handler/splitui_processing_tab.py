def run(main_window=None):
    main_window.processing_ui.clear_search_button.clicked.connect(main_window.table_search_clear)
    main_window.processing_ui.settings_table_button.clicked.connect(main_window.personalization_table_clicked)
    main_window.processing_ui.reduction_configuration_button.clicked.connect(main_window.reduction_configuration_button_clicked)
    main_window.processing_ui.browse_calibration_button.clicked.connect(main_window.browse_calibration_clicked)
    main_window.processing_ui.make_calibration_button.clicked.connect(main_window.make_calibration_clicked)
    main_window.processing_ui.h3_table.customContextMenuRequested.connect(main_window.h3_table_right_click)
