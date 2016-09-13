from PyQt4 import QtCore
import os

from mantid.simpleapi import *
import mantid


class MantidThread(QtCore.QThread):
    
    def setup(self, runs=None, parameters=None):
        self.runs = runs
        self.parameters = parameters
        
    def run(self):
        parameters = self.parameters
        
        SNSPowderReduction( Filename = self.runs,
                            MaxChunkSize = parameters['max_chunk_size'],
                            PreserveEvents = parameters['preserve_events'],
                            PushDataPositive = parameters['push_data_positive'],
                            CalibrationFile = parameters['calibration_file'],
                            CharacterizationRunsFile = parameters['characterization_file'],
                            BackgroundNumber = parameters['background_number'],
                            VanadiumNumber = parameters['vanadium_number'],
                            VanadiumBackgroundNumber = parameters['vanadium_background_number'],
                            ExpIniFileName = parameters['exp_ini_filename'],
                            RemovePromptPulseWidth = int(parameters['remove_prompt_pulse_width']),
                            ResampleX = parameters['resamplex'],
                            BinInDSpace = parameters['bin_in_d_space'],
                            FilterBadPulses = int(parameters['filter_bad_pulses']),
                            CropWavelengthMin = float(parameters['crop_wavelength_min']),
                            CropWavelengthMax = float(parameters['crop_wavelength_max']),
                            SaveAs = parameters['save_as'],
                            OutputDirectory = parameters['output_directory'],
                            StripVanadiumPeaks = parameters['strip_vanadium_peak'],
                            VanadiumRadius = parameters['vanadium_radius'],
                            NormalizeByCurrent = parameters['normalize_by_current'],
                            FinalDataUnits = parameters['final_data_units'])

