from __future__ import (absolute_import, division, print_function, unicode_literals)

# import mantid algorithms, numpy and matplotlib
import mantid.simpleapi as ms
import matplotlib.pyplot as plt
import numpy as np


def plot_gr_nr(gr_wksp,nr_wksp,xlims=(0,10),nrylims=(0,30),expected_n=None):
    """
    plots the g(r) workspace (gr_wksp) and coordination number, n(r) (nr_wksp)
    xlims is a tuple (min,max) and its default is (0,10) in units of Angstrom
    nrylims is a tuple (min,max) and its default is (0,30)
    expected_n is a list of expected coordination numbers.  A horizontal line will be plotted
          for each value given.  If none then no line will be plotted. default is None
     returns a handle to the figure
    """
    gr_h=ms.mtd[gr_wksp]
    nr_h=ms.mtd[nr_wksp]
    f1,ax1=plt.subplots(subplot_kw={'projection':'mantid'})
    ax1.plot(gr_h)
    ax1.set_ylabel('g(r)')
    #ax2=ax1.twinx()
    ax2=ax1._make_twin_axes(sharex=ax1,projection='mantid')
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position('right')
    ax2.yaxis.set_offset_position('right')
    ax1.yaxis.tick_left()
    ax2.xaxis.set_visible(False)
    ax2.patch.set_visible(False)
    ax2.plot(nr_h,'r')
    #plots.plotfunctions.plot(ax2,nr_h,'r')
    ax2.set_ylim(nrylims)
    ax1.set_xlim(xlims)
    ax2.set_ylabel('n(r)')
    if expected_n is not None:
        for n_val in expected_n:
            ax2.plot(xlims,[n_val,n_val],'g-')
    return f1


def isMonitor(wkspc_h):
    """
    given a workspace handle return a numpy boolean array
    with one element per spectrum.  The bool is true if the spectrum is a monitor
    """
    total_hist = wkspc_h.getNumberHistograms()
    mon_bool = np.empty(total_hist,dtype=bool)
    for histnum in range(total_hist):
        mon_bool[histnum] = wkspc_h.spectrumInfo().isMonitor(histnum)
    return mon_bool


def extractY(wkspc):
    """
    given a workspace name extractY from detectors only
    """
    h_w = ms.mtd[wkspc]
    mon_bool = isMonitor(h_w)
    # total_hist = h_w.getNumberHistograms()
    y = h_w.extractY()
    mon_mask = [ not m for m in  mon_bool ]
    y = y[mon_mask]
    return y, mon_bool, h_w


def plot_delta_d_ttheta(ddwkspc,group_workspace=None,cmap_str='viridis'):
    """
    generate a plot of Delta d / d vs theta given a workspace of
    Delta D/d vs. spectrum getNumberHistograms
    if a workspace of grouping is given the points will be colored according to group
    default=None
    by the given colormap (default='viridis')
    """
    #extract Delta d/ d values and populate a numpy array
    res_y, res_mon_bool, h_nr = extractY(ddwkspc)
    # if a group workspace is present use it to determine a grouping array
    if group_workspace is not None:
        grp, g_bool, h_g = extractY(group_workspace)
        if len(grp)!=len(res_y):
            raise RuntimeError('the groping workspace and the Delta d/ d workspace should'
                               ' have the same number of detector specta')
        grp = np.reshape(grp, -1)
    else:
        grp='b'
    #determine theta values
    ttheta = np.zeros(len(res_y))
    h_sI = h_nr.spectrumInfo()
    tthetaidx = 0
    total_hist=h_nr.getNumberHistograms()
    for histnum in range(total_hist):
        if not res_mon_bool[histnum]:
            ttheta[tthetaidx]=np.degrees(h_sI.twoTheta(histnum))
            tthetaidx+=1
    f1,ax1=plt.subplots()
    im = ax1.scatter(ttheta,res_y.squeeze(),c=grp,edgecolors='none',cmap=plt.get_cmap('viridis'))
    ax1.set_yscale('log')
    ax1.set_ylim((1e-3,1))
    ax1.set_ylabel(r'$\frac{\Delta d}{d}$')
    #ax1.set_ylabel('Delta d /d')
    ax1.set_xlabel(r'$2\theta (^\circ)$')
    if group_workspace is not None:
        cbar = f1.colorbar(im,ax = ax1)
        cbar.ax.set_ylabel('group number')

    return f1
