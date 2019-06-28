import os
from addie.autoNOM.step1_gui_handler import Step1GuiHandler
from addie.autoNOM.run_step1 import RunStep1


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


def run_autonom(main_window):
    """Will first create the output folder, then create the exp.ini file"""
    _run_autonom = RunStep1(parent=main_window)
    _run_autonom.create_folder()
    print(os.getcwd())
    _run_autonom.create_exp_ini_file()


def create_exp_ini_clicked(main_window):
    _run_autonom = RunStep1(parent=main_window, run_autonom=False)
    _run_autonom.create_folder()
    _run_autonom.create_exp_ini_file()


def check_step1_gui(main_window):
    '''check the status of the step1 GUI in order to enable or not the GO BUTTON at the bottom'''
    o_gui_handler = Step1GuiHandler(main_window=main_window)
    o_gui_handler.check_go_button()
