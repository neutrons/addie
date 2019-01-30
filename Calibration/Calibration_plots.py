from __future__ import (absolute_import, division, print_function, unicode_literals)

# import mantid algorithms, numpy and matplotlib
import mantid.simpleapi as ms
from mantid import plots
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
    ax2=ax1.twinx()
    plots.plotfunctions.plot(ax2,nr_h,'r')
    ax2.set_ylim(nrylims)
    ax1.set_xlim(xlims)
    ax2.set_ylabel('n(r)')
    if expected_n != None:
        for n_val in expected_n:
            ax2.plot(xlims,[n_val,n_val],'g-')
    return f1