import os
from qtpy.uic import loadUi

def load_ui(caller_filename, ui_relfilename, baseinstance):
    # directory containing the file
    if not os.path.isdir(caller_filename):
        filename = os.path.split(caller_filename)[0]
    # put together the full path to the ui file
    filename = os.path.join(filename, ui_relfilename)
    return loadUi(filename, baseinstance=baseinstance)
