import math
import numpy as np
from mantid.api import AnalysisDataService
try:
    from mantid.plots.datafunctions import get_spectrum    # mantid >4.2
except ImportError:
    from mantid.plots.helperfunctions import get_spectrum  # mantid <=4.2


def calculate_bank_angle(name):
    """ Calculate bank's angles (2theta) for each histogram
    :return: List of each histogram in banks angle
    """
    wksp = get_ws(name)

    angles = list()

    for wkspindex in range(wksp.getNumberHistograms()):
        instrument = wksp.getInstrument()
        sample_pos = instrument.getSample().getPos()
        source_pos = instrument.getSource().getPos()
        L1 = sample_pos - source_pos

        angle = wksp.getDetector(
            wkspindex).getPos().angle(L1) * 180. / math.pi
        angles.append(angle)
    return angles


def get_ws(name):
    name = str(name)
    assert AnalysisDataService.doesExist(
        name), 'Workspace "{}" does not exist.'.format(name)
    return AnalysisDataService.retrieve(name)


def get_ws_data(ws_name, wkspIndex=0, withDy=True):
    wksp = get_ws(ws_name)
    x, y, dy, _ = get_spectrum(wksp, wkspIndex, False,
                               withDy=withDy, withDx=False)
    return x, y, dy


def get_ws_unit(ws_name):
    """
    Find out the unit of the workspace
    """
    wksp = get_ws(ws_name)

    return wksp.getAxis(0).getUnit().unitID()


def get_y_range(ws_name, wkspindex=0):
    '''Returns the y - range for the selected index'''
    _, y, _ = get_ws_data(ws_name, wkspindex, withDy=False)
    return np.min(y), np.max(y)


def get_xy_range(ws_name, wkspindex=0):
    x, y, _ = get_ws_data(ws_name, wkspindex, withDy=False)
    return x[0], x[-1], np.min(y), np.max(y)
