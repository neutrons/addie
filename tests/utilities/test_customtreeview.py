from __future__ import absolute_import, print_function
import pytest
from addie.utilities.customtreeview import CustomizedTreeView


@pytest.fixture
def custom_tree_view(qtbot):
    return CustomizedTreeView(None)


def test_get_selected_items(qtbot, custom_tree_view):
    """Test get_selected_items in tree of CustomizedTreeView"""
    items = custom_tree_view.get_selected_items()
    assert items == []
    assert type(items) == list
