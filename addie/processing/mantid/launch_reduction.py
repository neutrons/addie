import os
import json
import re

from addie.processing.mantid.master_table.master_table_exporter import TableFileExporter as MantidTableExporter


def run_mantid(parent):
    num_rows = parent.processing_ui.h3_table.rowCount()
    if num_rows <= 0:
        print("Cannot import empty table.")
        return

    exporter = MantidTableExporter(parent=parent)

    # write out the full table to disk
    # TODO make a class level name so it can be reused
    try:
        import shutil
        path = os.path.join(os.path.expanduser('~'), '.mantid', 'JSON_output')
        shutil.rmtree(path)
    except:
        pass

    full_reduction_filename = os.path.join(
        os.path.expanduser('~'), '.mantid', 'addie.json')
    print('writing out full table to "{}"'.format(full_reduction_filename))
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
                        if type(item_af) == list:
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

    parent.launch_job_manager_mts(job_name='MantidTotalScattering',
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
        cond1 = type(item) == int
        cond2 = type(item) == float
        if not (cond1 or cond2):
            return False
    return True


def final_validator(final_dict):
    must_keys = ["Facility", "Instrument", "Title", "Sample", "Normalization",
                 "Calibration", "Merging", "CacheDir", "OutputDir"]

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
        if type(final_dict["Sample"]["Runs"]) == str:
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
            if type(final_dict["Sample"]["Background"]["Runs"]) == str:
                bkg_run_num = re.split("-|,| ", final_dict["Sample"]["Background"]["Runs"])
                if not check_all_decimal(bkg_run_num):
                    log_error(2, '["Sample"]["Background"]["Runs"]')
                    return False
            else:
                log_error(2, '["Sample"]["Background"]["Runs"]')
                return False
            if type(final_dict["Sample"]["Background"]["Background"]) == dict:
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
                if type(final_dict["Normalization"]["Background"]["Runs"]) == str:
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
        if not type(final_dict["Sample"]["Material"]) == str:
            log_error(2, '["Sample"]["Material"]')
            return False
    else:
        log_error(1, '["Sample"]["Material"]')
    if "MassDensity" in final_dict["Sample"]:
        cond1 = final_dict["Sample"]["MassDensity"]
        cond2 = type(final_dict["Sample"]["MassDensity"]) == int
        cond3 = type(final_dict["Sample"]["MassDensity"]) == float
        if not (cond1 and (cond2 or cond3)):
            log_error(2, '["Sample"]["MassDensity"]')
            return False
    else:
        log_error(1, '["Sample"]["MassDensity"]')
    if "PackingFraction" in final_dict["Sample"]:
        cond1 = final_dict["Sample"]["PackingFraction"]
        cond2 = type(final_dict["Sample"]["PackingFraction"]) == int
        cond3 = type(final_dict["Sample"]["PackingFraction"]) == float
        if not (cond1 and (cond2 or cond3)):
            log_error(2, '["Sample"]["PackingFraction"]')
            return False
    else:
        log_error(1, '["Sample"]["PackingFraction"]')
    if "Geometry" in final_dict["Sample"]:
        if "Radius" in final_dict["Sample"]["Geometry"] and "Height" in final_dict["Sample"]["Geometry"]:
            cond1 = final_dict["Sample"]["Geometry"]["Radius"]
            cond2 = type(final_dict["Sample"]["Geometry"]["Radius"]) == int
            cond3 = type(final_dict["Sample"]["Geometry"]["Radius"]) == float
            if not (cond1 and (cond2 or cond3)):
                log_error(2, '["Sample"]["Geometry"]["Radius"]')
                return False
            cond1 = final_dict["Sample"]["Geometry"]["Height"]
            cond2 = type(final_dict["Sample"]["Geometry"]["Height"]) == int
            cond3 = type(final_dict["Sample"]["Geometry"]["Height"]) == float
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
        if type(final_dict["Normalization"]["Runs"]) == str:
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
            if type(final_dict["Normalization"]["Background"]["Runs"]) == str:
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
        if not type(final_dict["Normalization"]["Material"]) == str:
            log_error(2, '["Normalization"]["Material"]')
            return False
    else:
        log_error(1, '["Normalization"]["Material"]')
    if "MassDensity" in final_dict["Normalization"]:
        cond1 = final_dict["Normalization"]["MassDensity"]
        cond2 = type(final_dict["Normalization"]["MassDensity"]) == int
        cond3 = type(final_dict["Normalization"]["MassDensity"]) == float
        if not (cond1 and (cond2 or cond3)):
            log_error(2, '["Normalization"]["MassDensity"]')
            return False
    else:
        log_error(1, '["Normalization"]["MassDensity"]')
    if "PackingFraction" in final_dict["Normalization"]:
        cond1 = final_dict["Normalization"]["PackingFraction"]
        cond2 = type(final_dict["Normalization"]["PackingFraction"]) == int
        cond3 = type(final_dict["Normalization"]["PackingFraction"]) == float
        if not (cond1 and (cond2 or cond3)):
            log_error(2, '["Normalization"]["PackingFraction"]')
            return False
    else:
        log_error(1, '["Normalization"]["PackingFraction"]')
    if "Geometry" in final_dict["Normalization"]:
        if "Radius" in final_dict["Normalization"]["Geometry"] and "Height" in final_dict["Normalization"]["Geometry"]:
            cond1 = final_dict["Normalization"]["Geometry"]["Radius"]
            cond2 = type(final_dict["Normalization"]["Geometry"]["Radius"]) == int
            cond3 = type(final_dict["Normalization"]["Geometry"]["Radius"]) == float
            if not (cond1 and (cond2 or cond3)):
                log_error(2, '["Normalization"]["Geometry"]["Radius"]')
                return False
            cond1 = final_dict["Normalization"]["Geometry"]["Height"]
            cond2 = type(final_dict["Normalization"]["Geometry"]["Height"]) == int
            cond3 = type(final_dict["Normalization"]["Geometry"]["Height"]) == float
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
        if type(final_dict["Merging"]["QBinning"]) == list:
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
