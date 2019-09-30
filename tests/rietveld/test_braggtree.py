from __future__ import absolute_import, print_function
import pytest
import os
from mantid.api import AnalysisDataService

from tests import DATA_DIR

from addie.rietveld.braggtree import BraggTree, BankRegexException
from addie.main import MainWindow
from addie.rietveld import event_handler


@pytest.fixture
def main_window(qtbot):
    main_window = MainWindow()
    return main_window


@pytest.fixture
def rietveld_event_handler(qtbot):
    return event_handler


@pytest.fixture
def bragg_tree(qtbot, main_window):
    return BraggTree(main_window)


@pytest.fixture
def bragg_tree_loaded(qtbot, rietveld_event_handler, main_window):
    filenames = ['GSAS_NaNO3_230C.gsa', 'GSAS_NaNO3_275C.gsa']
    bragg_file_names = [ os.path.join(DATA_DIR, f) for f in filenames ]
    rietveld_event_handler.load_bragg_files(main_window, bragg_file_names)
    bragg_tree = main_window.rietveld_ui.treeWidget_braggWSList
    return bragg_tree


def test_get_tree_structure(qtbot, bragg_tree_loaded):
    """Test we can get the Bragg tree structure without exception"""
    bragg_tree_loaded._get_tree_structure()


def test_add_bragg_ws_group(qtbot, bragg_tree):
    """Test we can add a list of banks to workspace group"""
    ws_group_name = "WorkspaceGroup"
    bank_angles = [20, 30, 90]
    bank_list = list()
    for i, angle in enumerate(bank_angles):
        bank_list.append('Bank {} - {}'.format(i + 1, angle))
    bragg_tree.add_bragg_ws_group(ws_group_name, bank_list)


def test_get_bank_id(qtbot, bragg_tree):
    """Test we can extract a bank id from bank workspace name"""
    target = 12345
    bank_wksp_name = "Bank {} - 90.0".format(target)
    bank_id = bragg_tree._get_bank_id(bank_wksp_name)
    assert int(bank_id) == target


def test_get_bank_id_exception(qtbot, bragg_tree):
    """Test for raised exception from a bad workspace name"""
    bad_ws = "Bank jkl 1 -- 90.0"
    with pytest.raises(BankRegexException):
        bragg_tree._get_bank_id(bad_ws)


def test_do_plot_ws(qtbot, bragg_tree_loaded):
    """Test for plotting selected bank workspace"""
    group_index = bragg_tree_loaded.model().index(1,0)
    bank_index = bragg_tree_loaded.model().index(0,0,group_index)
    bragg_tree_loaded.setCurrentIndex(bank_index)
    print(AnalysisDataService.getObjectNames())
    ws = AnalysisDataService.retrieve('GSAS_NaNO3_230C')
    print(ws.id())
    bragg_tree_loaded.do_plot_ws()


def test_do_plot_ws_exception(qtbot):
    """Test for raised exception from MainWindow==None"""
    bragg_tree = BraggTree(None)
    with pytest.raises(NotImplementedError):
        bragg_tree.do_plot_ws()
