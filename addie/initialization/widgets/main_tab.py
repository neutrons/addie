from qtpy.QtWidgets import QVBoxLayout
import os
from addie.utilities.general import get_ucams
from mantidqt.widgets.jupyterconsole import InProcessJupyterConsole

IPYTHON_STARTUP_CODE = '''import numpy as np
from mantid.simpleapi import *
'''


def run(main_window=None):

    # frame_dockWidget_ipython
    temp_layout = QVBoxLayout()
    main_window.ui.frame_dockWidget_ipython.setLayout(temp_layout)
    main_window.ui.dockWidget_ipython = InProcessJupyterConsole(main_window, startup_code=IPYTHON_STARTUP_CODE)
    temp_layout.addWidget(main_window.ui.dockWidget_ipython)

    main_window.ui.splitter_3.setStyleSheet("""
                                            QSplitter::handle {
                                            image: url(':/MPL Toolbar/splitter_icon.png');
                                            }
                                            """)

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
