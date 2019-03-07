import six
import numpy as np
from mantid.simpleapi import mtd, LoadDiffCal, CalculateDIFC
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection


def PlotCalibration(group, cal, mask):

    CalculateDIFC(InputWorkspace=group, CalibrationWorkspace=cal, OutputWorkspace='A')
    CalculateDIFC(InputWorkspace=group, OutputWorkspace='B')
    offset = 1 - mtd['A']/mtd['B']

    #Accept either name or pointer to mask
    if isinstance(mask, six.string_types):
        mask = mtd[mask]

   #Calculate angles theta and phi from detector position.
   #Separate masked and unmasked detectors for plotting.
   #Offset values of unma]sked detectors are stored for plotting
    theta_array = []
    phi_array = []
    value_array = []
    masked_theta_array = []
    masked_phi_array = []
    info = offset.spectrumInfo()
    for idx, x in enumerate(info):
        pos = x.position
        theta =  np.arccos(pos[2] / pos.norm())
        phi = np.arctan2(pos[1], pos[0])
        if mask.dataY(idx):
            masked_theta_array.append(theta)
            masked_phi_array.append(phi)
        else:
            theta_array.append(theta)
            phi_array.append(phi)
            value_array.append(np.sum(offset.dataY(idx)))

    #Use the largest solid angle for circle radius
    sample_position = info.samplePosition()
    maximum_solid_angle = 0.0
    for idx in six.moves.xrange(info.size()):
        maximum_solid_angle = max(maximum_solid_angle, offset.getDetector(idx).solidAngle(sample_position))

    #Radius also includes a fudge factor to improve plotting.
    #May need to add finer adjustments on a per-instrument basis.
    #Small circles seem to alias less than rectangles.
    radius = maximum_solid_angle*8.0
    patches = []
    for x1, y1 in six.moves.zip(theta_array, phi_array):
        circle = Circle((x1, y1), radius)
        patches.append(circle)

    masked_patches = []
    for x1, y1 in six.moves.zip(masked_theta_array, masked_phi_array):
        circle = Circle((x1, y1), radius)
        masked_patches.append(circle)

    #Matplotlib requires this to be a Numpy array.
    colors = np.array(value_array)
    p = PatchCollection(patches)
    p.set_array(colors)
    p.set_clim(-0.1,0.1)
    p.set_edgecolor('face')

    fig, ax = plt.subplots()
    ax.add_collection(p)
    mp = PatchCollection(masked_patches)
    mp.set_facecolor('gray')
    mp.set_edgecolor('face')
    ax.add_collection(mp)
    fig.colorbar(p, ax=ax)
    ax.set_xlabel(r'$\phi$')
    ax.set_xlim(0.0,np.pi)
    ax.set_ylabel(r'$\theta$')
    ax.set_ylim(-np.pi,np.pi)
    return fig, ax


#Input for NOMAD
LoadDiffCal(InstrumentName='NOMAD',
            Filename='/SNS/NOM/shared/CALIBRATION/2019_1_1B_CAL/NOM_calibrate_d122825_2019_01_17.h5', WorkspaceName='NOM')
mask = mtd['NOM_mask']

#Input for POWGEN
#LoadDiffCal(InstrumentName='POWGEN',
#            Filename='/SNS/PG3/shared/CALIBRATION/2019_1_11A_CAL/PG3_PAC_d2817_2019_01_22.h5',
#            WorkspaceName='PG3')
#mask = mtd['PG3_mask']

fig, ax = PlotCalibration('NOM_group', 'NOM_cal', mask)
plt.show()
