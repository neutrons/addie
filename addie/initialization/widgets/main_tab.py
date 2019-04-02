from qtpy.QtWidgets import QVBoxLayout

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

