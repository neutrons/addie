def run(main_window=None):
    main_window.postprocessing_ui_m.pushButton_loadWorkspaces.clicked.connect(main_window.open_and_load_workspaces)
    main_window.postprocessing_ui_m.pushButton_extract.clicked.connect(main_window.extract_button)
    main_window.postprocessing_ui_m.pushButton_clearPostProcessingCanvas.clicked.connect(main_window.clear_post_processing_canvas)
    main_window.postprocessing_ui_m.comboBox_banks.currentTextChanged.connect(main_window.change_bank)
    main_window.postprocessing_ui_m.doubleSpinBox_Qmin.valueChanged.connect(main_window.set_merge_values)
    main_window.postprocessing_ui_m.doubleSpinBox_Qmax.valueChanged.connect(main_window.set_merge_values)
    main_window.postprocessing_ui_m.lineEdit_Yoffset.textChanged.connect(main_window.set_merge_values)
    main_window.postprocessing_ui_m.lineEdit_Yscale.textChanged.connect(main_window.set_merge_values)
