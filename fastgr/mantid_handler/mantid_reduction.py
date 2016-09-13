import os

import fastgr.step2_handler.table_handler


class GlobalMantidReduction(object):
    
    parameters = {'max_chunk_size': 8,
                  'preserve_events': True,
                  'exp_ini_filename': 'exp.ini',
                  'push_data_positive': 'AddMinimum',
                  'remove_prompt_pulse_width': 50,
                  'bin_in_d_space': True,
                  'filter_bad_pulses': 25,
                  'save_as': 'gsas fullprof topas',
                  'strip_vanadium_peaks': True,
                  'normalize_by_current': True,
                  'final_data_units': 'dSpacing',
                  'runs': [],
                  'calibration_file': '',
                  'characterization_file': '',
                  'background_number': '',
                  'vanadium_number': '',
                  'vanadium_background_number': '',
                  'resamplex': None,
                  'crop_wavelength_min': None,
                  'corp_wavelength_max': None,
                  'output_directory':  '',
                  'vanadium_radius': None}
    
    def __init__(self, parent=None):
        self.parent = parent
        self.collect_parameters()
        self.collect_runs()
        self.create_output_folder()
        
    def collect_parameters(self):
        _parameters = self.parameters
        
        _current_folder = self.parent.current_folder
        _exp_ini = os.path.join(_current_folder, _parameters['exp_ini_filename'])
        _parameters['exp_ini_filename'] = str(_exp_ini)
        
        _parameters['calibration_file'] = str(self.parent.ui.mantid_calibration_value.text())
        _parameters['characterization_file'] = str(self.parent.ui.mantid_characterization_value.text())
        _parameters['background_number'] = str(self.collect_background_number())
        _parameters['vanadium_number'] = str(self.parent.ui.vanadium.text())
        _parameters['vanadium_background_number'] = str(self.parent.ui.vanadium_background.text())
        _parameters['resamplex'] = str(self.parent.ui.mantid_number_of_bins.text())
        _parameters['crop_wavelength_min'] = str(self.parent.ui.mantid_min_crop_wavelength.text())
        _parameters['crop_wavelength_max'] = str(self.parent.ui.mantid_max_crop_wavelength.text())
        _parameters['output_directory'] = str(self.parent.ui.mantid_output_directory_value.text())
        _parameters['vanadium_radius'] = float(str(self.parent.ui.mantid_vanadium_radius.text()))
        self.parameters = _parameters
        
    def collect_runs(self):
        o_table_handler = fastgr.step2_handler.table_handler.TableHandler(parent = self.parent)
        o_table_handler.retrieve_list_of_selected_rows()
        list_of_selected_row = o_table_handler.list_selected_row
        runs = []
        for _row in list_of_selected_row:
            _runs = _row['runs']
            runs.append(_runs)
        self.parameters['runs'] = runs

    def collect_background_number(self):
        if self.parent.ui.background_yes.isChecked():
            return str(self.parent.ui.background_line_edit.text())
        else:
            return str(self.parent.ui.background_no_field.text())
        
    def run(self):
        for index, runs in enumerate(self.parameters['runs']):
            _o_mantid = self.parent._mantid_thread_array[index]
            _o_mantid.setup(runs = runs, parameters = self.parameters)
            _o_mantid.run()
            
    def create_output_folder(self):
        output_folder = self.parameters['output_directory']
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
