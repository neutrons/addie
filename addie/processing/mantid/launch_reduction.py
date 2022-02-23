import os
import traceback
import json

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
        path = os.path.join(os.path.expanduser('~'),'.mantid' ,'JSON_output')
        shutil.rmtree(path)
    except:
        pass

    full_reduction_filename = os.path.join(
        os.path.expanduser('~'), '.mantid', 'addie.json')
    print('writing out full table to "{}"'.format(full_reduction_filename))
    for row in range(num_rows):
        dictionary,activate = exporter.retrieve_row_info(row)
        if activate is True:
            filename = os.path.join(os.path.expanduser('~'),'.mantid' ,'JSON_output',dictionary['Title'] +'_'+ str(row) + '.json')
            exporter.export(filename,row)
            print("Row",row,"Successfully output to",filename)
            with open(filename) as json_file:
                data_tmp = json.load(json_file)
            dict_out_tmp = {}
            container_type=""
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
                            sample_tmp["MassDensity"] = float(item_s["MassDensity"])
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
                            van_tmp["MassDensity"] = float(item_v["MassDensity"])
                    dict_out_tmp[key] = van_tmp
                else:
                    dict_out_tmp[key] = item
            if container_type:
                dict_out_tmp["Environment"] = { "Name": "InAir",
                                                "Container": container_type}
            filename_to_run = os.path.join(os.path.expanduser('~'),'.mantid' ,'JSON_output', 'running_tmp.json')
            with open(filename_to_run, 'w') as outfile:
                json.dump(dict_out_tmp, outfile, indent=2)
            _script_to_run = "bash /SNS/NOM/shared/scripts/mantidtotalscattering/run_mts.sh " + filename_to_run
            parent.launch_job_manager(job_name='MantidTotalScattering',
                                      script_to_run=_script_to_run)
