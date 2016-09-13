import fastgr.step2_handler.table_handler


class MantidReduction(object):
    ''' One reduction for each row selected '''

    _filename = ''




class GlobalMantidReduction(object):
    
    parameters = {'_max_chunk_size': 8,
                  '_preserve_events': True,
                  '_push_data_positive': '/AddMinimum',
                  '_remove_prompt_pulse_width': 50,
                  '_bin_in_d_space': True,
                  '_filter_bad_pulses': 25,
                  '_save_as': 'gsas fullprof topas',
                  '_strip_vanadium_peaks': True,
                  '_normalize_by_current': True,
                  '_final_data_units': 'dSpacing',
                  '_runs': [],
                  '_calibration_file': '',
                  '_characterization_file': '',
                  '_background_number': '',
                  '_vanadium_number': '',
                  '_vanadium_background_number': '',
                  '_resamplex': None,
                  '_crop_wavelength_min': None,
                  '_corp_wavelength_max': None,
                  '_output_directory':  '',
                  '_vanadium_radius': None}
    
    def __init__(self, parent=None):
        self.parent = parent
        self.collect_parameters()
        self.collect_runs()
        
    def collect_parameters(self):
        _parameters = self.parameters
        
        _parameters['_calibration_file'] = str(self.parent.ui.mantid_calibration_value.text())
        _parameters['_characterization_file'] = str(self.parent.ui.mantid_characterization_value.text())
        _parameters['_background_number'] = self.collect_background_number()
        _parameters['_vanadium_number'] = str(self.parent.ui.vanadium.text())
        _parameters['_vanadium_background_number'] = str(self.parent.ui.vanadium_background.text())
        _parameters['_resamplex'] = str(self.parent.ui.mantid_number_of_bins.text())
        _parameters['_crop_wavelength_min'] = str(self.parent.ui.mantid_min_crop_wavelength.text())
        _parameters['_crop_wavelength_max'] = str(self.parent.ui.mantid_max_crop_wavelength.text())
        _parameters['_output_directory'] = str(self.parent.ui.mantid_output_directory_value.text())
        _parameters['_vanadium_radius'] = str(self.parent.ui.mantid_vanadium_radius.text())
        self.parameters = _parameters
        
    def collect_runs(self):
        o_table_handler = fastgr.step2_handler.table_handler.TableHandler(parent = self.parent)
        o_table_handler.retrieve_list_of_selected_rows()
        list_of_selected_row = o_table_handler.list_selected_row
        runs = []
        for _row in list_of_selected_row:
            _runs = _row['runs']
            runs.append(_runs)
        self.parameters['_runs'] = runs

    def collect_background_number(self):
        if self.parent.ui.background_yes.isChecked():
            return str(self.parent.ui.background_line_edit.text())
        else:
            return str(self.parent.ui.background_no_field.text())
        
    def run(self):
        pass
        