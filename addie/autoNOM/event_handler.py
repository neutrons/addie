from addie.autoNOM.step1_gui_handler import Step1GuiHandler
from addie.processing.mantid.master_table.master_table_exporter import TableFileExporter as MantidTableExporter


def select_current_folder_clicked(main_window):
    o_gui = Step1GuiHandler(main_window=main_window)
    o_gui.select_working_folder()
    main_window.check_step1_gui()

def create_new_autonom_folder_button_clicked(main_window, status):
    o_gui_handler = Step1GuiHandler(main_window=main_window)
    o_gui_handler.new_autonom_group_box(status=status)

def output_folder_radio_buttons(main_window):
    o_gui_handler = Step1GuiHandler(main_window=main_window)
    o_gui_handler.manual_output_folder_button_handler()
    o_gui_handler.check_go_button()

def manual_output_folder_button_clicked(main_window):
    o_gui = Step1GuiHandler(main_window=main_window)
    o_gui.select_manual_output_folder()
    main_window.check_step1_gui()

def run_mantid(main_window):
    # TODO make a class level name so it can be reused
    filename = os.path.join(os.path.expanduser('~'), '.mantid', 'addie.json')

    # TODO should go to console as well
    print('writing out table to "{}"'.format(filename))
    # maybe this way
    exporter = MantidTableExporter(parent=main_window, filename=filename)
    exporter.create_dictionary()
    exporter.export()

    # TODO should do the real thing rather than print a message
    # main_window.launch_job_manager(job_name='mantid', script_to_run=TODO)
    print('supposed to run mantid now')
