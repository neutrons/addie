import os
from qtpy.uic import loadUi
import addie

addie_path =  os.path.dirname(os.path.abspath(addie.__file__))
designer_path = os.path.join(addie_path, '../designer')

def load_ui(ui_filename, baseinstance):
    ui_filename = os.path.split(ui_filename)[-1]

    # get the location of the designer directory
    # this function assumes that all ui files are there
    filename = os.path.join(designer_path, ui_filename)

    return loadUi(filename, baseinstance=baseinstance)
