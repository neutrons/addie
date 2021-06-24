import os
from qtpy.QtWidgets import QFileDialog
from mantid.api import AnalysisDataService
import mantid.simpleapi as simpleapi

import addie.utilities.workspaces


def open_bragg_files(main_window):
    """
    Get the Bragg files including GSAS, NeXus, 3-column ASCii from File Dialog
    :retur: List of Bragg Files to load
    """
    # get file
    ext = 'GSAS (*.gsa *.gda *.gss);;Processed Nexus (*.nxs);;dat (*.dat);;All (*.*)'

    # get default dir
    if main_window._currDataDir is None:
        default_dir = os.getcwd()
    else:
        default_dir = addie.utilities.get_default_dir(
            main_window, sub_dir='GSAS')

    bragg_file_names = QFileDialog.getOpenFileNames(
        main_window, 'Choose Bragg File', default_dir, ext)
    if isinstance(bragg_file_names, tuple):
        bragg_file_names = bragg_file_names[0]
    if bragg_file_names is None or bragg_file_names == '' or len(
            bragg_file_names) == 0:
        return
    bragg_file_names = [str(bragg_file_name)
                        for bragg_file_name in bragg_file_names]

    # update stored data directory
    try:
        main_window._currDataDir = os.path.split(
            os.path.abspath(bragg_file_names[0]))[0]
    except IndexError as index_err:
        err_message = 'Unable to get absolute path of {0} due to {1}'.format(
            bragg_file_names, index_err)
        print(err_message)

    addie.utilities.check_in_fixed_dir_structure(main_window, sub_dir='GSAS')
    return bragg_file_names


def load_bragg_by_filename(file_name):
    """
    Load Bragg diffraction file (including 3-column data file, GSAS file) for Rietveld
    """
    # load with different file type
    base_file_name = os.path.basename(file_name).lower()
    gss_ws_name = os.path.basename(file_name).split('.')[0]
    if base_file_name.endswith('.gss') or base_file_name.endswith(
            '.gsa') or base_file_name.endswith('.gda'):
        simpleapi.LoadGSS(Filename=file_name,
                          OutputWorkspace=gss_ws_name)
    elif base_file_name.endswith('.nxs'):
        simpleapi.LoadNexusProcessed(
            Filename=file_name, OutputWorkspace=gss_ws_name)
        simpleapi.ConvertUnits(
            InputWorkspace=gss_ws_name,
            OutputWorkspace=gss_ws_name,
            EMode='Elastic',
            Target='TOF')
    elif base_file_name.endswith('.dat'):
        simpleapi.LoadAscii(Filename=file_name,
                            OutputWorkspace=gss_ws_name,
                            Unit='TOF')
    else:
        raise RuntimeError(
            'File %s is not of a supported type.' %
            file_name)

    # check
    assert AnalysisDataService.doesExist(gss_ws_name)
    angle_list = addie.utilities.workspaces.calculate_bank_angle(gss_ws_name)

    return gss_ws_name, angle_list


def load_bragg_files(main_window, bragg_file_names):
    """
    Load Bragg files including GSAS, NeXus, 3-column ASCii.
    """
    if not bragg_file_names:
        return list()

    # load file
    try:
        gss_ws_names = list()
        for bragg_file_name in bragg_file_names:
            gss_ws_name, bank_angles = load_bragg_by_filename(bragg_file_name)
            gss_ws_names.append(gss_ws_name)
            banks_list = list()
            for i, angle in enumerate(bank_angles):
                banks_list.append('Bank {} - {}'.format(i + 1, angle))

            # add to tree
            main_window.rietveld_ui.treeWidget_braggWSList.add_bragg_ws_group(
                gss_ws_name, banks_list)

        # get plot mode
        if len(bragg_file_names) == 1:
            main_window.rietveld_ui.graphicsView_bragg.set_to_single_gss(True)
            main_window.rietveld_ui.radioButton_multiBank.setChecked(True)
            main_window.rietveld_ui.radioButton_multiGSS.setChecked(False)
        else:
            main_window.rietveld_ui.graphicsView_bragg.set_to_single_gss(False)
            main_window.rietveld_ui.radioButton_multiBank.setChecked(False)
            main_window.rietveld_ui.radioButton_multiGSS.setChecked(True)

        multi_bank_mode = main_window.rietveld_ui.radioButton_multiBank.isChecked()

        if multi_bank_mode:
            # single-GSS/multi-bank mode
            # rename bank
            for bank_id in main_window._braggBankWidgets:
                bank_check_box = main_window._braggBankWidgets[bank_id]

                if bank_id > len(
                        bank_angles) or bank_angles[bank_id - 1] is None:
                    bank_check_box.setText('Bank %d' % bank_id)
                else:
                    bank_check_box.setText('Bank %.1f' %
                                           bank_angles[bank_id - 1])

            # clear all previous lines
            main_window.rietveld_ui.graphicsView_bragg.reset()

        # banks
        main_window._onCanvasGSSBankList = get_bragg_banks_selected(
            main_window)
        if len(main_window._onCanvasGSSBankList) == 0:
            # select bank 1 as default
            main_window._noEventBankWidgets = True
            main_window.rietveld_ui.checkBox_bank1.setChecked(True)
            main_window._noEventBankWidgets = False
            main_window._onCanvasGSSBankList = get_bragg_banks_selected(
                main_window)

        # while in multiple-gss mode, no change will be made on the canvas at
        # all

        # prepare to plot new Bragg
        plot_data_dict = dict()
        for gss_ws_name in gss_ws_names:
            plot_data_dict[gss_ws_name] = main_window._onCanvasGSSBankList[:]

        # plot
        # FIXME/ISSUE/NOW - get a summary on calling to plot_banks
        main_window.rietveld_ui.graphicsView_bragg.plot_banks(
            plot_data_dict, main_window._currBraggXUnit)

        # reset unit
        reset_bragg_data_range(main_window, main_window._currBraggXUnit)

    except RuntimeError as e:
        print('Encountered exception')
        print(e)

    except ValueError:
        main_window.setStyleSheet(
            "QStatusBar{padding-left:8px;color:red;font-weight:bold;}")
        main_window.ui.statusbar.showMessage(
            "Error loading {}".format(bragg_file_names),
            main_window.statusbar_display_time)

    check_rietveld_widgets(main_window)


def open_and_load_bragg_files(main_window):
    """
    Load Bragg files including GSAS, NeXus, 3-column ASCii.
    """
    bragg_file_names = open_bragg_files(main_window)
    load_bragg_files(main_window, bragg_file_names)


def check_rietveld_widgets(main_window):
    """enable or not the widgets according to status of plots"""

    if not main_window._onCanvasGSSBankList:
        enable_widgets = False
    else:
        enable_widgets = True
    ui = main_window.rietveld_ui
    ui.checkBox_bank1.setEnabled(enable_widgets)
    ui.checkBox_bank2.setEnabled(enable_widgets)
    ui.checkBox_bank3.setEnabled(enable_widgets)
    ui.checkBox_bank4.setEnabled(enable_widgets)
    ui.checkBox_bank5.setEnabled(enable_widgets)
    ui.checkBox_bank6.setEnabled(enable_widgets)
    ui.radioButton_multiBank.setEnabled(enable_widgets)
    ui.radioButton_multiGSS.setEnabled(enable_widgets)
    ui.pushButton_rescaleGSAS.setEnabled(enable_widgets)
    ui.pushButton_gsasColorStyle.setEnabled(enable_widgets)
    ui.pushButton_clearBraggCanvas.setEnabled(enable_widgets)
    ui.comboBox_xUnit.setEnabled(enable_widgets)


def plot_bragg_bank(main_window):
    """
    Find out which bank will be plot

    cases to trigger this event:
    1. select more banks
    2. deselect some banks

    Returns
    -------

    """
    # check mutex for not responding the event
    if main_window._noEventBankWidgets:
        return
    # check
    # assert main_window._gssGroupName is not None, 'GSAS group name cannot be None'

    # get mode for plotting
    plot_multi_gss = main_window.rietveld_ui.radioButton_multiGSS.isChecked()

    # find the change of the banks
    current_bank_set = set(get_bragg_banks_selected(main_window))
    prev_bank_set = set(main_window._onCanvasGSSBankList)

    if plot_multi_gss:
        # multi-gss/single-bank mode
        # get the banks to remove
        rm_bank_list = main_window._onCanvasGSSBankList[:]

        # deselect all the old banks and thus turn on the mutex
        main_window._noEventBankWidgets = True
        # turn off the
        set_bragg_banks_selected(
            main_window, main_window._onCanvasGSSBankList, False)
        # turn off mutex
        main_window._noEventBankWidgets = False

        # set banks to add
        new_bank_list = list(current_bank_set - prev_bank_set)
        assert len(
            new_bank_list) <= 1, 'Impossible to have more than 1 banks selected in multi-GSS mode.'

        # set the current on canvas
        main_window._onCanvasGSSBankList = new_bank_list

    else:
        # single-gss/multi-bank mode
        # determine the banks to add
        new_bank_list = list(current_bank_set - prev_bank_set)
        rm_bank_list = list(prev_bank_set - current_bank_set)

        # set the current on-canvas
        main_window._onCanvasGSSBankList = list(current_bank_set)

    # END-IF-ELSE

    # get GSS data (group)
    if plot_multi_gss:
        # multiple GSAS file/single bank mode: get GSAS group from tree
        gss_group_list = main_window.rietveld_ui.treeWidget_braggWSList.get_main_nodes()
        gss_group_list.remove('workspaces')
    else:
        # single GSAS file mode
        status, ret_obj = main_window.rietveld_ui.treeWidget_braggWSList.get_current_main_nodes()
        # ZYP -> Sometimes, it can happen that the returned `status` here is
        # `True`, but we have empty `ret_obj`. So we need to tackle such a
        # situation. Since this will happen when multiple GSS files exist in wks,
        # and therefore when this happens, we just simply roll into the multiple GSS mode.
        if status:
            if len(ret_obj) > 0:
                gss_group = ret_obj[0]
            else:
                gss_group_list = main_window.rietveld_ui.treeWidget_braggWSList.get_main_nodes()
                gss_group_list.remove('workspaces')
        else:
            raise RuntimeError(
                'Unable to get current selected main node(s) due to {0}.'.format(ret_obj))
        if len(ret_obj) > 0:
            gss_group_list = [gss_group]

    # remove banks from plot
    for gss_group_name in gss_group_list:
        main_window.rietveld_ui.graphicsView_bragg.remove_gss_banks(
            gss_group_name, rm_bank_list)

    # get new bank data
    plot_data_dict = dict()
    for ws_group in gss_group_list:
        plot_data_dict[ws_group] = new_bank_list[:]

    # ZYP -> Check whether selected bank (to plot) exists or not.
    # ZYP -> If not, no action will be taken and msg will be printed out to terminal.
    banks_checker_ok = True
    leaf_dict_temp = main_window.rietveld_ui.treeWidget_braggWSList._leafDict
    for ws_group in gss_group_list:
        for bank_to_check in plot_data_dict[ws_group]:
            if int(bank_to_check) > len(leaf_dict_temp[ws_group]):
                print("Bank-{0} not existing in {1} and therefore not to be plotted.".format(bank_to_check, ws_group))
                banks_checker_ok = False
                break

    if plot_multi_gss:
        main_window.rietveld_ui.graphicsView_bragg.set_to_single_gss(False)
    else:
        main_window.rietveld_ui.graphicsView_bragg.set_to_single_gss(True)
        status, ws_name_list = main_window.rietveld_ui.treeWidget_braggWSList.get_current_main_nodes()
        # ZYP -> Sometimes, it can happen that the returned `status` here is
        # `True`, but we have empty `ret_obj`. So we need to tackle such a
        # situation. Since this will happen when multiple GSS files exist in wks,
        # and therefore when this happens, we just simply roll into the multiple GSS mode.
        if len(ws_name_list) == 0:
            ws_name_list = main_window.rietveld_ui.treeWidget_braggWSList.get_main_nodes()
            ws_name_list.remove("workspaces")
        plot_data_dict = {ws_name_list[0]: plot_data_dict[ws_name_list[0]]}

    # plot new
    # ZYP -> Check whether selected bank (to plot) exists or not.
    if banks_checker_ok:
        main_window.rietveld_ui.graphicsView_bragg.plot_banks(
            plot_data_dict, main_window._currBraggXUnit)

        # reset
        reset_bragg_data_range(main_window, main_window._currBraggXUnit)

        # rescale
        do_rescale_bragg(main_window)


def do_rescale_bragg(main_window):
    """ Rescale the figure of Bragg diffraction data
    """
    min_y_value = main_window.rietveld_ui.graphicsView_bragg.get_y_min()
    max_y_value = main_window.rietveld_ui.graphicsView_bragg.get_y_max()
    delta_y = max(1, max_y_value - min_y_value)

    y_lower_limit = min_y_value - delta_y * 0.05
    y_upper_limit = max_y_value + delta_y * 0.05

    main_window.rietveld_ui.graphicsView_bragg.setXYLimit(
        ymin=y_lower_limit, ymax=y_upper_limit)


def switch_bragg_unit(main_window=None):
    """
    Unit of Bragg plot is changed.
    Requirements:
    1. clear the canvas
    2. plot all the banks in the new units
    3. reset the limit
    """
    # get current unit and check whether re-plot all banks is not a choice
    x_unit = str(main_window.rietveld_ui.comboBox_xUnit.currentText())
    # convert Q to MomentumTransfer by Mantid standard
    if x_unit == 'Q':
        x_unit = 'MomentumTransfer'

    if x_unit == main_window._currBraggXUnit:
        # return if no change. then this cannot happen
        raise RuntimeError('New unit %s is same as original unit %s.' % (
            x_unit, main_window._currBraggXUnit))
    else:
        main_window._currBraggXUnit = x_unit

    # reset canvas
    main_window.rietveld_ui.graphicsView_bragg.reset()

    # get bank to plot
    bank_list = get_bragg_banks_selected(main_window)

    # get data sets
    ws_group_list = main_window.rietveld_ui.treeWidget_braggWSList.get_selected_items_of_level(
        target_item_level=1, excluded_parent=None, return_item_text=True)
    if 'workspaces' in ws_group_list:
        ws_group_list.remove('workspaces')
    if len(ws_group_list) == 0:
        print("[Warning] At least 1 GSS file must be selected.")
        return

    # check
    assert len(bank_list) == 1 or len(ws_group_list) == 1, 'Must be either single bank (%d now) or ' \
        'single GSS (%d now).' % (len(bank_list),
                                  len(ws_group_list))

    # get data and plot
    plot_data_dict = dict()
    for ws_group in ws_group_list:
        plot_data_dict[ws_group] = main_window._myController.get_bank_numbers(
            ws_group)

    # plot
    main_window.rietveld_ui.graphicsView_bragg.plot_banks(
        plot_data_dict, main_window._currBraggXUnit)

    # reset unit
    reset_bragg_data_range(main_window, x_unit)


def get_bragg_banks_selected(main_window=None):
    """
    Find out the banks of bragg-tab that are selected.
    """
    bank_id_list = list()
    for bank_id in main_window._braggBankWidgets:
        bank_checkbox = main_window._braggBankWidgets[bank_id]
        if bank_checkbox.isChecked():
            bank_id_list.append(bank_id)

    return bank_id_list


def reset_bragg_data_range(main_window, x_unit):
    main_window.rietveld_ui.graphicsView_bragg.set_unit(x_unit)

    if x_unit == 'TOF':
        main_window.rietveld_ui.graphicsView_bragg.setXYLimit(xmin=0,
                                                              xmax=20000,
                                                              ymin=None,
                                                              ymax=None)
    elif x_unit == 'MomentumTransfer':
        main_window.rietveld_ui.graphicsView_bragg.setXYLimit(xmin=0,
                                                              xmax=20,
                                                              ymin=None,
                                                              ymax=None)
    elif x_unit == 'dSpacing':
        main_window.rietveld_ui.graphicsView_bragg.setXYLimit(xmin=0,
                                                              xmax=7,
                                                              ymin=None,
                                                              ymax=None)
    else:
        raise RuntimeError('Unit %s unknown' % x_unit)


def do_clear_bragg_canvas(main_window):
    """
    Clear all the plots on Bragg-canvas
    """
    main_window.rietveld_ui.graphicsView_bragg.reset()
    clear_bank_checkboxes(main_window)
    main_window._onCanvasGSSBankList = list()


def clear_bank_checkboxes(main_window):
    main_window._noEventBankWidgets = True
    for check_box in list(main_window._braggBankWidgets.values()):
        check_box.setChecked(False)
    main_window._noEventBankWidgets = False


def evt_change_gss_mode(main_window):
    """ switch between multi-gss/single-bank mode and singl-gss/multiple-bank mode
    :return:
    """
    if main_window is None:
        raise NotImplementedError('Main window has not been set up!')

    # check the mode (multiple bank or multiple GSS)
    single_gss_mode = main_window.rietveld_ui.radioButton_multiBank.isChecked()
    assert single_gss_mode != main_window.rietveld_ui.radioButton_multiGSS.isChecked(
    ), 'Multi bank and multi GSS cannot be checked simultaneously.'

    # get the banks that are selected
    to_plot_bank_list = get_bragg_banks_selected(main_window)
    on_canvas_ws_list = main_window.rietveld_ui.graphicsView_bragg.get_workspaces()
    # return with doing anything if the canvas is empty, i.e., no bank is
    # selected
    if len(to_plot_bank_list) == 0:
        return
    # return if there is no workspace that is plotted on canvas now
    if len(on_canvas_ws_list) == 0:
        return

    # set to single GSS
    main_window.rietveld_ui.graphicsView_bragg.set_to_single_gss(
        single_gss_mode)

    # process the plot with various situation
    if single_gss_mode:
        # switch to single GSAS mode from multiple GSAS mode.
        #  select the arbitrary gsas file to
        msg = 'From multi-GSS-single-Bank mode, only 1 bank can be selected.'
        assert len(to_plot_bank_list) == 1, msg

        # skip if there is one and only one workspace
        if len(on_canvas_ws_list) == 1:
            return
        else:
            status, ws_name_list = main_window.rietveld_ui.treeWidget_braggWSList.get_current_main_nodes()
            if not status:
                raise RuntimeError(str(ws_name_list))

        # plot
        plot_bragg(
            main_window,
            ws_list=[
                ws_name_list[0]],
            bankIds=to_plot_bank_list,
            clear_canvas=True)

    else:
        # multiple GSAS mode. as currently there is one GSAS file that is plot, then the first bank
        # that is plotted will be kept on the canvas
        # assumption: switched from single-bank mode

        # skip if there is one and only 1 bank that is selected
        # if len(to_plot_bank_list) == 1:
        # TEST/ISSUE/NOW - Need to re-plot with correct color!
        #     return
        # else:
        # choose first bank
        bank_on_canvas = to_plot_bank_list[0]
        wkspaces = main_window.rietveld_ui.treeWidget_braggWSList.get_main_nodes()
        wkspaces.remove('workspaces')  # can't plot that

        # disable all the banks except the one to plot. Notice the mutex must
        # be on
        main_window._noEventBankWidgets = True
        for bank_id in main_window._braggBankWidgets:
            if bank_id != bank_on_canvas:
                main_window._braggBankWidgets[bank_id].setChecked(False)
        main_window._noEventBankWidgets = False

        # plot
        plot_bragg(
            main_window,
            ws_list=wkspaces,
            bankIds=[bank_on_canvas],
            clear_canvas=True)

        # set
        main_window._onCanvasGSSBankList = [bank_on_canvas]


def plot_bragg(main_window, ws_list, bankIds, clear_canvas=False):
    """
    Parameters
    ----------
    ws_list: list of (single spectrum) Bragg workspace
    bankIds: list of bank ids to plot
    clear_canvas
    """
    # check
    assert isinstance(ws_list, list)

    # clear canvas if necessary
    if clear_canvas:
        main_window.rietveld_ui.graphicsView_bragg.reset()

    # get unit
    curr_unit = main_window._currBraggXUnit

    # set the bank to be checked
    for bank in bankIds:
        main_window._braggBankWidgets[bank].setChecked(True)

    # plot all workspsaces
    plot_data_dict = dict()
    leaf_dict_temp = main_window.rietveld_ui.treeWidget_braggWSList._leafDict
    for bragg_ws_name in ws_list:
        # construct dictionary for plotting
        # main_window._myController.get_bank_numbers(ws_group)
        to_plot = []
        for bank_temp in bankIds:
            if int(bank_temp) <= len(leaf_dict_temp[bragg_ws_name]):
                to_plot.append(bank_temp)
            else:
                print("Bank-{0} not existing in {1} and therefore not to be plotted.".format(bank_temp, bragg_ws_name))
        # plot_data_dict[bragg_ws_name] = bankIds
        plot_data_dict[bragg_ws_name] = to_plot

    # plot
    main_window.rietveld_ui.graphicsView_bragg.plot_banks(
        plot_data_dict, curr_unit)


def do_set_bragg_color_marker(main_window):
    """
    set the color/marker to plots on bragg canvas
    :return:
    """
    # get the current figure' on-shown plots
    plot_id_label_list = main_window.rietveld_ui.graphicsView_bragg.get_current_plots()

    # get the line ID, color, and marker
    ps = addie.utilities.specify_plots_style
    plot_id_list, color, marker = ps.get_plots_color_marker(
        main_window, plot_label_list=plot_id_label_list)
    #print('"{}" "{}" "{}"'.format(plot_id_list, color, marker))
    if plot_id_list is None:
        # operation is cancelled by user
        pass
    else:
        # set the color and mark
        for plot_id in plot_id_list:
            main_window.rietveld_ui.graphicsView_bragg.updateLine(
                ikey=plot_id, linecolor=color, marker=marker, markercolor=color)


def set_bragg_ws_to_plot(main_window, gss_group_name):
    """
    Set a Bragg workspace group to plot.  If the Bragg-tab is in
    (1) single-GSS mode, then switch to plot this gss_group
    (2) multiple-GSS mode, then add this group to current canvas
    Parameters
    ----------
    gss_group_name
    """
    # check
    assert isinstance(gss_group_name, str), 'GSS workspace group name is expected to be a string, but not' \
        ' %s.' % str(type(gss_group_name))

    # get the banks to plot - change to workspace index
    selected_banks = get_bragg_banks_selected(main_window)

    # process
    if main_window.rietveld_ui.radioButton_multiBank.isChecked(
    ):  # single-GSS/multi-bank mode
        # reset canvas
        main_window.rietveld_ui.graphicsView_bragg.reset()
    else:  # multiple-GSS/single-bank mode
        # canvas is not reset
        assert len(
            selected_banks) <= 1, 'At most 1 bank can be plot in multiple-GSS mode.'

    plot_bragg(main_window, ws_list=[gss_group_name],
               bankIds=selected_banks, clear_canvas=False)


def set_bragg_banks_selected(main_window, bank_id_list, status):
    """
    set the status of selected bank IDs
    Note: mutex on Bragg Bank selection widgets is not turned on!!!
    Parameters
    ----------
    bank_id_list
    status

    Returns
    -------

    """
    # check inputs
    assert isinstance(bank_id_list, list), 'Bank IDs {0} must be given in a list but not a {1}.' \
                                           ''.format(bank_id_list,
                                                     type(bank_id_list))
    assert isinstance(status, bool), 'Selection status {0} must be a boolean but not a {1}.' \
                                     ''.format(status, type(status))

    # set
    for bank_id in bank_id_list:
        main_window._braggBankWidgets[bank_id].setChecked(status)
