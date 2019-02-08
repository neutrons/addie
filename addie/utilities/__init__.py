import os
from qtpy.uic import loadUi

def load_ui(ui_filename, baseinstance):
    cwd = os.getcwd()
    ui_filename = os.path.split(ui_filename)[-1]

    # get the location of the designer directory
    # this function assumes that all ui files are there
    filename = os.path.join(cwd, 'designer', ui_filename)

    return loadUi(filename, baseinstance=baseinstance)
