from qtpy.QtWidgets import QFileDialog

from addie.processing.mantid.master_table.table_tree_handler import TableTreeHandler, TableConfig, H3TableHandler
from addie.processing.mantid.master_table.selection_handler import TableHandler as MtdTableHandler
from addie.processing.mantid.master_table.table_row_handler import TableRowHandler
from addie.processing.mantid.master_table.periodic_table.material_handler import MaterialHandler
from addie.processing.mantid.master_table.mass_density_handler import MassDensityHandler
from addie.processing.mantid.master_table.geometry_handler import DimensionsSetter
from addie.processing.mantid.master_table.resonance_handler import ResonanceSetter
from addie.processing.mantid.master_table.self_scattering_handler import ScatteringSetter
from addie.processing.mantid.master_table.import_from_run_number_handler import ImportFromRunNumberHandler
from addie.processing.mantid.master_table.import_from_database.load_into_master_table import LoadIntoMasterTable
from addie.processing.mantid.make_calibration_handler.make_calibration import MakeCalibrationLauncher
from addie.processing.mantid.master_table.reduction_configuration_handler import ReductionConfigurationHandler
from addie.processing.mantid.master_table.master_table_loader import AsciiLoader

from addie.processing.mantid.master_table.tree_definition import INDEX_OF_COLUMNS_WITH_MASS_DENSITY

# ONCat integration
try:
    from addie.processing.mantid.master_table.import_from_database.import_from_database_handler import ImportFromDatabaseHandler
    import pyoncat # noqa
    ONCAT_ENABLED = True
except ImportError:
    print('pyoncat module not found. Functionality disabled')
    ONCAT_ENABLED = False


def personalization_table_clicked(main_window):
    _ = TableTreeHandler(parent=main_window)
    _table_config = TableConfig(main_window=main_window)
    current_config = _table_config.get_current_config()
    _table_config.update_tree_dict_and_tree(config_to_load=current_config)


def table_search(main_window):
    o_table = MtdTableHandler(parent=main_window)
    o_table.search(main_window)


def table_search_clear(main_window):
    o_table = MtdTableHandler(parent=main_window)
    o_table.clear_search()


def load_this_config(main_window, key='', resize=False):
    if key == '':
        return

    if key == 'FULL_RESET':
        config_to_load = main_window.reset_config_dict['table']
    else:
        config_to_load = main_window.config_dict[key]['table']

    h1_dict = config_to_load['h1']
    h2_dict = config_to_load['h2']
    h3_dict = config_to_load['h3']

    o_table = TableConfig(main_window=main_window)
    o_table.disconnect_table_ui()

    for _col in h1_dict:
        _visible = h1_dict[_col]['visible']
        _width = h1_dict[_col]['width']
        o_table.set_size_and_visibility_column(
            h1=_col, width=_width, visibility=_visible, resize=resize)

    for _col in h2_dict:
        _visible = h2_dict[_col]['visible']
        _width = h2_dict[_col]['width']
        o_table.set_size_and_visibility_column(
            h2=_col, width=_width, visibility=_visible, resize=resize)

    for _col in h3_dict:
        _visible = h3_dict[_col]['visible']
        _width = h3_dict[_col]['width']
        o_table.set_size_and_visibility_column(
            h3=_col, width=_width, visibility=_visible, resize=resize)

    o_table.update_tree_dict_and_tree(config_to_load)

    o_table.disconnect_table_ui(unblock_all=True)


def h3_table_right_click(main_window):
    o_h3_table = H3TableHandler(main_window=main_window)
    o_h3_table.right_click()


def check_status_of_right_click_buttons(main_window):
    o_h3_table = H3TableHandler(main_window=main_window)
    o_h3_table.check_status_of_right_click_buttons()


def scroll_h1_table(main_window, value):
    main_window.processing_ui.h2_table.horizontalScrollBar().setValue(value)
    main_window.processing_ui.h3_table.horizontalScrollBar().setValue(value)


def scroll_h2_table(main_window, value):
    main_window.processing_ui.h1_table.horizontalScrollBar().setValue(value)
    main_window.processing_ui.h3_table.horizontalScrollBar().setValue(value)


def scroll_h3_table(main_window, value):
    main_window.processing_ui.h1_table.horizontalScrollBar().setValue(value)
    main_window.processing_ui.h2_table.horizontalScrollBar().setValue(value)


def resizing_h1(main_window, index_column, old_size, new_size):

    o_table = TableConfig(main_window=main_window)
    o_table.disconnect_table_ui()

    h2_children = o_table.get_h2_children_from_h1(h1=index_column)
    last_h2_visible = o_table.get_last_h2_visible(list_h2=h2_children)
    list_h3 = o_table.get_h3_children_from_h2(h2=last_h2_visible)
    last_h3_visible = o_table.get_last_h3_visible(list_h3=list_h3)

    size_diff = new_size - old_size

    # add this size_diff to last_h2 and last_h3
    last_h3_visible_size = o_table.get_size_column(h3=last_h3_visible)
    if (last_h3_visible_size < main_window.minimum_col_width) and \
            (new_size < old_size):
        o_table.set_size_column(h1=index_column, width=old_size)
    else:
        last_h2_visible_size = o_table.get_size_column(h2=last_h2_visible)
        o_table.set_size_column(
            h2=last_h2_visible, width=last_h2_visible_size + size_diff)
        o_table.set_size_column(
            h3=last_h3_visible, width=last_h3_visible_size + size_diff)

    o_table.disconnect_table_ui(unblock_all=True)


def resizing_h2(main_window, index_column, old_size, new_size):
    o_table = TableConfig(main_window=main_window)
    o_table.disconnect_table_ui()

    h1_parent = o_table.get_h1_parent_from_h2(h2=index_column)
    h3_children = o_table.get_h3_children_from_h2(h2=index_column)
    last_h3_visible = o_table.get_last_h3_visible(list_h3=h3_children)

    size_diff = new_size - old_size

    last_h3_visible_size = o_table.get_size_column(h3=last_h3_visible)
    if (last_h3_visible_size < main_window.minimum_col_width) and \
            (new_size < old_size):
        o_table.set_size_column(h2=index_column, width=old_size)
    else:
        # add this size_diff to parent and last h3
        parent_size = o_table.get_size_column(h1=h1_parent)
        o_table.set_size_column(h1=h1_parent, width=parent_size + size_diff)
        o_table.set_size_column(
            h3=last_h3_visible, width=last_h3_visible_size + size_diff)

    o_table.disconnect_table_ui(unblock_all=True)


def resizing_h3(main_window, index_column, old_size, new_size):

    o_table = TableConfig(main_window=main_window)
    o_table.disconnect_table_ui()

    [h1_parent, h2_parent] = o_table.get_h1_h2_parent_from_h3(h3=index_column)

    size_diff = new_size - old_size

    h1_parent_size = o_table.get_size_column(h1=h1_parent)
    o_table.set_size_column(h1=h1_parent, width=h1_parent_size + size_diff)
    h2_parent_size = o_table.get_size_column(h2=h2_parent)
    o_table.set_size_column(h2=h2_parent, width=h2_parent_size + size_diff)

    o_table.disconnect_table_ui(unblock_all=True)


def init_tree(main_window):
    main_window.addItems(main_window.ui.treeWidget.invisibleRootItem())
    main_window.ui.treeWidget.itemChanged.connect(
        main_window.tree_item_changed)


def tree_item_changed(main_window, item):
    """this will change the way the big table will look like by hidding or showing columns"""

    o_table = TableConfig(main_window=main_window)
    o_table.block_table_header_ui(block_all=False,
                                  block_h1=True,
                                  block_h2=True)

    h_columns_affected = o_table.get_h_columns_from_item_name(
        item_name=o_table.get_item_name(item))

    o_table.change_state_tree(list_ui=h_columns_affected['list_tree_ui'],
                              list_parent_ui=h_columns_affected['list_parent_ui'],
                              state=item.checkState(0))

    o_table.update_table_columns_visibility()
    o_table.resizing_table(tree_dict=h_columns_affected, block_ui=False)

    o_table.block_table_header_ui(unblock_all=True)


def master_table_select_state_changed(main_window, state, key):
    o_table = TableRowHandler(main_window=main_window)
    o_table.activated_row_changed(key=key, state=state)


# sample columns
def sample_material_button_pressed(main_window, key):
    MaterialHandler(parent=main_window, key=key, data_type='sample')


def sample_material_line_edit_entered(main_window, key):
    o_table = TableRowHandler(main_window=main_window)
    o_table.transfer_widget_states(from_key=key, data_type='sample')


def sample_mass_density_button_pressed(main_window, key):
    MassDensityHandler(parent=main_window, data_type='sample', key=key)


def sample_mass_density_line_edit_entered(main_window, key):
    o_table = TableRowHandler(main_window=main_window)
    o_table.transfer_widget_states(from_key=key, data_type='sample')
    main_window.check_master_table_column_highlighting(
        column=INDEX_OF_COLUMNS_WITH_MASS_DENSITY[0])


def sample_shape_changed(main_window, index, key):
    o_table = TableRowHandler(main_window=main_window)
    o_table.shape_changed(shape_index=index, key=key, data_type='sample')


def sample_abs_correction_changed(main_window, text, key):
    o_table = TableRowHandler(main_window=main_window)
    o_table.abs_correction_changed(value=text, key=key, data_type='sample')


def sample_multi_scattering_correction_changed(main_window, text, key):
    o_table = TableRowHandler(main_window=main_window)
    o_table.multi_scattering_correction(
        value=text, key=key, data_type='sample')


def sample_inelastic_correction_changed(main_window, text, key):
    o_table = TableRowHandler(main_window=main_window)
    o_table.inelastic_correction_changed(
        value=text, key=key, data_type='sample')


def sample_placzek_button_pressed(main_window, key):
    o_table = TableRowHandler(main_window=main_window)
    o_table.placzek_button_pressed(key=key, data_type='sample')


def sample_dimensions_setter_button_pressed(main_window, key):
    o_dimensions_ui = DimensionsSetter(
        parent=main_window, key=key, data_type='sample')
    o_dimensions_ui.show()


def sample_resonance_button_pressed(main_window, key):
    o_resonance_ui = ResonanceSetter(
        parent=main_window, key=key, data_type='sample')
    o_resonance_ui.show()


def self_scattering_button_pressed(main_window, key):
    o_scattering_ui = ScatteringSetter(
        parent=main_window, key=key)
    o_scattering_ui.show()


# normalization columns
def normalization_material_button_pressed(main_window, key):
    MaterialHandler(parent=main_window, key=key, data_type='normalization')


def normalization_material_line_edit_entered(main_window, key):
    o_table = TableRowHandler(main_window=main_window)
    o_table.transfer_widget_states(from_key=key, data_type='normalization')


def normalization_mass_density_button_pressed(main_window, key):
    MassDensityHandler(parent=main_window, data_type='normalization', key=key)


def normalization_mass_density_line_edit_entered(main_window, key):
    o_table = TableRowHandler(main_window=main_window)
    o_table.transfer_widget_states(from_key=key, data_type='normalization')
    main_window.check_master_table_column_highlighting(
        column=INDEX_OF_COLUMNS_WITH_MASS_DENSITY[1])


def normalization_shape_changed(main_window, text, key):
    o_table = TableRowHandler(main_window=main_window)
    o_table.shape_changed(shape_index=text, key=key, data_type='normalization')


def normalization_abs_correction_changed(main_window, text, key):
    o_table = TableRowHandler(main_window=main_window)
    o_table.abs_correction_changed(
        value=text, key=key, data_type='normalization')


def normalization_multi_scattering_correction_changed(main_window, text, key):
    o_table = TableRowHandler(main_window=main_window)
    o_table.multi_scattering_correction(
        value=text, key=key, data_type='normalization')


def normalization_inelastic_correction_changed(main_window, text, key):
    o_table = TableRowHandler(main_window=main_window)
    o_table.inelastic_correction_changed(
        value=text, key=key, data_type='normalization')


def normalization_placzek_button_pressed(main_window, key):
    o_table = TableRowHandler(main_window=main_window)
    o_table.placzek_button_pressed(key=key, data_type='normalization')


def normalization_dimensions_setter_button_pressed(main_window, key):
    o_dimensions_ui = DimensionsSetter(
        parent=main_window, key=key, data_type='normalization')
    o_dimensions_ui.show()


def launch_import_from_database_handler(main_window):
    if ONCAT_ENABLED:
        ImportFromDatabaseHandler(parent=main_window)
    else:
        print('oncat functionality disabled')


def launch_import_from_run_number_handler(main_window):
    ImportFromRunNumberHandler(parent=main_window)


def make_calibration_clicked(main_window):
    MakeCalibrationLauncher(parent=main_window)


def browse_calibration_clicked(main_window):
    _calibration_folder = main_window.calibration_folder
    [_calibration_file, _] = QFileDialog.getOpenFileName(parent=main_window,
                                                         caption="Select Calibration File",
                                                         directory=_calibration_folder,
                                                         filter=main_window.calibration_extension)
    if _calibration_file:
        main_window.processing_ui.calibration_file.setText(_calibration_file)


def from_oncat_to_master_table(main_window, json=None, with_conflict=False, ignore_conflicts=False):
    if main_window.import_from_database_ui:
        main_window.import_from_database_ui.close()

    LoadIntoMasterTable(parent=main_window, json=json,
                        with_conflict=with_conflict,
                        ignore_conflicts=ignore_conflicts)


def reduction_configuration_button_clicked(main_window):
    ReductionConfigurationHandler(parent=main_window)


def load_ascii(main_window, filename=""):
    o_ascii_loader = AsciiLoader(parent=main_window, filename=filename)
    o_ascii_loader.load()
