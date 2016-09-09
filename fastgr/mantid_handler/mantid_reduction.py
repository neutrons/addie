class MantidReduction(object):

    _max_chunk_size = 8
    _preserve_events = True
    _push_data_positive = '/AddMinimum'
    _remove_prompt_pulse_width = 50
    _bin_in_d_space = True
    _filter_bad_pulses = 25
    _save_as = 'gsas fullprof topas'
    _strip_vanadium_peaks = True
    _normalize_by_current = True
    _final_data_units = 'dSpacing'
    
    _filename = ''
    _calibration_file = ''
    _characterization_runs_file = ''
    _background_number = ''
    _vanadium_number = ''
    _vanadium_background_number = ''
    _resamplex = None
    _crop_wavelength_min = None
    _corp_wavelength_max = None
    _output_directory = ''
    _vanadium_radius = None
    
    def __init__(self, parent=None):
        self.parent = parent
        self.collect_parameters()
        
    def collect_parameters(self):
        
        # collect filename
        pass
        
    def run(self):
        pass