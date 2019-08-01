from __future__ import absolute_import, print_function
import pytest
from addie.rietveld.braggtree import BraggTree, BankRegexException


@pytest.fixture
def bragg_tree():
    return BraggTree(None)


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


def test_do_plot_ws_exception(qtbot, bragg_tree):
    """Test for raised exception from MainWindow==None"""
    with pytest.raises(NotImplementedError):
        bragg_tree.do_plot_ws()
