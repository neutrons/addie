import os
from qtpy.QtWidgets import QFileDialog, QMessageBox

from addie.utilities import check_in_fixed_dir_structure, get_default_dir
import addie.utilities.specify_plots_style as ps
import addie.utilities.workspaces
import addie.calculate_gr.edit_sq_dialog
from addie.calculate_gr.save_sq_dialog_message import SaveSqDialogMessageDialog
from addie.widgets.filedialog import get_save_file
from mantid.api import AnalysisDataService
import mantid.simpleapi as simpleapi
from pystog import Transformer, FourierFilter


def check_widgets_status(main_window, enable_gr_widgets=False):
    # index 0 is "all"
    number_of_sofq = main_window.calculategr_ui.comboBox_SofQ.count() - 1
    if number_of_sofq > 0:
        sofq_status = True
        gr_status = True
    else:
        sofq_status = False
        gr_status = False

    if enable_gr_widgets:
        gr_status = True

    sofq_widgets_status(main_window, sofq_status)
    gr_widgets_status(main_window, gr_status)


def sofq_widgets_status(main_window, sofq_status):
    list_sofq_ui = [main_window.calculategr_ui.pushButton_rescaleSq,
                    main_window.calculategr_ui.pushButton_sqColorStyle,
                    main_window.calculategr_ui.pushButton_editSofQ,
                    main_window.calculategr_ui.pushButton_clearSofQ,
                    main_window.calculategr_ui.pushButton_saveSQ,
                    main_window.calculategr_ui.pushButton_showQMinMax,
                    main_window.calculategr_ui.pushButton_generateGR]

    for _ui in list_sofq_ui:
        _ui.setEnabled(sofq_status)


def gr_widgets_status(main_window, gr_status):
    list_gr_ui = [main_window.calculategr_ui.pushButton_saveGR,
                  main_window.calculategr_ui.pushButton_rescaleGr,
                  main_window.calculategr_ui.pushButton_grColorStyle,
                  main_window.calculategr_ui.pushButton_generateSQ,
                  main_window.calculategr_ui.pushButton_clearGrCanvas]

    for _ui in list_gr_ui:
        _ui.setEnabled(gr_status)


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
        default_dir = get_default_dir(main_window, sub_dir='SofQ')

    # get the file
    ext = 'dat (*.dat);;nxs (*.nxs);;All (*.*)'
    sq_file_names = QFileDialog.getOpenFileNames(main_window,
                                                 'Choose S(Q) File',
                                                 default_dir,
                                                 ext)
    if isinstance(sq_file_names, tuple):
        sq_file_names = sq_file_names[0]
    if sq_file_names is None or sq_file_names == '' or len(sq_file_names) == 0:
        return

    # update current data directory
    main_window._currDataDir = os.path.split(
        os.path.abspath(sq_file_names[0]))[0]
    check_in_fixed_dir_structure(main_window, 'SofQ')

    # load S(q)
    for sq_file_name in sq_file_names:
        sq_file_name = str(sq_file_name)
        sq_ws_name, q_min, q_max = main_window._myController.load_sq(
            sq_file_name)
        if sq_ws_name == "InvalidInput" and q_min == 0 and q_max == 0:
            return
        # add to color management
        color = main_window._pdfColorManager.add_sofq(sq_ws_name)

        # set to the tree and combo box
        main_window.calculategr_ui.treeWidget_grWsList.add_sq(sq_ws_name)
        main_window.calculategr_ui.comboBox_SofQ.addItem(sq_ws_name)
        main_window.calculategr_ui.comboBox_SofQ.setCurrentIndex(
            main_window.calculategr_ui.comboBox_SofQ.count() - 1)

        # set the UI widgets
        main_window.calculategr_ui.doubleSpinBoxQmin.setValue(q_min)
        main_window.calculategr_ui.doubleSpinBoxQmax.setValue(q_max)

        # plot S(Q) - TODO why is it getting the name again?
        ws_name = main_window._myController.get_current_sq_name()

        plot_sq(main_window, ws_name, color=color, clear_prev=False)

        # calculate and calculate G(R)
        generate_gr_step1(main_window)

    check_widgets_status(main_window)


def plot_sq(main_window, ws_name, color, clear_prev):
    """
    Plot S(Q)
    :param ws_name:
    :param sq_color: S(Q) color (if None, find it from PDF color manager)
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
    plottable_name = main_window._myController.calculate_sqAlt(
        ws_name, sq_type)

    main_window.calculategr_ui.graphicsView_sq.plot_sq(
        plottable_name,
        sq_y_label=sq_type,
        reset_color_mark=clear_prev,
        color=color)


def generate_gr_step1(main_window):
    """ Handling event from push button 'Generate G(r)' by
    generating G(r) of selected workspaces
    :return:
    """
    # get S(Q) workspace
    comboBox_SofQ = main_window.calculategr_ui.comboBox_SofQ
    selected_sq = str(comboBox_SofQ.currentText())
    if selected_sq == 'All':
        sq_ws_name_list = list()
        for index in range(comboBox_SofQ.count()):
            item = str(comboBox_SofQ.itemText(index))
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
    msg = 'S(Q) workspaces {0} must be given by list but not {1}.'
    msg = msg.format(sq_ws_name_list, type(sq_ws_name_list))
    assert isinstance(sq_ws_name_list, list), msg
    if len(sq_ws_name_list) == 0:
        raise RuntimeError('User specified an empty list of S(Q)')

    # get r-range and q-range
    min_r = float(main_window.calculategr_ui.doubleSpinBoxRmin.value())
    max_r = float(main_window.calculategr_ui.doubleSpinBoxRmax.value())
    delta_r = float(main_window.calculategr_ui.doubleSpinBoxDelR.value())

    min_q = float(main_window.calculategr_ui.doubleSpinBoxQmin.value())
    max_q = float(main_window.calculategr_ui.doubleSpinBoxQmax.value())

    use_filter_str = str(
        main_window.calculategr_ui.comboBox_pdfCorrection.currentText())
    if use_filter_str == 'No Modification':
        pdf_filter = None
    elif use_filter_str == 'Lorch':
        pdf_filter = 'lorch'
    else:
        raise RuntimeError(
            'PDF filter {0} is not recognized.'.format(use_filter_str))
    rho0_str = str(main_window.calculategr_ui.lineEdit_rho.text())
    try:
        rho0 = float(rho0_str)
    except ValueError:
        print("WARNING: rho0 is not a float, will not be used in transform")
        rho0 = None

    # PDF type
    pdf_type = str(main_window.calculategr_ui.comboBox_pdfType.currentText())

    # loop for all selected S(Q)
    for sq_ws_name in sq_ws_name_list:
        # calculate G(r)
        gr_ws_name = main_window._myController.calculate_gr(
            sq_ws_name,
            pdf_type,
            min_r,
            delta_r,
            max_r,
            min_q,
            max_q,
            pdf_filter,
            rho0)
        if main_window.calculategr_ui.ff_check.checkState() == 2:
            if rho0 is None:
                print("WARNING: rho0 is not a float. Necessary for applying meaningful Fourier filter.")
                return
            # Fourier filter
            out_ws_temp = AnalysisDataService.retrieve(sq_ws_name)
            out_ws_r_temp = AnalysisDataService.retrieve(gr_ws_name)
            r_in = out_ws_r_temp.readX(0)
            q_in = out_ws_temp.readX(0)
            sq_in = out_ws_temp.readY(0)
            transformer = Transformer()
            import pystog
            print("PYSTOG:", pystog.__file__)
            r_in, gr_in, dg_in = transformer.S_to_G(q_in, sq_in, r_in)
            ff = FourierFilter()
            r_cutoff_ff_text = main_window.calculategr_ui.lineEdit_rcutoff.text()
            try:
                r_cutoff_ff = float(r_cutoff_ff_text)
            except ValueError:
                print("WARNING: rcutoff is not a float. Necessary for applying Fourier filter.")
                return

            q_ft, sq_ft, q_out, sq_out, r_out, gr_out, dsq_ft, dsq, dgr = ff.G_using_S(
                r_in,
                gr_in,
                q_in,
                sq_in,
                r_cutoff_ff,
                rho=rho0)

            new_sq_wks = sq_ws_name + "_ff_rcutoff_" + r_cutoff_ff_text.replace(".", "p")
            simpleapi.CreateWorkspace(
                DataX=q_out,
                DataY=sq_out,
                OutputWorkspace=new_sq_wks,
                NSpec=1,
                unitX="MomentumTransfer")
            main_window.calculategr_ui.treeWidget_grWsList.add_sq(new_sq_wks)
            main_window.calculategr_ui.treeWidget_grWsList._workspaceNameList.append(new_sq_wks)
            plot_sq(main_window, new_sq_wks, color=None, clear_prev=False)
            gr_ws_name = main_window._myController.calculate_gr(
                new_sq_wks,
                pdf_type,
                min_r,
                delta_r,
                max_r,
                min_q,
                max_q,
                pdf_filter,
                rho0)

        # check whether G(r) is in GofR plot to either update or add new plot
        update = main_window.calculategr_ui.graphicsView_gr.has_gr(gr_ws_name)

        # plot G(R)
        if not update:
            # a new line
            colorManager = main_window._pdfColorManager
            gr = colorManager.add_gofr(sq_ws_name, gr_ws_name, max_q)
            gr_color = gr[0]
            gr_style = gr[1]
            gr_marker = gr[2]
            gr_alpha = gr[3]

            gr_label = '{0} Q: ({1}, {2})'.format(sq_ws_name, min_q, max_q)
            plot_gr(
                main_window,
                gr_ws_name,
                gr_color,
                gr_style,
                gr_marker,
                gr_alpha,
                gr_label)
        else:
            plot_gr(main_window, gr_ws_name, line_color=None,
                    line_style=None, line_marker=None,
                    line_alpha=None, line_label=None)

        # add to tree
        # TODO/ISSUE/NOW - Need to find out the name of the
        gr_param_str = 'G(r) for Q(%.3f, %.3f)' % (min_q, max_q)
        main_window.calculategr_ui.treeWidget_grWsList.add_gr(
            gr_param_str, gr_ws_name)


def evt_qmin_changed(main_window):
    q_min = main_window.calculategr_ui.doubleSpinBoxQmin.value()
    q_max = main_window.calculategr_ui.doubleSpinBoxQmax.value()

    graphicsView_sq = main_window.calculategr_ui.graphicsView_sq

    if q_min < q_max and graphicsView_sq.is_boundary_shown():
        graphicsView_sq.move_left_indicator(q_min, relative=False)


def evt_qmax_changed(main_window):
    """
    Handle if the user change the value of Qmax of S(Q) including
    1. moving the right boundary in S(q) figure
    Returns:

    """
    q_min = main_window.calculategr_ui.doubleSpinBoxQmin.value()
    q_max = main_window.calculategr_ui.doubleSpinBoxQmax.value()

    graphicsView_sq = main_window.calculategr_ui.graphicsView_sq
    if q_min < q_max and graphicsView_sq.is_boundary_shown():
        graphicsView_sq.move_right_indicator(q_max, relative=False)


def evt_change_sq_type(main_window):
    """ Event handling to plot S(Q)
    """
    # get the current S(Q) names
    graphicsView_sq = main_window.calculategr_ui.graphicsView_sq
    curr_sq_list = graphicsView_sq.get_shown_sq_names()
    if len(curr_sq_list) == 0:
        return

    # reset the canvas
    graphicsView_sq.reset()

    # re-plot
    for sq_name in curr_sq_list:
        # plot S(Q)
        plot_sq(main_window, sq_name, color=None, clear_prev=False)


def plot_gr(main_window, ws_name, line_color, line_style,
            line_marker, line_alpha, line_label,
            auto=False):
    """Plot G(r) by their names (workspace as protocol)
    """
    # get the value
    vec_r, vec_g, vec_ge = addie.utilities.workspaces.get_ws_data(ws_name)

    # check whether the workspace is on the figure
    graphicsView_gr = main_window.calculategr_ui.graphicsView_gr
    has_gr = graphicsView_gr.has_gr(ws_name)
    current_grs = graphicsView_gr.get_current_grs()
    msg = '[DB...BAT] G(r) graphic has plot {0} is {1}. Keys are {2}'
    msg = msg.format(ws_name, has_gr, current_grs)
    print(msg)

    if graphicsView_gr.has_gr(ws_name):
        # update G(r) value of an existing plot
        graphicsView_gr.update_gr(
            ws_name, ws_name, plotError=False)
    else:
        # a new g(r) plot
        if auto:
            pcm = main_window._pdfColorManager
            line_color, line_style, line_alpha = pcm.get_gr_line(ws_name)

        # plot G(R)
        graphicsView_gr.plot_gr(
            ws_name, ws_name, plotError=False,
            color=line_color, style=line_style, marker=line_marker,
            alpha=line_alpha, label=line_label)


def _rescale(graphicsView):
    """ Rescale the figure of S(Q)
    """
    min_y_value = graphicsView.get_y_min()
    max_y_value = graphicsView.get_y_max()
    delta_y = max(1, max_y_value - min_y_value)

    y_lower_limit = min_y_value - delta_y * 0.05
    y_upper_limit = max_y_value + delta_y * 0.05

    graphicsView.setXYLimit(ymin=y_lower_limit, ymax=y_upper_limit)


def do_rescale_sofq(main_window):
    """ Rescale the figure of S(Q)
    """
    _rescale(main_window.calculategr_ui.graphicsView_sq)


def do_rescale_gofr(main_window):
    """ Rescale the figure of G(r)
    """
    _rescale(main_window.calculategr_ui.graphicsView_gr)


def do_show_sq_bound(main_window):
    """
    Show or hide the left and right boundary of the S(Q)
    """
    q_left = main_window.calculategr_ui.doubleSpinBoxQmin.value()
    q_right = main_window.calculategr_ui.doubleSpinBoxQmax.value()
    main_window.calculategr_ui.graphicsView_sq.toggle_boundary(q_left, q_right)


def do_load_gr(main_window):
    """
    Load an ASCII file containing G(r)
    """
    # get default dir
    if main_window._currDataDir is None:
        default_dir = os.getcwd()
    else:
        default_dir = get_default_dir(main_window, 'gofr')

    # pop out file
    file_filter = 'Data Files (*.dat);; PDFgui (*.gr);;All Files (*.*)'
    g_file_name = QFileDialog.getOpenFileName(
        main_window, 'Open a G(r) file', default_dir, file_filter)
    if isinstance(g_file_name, tuple):
        g_file_name = g_file_name[0]
    # return if operation is cancelled
    if g_file_name is None or g_file_name == '':
        return

    # update current data directory
    main_window._currDataDir = os.path.split(os.path.abspath(g_file_name))[0]
    # set default data directory if in fixed file structure
    check_in_fixed_dir_structure(main_window, 'gofr')

    # read file
    status, ret_obj = main_window._myController.load_gr(g_file_name)
    if not status:
        err_msg = ret_obj
        print('[Error]: %s' % err_msg)
        return
    else:
        gr_ws_name = ret_obj

    # plot_gr
    pcm = main_window._pdfColorManager
    gr_color, gr_style, gr_marker, gr_alpha = pcm.add_gofr(
        None, gr_ws_name, None)
    gr_label = gr_ws_name

    plot_gr(main_window, gr_ws_name,
            line_color=gr_color,
            line_style=gr_style,
            line_marker=gr_marker,
            line_alpha=gr_alpha,
            line_label=gr_label)

    # put the loaded G(r) workspace to tree 'workspaces'
    main_window.calculategr_ui.treeWidget_grWsList.add_child_main_item(
        'workspaces', gr_ws_name)

    check_widgets_status(main_window, enable_gr_widgets=True)


def do_save_gr(main_window):
    """
    Save the selected the G(r) from menu to ASCII file
    """

    # read the selected item from the tree
    gr_list = main_window.calculategr_ui.treeWidget_grWsList
    gr_name_list = gr_list.get_selected_items_of_level(
        2, excluded_parent='SofQ', return_item_text=True)
    if len(gr_name_list) != 1:
        err_msg = 'ERROR: Only 1 workspace of G(r) can be selected.'
        err_msg += '{0} are selected.\n Selection: {1}'
        err_msg = err_msg.format(len(gr_name_list), str(gr_name_list))
        QMessageBox.warning(main_window, 'Error', err_msg)
        return
    else:
        gr_ws_name = gr_name_list[0]

    # pop-up a dialog for the file to save
    default_dir = os.getcwd()
    caption = 'Save G(r)'

    FILE_FILTERS = {'PDFgui (*.gr)': 'gr',
                    'XYE (*.xye)': 'xye',
                    'CSV XYE (*.csv)': 'csv',
                    'RMCProfile (*.dat)': 'dat'}

    filename, filetype = get_save_file(
        parent=main_window,
        directory=default_dir,
        caption=caption,
        filter=FILE_FILTERS)
    if not filename:  # user pressed cancel
        return

    if filetype == 'dat':
        filetype = 'rmcprofile'

    # save!
    main_window._myController.save_ascii(gr_ws_name, filename, filetype)


def do_save_sq(main_window):
    """Save the selected the G(r) from menu to ASCII file
    :return:
    """
    # TEST/ISSUE/NOW - Test!

    # read the selected item from the tree... return if nothing is selected
    gr_list = main_window.calculategr_ui.treeWidget_grWsList
    sq_name_list = gr_list.get_selected_items_of_level(
        2, excluded_parent='GofR', return_item_text=True)
    if len(sq_name_list) == 0:
        # show dialog message here.
        o_dialog = SaveSqDialogMessageDialog(main_window=main_window)
        o_dialog.show()

    FILE_FILTERS = {'XYE (*.xye)': 'xye',
                    'CSV XYE (*.csv)': 'csv',
                    'SofQ (*.sq)': 'sq'}
    # used to support .dat extension, but save_ascii assumes rmcprofile file

    # loop the SofQ name to save
    for sq_name in sq_name_list:
        # get the output file name first

        filename, filetype = get_save_file(
            parent=main_window,
            directory=main_window._currWorkDir,
            caption='Input File Name to Save S(Q) {0}'.format(sq_name),
            filter=FILE_FILTERS)
        if not filename:
            # skip if the user cancel the operation on this S(Q)
            continue

        # save file
        main_window._myController.save_ascii(sq_name, filename, filetype)


def do_edit_sq(main_window):
    """
    Launch a dialog box to edit S(Q) by shift and scaling.
    :return:
    """
    # create dialog instance if it does not exist
    if main_window._editSqDialog is None:
        sq_dialog = addie.calculate_gr.edit_sq_dialog
        main_window._editSqDialog = sq_dialog.EditSofQDialog(main_window)

    # get current S(Q) list and add to dialog
    sq_name_list = list()
    comboBox_SofQ = main_window.calculategr_ui.comboBox_SofQ
    num_sq = comboBox_SofQ.count()
    for isq in range(num_sq):
        sq_name = str(comboBox_SofQ.itemText(isq))
        sq_name_list.append(sq_name)
    # END-FOR

    main_window._editSqDialog.add_sq_by_name(sq_name_list)

    # show
    main_window._editSqDialog.show()


def do_generate_sq(main_window):
    """
    generate S(Q) from G(r) by PDFFourierTransform
    """
    # TODO/ISSUE/NOW - Need to implement!
    raise NotImplementedError(
        'Dialog box for generating S(Q) has not been implemented yet.')
    # get setup
    min_r = float(main_window.calculategr_ui.doubleSpinBoxRmin.value())
    max_r = float(main_window.calculategr_ui.doubleSpinBoxRmax.value())
    min_q = main_window.calculategr_ui.doubleSpinBoxQmin.value()
    max_q = main_window.calculategr_ui.doubleSpinBoxQmax.value()

    # launch the dialog bo
    if main_window._generateSofQDialog is None:
        main_window._generateSofQDialog = None

    main_window._generateSofQDialog.set_r_range(min_r, max_r)
    main_window._generateSofQDialog.set_q_range(min_q, max_q)

    main_window._generateSofQDialog.show()


def _set_color_marker(main_window, graphicsView):
    plot_id_label_list = graphicsView.get_current_plots()

    # get the line ID, color, and marker
    plot_id_list, color, marker = ps.get_plots_color_marker(
        main_window,
        plot_label_list=plot_id_label_list)

    if plot_id_list is None:
        # operation is cancelled by user
        pass
    else:
        # set the color and mark
        for plot_id in plot_id_list:
            graphicsView.updateLine(
                ikey=plot_id,
                linecolor=color,
                marker=marker,
                markercolor=color)


def do_set_gofr_color_marker(main_window):
    """
    set the color/marker to plots on G(r) canvas
    """
    graphicsView_gr = main_window.calculategr_ui.graphicsView_gr
    _set_color_marker(main_window, graphicsView_gr)


def do_set_sq_color_marker(main_window):
    """
    set the color/marker on S(q) canvas
    """
    graphicsView_gr = main_window.calculategr_ui.graphicsView_gr
    _set_color_marker(main_window, graphicsView_gr)


# events from menu
def do_reset_gr_tab(main_window):
    """
    Reset G(r)-tab, including deleting all the G(r) and S(Q) workspaces,
    clearing the G(r) and S(Q) trees, and clearing both G(r) and S(Q) canvas
    """
    # get workspace from trees
    ui = main_window.calculategr_ui
    gr_list = ui.treeWidget_grWsList
    workspace_list = gr_list.get_workspaces()

    # reset the tree to initial status
    gr_list.reset_gr_tree()

    # delete all the workspaces
    for workspace in workspace_list:
        main_window._myController.delete_workspace(workspace)

    # clear all the canvas
    ui.graphicsView_gr.clear_all_lines()
    ui.graphicsView_sq.clear_all_lines()

    # clear the S(Q) combo box
    ui.comboBox_SofQ.clear()
    ui.comboBox_SofQ.addItem('All')


def edit_sq(main_window, sq_name, scale_factor, shift):
    """Edit S(Q) in workspace with scale_factor * Y[i] + shift
    :param sq_name:
    :param scale_factor:
    :param shift:
    """
    # convert
    sq_name = str(sq_name)

    # check inputs
    msg = 'S(Q) workspace name {0} must be a string but not a {1}.'
    msg = msg.format(sq_name, type(sq_name))
    assert isinstance(sq_name, str), msg

    msg = 'Scale factor {0} must be a float but not a {1}.'
    msg = msg.format(scale_factor, type(scale_factor))
    assert isinstance(scale_factor, float),  msg

    msg = 'Shift {0} must be a float but not a {1}.'
    assert isinstance(shift, float), msg.format(shift, type(shift))

    # call the controller
    edit_sq_name = sq_name + '_Edit'
    main_window._myController.edit_matrix_workspace(
        sq_name, scale_factor, shift, edit_sq_name)
    # add new S(Q)
    main_window._pdfColorManager.add_sofq(edit_sq_name)

    color, marker = main_window.calculategr_ui.graphicsView_sq.get_plot_info(
        sq_name)
    print('[DB...BAT] Original SofQ {0} has color {0} marker {1}'.format(
        color, marker))

    # re-plot
    main_window.calculategr_ui.graphicsView_sq.plot_sq(
        edit_sq_name,
        sq_y_label=sq_name + ' In Edit',
        reset_color_mark=False,
        color=color, marker=marker)

    # calculate G(r) too
    generate_gr_step2(main_window, [edit_sq_name])


def clear_bank_checkboxes(main_window):
    main_window._noEventBankWidgets = True
    for check_box in list(main_window._braggBankWidgets.values()):
        check_box.setChecked(False)
    main_window._noEventBankWidgets = False


def remove_gr_from_plot(main_window, gr_name):
    """Remove a GofR line from GofR canvas
    :param gr_name: supposed to the G(r) name that is same as workspace
                    name and plot key on canvas as well
    """
    # check
    msg = 'G(r) plot key {0} must be a string but not a {1}'
    msg = msg.format(gr_name, type(gr_name))
    assert isinstance(gr_name, str), msg

    # remove
    main_window.calculategr_ui.graphicsView_gr.remove_gr(plot_key=gr_name)


def remove_sq_from_plot(main_window, sq_name):
    """
    Remove an SofQ line from SofQ canvas
    :param gr_name: supposed to the S(Q) name that is same as workspace
                    name and plot key on canvas as well
    """
    # check
    assert isinstance(sq_name, str)

    # remove
    graphicsView_sq = main_window.calculategr_ui.graphicsView_sq
    if graphicsView_sq.is_on_canvas(sq_name):
        graphicsView_sq.remove_sq(sq_ws_name=sq_name)


def update_sq_boundary(main_window, boundary_index, new_position):
    """Update the S(Q) range at the main app inputs
    :param boundary_index:
    :param new_position:
    :return:
    """
    # check
    msg = 'Boundary index {0} must be an integer but not {1}.'
    msg = msg.format(boundary_index, type(boundary_index))
    assert isinstance(boundary_index, int), msg

    msg = 'New position {0} must be a float but not {1}.'
    assert isinstance(new_position, float),  msg.format(
        new_position, type(new_position))

    # set value
    if boundary_index == 1:
        # left boundary
        main_window.calculation_gr_ui.doubleSpinBoxQmin.setValue(new_position)
    elif boundary_index == 2:
        # right boundary
        main_window.calculation_gr_ui.doubleSpinBoxQmax.setValue(new_position)
    else:
        # exception
        msg = 'Boundary index {} in method update_sq_boundary() not supported.'
        raise RuntimeError(msg.format(new_position))


def add_edited_sofq(main_window, sofq_name, edited_sq_name, shift, scale):
    """add an edited S(Q) to cached dictionary
    :param sofq_name:
    :param edited_sq_name:
    :param shift:
    :param scale:
    """
    # check
    msg = 'SofQ workspace name {0} must be a string but not a {1}.'
    msg = msg.format(sofq_name, type(sofq_name))
    assert isinstance(sofq_name, str),  msg

    msg = 'Edited S(Q) workspace name {0} must be a string but not a {1}.'
    msg = msg.format(edited_sq_name, type(edited_sq_name))
    assert isinstance(edited_sq_name, str),  msg

    # add the entry for the original S(Q) if not done yet
    if sofq_name not in main_window._editedSofQDict:
        main_window._editedSofQDict[sofq_name] = dict()

    # add entry
    main_window._editedSofQDict[sofq_name][shift, scale] = edited_sq_name

    # add the line and color manager
    main_window._pdfColorManager.add_sofq(edited_sq_name)


def has_edit_sofq(main_window, raw_sofq_name, shift, scale):
    """ check whether an edited S(Q) has been cached already
    :param raw_sofq_name:
    :param shift:
    :param scale:
    :return:
    """
    # check
    assert isinstance(raw_sofq_name, str)

    if raw_sofq_name not in main_window._editedSofQDict:
        return False

    return (shift, scale) in main_window._editedSofQDict[raw_sofq_name]
