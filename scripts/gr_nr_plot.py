from __future__ import (absolute_import, division, print_function, unicode_literals)

import time
import mantid.simpleapi as ms
# from mantid import plots
# import matplotlib.pyplot as plt

# import numpy as np

import os
from addie.calibration.Calibration_plots import plot_gr_nr

path = os.path.dirname(os.path.realpath(__file__))
ms.LoadNexusProcessed(os.path.join(path, 'diamond_gr.nxs'),
                      OutputWorkspace='gr')
ms.LoadNexusProcessed(os.path.join(path, 'diamond_nr.nxs'),
                      OutputWorkspace='nr')
f1=plot_gr_nr('gr','nr',expected_n=[4,16,28])
f1.show()
time.sleep(5)
