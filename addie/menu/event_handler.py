from qtpy.QtCore import QUrl
from qtpy.QtGui import QDesktopServices

from addie.menu.preview_ascii.step3_gui_handler import Step3GuiHandler
from addie.menu.file.configuration.import_configuration import ImportConfiguration
from addie.menu.file.configuration.export_configuration import ExportConfiguration
from addie.processing.idl.undo_handler import UndoHandler
from addie.about import AboutDialog
from addie.menu.file.settings.advanced_file_window import AdvancedWindowLauncher
from addie.utilities.ipts_file_transfer_dialog import IptsFileTransferDialog
from addie.utilities.job_status_handler import JobStatusHandler


def do_show_help(main_window):
    """ Show help
    """
    # close previous service
    main_window._assistantProcess.close()
    main_window._assistantProcess.waitForFinished()

    # launch
    helper_url = QUrl('https://neutrons.ornl.gov/nomad/users')
    QDesktopServices.openUrl(helper_url)


def action_preview_ascii_clicked(main_window):
    o_gui = Step3GuiHandler(parent=main_window)
    o_gui.browse_file()


def action_load_configuration_clicked(main_window):
    o_import_config = ImportConfiguration(parent=main_window)
    o_import_config.run()


def action_save_configuration_clicked(main_window):
    o_export_config = ExportConfiguration(parent=main_window)
    o_export_config.run()


def action_undo_clicked(main_window):
    o_undo = UndoHandler(parent=main_window)
    o_undo.undo_table()


def action_redo_clicked(main_window):
    o_undo = UndoHandler(parent=main_window)
    o_undo.redo_table()


def help_about_clicked(main_window):
    _about = AboutDialog(parent=main_window)
    _about.display()


def activate_reduction_tabs(main_window):
    if main_window.post_processing in main_window.idl_modes:
        tab_0 = True
        tab_1 = True
        tab_2 = False
        tab_3 = False
        tab_4 = True
        tab_5 = True
        current_index = 0
        visible_menu_configuration = True
    else:
        tab_0 = False
        tab_1 = False
        tab_2 = True
        tab_3 = True
        tab_4 = True
        tab_5 = True
        current_index = 2
        visible_menu_configuration = False
    main_window.ui.main_tab.setTabEnabled(0, tab_0)
    main_window.ui.main_tab.setTabEnabled(1, tab_1)
    main_window.ui.main_tab.setTabEnabled(2, tab_2)
    main_window.ui.main_tab.setTabEnabled(3, tab_3)
    main_window.ui.main_tab.setTabEnabled(4, tab_4)
    main_window.ui.main_tab.setTabEnabled(5, tab_5)
    main_window.setStyleSheet("QTabBar::tab::disabled {width: 0; height: 0; margin: 0; padding: 0; border: none;} ")
    main_window.ui.main_tab.setCurrentIndex(current_index)

    # also hide the file>configration buttons when working with Mantid
    main_window.ui.menuLoad_Configuration.menuAction().setVisible(visible_menu_configuration)


def advanced_option_clicked(main_window):
    AdvancedWindowLauncher(parent=main_window)


def menu_ipts_file_transfer_clicked(main_window):
    _o_ipts = IptsFileTransferDialog(parent=main_window)
    _o_ipts.show()


def window_job_monitor_clicked(main_window):
    _ = JobStatusHandler(parent=main_window)
