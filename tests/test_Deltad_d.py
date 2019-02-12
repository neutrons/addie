from __future__ import (absolute_import, division, print_function, unicode_literals)

# import mantid algorithms, numpy and matplotlib
sys.path.append('../Calibration')
import mantid.simpleapi as ms
import time
import matplotlib.pyplot as plt
from Calibration_plots import plot_delta_d_ttheta
import numpy as np

#ms.LoadNexusProcessed(Filename='NOM_group.nxs', OutputWorkspace='NOM_group')
ms.LoadDetectorsGroupingFile(InputFile='Nom_group_detectors.xml',OutputWorkspace='NOM_group')
ms.LoadNexusProcessed(Filename='NOM_resolution.nxs', OutputWorkspace='NOM_res')

#test case with grouping workspace
f1 = plot_delta_d_ttheta('Nom_res',groupwkspc='Nom_group')
f1.show()

#test case without grouping workspace
f2 = plot_delta_d_ttheta('Nom_res')
f2.show()

time.sleep(5)
