import os
from qtpy.uic import loadUi
from addie import ui


def load_ui(ui_filename, baseinstance):
    ui_filename = os.path.split(ui_filename)[-1]
    ui_path = os.path.dirname(ui.__file__)

    # get the location of the ui directory
    # this function assumes that all ui files are there
    filename = os.path.join(ui_path, ui_filename)

    return loadUi(filename, baseinstance=baseinstance)


def check_in_fixed_dir_structure(main_window, sub_dir):
    """
    Check whether _currDataDir ends with 'GSAS', 'gofr' or 'SofQ'
    If it is, then reset the _currDataDir to its upper directory
    and set the in-format flag; Otherwise, keep as is.
    """
    # make sure that the last character of currDataDir is not /
    currDataDir = main_window._currDataDir
    if currDataDir.endswith('/') or currDataDir.endswith('\\'):
        # consider Linux and Windows case
        currDataDir = currDataDir[:-1]

    # split
    main_path, last_dir = os.path.split(currDataDir)
    if last_dir == sub_dir:
        main_window._inFixedDirectoryStructure = True
        currDataDir = main_path
    else:
        main_window._inFixedDirectoryStructure = False


def get_default_dir(main_window, sub_dir):
    """ Get the default data directory.
    If is in Fixed-Directory-Structure, then _currDataDir is the
    parent directory for all GSAS, gofr and SofQ
    and thus return the data directory with _currDataDir joined with sub_dir
    Otherwise, no operation
    """
    # check
    msg = 'sub directory must be a string but not {}.'.format(type(sub_dir))
    assert isinstance(sub_dir, str), msg

    if main_window._inFixedDirectoryStructure:
        default_dir = os.path.join(main_window._currDataDir, sub_dir)
    else:
        default_dir = main_window._currDataDir

    return default_dir
