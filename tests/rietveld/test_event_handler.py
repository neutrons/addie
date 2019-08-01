from __future__ import absolute_import, print_function
import pytest
from addie.rietveld import event_handler


@pytest.fixture
def rietveld_event_handler(qtbot):
    return event_handler


def test_evt_change_gss_mode_exception(qtbot, rietveld_event_handler):
    """Test we can extract a bank id from bank workspace name"""
    with pytest.raises(NotImplementedError):
        rietveld_event_handler.evt_change_gss_mode(None)
