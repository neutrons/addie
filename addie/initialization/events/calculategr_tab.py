def run(main_window=None):
    main_window.calculategr_ui.pushButton_loadSQ.clicked.connect(main_window.do_load_sq)
    main_window.calculategr_ui.comboBox_SofQType.currentIndexChanged.connect(main_window.evt_change_sq_type)
    main_window.calculategr_ui.pushButton_rescaleSq.clicked.connect(main_window.do_rescale_sofq)
    main_window.calculategr_ui.pushButton_rescaleGr.clicked.connect(main_window.do_rescale_gofr)
    main_window.calculategr_ui.pushButton_clearSofQ.clicked.connect(main_window.do_clear_sq)
    main_window.calculategr_ui.pushButton_showQMinMax.clicked.connect(main_window.do_show_sq_bound)
    main_window.calculategr_ui.pushButton_generateGR.clicked.connect(main_window.do_generate_gr)
    main_window.calculategr_ui.pushButton_loadGofR.clicked.connect(main_window.do_load_gr)
    main_window.calculategr_ui.pushButton_saveGR.clicked.connect(main_window.do_save_gr)
    main_window.calculategr_ui.pushButton_clearGrCanvas.clicked.connect(main_window.do_clear_gr)
    main_window.calculategr_ui.pushButton_saveSQ.clicked.connect(main_window.do_save_sq)
    main_window.calculategr_ui.pushButton_editSofQ.clicked.connect(main_window.do_edit_sq)
    main_window.calculategr_ui.pushButton_generateSQ.clicked.connect(main_window.do_generate_sq)

    main_window.calculategr_ui.doubleSpinBoxQmin.valueChanged.connect(main_window.evt_qmin_changed)
    main_window.calculategr_ui.doubleSpinBoxQmax.valueChanged.connect(main_window.evt_qmax_changed)

    main_window.calculategr_ui.pushButton_grColorStyle.clicked.connect(main_window.do_set_gofr_color_marker)
    main_window.calculategr_ui.pushButton_sqColorStyle.clicked.connect(main_window.do_set_sq_color_marker)

    #  menu operations
    main_window.ui.actionReset_GofR_tab.triggered.connect(main_window.do_reset_gr_tab)
    main_window.ui.actionReset_GSAS_tab.triggered.connect(main_window.do_reset_gsas_tab)
