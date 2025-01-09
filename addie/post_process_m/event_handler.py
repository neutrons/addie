import os
import json
import subprocess
from qtpy.QtWidgets import QFileDialog, QMessageBox, QApplication
from h5py import File
import addie.utilities.workspaces
from pystog.stog import StoG
from mantid.simpleapi import \
    CreateWorkspace, \
    Fit, \
    mtd, \
    DeleteWorkspace
import numpy as np
from scipy.signal import argrelextrema
from datetime import datetime

weekdays = [
    'Mon',
    'Tue',
    'Wed',
    'Thu',
    'Fri',
    'Sat',
    'Sun'
]
pystog_cli = "/SNS/users/y8z/miniconda/envs/pystog/bin/pystog_cli"


def open_workspaces(main_window):
    ext = 'Processed Nexus (*.nxs);;All (*.*)'

    if main_window._currDataDir is None:
        default_dir = os.getcwd()
    else:
        default_dir = addie.utilities.get_default_dir(
            main_window, sub_dir='GSAS')

    workspace_file_names = QFileDialog.getOpenFileNames(
        main_window, 'Choose Reduced Nexus File', default_dir, ext)
    if isinstance(workspace_file_names, tuple):
        workspace_file_names = workspace_file_names[0]
    if workspace_file_names is None or workspace_file_names == '' or len(
            workspace_file_names) == 0:
        return
    workspace_file_names = [str(workspace_file_name)
                            for workspace_file_name in workspace_file_names]

    # update stored data directory
    try:
        main_window._currDataDir = os.path.split(
            os.path.abspath(workspace_file_names[0]))[0]
    except IndexError as index_err:
        err_message = 'Unable to get absolute path of {0} due to {1}'.format(
            workspace_file_names, index_err)
        print(err_message)

    addie.utilities.check_in_fixed_dir_structure(main_window, sub_dir='GSAS')
    return workspace_file_names[0]


def open_config_file(main_window):
    ext = 'JSON (*.json)'

    if main_window._currDataDir is None:
        default_dir = os.getcwd()
    else:
        default_dir = addie.utilities.get_default_dir(
            main_window, sub_dir='GSAS')

    mconfig_file_name = QFileDialog.getSaveFileName(
        main_window, 'Choose Config File to Save As', default_dir, ext)
    if isinstance(mconfig_file_name, tuple):
        mconfig_file_name = str(mconfig_file_name[0])
    if mconfig_file_name is None or mconfig_file_name == '' or len(
            mconfig_file_name) == 0:
        return

    # update stored data directory
    try:
        main_window._currDataDir = os.path.split(
            os.path.abspath(mconfig_file_name))[0]
    except IndexError as index_err:
        err_message = 'Unable to get absolute path of {0} due to {1}'.format(
            mconfig_file_name, index_err)
        print(err_message)

    addie.utilities.check_in_fixed_dir_structure(main_window, sub_dir='GSAS')
    return mconfig_file_name


def open_config_file_r(main_window):
    ext = 'JSON (*.json)'

    if main_window._currDataDir is None:
        default_dir = os.getcwd()
    else:
        default_dir = addie.utilities.get_default_dir(
            main_window, sub_dir='GSAS')

    mconfig_file_name = QFileDialog.getOpenFileName(
        main_window, 'Choose Config File to Load', default_dir, ext)
    if isinstance(mconfig_file_name, tuple):
        mconfig_file_name = str(mconfig_file_name[0])
    if mconfig_file_name is None or mconfig_file_name == '' or len(
            mconfig_file_name) == 0:
        return

    # update stored data directory
    try:
        main_window._currDataDir = os.path.split(
            os.path.abspath(mconfig_file_name))[0]
    except IndexError as index_err:
        err_message = 'Unable to get absolute path of {0} due to {1}'.format(
            mconfig_file_name, index_err)
        print(err_message)

    addie.utilities.check_in_fixed_dir_structure(main_window, sub_dir='GSAS')
    return mconfig_file_name


def load_workspaces(main_window, workspace_files):

    # extract the workspaces and banks
    workspaces, banks = extract_from_input_file(workspace_files, main_window)

    # display number of banks
    main_window.postprocessing_ui_m.label_numBanks.setText(str(banks))

    # clear the combobox before adding
    main_window.postprocessing_ui_m.comboBox_banks.clear()

    workspace_table = main_window.postprocessing_ui_m.frame_workspaces_table

    # load the combobox with banks
    for bank in range(1, banks + 1):
        main_window.postprocessing_ui_m.comboBox_banks.addItem(str(bank))

    workspace_table.load(workspaces, main_window)


def extract_from_input_file(input_file, main_window):
    main_window._inputFile = input_file
    wks_list = list()
    data = File(input_file, "r")
    for name, group in data.items():
        index = os.path.join(name, "title").replace("\\", "/")
        wks_list.append(str(data[index][()][0]).split("'")[1].split("'")[0])

    title = wks_list[0]

    for name, group in data.items():
        index = os.path.join(name, "title").replace("\\", "/")
        if data[index][(0)].decode("UTF-8") == title:
            ypath = os.path.join("/", name,
                                 "workspace", "values").replace("\\", "/")
            break

    return wks_list, len(data[ypath][()])


def save_mconfig(main_window):
    mcofnig_file_name = open_config_file(main_window)
    if mcofnig_file_name is None:
        return

    dict_tmp = dict()
    if mcofnig_file_name[-5:] == ".json":
        file_out = open(mcofnig_file_name, "w")
    else:
        file_out = open(mcofnig_file_name + ".json", "w")
    for key in main_window._bankDict.keys():
        dict_tmp[key] = { "Qmin": main_window._bankDict[key]['Qmin'],
                          "Qmax": main_window._bankDict[key]['Qmax'],
                          "Yoffset": main_window._bankDict[key]['Yoffset'],
                          "Yscale": main_window._bankDict[key]['Yscale'] }
    remove_bkg = main_window.postprocessing_ui_m.checkBox_bkg_removal.isChecked()
    dict_tmp["RemoveBkg"] = remove_bkg
    json.dump(dict_tmp, file_out, indent=2)
    file_out.close()

    main_window.ui.statusbar.setStyleSheet("color: blue")
    main_window.ui.statusbar.showMessage("Config file successfully saved!",
                                         main_window.statusbar_display_time)


def load_mconfig(main_window):
    mcofnig_file_name = open_config_file_r(main_window)
    if mcofnig_file_name is None:
        return

    if mcofnig_file_name[-5:] == ".json":
        with open(mcofnig_file_name, "r") as mconfig_json:
            try:
                mconfig_in = json.load(mconfig_json)
            except json.decoder.JSONDecodeError as err:
                print("[Error] Could not load in JSON file", mcofnig_file_name)
                print("[Error]", err)
                return
    else:
        print("[Error] Not a JSON file selected. Try again.")
        return

    for key in main_window._bankDict.keys():
        if str(key) in mconfig_in.keys():
            if 'Qmin' in mconfig_in[str(key)].keys():
                qmin_tmp = mconfig_in[str(key)]['Qmin']
                main_window._bankDict[key]['Qmin'] = qmin_tmp
                if key == 1 and main_window.postprocessing_ui_m.comboBox_banks.currentText() == "1":
                    main_window.postprocessing_ui_m.doubleSpinBox_Qmin.setValue(float(qmin_tmp))
            if 'Qmax' in mconfig_in[str(key)].keys():
                qmax_tmp = mconfig_in[str(key)]['Qmax']
                main_window._bankDict[key]['Qmax'] = qmax_tmp
                if key == 1 and main_window.postprocessing_ui_m.comboBox_banks.currentText() == "1":
                    main_window.postprocessing_ui_m.doubleSpinBox_Qmax.setValue(float(qmax_tmp))
            if 'Yoffset' in mconfig_in[str(key)].keys():
                yoffset_tmp = mconfig_in[str(key)]['Yoffset']
                main_window._bankDict[key]['Yoffset'] = yoffset_tmp
                if key == 1 and main_window.postprocessing_ui_m.comboBox_banks.currentText() == "1":
                    main_window.postprocessing_ui_m.lineEdit_Yoffset.setText(yoffset_tmp)
            if 'Yscale' in mconfig_in[str(key)].keys():
                yscale_tmp = mconfig_in[str(key)]['Yscale']
                main_window._bankDict[key]['Yscale'] = yscale_tmp
                if key == 1 and main_window.postprocessing_ui_m.comboBox_banks.currentText() == "1":
                    main_window.postprocessing_ui_m.lineEdit_Yscale.setText(yscale_tmp)
    if 'RemoveBkg' in mconfig_in.keys():
        main_window.postprocessing_ui_m.checkBox_bkg_removal.setChecked(mconfig_in["RemoveBkg"])

    main_window.ui.statusbar.setStyleSheet("color: blue")
    main_window.ui.statusbar.showMessage("Config file successfully loaded!",
                                         main_window.statusbar_display_time)


def open_and_load_workspaces(main_window):
    workspace_files = open_workspaces(main_window)

    if workspace_files is None:
        return
    else:
        main_window._workspace_files = workspace_files
        load_workspaces(main_window, workspace_files)

        main_window.postprocessing_ui_m.pushButton_loadmc.setEnabled(False)
        main_window.postprocessing_ui_m.pushButton_loadsc.setEnabled(False)
        main_window.postprocessing_ui_m.pushButton_savemc.setEnabled(False)
        main_window.postprocessing_ui_m.pushButton_savesc.setEnabled(False)
        main_window.postprocessing_ui_m.pushButton_mergeBanks.setEnabled(False)
        main_window.postprocessing_ui_m.pushButton_StoG.setEnabled(False)
        if main_window.postprocessing_ui_m.checkBox_defaultWorkspace.isChecked():
            main_window.postprocessing_ui_m.pushButton_extract.setEnabled(True)
            main_window.postprocessing_ui_m.frame_workspaces_table.cur_wks = 'SQ_banks_normalized'

        main_window.ui.statusbar.setStyleSheet("color: blue")
        main_window.ui.statusbar.showMessage("NeXus file successfully loaded!",
                                             main_window.statusbar_display_time)


def extract_button(main_window):
    nxs = main_window._inputFile
    banks = int(main_window.postprocessing_ui_m.label_numBanks.text())
    wks = main_window.postprocessing_ui_m.frame_workspaces_table.get_current_workspace()
    out = main_window.output_folder

    if not os.path.exists(os.path.join(out, "SofQ_merged")):
        os.makedirs(os.path.join(out, "SofQ_merged"))

    try:
        files = extractor(main_window, nxs, banks, wks, os.path.join(out, "SofQ_merged"))
    except:
        return

    initialize_banks(main_window, banks)

    file_list = main_window.postprocessing_ui_m.frame_filelist_tree
    file_list.reset_files_tree()
    file_list.set_workspace(wks)
    file_list.add_raw_data(files)
    initiate_bank_data(main_window, files, wks)

    main_window.postprocessing_ui_m.pushButton_loadmc.setEnabled(True)
    main_window.postprocessing_ui_m.pushButton_savemc.setEnabled(True)
    main_window.postprocessing_ui_m.pushButton_mergeBanks.setEnabled(True)

    main_window.ui.statusbar.setStyleSheet("color: blue")
    main_window.ui.statusbar.showMessage("Workspace successfully extracted!",
                                         main_window.statusbar_display_time)


def extractor(main_window, nexus_file: str, num_banks: int, wks_name: str, out_dir: str):
    stog = StoG(**{"Outputs": {"StemName": out_dir + "/"}})
    head, tail = os.path.split(nexus_file)
    main_window._stem = tail.split('.')[0]
    all_files = list()

    for i in range(num_banks):
        stog.read_nexus_file_by_bank(nexus_file, i, wks_name)
        output_file = "{}_bank{}".format(tail.split(".")[0], i + 1)
        os.rename(os.path.join(out_dir, f"{wks_name}_bank{i}.dat"),
                  os.path.join(out_dir, f"{output_file}.dat"))
        all_files.append(output_file)

    return all_files


def initiate_bank_data(main_window, item_list, workspace):
    with open(main_window.addie_config_file, "r") as f:
        config_j = json.load(f)
    if "BankQMin" in config_j and "BankQMax" in config_j:
        qmin_valid = config_j["BankQMin"]
        qmax_valid = config_j["BankQMax"]
    else:
        if len(main_window._bankDict) == 6:
            qmin_valid = [0., 0., 0., 3., 4., 0.]
            qmax_valid = [14., 25., 40., 40., 40., 6.]
        elif len(main_window._bankDict) == 1:
            qmin_valid = [0.]
            qmax_valid = [40.]
        else:
            qmin_valid = [0. for _ in range(len(main_window._bankDict))]
            qmax_valid = [40. for _ in range(len(main_window._bankDict))]

    for item in item_list:
        current_bank = int(item[-1])
        output_file = os.path.join(main_window.output_folder,
                                   "SofQ_merged",
                                   item + ".dat")
        # read the file for this bank
        file_in = open(output_file, "r")
        line = file_in.readline()
        line = file_in.readline()
        x_list = []
        y_list = []
        #add to the list
        while line:
            line = file_in.readline()
            if line:
                if line.split()[1] != "nan":
                    x_tmp = float(line.split()[0])
                    y_tmp = float(line.split()[1])
                    if qmin_valid[current_bank - 1] <= x_tmp <= qmax_valid[current_bank - 1]:
                        x_list.append(x_tmp)
                        y_list.append(y_tmp)
        file_in.close()
        main_window._bankDict[current_bank]['xList'] = x_list
        main_window._bankDict[current_bank]['yList'] = y_list


def plot(main_window, item_list, banks, workspace, mode):
    for item in item_list:
        if mode == 'Merged':
            if item[-7:] == "_raw.sq":
                x_list = main_window._merged_data[main_window._stem]['XListRaw']
                y_list = main_window._merged_data[main_window._stem]['YListRaw']
            elif item[-7:] == "_bkg.sq":
                x_list = main_window._merged_data[main_window._stem]['XList']
                y_list = main_window._merged_data[main_window._stem]['Bkg']
            else:
                x_list = main_window._merged_data[main_window._stem]['XList']
                y_list = main_window._merged_data[main_window._stem]['YList']
            main_window.postprocessing_ui_m.ppm_view.plot(item, x_list, y_list)

        elif mode == 'Raw':
            # add the x_list and y_list to the dictionary entry for the bank
            x_list = main_window._bankDict[int(item[-1])]['xList']
            y_list = main_window._bankDict[int(item[-1])]['yList']
            main_window.postprocessing_ui_m.ppm_view.plot(item, x_list, y_list)

        elif mode == 'StoG':
            x_list = main_window._pystog_output_files[item]["xlist"]
            y_list = main_window._pystog_output_files[item]["ylist"]
            main_window.postprocessing_ui_m.ppm_view.plot(item, x_list, y_list)


def clear_canvas(main_window):
    # main_window._bankDict = dict()
    main_window.postprocessing_ui_m.ppm_view.canvas_reset()


def change_bank(main_window):
    if main_window._workspace_files is None:
        return
    if not main_window.postprocessing_ui_m.comboBox_banks.currentText():
        return
    current_bank = int(main_window.postprocessing_ui_m.comboBox_banks.currentText())
    bank_dict = main_window._bankDict
    if bank_dict is not None:
        q_min = bank_dict[current_bank]["Qmin"]
        q_max = bank_dict[current_bank]["Qmax"]
        y_offset = bank_dict[current_bank]["Yoffset"]
        y_scale = bank_dict[current_bank]["Yscale"]
        main_window.postprocessing_ui_m.doubleSpinBox_Qmin.setValue(float(q_min))
        main_window.postprocessing_ui_m.doubleSpinBox_Qmax.setValue(float(q_max))
        main_window.postprocessing_ui_m.lineEdit_Yoffset.setText(y_offset)
        main_window.postprocessing_ui_m.lineEdit_Yscale.setText(y_scale)


# initialize a dictionary holding data about a bank (starts at default)
def initialize_banks(main_window, banks):
    bank_dict = dict()
    for bank in range(banks):
        # bank holds in order: Qmin, Qmax, Yoffset, Yscale
        bank_dict[bank + 1] = {'Qmin': '0.0', 'Qmax': '0.0', 'Yoffset': '0.0', 'Yscale': '1.0', 'xList': [], 'yList': []}

    main_window._bankDict = bank_dict
    change_bank(main_window)


def set_merge_values(main_window):
    if main_window._workspace_files is None:
        return
    q_min = main_window.postprocessing_ui_m.doubleSpinBox_Qmin.value()
    q_max = main_window.postprocessing_ui_m.doubleSpinBox_Qmax.value()
    y_offset = main_window.postprocessing_ui_m.lineEdit_Yoffset.text()
    y_scale = main_window.postprocessing_ui_m.lineEdit_Yscale.text()

    current_bank = int(main_window.postprocessing_ui_m.comboBox_banks.currentText())
    bank_dict = main_window._bankDict

    if bank_dict is not None:
        bank_dict[current_bank]["Qmin"] = str(q_min)
        bank_dict[current_bank]["Qmax"] = str(q_max)
        bank_dict[current_bank]["Yoffset"] = y_offset
        bank_dict[current_bank]["Yscale"] = y_scale


def bkg_finder(all_data: list,
               all_range: list,
               fudge_factor: list):
    x_out = []
    y_out = []
    y_bkg_out = []
    for bank, bank_data in enumerate(all_data):
        if all_range[bank][1] != 0:
            x_bank = bank_data[0]
            y_bank = bank_data[1]

            y_bank = np.asarray(y_bank)

            x_min = argrelextrema(np.asarray(y_bank), np.less, order=5)
            y_min = [y_bank[item] for item in x_min[0]]
            x_min = [x_bank[item] for item in x_min[0]]

            if len(x_min) > 3:
                ws_real_bkg = CreateWorkspace(x_min, y_min)

                c_factor = [1., 10., 0.1, 0.05, 0.01, 0.001]
                for c_factor_try in c_factor:
                    c_init = c_factor_try * 0.1
                    Fit(f"name=UserFunction, Formula=a-b*exp(-c*x*x), a=1, b=0.1, c={c_init}",
                        ws_real_bkg,
                        Output='ws_real_bkg_fitted')
                    c_err = mtd['ws_real_bkg_fitted_Parameters'].row(2)["Error"]
                    if c_err != 0. and c_err != float("inf") and c_err != float("-inf"):
                        break

                a_init = mtd['ws_real_bkg_fitted_Parameters'].row(0)["Value"]
                b_init = mtd['ws_real_bkg_fitted_Parameters'].row(1)["Value"]
                c_init = mtd['ws_real_bkg_fitted_Parameters'].row(2)["Value"]
                c_used = fudge_factor[bank] * c_init

                cond_1 = abs(a_init) > 100. or abs(a_init) < 1.E-5
                cond_2 = abs(b_init) > 100. or abs(b_init) < 1.E-5
                cond_3 = abs(c_init) > 100. or abs(c_init) < 1.E-5

                if not (cond_1 or cond_2 or cond_3):
                    y_bkg = [a_init - b_init * np.exp(-c_used * item**2.) for item in x_bank]
                else:
                    y_bkg = [0 for _ in x_bank]
            else:
                y_bkg = [0 for _ in x_bank]

            for i in range(len(x_bank)):
                if bank == len(all_data) - 1:
                    if all_range[bank][0] <= x_bank[i] <= all_range[bank][1]:
                        x_out.append(x_bank[i])
                        y_out.append(y_bank[i] - y_bkg[i])
                        y_bkg_out.append(y_bkg[i])
                else:
                    if all_range[bank][0] <= x_bank[i] < all_range[bank][1]:
                        x_out.append(x_bank[i])
                        y_out.append(y_bank[i] - y_bkg[i])
                        y_bkg_out.append(y_bkg[i])

    # Remove all workspaces
    DeleteWorkspace("ws_real_bkg")
    DeleteWorkspace("ws_real_bkg_fitted_Workspace")
    DeleteWorkspace("ws_real_bkg_fitted_Parameters")
    DeleteWorkspace("ws_real_bkg_fitted_NormalisedCovarianceMatrix")

    return x_out, y_out, y_bkg_out


def merge_banks(main_window):
    if main_window._workspace_files is None or main_window._bankDict is None:
        return

    print("[Info] Merging banks...")

    bk_range_init = list()
    for bank in range(len(main_window._bankDict)):
        try:
            qmin_tmp = float(main_window._bankDict[bank + 1]['Qmin'])
        except ValueError:
            qmin_tmp = 0.
        try:
            qmax_tmp = float(main_window._bankDict[bank + 1]['Qmax'])
        except ValueError:
            qmax_tmp = 0.
        bk_range_init.append((qmin_tmp, qmax_tmp))

    bk_range_sti = sorted(enumerate(bk_range_init), key=lambda x: x[1])
    bk_st_dict = dict()
    for count, item in enumerate(bk_range_sti):
        bk_st_dict[count] = item[0]
    bk_range_st = [item[1] for item in bk_range_sti]
    st_index = [item[0] for item in bk_range_sti]
    if sorted(st_index) == st_index:
        prob_nom_phys_bank = True
    else:
        prob_nom_phys_bank = False

    banks_x = []
    banks_y = []
    for bank in range(len(main_window._bankDict)):
        banks_x.append(main_window._bankDict[bk_st_dict[bank] + 1]['xList'])
        banks_y.append(main_window._bankDict[bk_st_dict[bank] + 1]['yList'])

    qmin_list = list()
    qmax_list = list()
    qmax_max = 0.
    qmax_max_bank = 0
    # TODO: The hard coded `qmin_valid` and `qmax_valid` needs to be
    # updated to adapt to general way of grouping detectors into banks.
    if prob_nom_phys_bank:
        if len(main_window._bankDict) == 6:
            qmin_valid = [0., 0., 0., 3., 4., 0.]
            qmax_valid = [14., 25., 40., 40., 40., 6.]
        elif len(main_window._bankDict) == 1:
            qmin_valid = [0.]
            qmax_valid = [40.]
        else:
            qmin_valid = [0. for _ in range(len(main_window._bankDict))]
            qmax_valid = [40. for _ in range(len(main_window._bankDict))]
    else:
        qmin_valid = [0. for _ in range(len(main_window._bankDict))]
        qmax_valid = [40. for _ in range(len(main_window._bankDict))]

    valid_region = False
    for bank in range(len(main_window._bankDict)):
        qmin_tmp = bk_range_st[bank][0]
        qmax_tmp = bk_range_st[bank][1]

        if bank > 0 and qmax_tmp > 0.:
            qmax_to_compare = 0.
            for bank_tmp in range(bank):
                if qmax_list[-(bank_tmp + 1)] > 0.:
                    qmax_to_compare = qmax_list[-(bank_tmp + 1)]
                    break
            if qmax_to_compare == 0.:
                qmax_to_compare = qmin_tmp
            if qmin_tmp != qmax_to_compare:
                msg_p1 = "[Error] Gap or overlap found in between banks. "
                msg_p2 = "This is not supported."
                print(msg_p1 + msg_p2)
                main_window.ui.statusbar.setStyleSheet("color: red")
                main_window.ui.statusbar.showMessage(
                    "Merge banks failed", main_window.statusbar_display_time)
                QApplication.restoreOverrideCursor()
                return
        if qmin_tmp == qmax_tmp:
            qmin_list.append(0.)
            qmax_list.append(0.)
        elif qmin_tmp > qmax_tmp:
            msg_p1 = f"[Error] Qmax smaller than Qmin for bank-{bank+1}. "
            msg_p2 = "Please input valid values and try again."
            print(msg_p1 + msg_p2)
            main_window.ui.statusbar.setStyleSheet("color: red")
            main_window.ui.statusbar.showMessage(
                "Merge banks failed", main_window.statusbar_display_time)
            QApplication.restoreOverrideCursor()
            return
        elif qmin_tmp < qmin_valid[bank] or qmax_tmp > qmax_valid[bank]:
            msg_p1 = f"[Error] Qmin or Qmax out of the valid region for bank-{bank+1}. "
            msg_p2 = "Please input valid values and try again."
            print(msg_p1 + msg_p2)
            main_window.ui.statusbar.setStyleSheet("color: red")
            main_window.ui.statusbar.showMessage(
                "Merge banks failed", main_window.statusbar_display_time)
            QApplication.restoreOverrideCursor()
            return
        else:
            valid_region = True
            qmin_list.append(qmin_tmp)
            qmax_list.append(qmax_tmp)
            if qmax_tmp > qmax_max:
                qmax_max = qmax_tmp
                qmax_max_bank = bank

    if not valid_region:
        print("[Error] Qmin and Qmax values are all zero for all banks.")
        print("[Error] Please input valid values and try again.")
        main_window.ui.statusbar.setStyleSheet("color: red")
        main_window.ui.statusbar.showMessage(
            "Merge banks failed", main_window.statusbar_display_time)
        QApplication.restoreOverrideCursor()
        return

    remove_bkg = main_window.postprocessing_ui_m.checkBox_bkg_removal.isChecked()
    if not remove_bkg:
        x_merged = list()
        y_merged = list()

        range_tmp = list(range(len(main_window._bankDict)))
        for bank in range_tmp:
            yoffset_tmp = main_window._bankDict[bk_st_dict[bank] + 1]['Yoffset']
            yscale_tmp = main_window._bankDict[bk_st_dict[bank] + 1]['Yscale']
            if yoffset_tmp.strip() == "":
                yoffset_tmp = 0.0
            if yscale_tmp.strip() == "":
                yscale_tmp = 1.0
            yoffset_tmp = float(yoffset_tmp)
            yscale_tmp = float(yscale_tmp)
            if bank == qmax_max_bank:
                for i, x_val in enumerate(banks_x[bank]):
                    if qmin_list[bank] <= x_val <= qmax_list[bank]:
                        x_merged.append(x_val)
                        y_merged.append(banks_y[bank][i] / yscale_tmp + yoffset_tmp)
            else:
                for i, x_val in enumerate(banks_x[bank]):
                    if qmin_list[bank] <= x_val < qmax_list[bank]:
                        x_merged.append(x_val)
                        y_merged.append(banks_y[bank][i] / yscale_tmp + yoffset_tmp)
    else:
        bank_range = list()
        yscale_list = list()
        yoffset_list = list()
        all_data = list()
        x_merged_raw = list()
        y_merged_raw = list()
        # TODO: The hard coded `qmax_bkg_est` and `fudge_factor` needs to be
        # updated to adapt to general way of grouping detectors into banks.
        if prob_nom_phys_bank:
            if len(main_window._bankDict) == 6:
                qmax_bkg_est = [14., 25., 25., 25., 40., 6.]
                fudge_factor = [1., 1., 1., 1., 1., 1.]
            elif len(main_window._bankDict) == 1:
                qmax_bkg_est = [40.]
                fudge_factor = [1.]
            else:
                qmax_bkg_est = [25. for _ in range(len(main_window._bankDict))]
                qmax_bkg_est[-1] = 0.
                qmax_bkg_est[-2] = 40.
                fudge_factor = [1. for _ in range(len(main_window._bankDict))]
        else:
            qmax_bkg_est = [25. for _ in range(len(main_window._bankDict))]
            qmax_bkg_est[-1] = 0.
            qmax_bkg_est[-2] = 40.
            fudge_factor = [1. for _ in range(len(main_window._bankDict))]

        range_tmp = list(range(len(main_window._bankDict)))
        for bank in range_tmp:
            bank_range.append([qmin_list[bank], qmax_list[bank]])
            yoffset_tmp = main_window._bankDict[bk_st_dict[bank] + 1]['Yoffset']
            yscale_tmp = main_window._bankDict[bk_st_dict[bank] + 1]['Yscale']
            if yoffset_tmp.strip() == "":
                yoffset_tmp = 0.0
            if yscale_tmp.strip() == "":
                yscale_tmp = 1.0
            yscale_list.append(float(yscale_tmp))
            yoffset_list.append(float(yoffset_tmp))
            x_tmp = list()
            y_tmp = list()
            if bank == qmax_max_bank:
                for i, x_val in enumerate(banks_x[bank]):
                    if qmin_list[bank] <= x_val <= qmax_bkg_est[bank]:
                        x_tmp.append(x_val)
                        y_tmp.append(banks_y[bank][i])
                    if qmin_list[bank] <= x_val <= qmax_list[bank]:
                        x_merged_raw.append(x_val)
                        y_merged_raw.append(banks_y[bank][i])

            else:
                for i, x_val in enumerate(banks_x[bank]):
                    if qmin_list[bank] <= x_val < qmax_bkg_est[bank]:
                        x_tmp.append(x_val)
                        y_tmp.append(banks_y[bank][i])
                    if qmin_list[bank] <= x_val < qmax_list[bank]:
                        x_merged_raw.append(x_val)
                        y_merged_raw.append(banks_y[bank][i])
            all_data.append([x_tmp, y_tmp])

        x_merged_init, y_merged_init, y_bkg_out = bkg_finder(
            all_data,
            bank_range,
            fudge_factor
        )
        x_merged = x_merged_init
        y_merged = list()
        for i, x_val in enumerate(x_merged):
            if i == len(x_merged) - 1:
                for j, b_r in enumerate(bank_range):
                    if x_val == b_r[1]:
                        y_merged.append(y_merged_init[i] / yscale_list[j] + yoffset_list[j])
            for j, b_r in enumerate(bank_range):
                if b_r[0] <= x_val < b_r[1]:
                    y_merged.append(y_merged_init[i] / yscale_list[j] + yoffset_list[j])

    if len(x_merged) == 0:
        print("[Error] Qmin and Qmax values are all zero for all banks.")
        print("[Error] Please input valid values and try again.")
        return

    main_window.ui.statusbar.setStyleSheet("color: blue")
    main_window.ui.statusbar.showMessage("Banks merged successfully!",
                                         main_window.statusbar_display_time)

    file_list = main_window.postprocessing_ui_m.frame_filelist_tree
    merged_data_ref = main_window._stem + '_merged.sq'
    if remove_bkg:
        main_window._merged_data[main_window._stem] = {'Name': merged_data_ref,
                                                       'XList': x_merged,
                                                       'YList': y_merged,
                                                       'XListRaw': x_merged_raw,
                                                       'YListRaw': y_merged_raw,
                                                       'Bkg': y_bkg_out
                                                       }
        file_list.add_merged_data(main_window._stem + '_merged_raw.sq')
        file_list.add_merged_data(main_window._stem + '_bkg.sq')
        file_list.add_merged_data(merged_data_ref)
    else:
        file_list.clear_merged_tree()
        main_window._merged_data[main_window._stem] = {'Name': merged_data_ref,
                                                       'XList': x_merged,
                                                       'YList': y_merged}
        file_list.add_merged_data(merged_data_ref)

    initiate_stog_data(main_window)

    main_window.postprocessing_ui_m.pushButton_savesc.setEnabled(True)
    main_window.postprocessing_ui_m.pushButton_loadsc.setEnabled(True)
    main_window.postprocessing_ui_m.pushButton_StoG.setEnabled(True)

    print("[Info] Banks successfully merged")


def save_file_raw(main_window, file_name):
    if isinstance(file_name, list):
        save_directory = QFileDialog.getExistingDirectory(main_window,
                                                          'Save Banks',
                                                          main_window.current_folder)
        for item in file_name:
            x_bank = main_window._bankDict[int(item[-1])]['xList']
            y_bank = main_window._bankDict[int(item[-1])]['yList']
            if save_directory is None or save_directory == '' or len(save_directory) == 0:
                return
            with open(os.path.join(save_directory, item + ".dat"), 'w') as new_file:
                new_file.write(str(len(x_bank)) + '\n')
                new_file.write('#\n')
                for i in range(len(x_bank)):
                    new_file.write(str(x_bank[i]) + ' ' + str(y_bank[i]) + '\n')

        main_window.ui.statusbar.setStyleSheet("color: blue")
        main_window.ui.statusbar.showMessage("Files saved successfully!",
                                             main_window.statusbar_display_time)
    else:
        x_bank = main_window._bankDict[int(file_name[-1])]['xList']
        y_bank = main_window._bankDict[int(file_name[-1])]['yList']
        out_file = os.path.join(main_window.output_folder, "SofQ_merged", file_name + '.dat')
        save_directory = QFileDialog.getSaveFileName(main_window, 'Save Bank',
                                                     out_file)
        if isinstance(save_directory, tuple):
            save_directory = save_directory[0]
        if save_directory is None or save_directory == '' or len(save_directory) == 0:
            return
        with open(save_directory, 'w') as new_file:
            new_file.write(str(len(x_bank)) + '\n')
            new_file.write('#\n')
            for i in range(len(x_bank)):
                new_file.write(str(x_bank[i]) + ' ' + str(y_bank[i]) + '\n')

        main_window.ui.statusbar.setStyleSheet("color: blue")
        main_window.ui.statusbar.showMessage("File saved successfully!",
                                             main_window.statusbar_display_time)


def save_file_merged(main_window, file_name, auto=False):
    out_dir_tmp = os.path.join(main_window.output_folder, "SofQ_merged")
    if not os.path.exists(out_dir_tmp):
        os.makedirs(out_dir_tmp)

    if auto:
        save_directory = out_dir_tmp
        save_file = file_name

        main_window._full_merged_path = os.path.join(save_directory, save_file)

    else:
        if file_name[-7:] == "_raw.sq":
            win_title = "Save Raw Merged File"
        elif file_name[-7:] == "_bkg.sq":
            win_title = "Save Background File"
        else:
            win_title = "Save Merged File"
        save_directory_user = QFileDialog.getSaveFileName(main_window, win_title,
                                                          os.path.join(out_dir_tmp,
                                                                       file_name),
                                                          '*.sq')
        if isinstance(save_directory_user, tuple):
            save_directory_user = save_directory_user[0]
        if save_directory_user is None or save_directory_user == '' or len(save_directory_user) == 0:
            return
        main_window._full_merged_path = save_directory_user

    if file_name[-7:] == "_raw.sq":
        x_merged = main_window._merged_data[main_window._stem]['XListRaw']
        y_merged = main_window._merged_data[main_window._stem]['YListRaw']
    elif file_name[-7:] == "_bkg.sq":
        x_merged = main_window._merged_data[main_window._stem]['XList']
        y_merged = main_window._merged_data[main_window._stem]['Bkg']
    else:
        x_merged = main_window._merged_data[main_window._stem]['XList']
        y_merged = main_window._merged_data[main_window._stem]['YList']

    with open(main_window._full_merged_path, 'w') as new_file:
        new_file.write(str(len(x_merged)) + '\n')
        new_file.write('#\n')
        for i in range(len(x_merged)):
            new_file.write("{0:10.3F}{1:20.6F}\n".format(x_merged[i], y_merged[i]))

    main_window.ui.statusbar.setStyleSheet("color: blue")
    main_window.ui.statusbar.showMessage("File saved successfully!",
                                         main_window.statusbar_display_time)


def save_file_stog(main_window, file_name):
    rc = main_window._pystog_inputs_collect["RippleParams"][0]
    rx = main_window._pystog_inputs_collect["RippleParams"][2]
    rn = main_window._pystog_inputs_collect["RippleParams"][1]

    if isinstance(file_name, list):
        save_directory = QFileDialog.getExistingDirectory(main_window,
                                                          'Save StoG Files',
                                                          main_window.current_folder)

        if save_directory is None or save_directory == '' or len(save_directory) == 0:
            return

        for item in file_name:
            x_stog = main_window._pystog_output_files[item]["xlist"]
            y_stog = main_window._pystog_output_files[item]["ylist"]

            if "pdffit.gr" in item:
                current_time = datetime.now()
                current_timezone = datetime.now().astimezone().strftime("%Z")
                current_weekday = current_time.weekday()
                time_stamp = weekdays[current_weekday] + " "
                time_stamp += current_time.strftime("%m-%d-%Y %H:%M:%S") + " "
                time_stamp += current_timezone
                kt = "Qmax"
                ts_qmax = float(main_window._pystog_inputs_collect[kt])
                with open(os.path.join(save_directory, item), 'w') as f:
                    f.write(f"# {len(x_stog)}\n")
                    f.write("# Pair Distribution Function (PDF)\n")
                    f.write(f"# created: {time_stamp}\n")
                    str_tmp = f"# comment: neutron, Qmax={ts_qmax}, "
                    str_tmp += "Qdamp=0.017659, Qbroad=0.0191822\n"
                    kt = "FourierFilter"
                    ft_sel = main_window._pystog_inputs_collect[kt]
                    if ft_sel:
                        kt = "Rmin"
                        ft_rmin = float(main_window._pystog_inputs_collect[kt])
                        str_tmp += f"# comment: Fourier filtered, rcut={ft_rmin} \n"
                    str_tmp += "# comment: Ripple removed, "
                    str_tmp += f"Rcutoff, 1st peak min, max = {rc}, {rn}, {rx}\n"
                    f.write(str_tmp)
                    for count, r_val in enumerate(x_stog):
                        if count == len(x_stog) - 1:
                            f.write("{0:16.12F}{1:18.12F}".format(r_val,
                                                                  y_stog[count]))
                        else:
                            f.write("{0:16.12F}{1:18.12F}\n".format(r_val,
                                                                    y_stog[count]))
            else:
                with open(os.path.join(save_directory, item), 'w') as new_file:
                    new_file.write(str(len(x_stog)) + '\n')
                    new_file.write('#\n')
                    for i in range(len(x_stog)):
                        new_file.write(str(x_stog[i]) + ' ' + str(y_stog[i]) + '\n')
        main_window.ui.statusbar.setStyleSheet("color: blue")
        main_window.ui.statusbar.showMessage("Files saved successfully!",
                                             main_window.statusbar_display_time)
    else:
        last_char = file_name[-2:]
        if last_char == 'sq':
            default = '*.sq;;*.fq;;*.gr;;All (*.*)'
        elif last_char == 'fq':
            default = '*.fq;;*.sq;;*.gr;;All (*.*)'
        elif last_char == 'gr':
            default = '*.gr;;*.fq;;*.sq;;All (*.*)'
        out_file = os.path.join(main_window.output_folder,
                                "StoG",
                                file_name)
        save_file = QFileDialog.getSaveFileName(main_window,
                                                'Save StoG File',
                                                out_file,
                                                default)
        if isinstance(save_file, tuple):
            save_file = save_file[0]
        if save_file is None or save_file == '' or len(save_file) == 0:
            return

        x_stog = main_window._pystog_output_files[file_name]["xlist"]
        y_stog = main_window._pystog_output_files[file_name]["ylist"]

        if "pdffit.gr" in file_name:
            current_time = datetime.now()
            current_timezone = datetime.now().astimezone().strftime("%Z")
            current_weekday = current_time.weekday()
            time_stamp = weekdays[current_weekday] + " "
            time_stamp += current_time.strftime("%m-%d-%Y %H:%M:%S") + " "
            time_stamp += current_timezone
            kt = "Qmax"
            ts_qmax = float(main_window._pystog_inputs_collect[kt])
            with open(save_file, 'w') as f:
                f.write(f"# {len(x_stog)}\n")
                f.write("# Pair Distribution Function (PDF)\n")
                f.write(f"# created: {time_stamp}\n")
                str_tmp = f"# comment: neutron, Qmax={ts_qmax}, "
                str_tmp += "Qdamp=0.017659, Qbroad=0.0191822\n"
                kt = "FourierFilter"
                ft_sel = main_window._pystog_inputs_collect[kt]
                if ft_sel:
                    kt = "Rmin"
                    ft_rmin = float(main_window._pystog_inputs_collect[kt])
                    str_tmp += f"# comment: Fourier filtered, rcut={ft_rmin} \n"
                str_tmp += "# comment: Ripple removed, "
                str_tmp += f"Rcutoff, 1st peak min, max = {rc}, {rn}, {rx}\n"
                f.write(str_tmp)
                for count, r_val in enumerate(x_stog):
                    if count == len(x_stog) - 1:
                        f.write("{0:16.12F}{1:18.12F}".format(r_val,
                                                              y_stog[count]))
                    else:
                        f.write("{0:16.12F}{1:18.12F}\n".format(r_val,
                                                                y_stog[count]))
        else:
            with open(save_file, 'w') as new_file:
                new_file.write(str(len(x_stog)) + '\n')
                new_file.write('#\n')
                for i in range(len(x_stog)):
                    new_file.write(str(x_stog[i]) + ' ' + str(y_stog[i]) + '\n')

        main_window.ui.statusbar.setStyleSheet("color: blue")
        main_window.ui.statusbar.showMessage("File saved successfully!",
                                             main_window.statusbar_display_time)


# TODO: Add checking of inputs
def initiate_stog_data(main_window):
    pystog_inputs = main_window._pystog_inputs_collect

    pystog_inputs["Qmin"] = main_window._merged_data[main_window._stem]['XList'][0]
    pystog_inputs["Qmax"] = main_window._merged_data[main_window._stem]['XList'][-1]
    pystog_inputs["Yoffset"] = main_window.postprocessing_ui_m.lineEdit_Yoffset_stog.text()
    ys_text_tmp = main_window.postprocessing_ui_m.lineEdit_Yscale_stog.text()
    ys_text = "{0:5.3F}".format(1.0 / float(ys_text_tmp))
    pystog_inputs["Yscale"] = ys_text
    pystog_inputs["Qoffset"] = main_window.postprocessing_ui_m.lineEdit_Qoffset.text()
    pystog_inputs["Rmax"] = str(main_window.postprocessing_ui_m.doubleSpinBox_Rmax.value())
    pystog_inputs["Rstep"] = str(main_window.postprocessing_ui_m.doubleSpinBox_Rstep.value())
    pystog_inputs["NumberDensity"] = main_window.postprocessing_ui_m.lineEdit_numberDensity.text()
    pystog_inputs["FaberZiman"] = main_window.postprocessing_ui_m.lineEdit_faberZiman.text()
    pystog_inputs["Lorch"] = main_window.postprocessing_ui_m.buttonGroup_Lorch.checkedButton().text() == 'Yes'
    pystog_inputs["FourierFilter"] = main_window.postprocessing_ui_m.buttonGroup_FF.checkedButton().text() == 'Yes'
    pystog_inputs["Rmin"] = str(main_window.postprocessing_ui_m.doubleSpinBox_Rmin.value())
    pystog_inputs["RippleParams"] = main_window.postprocessing_ui_m.lineEdit_rippleParams.text()
    pystog_inputs["RealSpaceFunction"] = main_window.postprocessing_ui_m.comboBox_pdfform.currentText()


def set_stog_values(main_window):
    pystog_inputs = main_window._pystog_inputs_collect
    pystog_inputs["Qmin"] = main_window._merged_data[main_window._stem]['XList'][0]
    pystog_inputs["Qmax"] = main_window._merged_data[main_window._stem]['XList'][-1]
    pystog_inputs["Yoffset"] = main_window.postprocessing_ui_m.lineEdit_Yoffset_stog.text()
    ys_text_tmp = main_window.postprocessing_ui_m.lineEdit_Yscale_stog.text()
    ys_text = "{0:5.3F}".format(1.0 / (float(ys_text_tmp) + 1.E-20))
    pystog_inputs["Yscale"] = ys_text
    pystog_inputs["Qoffset"] = main_window.postprocessing_ui_m.lineEdit_Qoffset.text()
    pystog_inputs["Rmax"] = str(main_window.postprocessing_ui_m.doubleSpinBox_Rmax.value())
    pystog_inputs["Rstep"] = str(main_window.postprocessing_ui_m.doubleSpinBox_Rstep.value())
    pystog_inputs["NumberDensity"] = main_window.postprocessing_ui_m.lineEdit_numberDensity.text()
    pystog_inputs["FaberZiman"] = main_window.postprocessing_ui_m.lineEdit_faberZiman.text()
    pystog_inputs["Lorch"] = main_window.postprocessing_ui_m.buttonGroup_Lorch.checkedButton().text() == 'Yes'
    pystog_inputs["FourierFilter"] = main_window.postprocessing_ui_m.buttonGroup_FF.checkedButton().text() == 'Yes'
    pystog_inputs["Rmin"] = str(main_window.postprocessing_ui_m.doubleSpinBox_Rmin.value())
    pystog_inputs["RippleParams"] = main_window.postprocessing_ui_m.lineEdit_rippleParams.text()
    pystog_inputs["RealSpaceFunction"] = main_window.postprocessing_ui_m.comboBox_pdfform.currentText()


def set_stog_values_load(main_window, stog_dict):
    pystog_inputs = main_window._pystog_inputs_collect
    pystog_inputs["Qmin"] = main_window._merged_data[main_window._stem]['XList'][0]
    pystog_inputs["Qmax"] = main_window._merged_data[main_window._stem]['XList'][-1]

    pystog_inputs["Yoffset"] = stog_dict["Yoffset"]
    main_window.postprocessing_ui_m.lineEdit_Yoffset_stog.setText(stog_dict["Yoffset"])
    pystog_inputs["Yscale"] = stog_dict["Yscale"]
    ys_text = "{0:5.3F}".format(1. / float(pystog_inputs["Yscale"]))
    main_window.postprocessing_ui_m.lineEdit_Yscale_stog.setText(ys_text)
    pystog_inputs["Qoffset"] = stog_dict["Qoffset"]
    main_window.postprocessing_ui_m.lineEdit_Qoffset.setText(stog_dict["Qoffset"])
    pystog_inputs["Rmax"] = stog_dict["Rmax"]
    main_window.postprocessing_ui_m.doubleSpinBox_Rmax.setValue(float(stog_dict["Rmax"]))
    pystog_inputs["Rstep"] = stog_dict["Rstep"]
    main_window.postprocessing_ui_m.doubleSpinBox_Rstep.setValue(float(stog_dict["Rstep"]))
    pystog_inputs["NumberDensity"] = stog_dict["NumberDensity"]
    main_window.postprocessing_ui_m.lineEdit_numberDensity.setText(stog_dict["NumberDensity"])
    pystog_inputs["FaberZiman"] = stog_dict["FaberZiman"]
    main_window.postprocessing_ui_m.lineEdit_faberZiman.setText(stog_dict["FaberZiman"])
    pystog_inputs["RealSpaceFunction"] = stog_dict["RealSpaceFunction"]
    if stog_dict["RealSpaceFunction"] == "g(r)":
        main_window.postprocessing_ui_m.comboBox_pdfform.setCurrentIndex(0)
    else:
        main_window.postprocessing_ui_m.comboBox_pdfform.setCurrentIndex(1)
    pystog_inputs["Lorch"] = stog_dict["Lorch"]
    if stog_dict["Lorch"]:
        main_window.postprocessing_ui_m.buttonGroup_Lorch.checkedButton().setText("Yes")
    else:
        main_window.postprocessing_ui_m.buttonGroup_Lorch.checkedButton().setText("No")
    pystog_inputs["FourierFilter"] = stog_dict["FourierFilter"]
    if stog_dict["FourierFilter"]:
        main_window.postprocessing_ui_m.buttonGroup_FF.checkedButton().setText("Yes")
    else:
        main_window.postprocessing_ui_m.buttonGroup_FF.checkedButton().setText("No")
    pystog_inputs["Rmin"] = stog_dict["Rmin"]
    main_window.postprocessing_ui_m.doubleSpinBox_Rmin.setValue(float(stog_dict["Rmin"]))
    if "RippleParams" in stog_dict.keys():
        pystog_inputs["RippleParams"] = stog_dict["RippleParams"]
        main_window.postprocessing_ui_m.lineEdit_rippleParams.setText(stog_dict["RippleParams"])


# verify the stog values, also converts the rippleparams
def check_verify_stog(stog_dict):
    for key in stog_dict:
        if(isinstance(stog_dict[key], bool)):
            pass
        elif stog_dict[key] == '':
            return False
        elif key == "RippleParams":
            if(isinstance(stog_dict[key], str)):
                stog_dict["RippleParams"] = [float(item) for item in stog_dict["RippleParams"].split(",")]
            if len(stog_dict["RippleParams"]) != 3:
                return False
        else:
            if key != "RealSpaceFunction":
                try:
                    value = float(stog_dict[key])
                    if not isinstance(value, float):
                        return False
                except ValueError:
                    return False
    return True


def execute_stog(main_window):
    if main_window._workspace_files is None or len(main_window._merged_data) == 0:
        return
    pystog_inputs = main_window._pystog_inputs_collect
    initiate_stog_data(main_window)
    if not check_verify_stog(pystog_inputs):
        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setText("Some StoG data or parameters are incorrect. StoG was not run.")
        msg.exec()
        return

    if not os.path.exists(os.path.join(main_window.output_folder, "StoG")):
        os.makedirs(os.path.join(main_window.output_folder, "StoG"))

    json_format = convert_json(main_window, pystog_inputs)
    if json_format is None:
        print("[Error] Invalid PyStoG input. Check the input params and the output directory.")
        main_window.ui.statusbar.setStyleSheet("color: red")
        main_window.ui.statusbar.showMessage("PyStoG execution failed!",
                                             main_window.statusbar_display_time)
        return

    print("[Info] The json file is created.")
    print("[Info] PyStoG in progress...")
    cwd = os.getcwd()
    path = os.path.join(os.path.expanduser('~'), '.mantid')
    os.chdir(path)
    with open('pystog_input.json', 'w') as pystog_file:
        json.dump(json_format, pystog_file, indent=2)
    subprocess.check_call([pystog_cli, "--json", "pystog_input.json"])
    os.chdir(cwd)
    print("[Info] PyStoG successfully executed")

    main_window.ui.statusbar.setStyleSheet("color: blue")
    main_window.ui.statusbar.showMessage("PyStoG successfully executed!",
                                         main_window.statusbar_display_time)

    added_stog = add_stog_data(main_window)
    if added_stog is None:
        return
    generate_final(main_window)

    current_dir = main_window.current_folder
    if os.path.isfile(os.path.join(current_dir, "ft.dat")):
        os.rename(os.path.join(current_dir, "ft.dat"),
                  os.path.join(main_window.output_folder,
                               "StoG",
                               "ft.dat"))
    if os.path.isfile(os.path.join(current_dir, "pystog_input.json")):
        os.rename(os.path.join(current_dir, "pystog_input.json"),
                  os.path.join(main_window.output_folder,
                               "StoG",
                               "pystog_input.json"))


def save_sconfig(main_window):
    pystog_inputs = main_window._pystog_inputs_collect
    initiate_stog_data(main_window)
    if not check_verify_stog(pystog_inputs):
        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setText("Some StoG data or parameters are incorrect. StoG was not run.")
        msg.exec()
        return

    scofnig_file_name = open_config_file(main_window)
    if scofnig_file_name is None:
        return

    if scofnig_file_name[-5:] == ".json":
        file_out = open(scofnig_file_name, "w")
    else:
        file_out = open(scofnig_file_name + ".json", "w")

    json_format = convert_json(main_window, pystog_inputs)
    json.dump(json_format, file_out, indent=2)
    file_out.close()
    print("[Info] The json file is saved to ", scofnig_file_name)

    main_window.ui.statusbar.setStyleSheet("color: blue")
    main_window.ui.statusbar.showMessage("Config file successfully saved!",
                                         main_window.statusbar_display_time)


def load_sconfig(main_window):
    scofnig_file_name = open_config_file_r(main_window)
    if scofnig_file_name is None:
        return

    if scofnig_file_name[-5:] == ".json":
        with open(scofnig_file_name, "r") as sconfig_json:
            try:
                sconfig_in = json.load(sconfig_json)
            except json.decoder.JSONDecodeError as err:
                print("[Error] Could not load in JSON file", scofnig_file_name)
                print("[Error]", err)
                return
    else:
        print("[Error] Not a JSON file selected. Try again.")
        return

    stog_format = convert_json_inverse(main_window, sconfig_in)
    set_stog_values_load(main_window, stog_format)

    main_window.ui.statusbar.setStyleSheet("color: blue")
    main_window.ui.statusbar.showMessage("Config file successfully loaded!",
                                         main_window.statusbar_display_time)


def convert_json(main_window, stog_dict):
    json_dict = dict()

    if not os.path.exists(main_window._full_merged_path):
        return
    json_dict["Files"] = [{"Filename": os.path.abspath(main_window._full_merged_path),
                           "ReciprocalFunction": "S(Q)",
                           "Qmin": stog_dict["Qmin"],
                           "Qmax": stog_dict["Qmax"],
                           "Y": {"Offset": float(stog_dict["Yoffset"]),
                                 "Scale": float(stog_dict["Yscale"])},
                           "X": {"Offset": float(stog_dict["Qoffset"])}}]

    json_dict["RealSpaceFunction"] = stog_dict["RealSpaceFunction"]

    json_dict["NumberDensity"] = float(stog_dict["NumberDensity"])
    json_dict["Rmax"] = float(stog_dict["Rmax"])
    json_dict["Rpoints"] = int(float(stog_dict["Rmax"])/float(stog_dict["Rstep"]))
    if(stog_dict["FourierFilter"]):
        json_dict["FourierFilter"] = {"Cutoff": float(stog_dict["Rmin"])}
    json_dict["<b_coh>^2"] = float(stog_dict["FaberZiman"])
    json_dict["LorchFlag"] = stog_dict["Lorch"]
    json_dict["RippleParams"] = stog_dict["RippleParams"]
    output = os.path.join(main_window.output_folder,
                          "StoG",
                          main_window._stem)
    json_dict["Outputs"] = {"StemName": os.path.abspath(output)}
    return json_dict


def convert_json_inverse(main_window, json_dict):
    stog_dict = dict()

    stog_dict["Qmin"] = str(json_dict["Files"][0]["Qmin"])
    stog_dict["Qmax"] = str(json_dict["Files"][0]["Qmax"])
    stog_dict["Yoffset"] = str(json_dict["Files"][0]["Y"]["Offset"])
    stog_dict["Yscale"] = str(json_dict["Files"][0]["Y"]["Scale"])
    stog_dict["Qoffset"] = str(json_dict["Files"][0]["X"]["Offset"])
    stog_dict["NumberDensity"] = str(json_dict["NumberDensity"])
    stog_dict["Rmax"] = str(json_dict["Rmax"])
    stog_dict["Rstep"] = "{0:5.3F}".format(float(json_dict["Rmax"]) / float(json_dict["Rpoints"]))
    if "FourierFilter" in json_dict.keys():
        stog_dict["FourierFilter"] = True
        stog_dict["Rmin"] = str(json_dict["FourierFilter"]["Cutoff"])
    else:
        stog_dict["FourierFilter"] = False
    stog_dict["FaberZiman"] = str(json_dict["<b_coh>^2"])
    stog_dict["Lorch"] = json_dict["LorchFlag"]
    stog_dict["RealSpaceFunction"] = json_dict["RealSpaceFunction"]
    if "RippleParams" in json_dict.keys():
        if isinstance(json_dict["RippleParams"], str):
            stog_dict["RippleParams"] = json_dict["RippleParams"]
        elif isinstance(json_dict["RippleParams"], list):
            str_tmp = ",".join([str(item) for item in json_dict["RippleParams"]])
            stog_dict["RippleParams"] = str_tmp
        else:
            pass

    return stog_dict


def add_stog_data(main_window):
    file_list_tree = main_window.postprocessing_ui_m.frame_filelist_tree

    stem = main_window._stem

    data_sq = stem + ".sq"
    data_gr = stem + ".gr"
    data_ft_sq = stem + "_ft.sq"
    data_ft_gr = stem + "_ft.gr"
    data_rmc_fq = stem + "_rmc.fq"
    data_rmc_gr = stem + "_rmc.gr"
    data_pdffit_gr = stem + "_pdffit.gr"

    data_list = [
        data_sq,
        data_gr,
        data_ft_sq,
        data_ft_gr,
        data_rmc_fq,
        data_rmc_gr,
        data_pdffit_gr
    ]

    for file_name in data_list:
        if file_name == data_pdffit_gr:
            file_tmp = os.path.join(
                main_window.output_folder,
                "StoG",
                data_rmc_gr
            )
            file_out_tmp = os.path.join(
                main_window.output_folder,
                "StoG",
                data_pdffit_gr
            )
            try:
                file_in = open(file_tmp, "r")
            except FileNotFoundError:
                err_msg = f"[Error] S(Q) data file {file_tmp} not found. "
                err_msg += "Please check the output dir setting."
                print(err_msg)
                main_window.ui.statusbar.setStyleSheet("color: red")
                main_window.ui.statusbar.showMessage(
                    "S(Q) file loading error, see the terminal for more info!",
                    main_window.statusbar_display_time
                )
                return

            line = file_in.readline()
            line = file_in.readline()
            x_list = []
            y_list = []
            while line:
                line = file_in.readline()
                if line:
                    if line.split()[1] != "nan":
                        x_val = float(line.split()[0])
                        x_list.append(x_val)
                        y_val = float(line.split()[1])
                        kt = "NumberDensity"
                        rho_val = float(main_window._pystog_inputs_collect[kt])
                        kt = "FaberZiman"
                        fz_val = float(main_window._pystog_inputs_collect[kt])
                        y_val *= (4. * np.pi * x_val * rho_val / fz_val)
                        y_list.append(y_val)
            file_in.close()

            with open(file_out_tmp, "w") as f:
                current_time = datetime.now()
                current_timezone = datetime.now().astimezone().strftime("%Z")
                current_weekday = current_time.weekday()
                time_stamp = weekdays[current_weekday] + " "
                time_stamp += current_time.strftime("%m-%d-%Y %H:%M:%S") + " "
                time_stamp += current_timezone
                kt = "Qmax"
                ts_qmax = float(main_window._pystog_inputs_collect[kt])
                f.write(f"# {len(x_list)}\n")
                f.write("# Pair Distribution Function (PDF)\n")
                f.write(f"# created: {time_stamp}\n")
                str_tmp = f"# comment: neutron, Qmax={ts_qmax}, "
                str_tmp += "Qdamp=0.017659, Qbroad=0.0191822\n"
                f.write(str_tmp)
                for count, r_val in enumerate(x_list):
                    if count == len(x_list) - 1:
                        f.write("{0:16.12F}{1:18.12F}".format(r_val,
                                                              y_list[count]))
                    else:
                        f.write("{0:16.12F}{1:18.12F}\n".format(r_val,
                                                                y_list[count]))

            main_window._pystog_output_files[file_name] = {"xlist": x_list, "ylist": y_list}
            file_list_tree.add_stog_data(file_name)

            continue

        file_tmp = os.path.join(main_window.output_folder,
                                "StoG",
                                file_name)
        try:
            file_in = open(file_tmp, "r")
        except FileNotFoundError:
            err_msg = f"[Error] S(Q) data file {file_tmp} not found. "
            err_msg += "Please check the output dir setting."
            print(err_msg)
            main_window.ui.statusbar.setStyleSheet("color: red")
            main_window.ui.statusbar.showMessage(
                "S(Q) file loading error, see the terminal for more info!",
                main_window.statusbar_display_time
            )
            return

        line = file_in.readline()
        line = file_in.readline()
        x_list = []
        y_list = []
        while line:
            line = file_in.readline()
            if line:
                if line.split()[1] != "nan":
                    x_list.append(float(line.split()[0]))
                    y_list.append(float(line.split()[1]))
        file_in.close()

        main_window._pystog_output_files[file_name] = {"xlist": x_list, "ylist": y_list}
        file_list_tree.add_stog_data(file_name)

    return True


def generate_final(main_window):
    x_vals_final = main_window._pystog_output_files[main_window._stem + "_rmc.gr"]["xlist"]
    y_vals_init = main_window._pystog_output_files[main_window._stem + "_rmc.gr"]["ylist"]
    y_vals_final = list()

    rcut_final = main_window._pystog_inputs_collect["RippleParams"][0]
    rmax_final = main_window._pystog_inputs_collect["RippleParams"][2]
    rmin_final = main_window._pystog_inputs_collect["RippleParams"][1]
    faber_ziman = float(main_window._pystog_inputs_collect["FaberZiman"])
    for count, item in enumerate(x_vals_final):
        if (item <= rcut_final) and (item >= rmax_final or item <= rmin_final):
            y_vals_final.append(-faber_ziman)
        else:
            y_vals_final.append(y_vals_init[count])
    final_file_name = main_window._stem + "_rmc_rr.gr"
    out_file = os.path.join(main_window.output_folder,
                            "StoG",
                            final_file_name)
    file_final_out = open(out_file, "w")
    file_final_out.write("{0:d}\n".format(len(x_vals_final)))
    file_final_out.write("# pystog output with Fourier ripples removed\n")
    for count, item in enumerate(x_vals_final):
        file_final_out.write("{0:10.4F}{1:15.6F}\n".format(item, y_vals_final[count]))
    file_final_out.close()

    main_window._pystog_output_files[final_file_name] = {
        "xlist": x_vals_final,
        "ylist": y_vals_final
    }
    main_window.postprocessing_ui_m.frame_filelist_tree.add_stog_data(final_file_name)

    final_file_pdffit = main_window._stem + "_rr_pdffit.gr"
    kt = "NumberDensity"
    rho_val = float(main_window._pystog_inputs_collect[kt])
    x_final_pdffit = x_vals_final
    y_final_pdffit = list()
    for count, item in enumerate(x_final_pdffit):
        yt = y_vals_final[count] * 4. * np.pi * item * rho_val / faber_ziman
        y_final_pdffit.append(yt)

    out_file = os.path.join(
        main_window.output_folder,
        "StoG",
        final_file_pdffit
    )
    with open(out_file, "w") as f:
        current_time = datetime.now()
        current_timezone = datetime.now().astimezone().strftime("%Z")
        current_weekday = current_time.weekday()
        time_stamp = weekdays[current_weekday] + " "
        time_stamp += current_time.strftime("%m-%d-%Y %H:%M:%S") + " "
        time_stamp += current_timezone
        kt = "Qmax"
        ts_qmax = float(main_window._pystog_inputs_collect[kt])
        f.write(f"# {len(x_final_pdffit)}\n")
        f.write("# Pair Distribution Function (PDF)\n")
        f.write(f"# created: {time_stamp}\n")
        str_tmp = f"# comment: neutron, Qmax={ts_qmax}, "
        str_tmp += "Qdamp=0.017659, Qbroad=0.0191822\n"
        kt = "FourierFilter"
        ft_sel = main_window._pystog_inputs_collect[kt]
        if ft_sel:
            kt = "Rmin"
            ft_rmin = float(main_window._pystog_inputs_collect[kt])
            str_tmp += f"# comment: Fourier filtered, rcut={ft_rmin} \n"
        str_tmp += "# comment: Ripple removed, "
        str_tmp += f"Rcutoff, 1st peak min, max = {rcut_final}, {rmin_final}, {rmax_final}\n"
        f.write(str_tmp)
        for count, r_val in enumerate(x_final_pdffit):
            if count == len(x_final_pdffit) - 1:
                f.write("{0:16.12F}{1:18.12F}".format(r_val,
                                                      y_final_pdffit[count]))
            else:
                f.write("{0:16.12F}{1:18.12F}\n".format(r_val,
                                                        y_final_pdffit[count]))

    main_window._pystog_output_files[final_file_pdffit] = {
        "xlist": x_final_pdffit,
        "ylist": y_final_pdffit
    }
    main_window.postprocessing_ui_m.frame_filelist_tree.add_stog_data(final_file_pdffit)
