from __future__ import (absolute_import, division, print_function, unicode_literals)

import os
import time
import numpy as np
import matplotlib.pyplot as plt

import mantid.simpleapi as ms

from addie.calibration.Calibration_plots import plot_delta_d_ttheta

path = os.path.dirname(os.path.realpath(__file__))
ms.LoadDetectorsGroupingFile(InputFile=os.path.join(path, 'Nom_group_detectors.xml'),
                             OutputWorkspace='NOM_group')
ms.LoadNexusProcessed(Filename=os.path.join(path, 'NOM_resolution.nxs'),
                      OutputWorkspace='NOM_res')

#test case with grouping workspace
f1 = plot_delta_d_ttheta('Nom_res',groupwkspc='Nom_group')
f1.show()

#test case without grouping workspace
f2 = plot_delta_d_ttheta('Nom_res')
f2.show()

time.sleep(5)
