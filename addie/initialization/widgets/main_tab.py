from qtpy.QtWidgets import QVBoxLayout
import os

from addie.utilities.general import get_ucams


IPYTHON_STARTUP_CODE = '''import numpy as np
from mantid.simpleapi import *
'''


def run(main_window=None):

    main_window.ucams = get_ucams()
    set_default_folder_path(main_window)


def set_default_folder_path(main_window):

    # set default folder path
    # Where the calibration_folder and characterization folder will be initialized
    # using instrument name...
    # this is very important when the instrument changed
    instrument_short_name = main_window.instrument["short_name"]
    config_calibration_folder = main_window.config_calibration_folder

    main_window.calibration_folder = os.path.join(config_calibration_folder["pre"],
                                                  instrument_short_name,
                                                  config_calibration_folder["post"])

    config_characterization_file = main_window.config_characterization_folder
    main_window.characterization_folder = os.path.join(config_characterization_file["pre"],
                                                       instrument_short_name,
                                                       config_characterization_file["post"])
