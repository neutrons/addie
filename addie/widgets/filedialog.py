import os
from qtpy.QtWidgets import QFileDialog


def get_save_file(parent, directory=None, caption=None, filter=dict()):
    '''
    This is operating under the assumption that the file_filters parameter is a dict of filter:extension

    The filename will have the file extension appended if one isn't already found on it

    It returns a pair (<filename with extension>, <extension>). In the case of user cancelling, the filename
    returned is None
    '''
    # convert defaults into something useful
    if not directory:
        # try to get it from the parent
        if parent:
            try:
                directory = parent._currWorkDir
            except:
                pass
        # just give up and use the current working directory
        if not directory:
            directory = os.getcwd()

    if not caption:
        caption = 'Save File'

    if filter:
        dialogfilter = ';;'.join(filter.keys())
    else:
        dialogfilter = ''

    result = QFileDialog.getSaveFileName(parent=parent, directory=directory, caption=caption,
                                         filter=dialogfilter)

    # qt4/qt5 return slightly different things
    if isinstance(result, tuple):
        filename, filefilter = result
    else:
        filename = result
        filefilter = None

    # check if the user canceled
    if not filename:
        return None, filefilter

    # determine the type and add the extension
    extension = os.path.splitext(str(filename))[-1]
    filetype = filter.get(filefilter, None)
    if filetype is None:
        filetype = extension.replace('.', '')
    elif not extension:
        # implementation ties filetype to the extension
        filename = '{}.{}'.format(filename, filetype)

    return filename, filetype
