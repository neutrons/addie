from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import pytest
import mantid.simpleapi as ms

from tests import DATA_DIR, IMAGE_DIR
from addie.calibration import plot_utils


@pytest.fixture
def grp_wksp():
    group_filename = os.path.join(DATA_DIR, 'NOM_group_detectors.xml')
    ms.LoadDetectorsGroupingFile(InputFile=group_filename,
                                 OutputWorkspace='NOM_group')
    return ms.mtd['NOM_group']


@pytest.fixture
def res_wksp():
    res_filename = os.path.join(DATA_DIR, 'NOM_resolution.nxs')
    ms.LoadNexusProcessed(Filename=res_filename, OutputWorkspace='NOM_res')
    return ms.mtd['NOM_res']


@pytest.fixture
def diamond_nr():
    nr_filename = os.path.join(DATA_DIR, 'diamond_nr.nxs')
    ms.LoadNexusProcessed(Filename=nr_filename, OutputWorkspace='nr')
    return ms.mtd['nr']


@pytest.fixture
def diamond_gr():
    nr_filename = os.path.join(DATA_DIR, 'diamond_gr.nxs')
    ms.LoadNexusProcessed(Filename=nr_filename, OutputWorkspace='gr')
    return ms.mtd['gr']


@pytest.mark.mpl_image_compare(baseline_dir=IMAGE_DIR,
                               filename="plot_delta_d_ttheta.png")
def test_plot_delta_d_ttheta(res_wksp):
    fig = plot_utils.plot_delta_d_ttheta('NOM_res')
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=IMAGE_DIR,
                               filename="plot_delta_d_ttheta_with_group.png")
def test_plot_delta_d_ttheta_with_group(res_wksp, grp_wksp):
    fig = plot_utils.plot_delta_d_ttheta('NOM_res',
                                         group_workspace='NOM_group')
    return fig


@pytest.mark.mpl_image_compare(baseline_dir=IMAGE_DIR,
                               filename="gr_nr_plot.png")
def test_gr_nr_plot(diamond_gr, diamond_nr):
    fig = plot_utils.plot_gr_nr('gr', 'nr', expected_n=[4, 16, 28])
    return fig
