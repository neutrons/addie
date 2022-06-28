def run(main_window=None):
    main_window.postprocessing_ui_m.pushButton_loadWorkspaces.clicked.connect(main_window.open_and_load_workspaces)
    main_window.postprocessing_ui_m.pushButton_extract.clicked.connect(main_window.extract_button)
