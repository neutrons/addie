def run(main_window=None):
    main_window.ui.actionQuit.triggered.connect(main_window.evt_quit)
    main_window.ui.actionCheat_sheet.triggered.connect(main_window.do_show_help)
