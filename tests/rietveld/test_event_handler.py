from __future__ import absolute_import, print_function
import os
import pytest
from tests import DATA_DIR
from mantid.api import AnalysisDataService

from addie.rietveld import event_handler
from addie.main import MainWindow

bragg_file_names = ['GSAS_NaNO3_230C.gsa', 'GSAS_NaNO3_275C.gsa']
bragg_file_list = [os.path.join(DATA_DIR, name) for name in bragg_file_names]


@pytest.fixture
def rietveld_event_handler(qtbot):
    return event_handler


def test_load_bragg_files(qtbot, rietveld_event_handler):
    """Test load_bragg_files when no files to load"""
    main_window = MainWindow()
    rietveld_event_handler.load_bragg_files(main_window, None)


def test_plot_bragg_bank_for_multi_bank(qtbot, rietveld_event_handler):
    """Test plot_bragg_bank for Multi-Bank mode"""
    main_window = MainWindow()
    rietveld_event_handler.load_bragg_files(main_window, bragg_file_list)

    main_window.rietveld_ui.graphicsView_bragg.set_to_single_gss(True)
    main_window.rietveld_ui.radioButton_multiBank.setChecked(True)
    main_window.rietveld_ui.radioButton_multiGSS.setChecked(False)
    rietveld_event_handler.plot_bragg_bank(main_window)


def test_plot_bragg_bank_for_multi_gsas(qtbot, rietveld_event_handler):
    """Test plot_bragg_bank for Multi-GSAS mode"""
    main_window = MainWindow()
    rietveld_event_handler.load_bragg_files(main_window, bragg_file_list)

    main_window.rietveld_ui.graphicsView_bragg.set_to_single_gss(False)
    main_window.rietveld_ui.radioButton_multiBank.setChecked(False)
    main_window.rietveld_ui.radioButton_multiGSS.setChecked(True)
    rietveld_event_handler.plot_bragg_bank(main_window)


def test_evt_change_gss_mode_exception(qtbot, rietveld_event_handler):
    """Test we raise exception for main_window==None to change_gss_mode"""
    with pytest.raises(NotImplementedError):
        rietveld_event_handler.evt_change_gss_mode(None)


def test_load_bragg_by_filename(qtbot, rietveld_event_handler):
    """Test that we can load Bragg *.gsa (GSAS) files"""
    filename = 'NOM_127827.gsa'
    files = [os.path.join(DATA_DIR, filename)]

    for filename in files:
        wksp, angles = rietveld_event_handler.load_bragg_by_filename(filename)
        wksp == os.path.basename(filename).split('.')[0]

        angles_exp = [15.1, 31., 65., 120.4, 150.1, 8.6]  # copied from file by hand
        for obs, expected in zip(angles, angles_exp):
            assert obs == pytest.approx(expected, rel=0.1)

    assert AnalysisDataService.doesExist(wksp)
