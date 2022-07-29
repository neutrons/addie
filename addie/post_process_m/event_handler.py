import os
from qtpy.QtWidgets import QFileDialog
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

    files = extractor(nxs, banks, wks, out)

    initialize_banks(main_window, banks)

    file_list = main_window.postprocessing_ui_m.frame_filelist_tree
    file_list.reset_files_tree()
    file_list.load_data(files, wks)


def extractor(nexus_file: str, num_banks: int, wks_name: str, out_dir: str):
    stog = StoG(**{"Outputs": {"StemName": out_dir + "/"}})

    head, tail = os.path.split(nexus_file)
    all_files = list()

    for i in range(num_banks):
        stog.read_nexus_file_by_bank(nexus_file, i, wks_name)
        output_file = "{}_bank{}".format(tail.split(".")[0], i + 1)
        all_files.append(output_file)

    return all_files


def plot(main_window, bank_list, banks, workspace):
    for bank in bank_list:
        output_file = main_window.output_folder + "/" + workspace + "_bank" + str(int(bank[len(bank) - 1]) - 1) + ".dat"
        main_window.postprocessing_ui_m.ppm_view.plot_bank(bank, workspace, output_file)


def clear_canvas(main_window):
    main_window.postprocessing_ui_m.ppm_view.canvas_reset()


def change_bank(main_window):
    current_bank = int(main_window.postprocessing_ui_m.comboBox_banks.currentText())
    bank_dict = main_window._bankDict
    if bank_dict is not None:
        q_min = bank_dict[current_bank]["Qmin"]
        q_max = bank_dict[current_bank]["Qmax"]
        y_offset = bank_dict[current_bank]["Yoffset"]
        y_scale = bank_dict[current_bank]["Yscale"]
        main_window.postprocessing_ui_m.doubleSpinBox_Qmin.setValue(q_min)
        main_window.postprocessing_ui_m.doubleSpinBox_Qmax.setValue(q_max)
        main_window.postprocessing_ui_m.lineEdit_Yoffset.setText(y_offset)
        main_window.postprocessing_ui_m.lineEdit_Yscale.setText(y_scale)


# initialize a dictionary holding data about a bank (starts at default)
def initialize_banks(main_window, banks):
    bank_dict = dict()
    for bank in range(banks):

        # bank holds in order: Qmin, Qmax, Yoffset, Yscale
        bank_dict[bank + 1] = {'Qmin': 0.0, 'Qmax': 0.0, 'Yoffset': '0.0', 'Yscale': '1.0'}

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
        bank_dict[current_bank]["Qmin"] = q_min
        bank_dict[current_bank]["Qmax"] = q_max
        bank_dict[current_bank]["Yoffset"] = y_offset
        bank_dict[current_bank]["Yscale"] = y_scale


def merge_banks(main_window):
    pass
