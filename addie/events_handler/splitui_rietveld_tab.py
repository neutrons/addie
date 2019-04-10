def run(main_window=None):
    main_window.ui.pushButton_loadBraggFile.clicked.connect(main_window.do_load_bragg_file)
    main_window.ui.checkBox_bank1.toggled.connect(main_window.evt_plot_bragg_bank)
    main_window.ui.checkBox_bank2.toggled.connect(main_window.evt_plot_bragg_bank)
    main_window.ui.checkBox_bank3.toggled.connect(main_window.evt_plot_bragg_bank)
    main_window.ui.checkBox_bank4.toggled.connect(main_window.evt_plot_bragg_bank)
    main_window.ui.checkBox_bank5.toggled.connect(main_window.evt_plot_bragg_bank)
    main_window.ui.checkBox_bank6.toggled.connect(main_window.evt_plot_bragg_bank)
    main_window.ui.comboBox_xUnit.currentIndexChanged.connect(main_window.evt_switch_bragg_unit)
    main_window.ui.radioButton_multiBank.toggled.connect(main_window.evt_change_gss_mode)

    main_window.ui.pushButton_rescaleGSAS.clicked.connect(main_window.do_rescale_bragg)

    main_window.ui.pushButton_gsasColorStyle.clicked.connect(main_window.do_set_bragg_color_marker)
    main_window.ui.pushButton_clearBraggCanvas.clicked.connect(main_window.do_clear_bragg_canvas)
