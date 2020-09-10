from __future__ import absolute_import, print_function
import pytest
from qtpy.QtGui import QStandardItemModel

from addie.utilities.customtreeview import CustomizedTreeView
from addie.main import MainWindow

nodes = ['Test Workspaces']
main_item = 'test workspaces'
child_item = 'test bank'


@pytest.fixture
def custom_tree_view(qtbot):
    # Setup item model

    model = QStandardItemModel()
    model.setColumnCount(len(nodes))

    # Setup CustomTreeView to test against
    main_window = MainWindow()
    custom_tree_view = CustomizedTreeView(main_window)
    custom_tree_view._myNumCols = len(nodes)
    custom_tree_view.setModel(model)

    return custom_tree_view


@pytest.mark.skip()
def test_init_setup(qtbot, custom_tree_view):
    custom_tree_view.init_setup(nodes)
    assert custom_tree_view._myHeaderList == nodes


@pytest.mark.skip()
def test_add_main_item(qtbot, custom_tree_view):
    status, message = custom_tree_view.add_main_item(
        main_item,
        append=True,
        as_current_index=False)
    assert status is True
    assert message == ''


@pytest.mark.skip()
def test_get_selected_items(qtbot, custom_tree_view):
    """Test get_selected_items in tree of CustomizedTreeView"""
    tree = custom_tree_view
    tree.add_main_item(main_item, append=False, as_current_index=True)
    tree.add_child_main_item(main_item, child_item)
    items = custom_tree_view.get_selected_items()
    items_list = [str(item.text()) for item in items]
    assert items_list == [main_item]
    assert type(items) == list
