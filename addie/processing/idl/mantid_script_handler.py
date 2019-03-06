from __future__ import (absolute_import, division, print_function)


class MantidScriptHandler(object):

    script = None

    def __init__(self, parameters=None, run=None):

        script = "SNSPowderReduction( Filename = '{}',\n \
        MaxChunkSize = {}, \n \
        PreserveEvents = {}, \n \
        PushDataPositive = '{}', \n \
        CalibrationFile = '{}', \n \
        CharacterizationRunsFile = '{}', \n \
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
        FinalDataUnits = '{}')".format(run,
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
                                       parameters['final_data_units'])

        self.script = script
