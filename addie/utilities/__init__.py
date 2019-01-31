import os
from qtpy.uic import loadUi

def load_ui(ui_filename, baseinstance):
    ui_filename = os.path.split(ui_filename)[-1]

    # directory containing this file
    filename = __file__
    if not os.path.isdir(filename):
        filename = os.path.split(filename)[0]
    # get the location of the designer directory
    # this function assumes that all ui files are there
    filename = os.path.join(filename, '..', '..',  'designer')

    # put together the full path to the ui file
    filename = os.path.join(filename, ui_filename)
    return loadUi(filename, baseinstance=baseinstance)
