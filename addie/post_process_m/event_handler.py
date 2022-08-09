import os
import json
import subprocess
from qtpy.QtWidgets import QFileDialog, QMessageBox
from h5py import File
import addie.utilities.workspaces
from pystog.stog import StoG


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


def open_and_load_workspaces(main_window):
    workspace_files = open_workspaces(main_window)

    if workspace_files is None:
        return
    else:
        load_workspaces(main_window, workspace_files)


def extract_button(main_window):
    nxs = main_window._inputFile
    banks = int(main_window.postprocessing_ui_m.label_numBanks.text())
    wks = main_window.postprocessing_ui_m.frame_workspaces_table.get_current_workspace()
    out = main_window.output_folder

    if not os.path.exists(out):
        os.makedirs(out)

    files = extractor(main_window, nxs, banks, wks, out)

    initialize_banks(main_window, banks)

    file_list = main_window.postprocessing_ui_m.frame_filelist_tree
    file_list.reset_files_tree()
    file_list.set_workspace(wks)
    file_list.add_raw_data(files)
    initiate_bank_data(main_window, files, wks)


def extractor(main_window, nexus_file: str, num_banks: int, wks_name: str, out_dir: str):
    stog = StoG(**{"Outputs": {"StemName": out_dir + "/"}})
    head, tail = os.path.split(nexus_file)
    main_window._stem = tail.split('.')[0]
    all_files = list()

    for i in range(num_banks):
        stog.read_nexus_file_by_bank(nexus_file, i, wks_name)
        output_file = "{}_bank{}".format(tail.split(".")[0], i + 1)
        all_files.append(output_file)

    return all_files


def initiate_bank_data(main_window, item_list, workspace):
    for item in item_list:
        current_bank = int(item[-1])
        output_file = main_window.output_folder + "/" + workspace + "_bank" + str(int(item[len(item) - 1]) - 1) + ".dat"
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
                    x_list.append(float(line.split()[0]))
                    y_list.append(float(line.split()[1]))
        file_in.close()
        main_window._bankDict[current_bank]['xList'] = x_list
        main_window._bankDict[current_bank]['yList'] = y_list


def plot(main_window, item_list, banks, workspace, mode):
    for item in item_list:
        if mode == 'Merged':
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


def merge_banks(main_window):
    banks_x = []
    banks_y = []
    for bank in main_window._bankDict:
        banks_x.append(main_window._bankDict[bank]['xList'])
        banks_y.append(main_window._bankDict[bank]['yList'])

    x_merged = list()
    y_merged = list()

    for bank in range(len(main_window._bankDict)):
        qmin_tmp = main_window._bankDict[bank + 1]['Qmin']
        qmax_tmp = main_window._bankDict[bank + 1]['Qmax']
        yoffset_tmp = main_window._bankDict[bank + 1]['Yoffset']
        yscale_tmp = main_window._bankDict[bank + 1]['Yscale']
        if qmin_tmp.strip() == "" or qmax_tmp.strip() == "":
            continue
        else:
            qmin_tmp = float(qmin_tmp)
            qmax_tmp = float(qmax_tmp)
            if qmin_tmp == qmax_tmp:
                continue
            elif qmin_tmp > qmax_tmp:
                print(f"[Error] Qmax smaller than Qmin for bank-{bank+1}. Please input valid values and try again.")
                return
            else:
                pass
        if yoffset_tmp.strip() == "":
            yoffset_tmp = 0.0
        if yscale_tmp.strip() == "":
            yscale_tmp = 1.0
        yoffset_tmp = float(yoffset_tmp)
        yscale_tmp = float(yscale_tmp)
        for i, x_val in enumerate(banks_x[bank]):
            if qmin_tmp <= x_val < qmax_tmp:
                x_merged.append(x_val)
                y_merged.append(banks_y[bank][i] / yscale_tmp + yoffset_tmp)

    file_list = main_window.postprocessing_ui_m.frame_filelist_tree
    merged_data_ref = main_window._stem + '_merged.sq'
    main_window._merged_data[main_window._stem] = {'Name': merged_data_ref, 'XList': x_merged, 'YList': y_merged}

    file_list.add_merged_data(merged_data_ref)

    initiate_stog_data(main_window)


def save_file_raw(main_window, file_name):
    x_bank = main_window._bankDict[int(file_name[-1])]['xList']
    y_bank = main_window._bankDict[int(file_name[-1])]['yList']
    save_directory = QFileDialog.getSaveFileName(main_window, 'Save Bank',
                                                 main_window.output_folder + '/' + file_name + '.dat')
    with open(save_directory[0], 'w') as new_file:
        new_file.write(str(len(x_bank)) + '\n')
        new_file.write('#\n')
        for i in range(len(x_bank)):
            new_file.write(str(x_bank[i]) + ' ' + str(y_bank[i]) + '\n')


def save_file_merged(main_window, auto=False):
    if auto:
        save_directory = main_window.output_folder
        save_file = main_window._stem + '_merged.sq'

        main_window._full_merged_path = save_directory + '/' + save_file

    else:
        save_directory_user = QFileDialog.getSaveFileName(main_window, 'Save Merged File',
                                                          main_window.output_folder + '/' + main_window._stem + '_merged.sq',
                                                          '*.sq')
                                                # QFileDialog.ShowDirsOnly
                                                # | QFileDialog.DontResolveSymlinks)
        # save_file = main_window._stem + '_merged.sq'
        save_file = save_directory_user[0].split('/')[-1]
        # full_path = save_directory + '/' + save_file
        main_window._full_merged_path = save_directory_user[0]
        save_directory = save_directory_user[0]

    x_merged = main_window._merged_data[main_window._stem]['XList']
    y_merged = main_window._merged_data[main_window._stem]['YList']

    with open(main_window._full_merged_path, 'w') as new_file:
        new_file.write(str(len(x_merged)) + '\n')
        new_file.write('#\n')
        for i in range(len(x_merged)):
            new_file.write(str(x_merged[i]) + ' ' + str(y_merged[i]) + '\n')


def save_file_stog(main_window, file_name):
    save_file = QFileDialog.getSaveFileName(main_window, 'Save StoG File',
                                            main_window.output_folder + '/' + file_name, '*.sq;;*.fq;;*.gr;;All (*.*)')
    save_directory = save_file[0]

    x_stog = main_window._pystog_output_files[file_name]["xlist"]
    y_stog = main_window._pystog_output_files[file_name]["ylist"]

    with open(save_directory, 'w') as new_file:
        new_file.write(str(len(x_stog)) + '\n')
        new_file.write('#\n')
        for i in range(len(x_stog)):
            new_file.write(str(x_stog[i]) + ' ' + str(y_stog[i]) + '\n')


# TODO: Add checking of inputs
def initiate_stog_data(main_window):
    pystog_inputs = main_window._pystog_inputs_collect

    # TODO: Qmin, Qmax logic
    pystog_inputs["Qmin"] = 0.0
    pystog_inputs["Qmax"] = 35.0
    pystog_inputs["Yoffset"] = main_window.postprocessing_ui_m.lineEdit_Yoffset_stog.text()
    pystog_inputs["Yscale"] = main_window.postprocessing_ui_m.lineEdit_Yscale_stog.text()
    pystog_inputs["Qoffset"] = main_window.postprocessing_ui_m.lineEdit_Qoffset.text()
    pystog_inputs["Rmax"] = str(main_window.postprocessing_ui_m.doubleSpinBox_Rmax.value())
    pystog_inputs["Rstep"] = str(main_window.postprocessing_ui_m.doubleSpinBox_Rstep.value())
    pystog_inputs["NumberDensity"] = main_window.postprocessing_ui_m.lineEdit_numberDensity.text()
    pystog_inputs["FaberZiman"] = main_window.postprocessing_ui_m.lineEdit_faberZiman.text()
    pystog_inputs["Lorch"] = main_window.postprocessing_ui_m.buttonGroup_Lorch.checkedButton().text() == 'Yes'
    pystog_inputs["FourierFilter"] = main_window.postprocessing_ui_m.buttonGroup_FF.checkedButton().text() == 'Yes'
    pystog_inputs["Rmin"] = str(main_window.postprocessing_ui_m.doubleSpinBox_Rmin.value())
    pystog_inputs["RippleParams"] = main_window.postprocessing_ui_m.lineEdit_rippleParams.text()


def set_stog_values(main_window):
    pystog_inputs = main_window._pystog_inputs_collect
    pystog_inputs["Qmin"] = 0.0
    pystog_inputs["Qmax"] = 35.0
    pystog_inputs["Yoffset"] = main_window.postprocessing_ui_m.lineEdit_Yoffset_stog.text()
    pystog_inputs["Yscale"] = main_window.postprocessing_ui_m.lineEdit_Yscale_stog.text()
    pystog_inputs["Qoffset"] = main_window.postprocessing_ui_m.lineEdit_Qoffset.text()
    pystog_inputs["Rmax"] = str(main_window.postprocessing_ui_m.doubleSpinBox_Rmax.value())
    pystog_inputs["Rstep"] = str(main_window.postprocessing_ui_m.doubleSpinBox_Rstep.value())
    pystog_inputs["NumberDensity"] = main_window.postprocessing_ui_m.lineEdit_numberDensity.text()
    pystog_inputs["FaberZiman"] = main_window.postprocessing_ui_m.lineEdit_faberZiman.text()
    pystog_inputs["Lorch"] = main_window.postprocessing_ui_m.buttonGroup_Lorch.checkedButton().text() == 'Yes'
    pystog_inputs["FourierFilter"] = main_window.postprocessing_ui_m.buttonGroup_FF.checkedButton().text() == 'Yes'
    pystog_inputs["Rmin"] = str(main_window.postprocessing_ui_m.doubleSpinBox_Rmin.value())
    pystog_inputs["RippleParams"] = main_window.postprocessing_ui_m.lineEdit_rippleParams.text()


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
            value = float(stog_dict[key])
            if not isinstance(value, float):
                return False
    return True


def execute_stog(main_window):
    pystog_inputs = main_window._pystog_inputs_collect
    if not check_verify_stog(pystog_inputs):
        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setText("Some StoG data or parameters are incorrect. StoG was not run.")
        msg.exec()
        return

    json_format = convert_json(main_window, pystog_inputs)
    with open('pystog_input.json', 'w') as pystog_file:
        json.dump(json_format, pystog_file)
    print("The json file is created")
    subprocess.run(["pystog_cli", "--json", "pystog_input.json"])
    add_stog_data(main_window)
    generate_final(main_window)


def convert_json(main_window, stog_dict):
    json_dict = dict()

    json_dict["Files"] = [{"Filename": main_window._full_merged_path,
                           "ReciprocalFunction": "S(Q)",
                           "Qmin": stog_dict["Qmin"],
                           "Qmax": stog_dict["Qmax"],
                           "Y": {"Offset": float(stog_dict["Yoffset"]),
                                 "Scale": float(stog_dict["Yscale"])},
                           "X": {"Offset": float(stog_dict["Qoffset"])}}]

    json_dict["RealSpaceFunction"] = "G(r)"

    json_dict["NumberDensity"] = float(stog_dict["NumberDensity"])
    json_dict["Rmax"] = float(stog_dict["Rmax"])
    json_dict["Rpoints"] = int(float(stog_dict["Rmax"])/float(stog_dict["Rstep"]))
    if(stog_dict["FourierFilter"]):
        json_dict["FourierFilter"] = {"Cutoff": float(stog_dict["Rmin"])}
    json_dict["<b_coh>^2"] = float(stog_dict["FaberZiman"])
    json_dict["LorchFlag"] = stog_dict["Lorch"]
    output = main_window.output_folder + "/" + main_window._stem
    json_dict["Outputs"] = {"StemName": output}
    return json_dict


def add_stog_data(main_window):
    file_list_tree = main_window.postprocessing_ui_m.frame_filelist_tree

    stem = main_window._stem

    data_sq = stem + ".sq"
    data_gr = stem + ".gr"
    data_ft_sq = stem + "_ft.sq"
    data_ft_gr = stem + "_ft.gr"
    data_rmc_fq = stem + "_rmc.fq"
    data_rmc_gr = stem + "_rmc.gr"

    data_list = [data_sq, data_gr, data_ft_sq, data_ft_gr, data_rmc_fq, data_rmc_gr]

    for file_name in data_list:
        file_in = open(main_window.output_folder + "/" + file_name, "r")
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


def generate_final(main_window):
    x_vals_final = main_window._pystog_output_files[main_window._stem + "_rmc.gr"]["xlist"]
    y_vals_init = main_window._pystog_output_files[main_window._stem + "_rmc.gr"]["ylist"]
    y_vals_final = list()

    rcut_final = main_window._pystog_inputs_collect["RippleParams"][0]
    rmax_final = main_window._pystog_inputs_collect["RippleParams"][2]
    rmin_final = main_window._pystog_inputs_collect["RippleParams"][1]
    print(f"rcut: {rcut_final}, rmax: {rmax_final}, rmin: {rmin_final}")
    faber_ziman = float(main_window._pystog_inputs_collect["FaberZiman"])
    for count, item in enumerate(x_vals_final):
        if (item <= rcut_final) and (item >= rmax_final or item <= rmin_final):
            y_vals_final.append(faber_ziman)
        else:
            y_vals_final.append(y_vals_init[count])
    final_file_name = main_window._stem + "_rmc_rr.gr"
    file_final_out = open(main_window.output_folder + "/" + final_file_name, "w")
    file_final_out.write("{0:d}\n".format(len(x_vals_final)))
    file_final_out.write("# pystog output with Fourier ripples removed\n")
    for count, item in enumerate(x_vals_final):
        file_final_out.write("{0:10.4F}{1:15.6F}\n".format(item, y_vals_final[count]))
    file_final_out.close()

    main_window._pystog_output_files[final_file_name] = {"xlist": x_vals_final, "ylist": y_vals_final}
    main_window.postprocessing_ui_m.frame_filelist_tree.add_stog_data(final_file_name)
