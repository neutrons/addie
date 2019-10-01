from addie.processing.idl.table_handler import TableHandler as IdlTableHandler
from addie.processing.idl.undo_handler import UndoHandler
from addie.processing.idl.load_table_intermediate_step_interface import loadTableIntermediateStepInterface
from addie.processing.idl.step2_gui_handler import Step2GuiHandler
from addie.processing.idl.populate_background_widgets import PopulateBackgroundWidgets
from addie.processing.idl.populate_master_table import PopulateMasterTable


def import_table_clicked(main_window):
    main_window.postprocessing_ui.table.blockSignals(True)

    _o_table = IdlTableHandler(parent=main_window)
    _o_table._import()
    main_window.name_search_clicked()

    o_undo = UndoHandler(parent=main_window)
    o_undo.save_table(first_save=True)

    main_window.postprocessing_ui.table.blockSignals(False)


def export_table_clicked(main_window):
    _o_table = IdlTableHandler(parent=main_window)
    _o_table._export()


def move_to_folder_clicked(main_window):
    o_load_table = loadTableIntermediateStepInterface(parent=main_window)
    o_load_table.show()


def move_to_folder_step2(main_window):
    if not main_window.load_intermediate_step_ok:
        return

    o_gui = Step2GuiHandler(main_window=main_window)
    o_gui.move_to_folder()
    main_window.populate_table_clicked()


def populate_table_clicked(main_window):

    main_window.postprocessing_ui.table.blockSignals(True)

    _pop_table = PopulateMasterTable(main_window=main_window)
    _pop_table.run()
    _error_reported = _pop_table.error_reported

    if _error_reported:
        main_window.postprocessing_ui.table.blockSignals(False)
        return

    _pop_back_wdg = PopulateBackgroundWidgets(main_window=main_window)
    _pop_back_wdg.run()
    main_window.name_search_clicked()

    _o_gui = Step2GuiHandler(main_window=main_window)
    _o_gui.check_gui()

    o_undo = UndoHandler(parent=main_window)
    o_undo.save_table(first_save=True)

    main_window.postprocessing_ui.table.blockSignals(False)


def table_select_state_changed(main_window, state, row):
    _o_table_handler = IdlTableHandler(parent=main_window)
    _o_table_handler.check_selection_status(state, row)

    _o_gui = Step2GuiHandler(main_window=main_window)
    _o_gui.check_gui()
    _o_gui.define_new_ndabs_output_file_name()
    _o_gui.define_new_sum_scans_output_file_name()


def name_search_clicked(main_window):
    o_table = IdlTableHandler(parent=main_window)
    o_table.name_search()


def clear_name_search_clicked(main_window):
    o_table = IdlTableHandler(parent=main_window)
    main_window.postprocessing_ui.name_search.setText('')
    o_table.name_search()


def check_step2_gui(main_window, row, column):
    _o_gui = Step2GuiHandler(main_window=main_window)
    _o_gui.check_gui()
    _o_gui.step2_background_flag()
    _o_gui.step2_update_background_dropdown()

    if column == 1:
        o_pop = PopulateBackgroundWidgets(main_window=main_window)
        o_pop.refresh_contain()

    o_undo = UndoHandler(parent=main_window)
    o_undo.save_table()
