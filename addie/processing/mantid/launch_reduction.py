import json
import numpy as np
import os
import re
import subprocess
from h5py import File
from scipy.signal import argrelextrema
from qtpy.QtWidgets import QFileDialog, QApplication  # , QMessageBox

from addie.processing.mantid.master_table.master_table_exporter import \
    TableFileExporter as MantidTableExporter
from mantid.simpleapi import \
    CreateWorkspace, \
    FitPeaks, \
    Fit, \
    GetIPTS, \
    mtd, \
    DeleteWorkspace
from pystog.stog import StoG


def extractor(nexus_file: str, wks_name: str, out_dir: str, dir_name=None):
    '''Method for extracting workspace from nexus file.
    '''

    def extract_from_input_file(input_file):
        wks_list = list()
        data = File(input_file, "r")
        for name, _ in data.items():
            index = os.path.join(name, "title").replace("\\", "/")
            wks_list.append(str(data[index][()][0]).split("'")[1].split("'")[0])

        title = wks_list[0]

        for name, _ in data.items():
            index = os.path.join(name, "title").replace("\\", "/")
            if data[index][(0)].decode("UTF-8") == title:
                ypath = os.path.join("/", name,
                                     "workspace", "values").replace("\\", "/")
                break

        return wks_list, len(data[ypath][()])

    if dir_name:
        nexus_file = os.path.join(dir_name, nexus_file)

    wks_list, num_banks = extract_from_input_file(nexus_file)

    if wks_name not in wks_list:
        return False

    _, tail = os.path.split(nexus_file)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    stog = StoG(**{"Outputs": {"StemName": out_dir + "/"}})
    all_files = list()

    for i in range(num_banks):
        stog.read_nexus_file_by_bank(nexus_file, i, wks_name)
        output_file = "{}_bank{}".format(tail.split(".")[0], i + 1)
        os.rename(os.path.join(out_dir, wks_name + "_bank" + str(i) + ".dat"),
                  os.path.join(out_dir, output_file + ".dat"))
        all_files.append(output_file + ".dat")

    return (all_files, num_banks)


def config_merge_config(num_banks: int, input_json: dict):
    '''Method for configuring merge config dictionary.
    '''

    merge_config_loaded = input_json

    merge_config = dict()
    if "RemoveBkg" not in merge_config_loaded.keys():
        merge_config["RemoveBkg"] = True
    else:
        merge_config["RemoveBkg"] = merge_config_loaded["RemoveBkg"]
    for i in range(num_banks):
        bank = str(i + 1)
        merge_config[bank] = {}
        if bank in merge_config_loaded.keys():
            if "Qmin" in merge_config_loaded[bank].keys():
                merge_config[bank]["Qmin"] = merge_config_loaded[bank]["Qmin"]
            else:
                merge_config[bank]["Qmin"] = "0.0"
            if "Qmax" in merge_config_loaded[bank].keys():
                merge_config[bank]["Qmax"] = merge_config_loaded[bank]["Qmax"]
            else:
                merge_config[bank]["Qmax"] = "0.0"
            if "Yoffset" in merge_config_loaded[bank].keys():
                merge_config[bank]["Yoffset"] = merge_config_loaded[bank]["Yoffset"]
            else:
                merge_config[bank]["Yoffset"] = "0.0"
            if "Yscale" in merge_config_loaded[bank].keys():
                merge_config[bank]["Yscale"] = merge_config_loaded[bank]["Yscale"]
            else:
                merge_config[bank]["Yscale"] = "1.0"
        else:
            merge_config[bank]["Qmin"] = "0.0"
            merge_config[bank]["Qmax"] = "0.0"
            merge_config[bank]["Yoffset"] = "0.0"
            merge_config[bank]["Yscale"] = "1.0"

    return merge_config


def config_pystog_config(input_json: dict, out_dir: str, stem_name: str):
    '''Method for configure the input pystog config.
    '''

    pystog_config = input_json

    merged_file = os.path.join(os.path.dirname(out_dir),
                               "SofQ_merged",
                               stem_name + "_merged.sq")
    list_tmp = pystog_config["Files"]
    list_tmp[0]["Filename"] = merged_file
    pystog_config["Files"] = list_tmp

    pystog_config["Outputs"]["StemName"] = os.path.join(out_dir, stem_name)

    return pystog_config


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
            if bank == 4:
                x_left = []
                x_max_init = np.arange(x_bank[0], x_bank[-1], 0.1)
                for item in x_max_init:
                    x_left.append(str(item - 0.1))
                    x_left.append(str(item + 0.1))
                x_max = [str(item) for item in x_max_init]
            else:
                x_max = argrelextrema(y_bank, np.greater, order=1)
                x_left = []
                for item in x_max[0]:
                    x_left.append(str(x_bank[item] - 0.1))
                    x_left.append(str(x_bank[item] + 0.1))
                x_max = [str(x_bank[item]) for item in x_max[0]]

            centers = ','.join(x_max)
            boundary = ','.join(x_left)

            ws_tmp = CreateWorkspace(x_bank, y_bank)

            FitPeaks(InputWorkspace=ws_tmp,
                     StartWorkspaceIndex=0,
                     StopWorkspaceIndex=0,
                     PeakCenters=centers,
                     FitWindowBoundaryList=boundary,
                     PeakFunction="Gaussian",
                     BackgroundType="Quadratic",
                     FitFromRight=True,
                     HighBackground=False,
                     OutputWorkspace="ws_tmp_out",
                     OutputPeakParametersWorkspace="ws_tmp_param_out",
                     FittedPeaksWorkspace="ws_tmp_fit")

            x_bkg_pt = []
            y_bkg_pt = []
            for i in range(mtd['ws_tmp_param_out'].rowCount()):
                a0_tmp = mtd['ws_tmp_param_out'].row(i)["A0"]
                a1_tmp = mtd['ws_tmp_param_out'].row(i)["A1"]
                a2_tmp = mtd['ws_tmp_param_out'].row(i)["A2"]

                x_tmp = mtd['ws_tmp_param_out'].row(i)["PeakCentre"]
                y_tmp = a0_tmp + a1_tmp * x_tmp + a2_tmp * x_tmp**2.

                x_bkg_pt.append(x_tmp)
                y_bkg_pt.append(y_tmp)

            naughty_region_x = []
            naughty_region_y = []
            for count, x_e_tmp in enumerate(x_bank):
                if x_e_tmp > float(x_max[-1]):
                    naughty_region_x.append(x_e_tmp)
                    naughty_region_y.append(y_bank[count])
            bottom_tmp = argrelextrema(np.asarray(naughty_region_y), np.less, order=1)
            for item in bottom_tmp[0]:
                x_bkg_pt.append(naughty_region_x[item])
                y_bkg_pt.append(naughty_region_y[item])

            x_min = argrelextrema(np.asarray(y_bkg_pt), np.less, order=1)
            y_min = [y_bkg_pt[item] for item in x_min[0]]
            x_min = [x_bkg_pt[item] for item in x_min[0]]

            min_min = argrelextrema(np.asarray(y_min), np.less, order=1)
            y_min_min = [y_min[item] for item in min_min[0]]
            x_min_min = [x_min[item] for item in min_min[0]]

            ws_real_bkg = CreateWorkspace(x_min_min, y_min_min)

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

            y_bkg = [a_init - b_init * np.exp(-c_used * item**2.) for item in x_bank]
            for i in range(len(x_bank)):
                if all_range[bank][0] <= x_bank[i] < all_range[bank][1]:
                    x_out.append(x_bank[i])
                    y_out.append(y_bank[i] - y_bkg[i])
                    y_bkg_out.append(y_bkg[i])

    # Remove all workspaces
    DeleteWorkspace(ws_tmp)
    DeleteWorkspace("ws_tmp_param_out")
    DeleteWorkspace("ws_tmp_fit")
    DeleteWorkspace("ws_real_bkg")
    DeleteWorkspace("ws_tmp_out")
    DeleteWorkspace("ws_real_bkg_fitted_Workspace")
    DeleteWorkspace("ws_real_bkg_fitted_Parameters")
    DeleteWorkspace("ws_real_bkg_fitted_NormalisedCovarianceMatrix")

    return x_out, y_out, y_bkg_out


def merge_banks(all_files: list, out_dir: str, merge_config: dict, stem_name: str):

    banks_x = []
    banks_y = []

    for bank, file_name in enumerate(all_files):
        banks_x.append([])
        banks_y.append([])

        with open(os.path.join(out_dir, file_name), "r") as f:
            lines = f.readlines()[2:]
        for line in lines:
            banks_x[bank].append(float(line.split()[0]))
            banks_y[bank].append(float(line.split()[1]))

    num_banks = len(all_files)

    qmin_list = list()
    qmax_list = list()
    qmax_max = 0.
    qmax_max_bank = 0
    valid_region = False
    for bank in range(num_banks):
        qmin_tmp = merge_config[str(bank + 1)]['Qmin']
        qmax_tmp = merge_config[str(bank + 1)]['Qmax']
        if qmin_tmp.strip() == "" or qmax_tmp.strip() == "":
            qmin_list.append(0.)
            qmax_list.append(0.)
        else:
            qmin_tmp = float(qmin_tmp)
            qmax_tmp = float(qmax_tmp)
            if qmin_tmp == qmax_tmp:
                qmin_list.append(0.)
                qmax_list.append(0.)
            elif qmin_tmp > qmax_tmp:
                msg_p1 = f"[Error] Qmax smaller than Qmin for bank-{bank+1}. "
                msg_p2 = "Please input valid values and try again."
                print(msg_p1 + msg_p2)
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
        return

    remove_bkg = merge_config["RemoveBkg"]
    if not remove_bkg:
        x_merged = list()
        y_merged = list()

        for bank in range(num_banks):
            yoffset_tmp = merge_config[str(bank + 1)]['Yoffset']
            yscale_tmp = merge_config[str(bank + 1)]['Yscale']
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
        if num_banks == 6:
            qmax_bkg_est = [25., 25., 25., 25., 40., 0.]
            fudge_factor = [1., 1., 1., 0.7, 0.7, 1.]
        elif num_banks == 1:
            qmax_bkg_est = [40.]
            fudge_factor = [0.7]
        else:
            qmax_bkg_est = [25. for _ in range(num_banks)]
            qmax_bkg_est[-1] = 0.
            qmax_bkg_est[-2] = 40.
            fudge_factor = [1. for _ in range(num_banks)]
        for bank in range(num_banks):
            bank_range.append([qmin_list[bank], qmax_list[bank]])
            yoffset_tmp = merge_config[str(bank + 1)]['Yoffset']
            yscale_tmp = merge_config[str(bank + 1)]['Yscale']
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

        x_merged_init, y_merged_init, y_bkg_out = bkg_finder(all_data, bank_range, fudge_factor)
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

    merged_data_ref = stem_name + '_merged.sq'

    merge_data_out = os.path.join(out_dir, merged_data_ref)
    merge_f = open(merge_data_out, "w")
    merge_f.write("{0:10d}\n\n".format(len(x_merged)))
    for i, item in enumerate(x_merged):
        merge_f.write("{0:10.3F}{1:20.6F}\n".format(item, y_merged[i]))
    merge_f.close()

    return True


def run_mantid(parent):
    num_rows = parent.processing_ui.h3_table.rowCount()
    if num_rows <= 0:
        print("Cannot import empty table.")
        return

    exporter = MantidTableExporter(parent=parent)

    selected_item = parent.processing_ui.comboBox.currentText()
    if selected_item == "Merge":
        # for row in range(num_rows):
        #     dictionary, activate = exporter.retrieve_row_info(row)
        #     if activate is True:
        #         if row == 0:
        #             sam_title = dictionary["Title"]
        #         else:
        #             if dictionary["Title"] != sam_title:
        #                 msgBox = QMessageBox()
        #                 msgBox.setIcon(QMessageBox.Warning)
        #                 msgBox.setText("Different sample title found for selected rows! Continue?")
        #                 msgBox.setWindowTitle("Warning!")
        #                 msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        #                 returnValue = msgBox.exec()
        #                 if returnValue == QMessageBox.Cancel:
        #                     return

        m_config_j, _ = QFileDialog.getOpenFileName(parent,
                                                    "Select Merge Config File",
                                                    parent.output_folder,
                                                    "JSON (*.json)")

        if not m_config_j:
            return
        else:
            with open(m_config_j, "r") as f:
                try:
                    m_json = json.load(f)
                except json.decoder.JSONDecodeError as err:
                    err_msg = "Provided JSON file could not be loaded."
                    print("\n[Error] " + err_msg)
                    print("[Error] " + str(err))
                    parent.ui.statusbar.setStyleSheet("color: red")
                    parent.ui.statusbar.showMessage(
                        err_msg, parent.statusbar_display_time)
                    QApplication.restoreOverrideCursor()
                    return

        print("[Info] Merging banks for all the selected rows...")
        for row in range(num_rows):
            dictionary, activate = exporter.retrieve_row_info(row)
            if activate is True:
                sam_title = dictionary["Title"]
                check_file = os.path.join(parent.output_folder, "SofQ", f"{sam_title}.nxs")
                if not os.path.isfile(check_file):
                    instr_name = dictionary["Instrument"].upper()
                    run_num_tmp = int(dictionary["Sample"]["Runs"].split("-")[0])
                    ipts_dir = GetIPTS(Instrument=instr_name, RunNumber=run_num_tmp)
                    check_file = os.path.join(ipts_dir, "shared",
                                              "autoreduce", "multi_banks_summed",
                                              "SofQ", f"{sam_title}.nxs")
                    if not os.path.isfile(check_file):
                        print(f"[Warning] No reduced SofQ data found for row-{row}.")
                        print(f"[Warning] Check the directory {os.path.dirname(check_file)}")
                        continue
                # Extract row
                m_out_dir = os.path.join(os.path.dirname(os.path.dirname(check_file)),
                                         "SofQ_merged")
                extractor_out = extractor(nexus_file=check_file,
                                          wks_name="SQ_banks_normalized",
                                          out_dir=m_out_dir)
                if extractor_out:
                    merge_config = config_merge_config(num_banks=extractor_out[1],
                                                       input_json=m_json)
                    m_config_f = os.path.join(m_out_dir,
                                              f"{sam_title}_merge.json")
                    if not os.path.isfile(m_config_f):
                        with open(m_config_f, "w") as f:
                            json.dump(merge_config, f, indent=2)
                    m_return = merge_banks(all_files=extractor_out[0],
                                           out_dir=m_out_dir,
                                           merge_config=merge_config,
                                           stem_name=sam_title)
                    if m_return:
                        proc_msg = f"Banks merged successfully for row-{row}"
                    else:
                        proc_msg = f"Merging banks failed for row-{row}"
                    print("[Info] " + proc_msg)
                else:
                    continue

        parent.ui.statusbar.setStyleSheet("color: blue")
        parent.ui.statusbar.showMessage(
            "Jon done for all selected rows. Check the terminal for status of each row",
            parent.statusbar_display_time)
        print("[Info] All selected rows processed. Check the status above status for each row")

        QApplication.restoreOverrideCursor()

        return
    elif selected_item == "PyStoG":
        # for row in range(num_rows):
        #     dictionary, activate = exporter.retrieve_row_info(row)
        #     if activate is True:
        #         if row == 0:
        #             sam_title = dictionary["Title"]
        #         else:
        #             if dictionary["Title"] != sam_title:
        #                 msgBox = QMessageBox()
        #                 msgBox.setIcon(QMessageBox.Warning)
        #                 msgBox.setText("Different sample title found for selected rows! Continue?")
        #                 msgBox.setWindowTitle("Warning!")
        #                 msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        #                 returnValue = msgBox.exec()
        #                 if returnValue == QMessageBox.Cancel:
        #                     return

        p_config_j, _ = QFileDialog.getOpenFileName(parent,
                                                    "Select PyStoG Config File",
                                                    parent.output_folder,
                                                    "JSON (*.json)")

        if not p_config_j:
            return
        else:
            with open(p_config_j, "r") as f:
                try:
                    p_json = json.load(f)
                except json.decoder.JSONDecodeError as err:
                    err_msg = "Provided JSON file could not be loaded."
                    print("\n[Error] " + err_msg)
                    print("[Error] " + str(err))
                    parent.ui.statusbar.setStyleSheet("color: red")
                    parent.ui.statusbar.showMessage(
                        err_msg, parent.statusbar_display_time)
                    QApplication.restoreOverrideCursor()
                    return

        print("[Info] PyStoG for all the selected rows in progress...")
        for row in range(num_rows):
            dictionary, activate = exporter.retrieve_row_info(row)
            if activate is True:
                sam_title = dictionary["Title"]
                check_file = os.path.join(parent.output_folder,
                                          "SofQ_merged",
                                          f"{sam_title}_merged.sq")
                if not os.path.isfile(check_file):
                    print(f"[Warning] No merged SofQ data found for row-{row}.")
                    print(f"[Warning] Check the directory {os.path.dirname(check_file)}")
                    continue

                p_out_dir = os.path.join(parent.output_folder,
                                         "StoG")
                if not os.path.exists(p_out_dir):
                    os.mkdir(p_out_dir)

                pystog_config = config_pystog_config(input_json=p_json,
                                                     out_dir=p_out_dir,
                                                     stem_name=sam_title)
                p_config_f = os.path.join(p_out_dir,
                                          f"{sam_title}_pystog.json")
                with open(p_config_f, "w") as f:
                    json.dump(pystog_config, f, indent=2)
                cwd = os.getcwd()
                os.chdir(p_out_dir)
                subprocess.run(["pystog_cli", "--json", f"{sam_title}_pystog.json"])
                os.chdir(cwd)
                success_msg = f"PyStoG job done for row-{row}. If failed, see info above."
                print("[Info] " + success_msg)

        parent.ui.statusbar.setStyleSheet("color: blue")
        parent.ui.statusbar.showMessage(
            "Job done for all selected rows. Check the terminal for status of each row",
            parent.statusbar_display_time)
        QApplication.restoreOverrideCursor()
        print("[Info] All selected rows processed. Check the status above status for each row")

        return
    else:
        pass

    # write out the full table to disk
    # TODO make a class level name so it can be reused
    try:
        import shutil
        path = os.path.join(os.path.expanduser('~'), '.mantid', 'JSON_output')
        shutil.rmtree(path)
    except:
        pass

    _table_file = os.path.join(parent.output_folder, "exp.json")
    _parent_out_dir = parent.current_folder
    _table_file_current = os.path.join(_parent_out_dir, "exp.json")
    exporter.export(_table_file)
    exporter.export(_table_file_current)

    parent.ui.statusbar.setStyleSheet("color: blue")
    parent.ui.statusbar.showMessage(
        "Table has been exported in file {}".format(_table_file),
        parent.statusbar_display_time)

    all_commands = list()
    all_files = list()
    for row in range(num_rows):
        dictionary, activate = exporter.retrieve_row_info(row)
        if activate is True:
            try:
                filename = os.path.join(os.path.expanduser('~'),
                                        '.mantid',
                                        'JSON_output',
                                        dictionary['Title'] + '_' + str(row) + '.json')
                exporter.export(filename, row)
                print("Row", row, "Successfully output to", filename)
            except KeyError:
                print('[Error] Processing row-', row)
                log_error(1, 'Title')
                return
            with open(filename) as json_file:
                data_tmp = json.load(json_file)
            dict_out_tmp = {}
            container_type = ""
            for key, item in data_tmp.items():
                if "Sample" in key:
                    sample_tmp = {}
                    for key_s, item_s in item.items():
                        if "Density" not in key_s:
                            if "Material" in key_s:
                                string_tmp = item_s.replace("(", "").replace(")", "")
                                sample_tmp[key_s] = string_tmp
                            else:
                                sample_tmp[key_s] = item_s
                            if "Geometry" in key_s:
                                known_shape = ["PAC03", "PAC06", "PAC08",
                                               "PAC10", "QuartzTube03"]
                                if item_s["Shape"] in known_shape:
                                    shape_tmp = "Cylinder"
                                    container_type = item_s["Shape"]
                                else:
                                    shape_tmp = item_s["Shape"]
                                geo_dict_tmp = {}
                                for key_tmp in item_s:
                                    geo_dict_tmp[key_tmp] = item_s[key_tmp]
                                geo_dict_tmp["Shape"] = shape_tmp
                                sample_tmp[key_s] = geo_dict_tmp
                        else:
                            try:
                                sample_tmp["MassDensity"] = float(item_s["MassDensity"])
                            except KeyError:
                                sample_tmp["MassDensity"] = ""
                    dict_out_tmp[key] = sample_tmp
                elif "Normalization" in key or "Normalisation" in key:
                    van_tmp = {}
                    for key_v, item_v in item.items():
                        if "Density" not in key_v:
                            if "Material" in key_v:
                                string_tmp = item_v.replace("(", "").replace(")", "")
                                van_tmp[key_v] = string_tmp
                            else:
                                van_tmp[key_v] = item_v
                        else:
                            try:
                                van_tmp["MassDensity"] = float(item_v["MassDensity"])
                            except KeyError:
                                van_tmp["MassDensity"] = ""
                    dict_out_tmp[key] = van_tmp
                elif "Merging" in key:
                    merging_tmp = {}
                    for key_m, item_m in item.items():
                        if "QBinning" in key_m:
                            qbin_tmp = [float(entry_tmp) for entry_tmp in item_m]
                            merging_tmp[key_m] = qbin_tmp
                        else:
                            merging_tmp[key_m] = item_m
                    dict_out_tmp[key] = merging_tmp
                elif "AlignAndFocusArgs" in key:
                    af_tmp = {}
                    for key_af, item_af in item.items():
                        if isinstance(item_af, list):
                            try:
                                list_tmp = [float(entry_tmp) for entry_tmp in item_af]
                            except ValueError:
                                list_tmp = item_af
                            af_tmp[key_af] = list_tmp
                        else:
                            try:
                                entry_tmp = float(item_af)
                            except ValueError:
                                entry_tmp = item_af
                            af_tmp[key_af] = entry_tmp
                    dict_out_tmp[key] = af_tmp
                else:
                    dict_out_tmp[key] = item
            if container_type:
                dict_out_tmp["Environment"] = {"Name": "InAir",
                                               "Container": container_type}

            if final_validator(dict_out_tmp):
                if "CacheDir" in dict_out_tmp:
                    del dict_out_tmp["CacheDir"]
                filename_to_run = os.path.join(os.path.expanduser('~'),
                                               '.mantid',
                                               'JSON_output',
                                               'running_tmp_' + str(row) + '.json')
                with open(filename_to_run, 'w') as outfile:
                    json.dump(dict_out_tmp, outfile, indent=2)
                _script_to_run = "bash /SNS/NOM/shared/scripts/mantidtotalscattering/run_mts.sh " + filename_to_run
                all_commands.append(_script_to_run.split())
                all_files.append(filename_to_run)

    limit = 4

    if len(all_commands) > limit:
        all_commands = list()
        num_runs = len(all_files)
        chunk_size = num_runs // limit
        left_over = num_runs - (limit - 1) * chunk_size
        for i in range(limit):
            command_tmp = ""
            if i < limit - 1:
                for j in range(i * chunk_size, (i + 1) * chunk_size):
                    command_tmp += (" " + all_files[j])
            else:
                for j in range(left_over):
                    command_tmp += (" " + all_files[i * chunk_size + j])
            command_tmp = "bash /SNS/NOM/shared/scripts/mantidtotalscattering/run_mts_all.sh" + command_tmp
            all_commands.append(command_tmp.split())

    parent.launch_job_manager_mts(job_name='MTS',
                                  all_commands=all_commands)


def log_error(type_err, key):
    if type_err == 1:
        print("[Error] No '{0:s}' key found! Please check and rerun.".format(key))
    elif type_err == 2:
        print("[Error] No valid entry for '{0:s}' key! Please check and rerun.".format(key))


def check_all_decimal(input_list):
    input_list_tmp = [item for item in input_list if item]
    for item in input_list_tmp:
        if not item.isdecimal():
            return False
    return True


def check_all_number(input_list):
    for item in input_list:
        cond1 = isinstance(item, int)
        cond2 = isinstance(item, float)
        if not (cond1 or cond2):
            return False
    return True


def final_validator(final_dict):
    must_keys = ["Facility", "Instrument", "Title", "Sample", "Normalization",
                 "Calibration", "Merging", "OutputDir"]

    # Check all necessary keys and their non-empty entry.
    for key in must_keys:
        if key == "Normalization":
            if key not in final_dict.keys() and "Normalisation" not in final_dict.keys():
                log_error(1, key)
                return False
            else:
                if not (final_dict[key] or final_dict["Normalisation"]):
                    log_error(2, key)
                    return False
        else:
            if key not in final_dict.keys():
                log_error(1, key)
                return False
            else:
                if not final_dict[key]:
                    log_error(2, key)
                    return False

    # Check 'Sample' entry.
    if "Runs" in final_dict["Sample"]:
        if isinstance(final_dict["Sample"]["Runs"], str):
            run_num_tmp = re.split("-|,| ", final_dict["Sample"]["Runs"])
            if not check_all_decimal(run_num_tmp):
                log_error(2, '["Sample"]["Run"]')
                return False
        else:
            log_error(2, '["Sample"]["Run"]')
            return False
    else:
        log_error(1, '["Sample"]["Run"]')
        return False
    if "Background" in final_dict["Sample"]:
        if "Runs" in final_dict["Sample"]["Background"] and "Background" in final_dict["Sample"]["Background"]:
            if isinstance(final_dict["Sample"]["Background"]["Runs"], str):
                bkg_run_num = re.split("-|,| ", final_dict["Sample"]["Background"]["Runs"])
                if not check_all_decimal(bkg_run_num):
                    log_error(2, '["Sample"]["Background"]["Runs"]')
                    return False
            else:
                log_error(2, '["Sample"]["Background"]["Runs"]')
                return False
            if isinstance(final_dict["Sample"]["Background"]["Background"], dict):
                if "Runs" in final_dict["Sample"]["Background"]["Background"]:
                    bkg_run_num = re.split("-|,| ", final_dict["Sample"]["Background"]["Background"]["Runs"])
                    if not check_all_decimal(bkg_run_num):
                        log_error(2, '["Sample"]["Background"]["Background"]')
                        return False
                else:
                    log_error(2, '["Sample"]["Background"]["Background"]')
                    return False
            else:
                log_error(2, '["Sample"]["Background"]["Background"]')
                return False
        else:
            if "Runs" not in final_dict["Sample"]["Background"]:
                log_error(1, '["Sample"]["Background"]["Runs"]')
            if "Background" not in final_dict["Sample"]["Background"]:
                log_error(1, '["Sample"]["Background"]["Background"]')
            return False
    else:
        if "Background" in final_dict["Normalization"]:
            if "Runs" in final_dict["Normalization"]["Background"]:
                if isinstance(final_dict["Normalization"]["Background"]["Runs"], str):
                    bkg_run_num = re.split("-|,| ", final_dict["Normalization"]["Background"]["Runs"])
                    if not check_all_decimal(bkg_run_num):
                        log_error(2, '["Normalization"]["Background"]["Runs"]')
                        return False
                else:
                    log_error(2, '["Normalization"]["Background"]["Runs"]')
                    return False
            else:
                log_error(1, '["Normalization"]["Background"]["Runs"]')
                return False
        else:
            log_error(1, '["Normalization"]["Background"]')
            return False
        log_error(1, '["Sample"]["Background"]')
        return False
    if "Material" in final_dict["Sample"]:
        if not isinstance(final_dict["Sample"]["Material"], str):
            log_error(2, '["Sample"]["Material"]')
            return False
    else:
        log_error(1, '["Sample"]["Material"]')
    if "MassDensity" in final_dict["Sample"]:
        cond1 = final_dict["Sample"]["MassDensity"]
        cond2 = isinstance(final_dict["Sample"]["MassDensity"], int)
        cond3 = isinstance(final_dict["Sample"]["MassDensity"], float)
        if not (cond1 and (cond2 or cond3)):
            log_error(2, '["Sample"]["MassDensity"]')
            return False
    else:
        log_error(1, '["Sample"]["MassDensity"]')
    if "PackingFraction" in final_dict["Sample"]:
        cond1 = final_dict["Sample"]["PackingFraction"]
        cond2 = isinstance(final_dict["Sample"]["PackingFraction"], int)
        cond3 = isinstance(final_dict["Sample"]["PackingFraction"], float)
        if not (cond1 and (cond2 or cond3)):
            log_error(2, '["Sample"]["PackingFraction"]')
            return False
    else:
        log_error(1, '["Sample"]["PackingFraction"]')
    if "Geometry" in final_dict["Sample"]:
        if "Radius" in final_dict["Sample"]["Geometry"] and "Height" in final_dict["Sample"]["Geometry"]:
            cond1 = final_dict["Sample"]["Geometry"]["Radius"]
            cond2 = isinstance(final_dict["Sample"]["Geometry"]["Radius"], int)
            cond3 = isinstance(final_dict["Sample"]["Geometry"]["Radius"], float)
            if not (cond1 and (cond2 or cond3)):
                log_error(2, '["Sample"]["Geometry"]["Radius"]')
                return False
            cond1 = final_dict["Sample"]["Geometry"]["Height"]
            cond2 = isinstance(final_dict["Sample"]["Geometry"]["Height"], int)
            cond3 = isinstance(final_dict["Sample"]["Geometry"]["Height"], float)
            if not (cond1 and (cond2 or cond3)):
                log_error(2, '["Sample"]["Geometry"]["Height"]')
                return False
        else:
            if "Radius" not in final_dict["Sample"]["Geometry"]:
                log_error(1, '["Sample"]["Geometry"]["Radius"]')
            if "Height" not in final_dict["Sample"]["Geometry"]:
                log_error(1, '["Sample"]["Geometry"]["Height"]')
            return False
    else:
        log_error(1, '["Sample"]["Geometry"]')
        return False

    # Check 'Normalization' entry.
    if "Runs" in final_dict["Normalization"]:
        if isinstance(final_dict["Normalization"]["Runs"], str):
            run_num_tmp = re.split("-|,| ", final_dict["Normalization"]["Runs"])
            if not check_all_decimal(run_num_tmp):
                log_error(2, '["Normalization"]["Run"]')
                return False
        else:
            log_error(2, '["Normalization"]["Run"]')
            return False
    else:
        log_error(1, '["Normalization"]["Run"]')
        return False
    if "Background" in final_dict["Normalization"]:
        if "Runs" in final_dict["Normalization"]["Background"]:
            if isinstance(final_dict["Normalization"]["Background"]["Runs"], str):
                bkg_run_num = re.split("-|,| ", final_dict["Normalization"]["Background"]["Runs"])
                if not check_all_decimal(bkg_run_num):
                    log_error(2, '["Normalization"]["Background"]["Runs"]')
                    return False
            else:
                log_error(2, '["Normalization"]["Background"]["Runs"]')
                return False
        else:
            log_error(1, '["Normalization"]["Background"]["Runs"]')
            return False
    else:
        log_error(1, '["Normalization"]["Background"]')
        return False
    if "Material" in final_dict["Normalization"]:
        if not isinstance(final_dict["Normalization"]["Material"], str):
            log_error(2, '["Normalization"]["Material"]')
            return False
    else:
        log_error(1, '["Normalization"]["Material"]')
    if "MassDensity" in final_dict["Normalization"]:
        cond1 = final_dict["Normalization"]["MassDensity"]
        cond2 = isinstance(final_dict["Normalization"]["MassDensity"], int)
        cond3 = isinstance(final_dict["Normalization"]["MassDensity"], float)
        if not (cond1 and (cond2 or cond3)):
            log_error(2, '["Normalization"]["MassDensity"]')
            return False
    else:
        log_error(1, '["Normalization"]["MassDensity"]')
    if "PackingFraction" in final_dict["Normalization"]:
        cond1 = final_dict["Normalization"]["PackingFraction"]
        cond2 = isinstance(final_dict["Normalization"]["PackingFraction"], int)
        cond3 = isinstance(final_dict["Normalization"]["PackingFraction"], float)
        if not (cond1 and (cond2 or cond3)):
            log_error(2, '["Normalization"]["PackingFraction"]')
            return False
    else:
        log_error(1, '["Normalization"]["PackingFraction"]')
    if "Geometry" in final_dict["Normalization"]:
        if "Radius" in final_dict["Normalization"]["Geometry"] and "Height" in final_dict["Normalization"]["Geometry"]:
            cond1 = final_dict["Normalization"]["Geometry"]["Radius"]
            cond2 = isinstance(final_dict["Normalization"]["Geometry"]["Radius"], int)
            cond3 = isinstance(final_dict["Normalization"]["Geometry"]["Radius"], float)
            if not (cond1 and (cond2 or cond3)):
                log_error(2, '["Normalization"]["Geometry"]["Radius"]')
                return False
            cond1 = final_dict["Normalization"]["Geometry"]["Height"]
            cond2 = isinstance(final_dict["Normalization"]["Geometry"]["Height"], int)
            cond3 = isinstance(final_dict["Normalization"]["Geometry"]["Height"], float)
            if not (cond1 and (cond2 or cond3)):
                log_error(2, '["Normalization"]["Geometry"]["Height"]')
                return False
        else:
            if "Radius" not in final_dict["Normalization"]["Geometry"]:
                log_error(1, '["Normalization"]["Geometry"]["Radius"]')
            if "Height" not in final_dict["Normalization"]["Geometry"]:
                log_error(1, '["Normalization"]["Geometry"]["Height"]')
            return False
    else:
        log_error(1, '["Normalization"]["Geometry"]')
        return False

    # Check "Merging" entry
    if "QBinning" in final_dict["Merging"]:
        if isinstance(final_dict["Merging"]["QBinning"], list):
            cond1 = len(final_dict["Merging"]["QBinning"]) == 3
            cond2 = check_all_number(final_dict["Merging"]["QBinning"])
            if not (cond1 and cond2):
                log_error(2, '["Merging"]["QBinning"]')
                return False
        else:
            log_error(2, '["Merging"]["QBinning"]')
            return False
    else:
        log_error(1, '["Merging"]["QBinning"]')
        return False

    return True
