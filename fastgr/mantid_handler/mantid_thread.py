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

        print("[LOG] Running Mantid script:")
        print("SNSPowderReduction( Filename = '{}',\n \
                            MaxChunkSize = {}, \n \
                            PreserveEvents = {}, \n \
                            PushDataPositive = '{}', \n \
                            CalibrationFile = '{}', \n \
                            CharacterizationRunsFile = {}, \n \
                            BackgroundNumber = '{}', \n \
                            VanadiumNumber = '{}', \n \
                            VanadiumBackgroundNumber = '{}', \n \
                            ExpIniFileName = '{}', \n \
                            RemovePromptPulseWidth = {}, \n \
                            ResampleX = {}, \n \
                            BinInDSpace = {}, \n \
                            FilterBadPulses = {}, \n \
                            CropWavelengthMin = {}, \n \
                            CropWavelengthMax = {}, \n \
                            SaveAs = '{}', \n \
                            OutputDirectory = '{}', \n \
                            StripVanadiumPeaks = {}, \n \
                            VanadiumRadius = {}, \n \
                            NormalizeByCurrent = {}, \n \
                            FinalDataUnits = '{}')".format( self.runs,
                            parameters['max_chunk_size'],
                            parameters['preserve_events'],
                            parameters['push_data_positive'],
                            parameters['calibration_file'],
                            parameters['characterization_file'],
                            parameters['background_number'],
                            parameters['vanadium_number'],
                            parameters['vanadium_background_number'],
                            parameters['exp_ini_filename'],
                            parameters['remove_prompt_pulse_width'],
                            parameters['resamplex'],
                            parameters['bin_in_d_space'],
                            parameters['filter_bad_pulses'],
                            parameters['crop_wavelength_min'],
                            parameters['crop_wavelength_max'],
                            parameters['save_as'],
                            parameters['output_directory'],
                            parameters['strip_vanadium_peaks'],
                            parameters['vanadium_radius'],
                            parameters['normalize_by_current'],
                            parameters['final_data_units']))

        print(type(self.runs))
        print(type(parameters['max_chunk_size']))
        print(type(parameters['preserve_events']))
        print(type(parameters['push_data_positive']))
        print(type(parameters['calibration_file']))
        print(type(parameters['characterization_file']))
        print(type(parameters['background_number']))
        print(type(parameters['vanadium_number']))
        print(type(parameters['vanadium_background_number']))
        print(type(parameters['exp_ini_filename']))
        print(type(int(parameters['remove_prompt_pulse_width'])))
        print(type(parameters['resamplex']))
        print(type(parameters['bin_in_d_space']))
        print(type(int(parameters['filter_bad_pulses'])))
        print(type(float(parameters['crop_wavelength_min'])))
        print(type(float(parameters['crop_wavelength_max'])))
        print(type(parameters['save_as']))
        print(type(parameters['output_directory']))
        print(type(parameters['strip_vanadium_peaks']))
        print(type(parameters['vanadium_radius']))
        print(type(parameters['normalize_by_current']))
        print(type(parameters['final_data_units']))

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
                            StripVanadiumPeaks = parameters['strip_vanadium_peaks'],
                            VanadiumRadius = parameters['vanadium_radius'],
                            NormalizeByCurrent = parameters['normalize_by_current'],
                            FinalDataUnits = parameters['final_data_units'])

