from __future__ import (absolute_import, division, print_function, unicode_literals)

# import mantid algorithms, numpy and matplotlib
import time
import mantid.simpleapi as ms
from mantid import plots
import matplotlib.pyplot as plt

import numpy as np

import sys
sys.path.append('../Calibration')
from Calibration_plots import plot_gr_nr
    #f1.show()
#if __name__=="__main__":
ms.LoadNexusProcessed('diamond_gr.nxs',OutputWorkspace='gr')
ms.LoadNexusProcessed('diamond_nr.nxs',OutputWorkspace='nr')
f1=plot_gr_nr('gr','nr',expected_n=[4,16,28])
f1.show()
time.sleep(5)
