import os
from qtpy.QtWidgets import QFileDialog


def load_sq(main_window):
    """
    Load S(Q) from file
    Returns
    -------

    """
    # get default dir
    if main_window._currDataDir is None:
        default_dir = os.getcwd()
    else:
        default_dir = getDefaultDir(main_window,
                                    sub_dir='SofQ')

    # get the file
    ext = 'nxs (*.nxs);;dat (*.dat);;All (*.*)'
    sq_file_names = QFileDialog.getOpenFileNames(main_window,
                                                 'Choose S(Q) File',
                                                 default_dir,
                                                 ext)
    if isinstance(sq_file_names, tuple):
        sq_file_names = sq_file_names[0]
    if sq_file_names is None or sq_file_names == '' or len(sq_file_names) == 0:
        return

    # update current data directory
    main_window._currDataDir = os.path.split(os.path.abspath(sq_file_names[0]))[0]
    check_in_fixed_dir_structure(main_window, 'SofQ')

    # load S(q)
    for sq_file_name in sq_file_names:
        sq_file_name = str(sq_file_name)
        sq_ws_name, q_min, q_max = main_window._myController.load_sq(sq_file_name)
        # add to color management
        color = main_window._pdfColorManager.add_sofq(sq_ws_name)

        # set to the tree and combo box
        main_window.calculategr_ui.treeWidget_grWsList.add_sq(sq_ws_name)
        main_window.calculategr_ui.comboBox_SofQ.addItem(sq_ws_name)
        main_window.calculategr_ui.comboBox_SofQ.setCurrentIndex(main_window.calculategr_ui.comboBox_SofQ.count() - 1)

        # set the UI widgets
        main_window.calculategr_ui.doubleSpinBoxQmin.setValue(q_min)
        main_window.calculategr_ui.doubleSpinBoxQmax.setValue(q_max)

        # plot S(Q) - TODO why is it getting the name again?
        ws_name = main_window._myController.get_current_sq_name()

        main_window.plot_sq(ws_name, color=color, clear_prev=False)

        # calculate and calculate G(R)
        generate_gr_step1()

def getDefaultDir(main_window, sub_dir):
    """ Get the default data directory.
    If is in Fixed-Directory-Structure, then _currDataDir is the parent directory for all GSAS, gofr and SofQ
    and thus return the data directory with _currDataDir joined with sub_dir
    Otherwise, no operation
    """
    # check
    assert isinstance(sub_dir, str), 'sub directory must be a string but not %s.' % type(sub_dir)

    if main_window._inFixedDirectoryStructure:
        default_dir = os.path.join(main_window._currDataDir, sub_dir)
    else:
        default_dir = main_window._currDataDir

    return default_dir

def check_in_fixed_dir_structure(main_window, sub_dir):
    """
    Check whether _currDataDir ends with 'GSAS', 'gofr' or 'SofQ'
    If it is, then reset the _currDataDir to its upper directory and set the in-format flag;
    Otherwise, keep as is
    """
    # make sure that the last character of currDataDir is not /
    if main_window._currDataDir.endswith('/') or main_window._currDataDir.endswith('\\'):
        # consider Linux and Windows case
        main_window._currDataDir = main_window._currDataDir[:-1]

    # split
    main_path, last_dir = os.path.split(main_window._currDataDir)
    if last_dir == sub_dir:
        main_window._inFixedDirectoryStructure = True
        main_window._currDataDir = main_path
    else:
        main_window._inFixedDirectoryStructure = False

def plot_sq(main_window, ws_name, color, clear_prev):
    """
    Plot S(Q)
    :param ws_name:
    :param sq_color: color of S(Q).  If None, then try to find it from PDF color manager
    :param clear_prev:
    :return:
    """
    # clear previous lines
    if clear_prev:
        main_window.calculategr_ui.graphicsView_sq.reset()

    # get data
    vec_q, vec_sq, vec_se = main_window._myController.get_sq(ws_name)

    # get color
    if not color:
        color = main_window._pdfColorManager.add_sofq(ws_name)

    # convert to the function to plot
    sq_type = str(main_window.calculategr_ui.comboBox_SofQType.currentText())
    plottable_name = main_window._myController.calculate_sqAlt(ws_name, sq_type)

    main_window.calculategr_ui.graphicsView_sq.plot_sq(plottable_name,
                                                       sq_y_label=sq_type,
                                                       reset_color_mark=clear_prev,
                                                       color=color)

def generate_gr_step1(main_window):
    """ Handling event from push button 'Generate G(r)' by generating G(r) of selected workspaces
    :return:
    """
    # get S(Q) workspace
    selected_sq = str(main_window.ui.comboBox_SofQ.currentText())
    if selected_sq == 'All':
        sq_ws_name_list = list()
        for index in range(main_window.ui.comboBox_SofQ.count()):
            item = str(main_window.ui.comboBox_SofQ.itemText(index))
            if item != 'All':
                # add S(Q) name unless it is 'All'
                sq_ws_name_list.append(item)
            # END-IF
        # END-FOR
    else:
        # selected S(Q) is a single S(Q) name
        sq_ws_name_list = [selected_sq]

    # generate G(r)
    generate_gr_step2(main_window,
                      sq_ws_name_list=sq_ws_name_list)


def generate_gr_step2(main_window, sq_ws_name_list):
    """Generate G(r) from specified S(Q) workspaces
    """
    # check inputs
    assert isinstance(sq_ws_name_list, list), 'S(Q) workspaces {0} must be given by list but not {1}.' \
                                              ''.format(sq_ws_name_list, type(sq_ws_name_list))
    if len(sq_ws_name_list) == 0:
        raise RuntimeError('User specified an empty list of S(Q)')

    # get r-range and q-range
    min_r = float(main_window.calculategr_ui.doubleSpinBoxRmin.value())
    max_r = float(main_window.calculategr_ui.doubleSpinBoxRmax.value())
    delta_r = float(main_window.calculategr_ui.doubleSpinBoxDelR.value())

    min_q = float(main_window.calculategr_ui.doubleSpinBoxQmin.value())
    max_q = float(main_window.calculategr_ui.doubleSpinBoxQmax.value())

    use_filter_str = str(main_window.calculategr_ui.comboBox_pdfCorrection.currentText())
    if use_filter_str == 'No Modification':
        pdf_filter = None
    elif use_filter_str == 'Lorch':
        pdf_filter = 'lorch'
    else:
        raise RuntimeError('PDF filter {0} is not recognized.'.format(use_filter_str))
    rho0_str = str(main_window.ui.lineEdit_rho.text())
    try:
        rho0=float(rho0_str)
    except ValueError:
        rho0 = None

    # PDF type
    pdf_type = str(main_window.ui.comboBox_pdfType.currentText())

    # loop for all selected S(Q)
    for sq_ws_name in sq_ws_name_list:
        # calculate G(r)
        gr_ws_name = main_window._myController.calculate_gr(sq_ws_name, pdf_type, min_r, delta_r, max_r,
                                                     min_q, max_q, pdf_filter, rho0)

        # check whether G(r) is on GofR plot or not in order to determine this is an update or new plot
        update = main_window.ui.graphicsView_gr.has_gr(gr_ws_name)

        # plot G(R)
        if not update:
            # a new line
            gr_color, gr_style, gr_marker, gr_alpha = main_window._pdfColorManager.add_gofr(sq_ws_name, gr_ws_name, max_q)
            gr_label = '{0} Q: ({1}, {2})'.format(sq_ws_name, min_q, max_q)
            main_window.plot_gr(gr_ws_name, gr_color, gr_style, gr_marker, gr_alpha, gr_label)
        else:
            main_window.plot_gr(gr_ws_name, line_color=None, line_style=None, line_marker=None,
                         line_alpha=None, line_label=None)

        # add to tree
        # TODO/ISSUE/NOW - Need to find out the name of the
        gr_param_str = 'G(r) for Q(%.3f, %.3f)' % (min_q, max_q)
        main_window.ui.treeWidget_grWsList.add_gr(gr_param_str, gr_ws_name)
    # END-FOR

    return
