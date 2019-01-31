import numpy as np
import matplotlib.pyplot as plt
from mantid.simpleapi import *

chi2_threshold = 1e12

# Input dvalues (here are the diamond ones)
dvalues = (0.3117,0.3257,0.3499,0.4205,0.4645,0.4768,0.4996,0.5150,0.5441,0.5642,0.5947,
           0.6307,.6866,.7283,.8185,.8920,1.0758,1.2615,2.0599)

def get_fit_params_from_instrument_preselected_file(instrument):
    # Load files
    filename="%s_pdcalibration_diagnostics.nxs" % instrument

    cal_wksp = LoadNexusProcessed(Filename=filename)

    # Get the fitting parameters workspace
    if instrument == "NOM":
        wksp_name = "NOM_122825_diag_fitparam"
    if instrument == "PG3":
        wksp_name = "PG3_39169_diag_fitparam"
    return mtd[wksp_name]

def get_fit_params_by_fitting(wksp):
    pass

def get_column_data(wksp, val_col, chi2_col, threshold):
    values = list()
    for (val, chi2) in zip(wksp.column(val_col), wksp.column(chi2_col)):
        if chi2 < chi2_threshold:
            values.append(val)
    return values

def deltaD(tof_center, tof_width, dspace_center):
    tof_fwhm = 2.* np.sqrt(2.*np.log(2.)) * tof_width
    dspace_fwhm = (tof_fwhm / tof_center) * dspace_center
    return dspace_fwhm
    
if __name__=="__main__":
    wksp = get_fit_params_from_instrument_preselected_file("NOM")

    # Extract the column IDs of interest
    wksp_col = wksp.getColumnNames().index('wsindex')
    center_col = wksp.getColumnNames().index('centre')
    width_col = wksp.getColumnNames().index('width')
    peak_col = wksp.getColumnNames().index('peakindex')
    chi2_col = wksp.getColumnNames().index('chi2')

    # Extract data
    pixel_idx_vals = get_column_data(wksp, wksp_col, chi2_col, chi2_threshold)
    center_vals = get_column_data(wksp, center_col, chi2_col, chi2_threshold)
    width_vals = get_column_data(wksp, width_col, chi2_col, chi2_threshold)
    dspace_idx_vals = get_column_data(wksp, peak_col, chi2_col, chi2_threshold)

    # Make array where rows are pixels and cols are delta-d values (FWHM in dspace)
    pixels = np.unique(np.array(pixel_idx_vals))
    idx2pixel = { i:pid for i, pid in enumerate(pixels) }
    pixel2idx = { pid:i for i, pid in enumerate(pixels)}

    '''
     TODO: vectorize the for-loop to operate on arrays for : tof_center, tof_widths, dvalues
       step 1 - get vector for dvalues, maybe use np.vstack, to create a len(pixels) * len(dvalues) vector for step 3
       step 2 - vector operate on tof_widths to get tof_fwhms
       step 3 - vector operate on tof_fwhms / tof_centers * dvalues to get dspace_fwhms
     TODO: then, use histogramming (probably with a set number of bins) to reduce the number of points plotted.
           could do an array of len(n_histograms)*len(dvalues) that can be plotted quickly and easily and easier for linear regression
           would also be necessary before interactivity could be introduced for say: displaying number of pixels per dspacing,
                                                                                     changing sigma for inclusion around linear regression line, etc.
    '''
    pixel_deltaD = np.zeros((len(pixels), len(dvalues)))
    fig, ax = plt.subplots(1)
    for pidx, tof_center, tof_width, dspace_idx in zip(pixel_idx_vals, center_vals, width_vals, dspace_idx_vals):
        dspace_width = deltaD(tof_center, tof_width, dvalues[dspace_idx])
        pixel_deltaD[pixel2idx[pidx],dspace_idx] = dspace_width

    for idx, row in enumerate(pixel_deltaD):
        ax.plot(dvalues, row, 'o', label="Pixel: %d" % idx2pixel[idx])

    ax.legend()
    plt.show()
        
         
