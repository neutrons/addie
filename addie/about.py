from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import (QMessageBox)
from qtpy import PYQT_VERSION, PYQT4, PYQT5
from numpy.version import version as numpy_version_str
from matplotlib import __version__ as matplotlib_version_str
import sys
import mantid
from addie import __version__ as addie_version

# qtpy does not provide an abstraction for this
if PYQT5:
    from PyQt5.QtCore import QT_VERSION_STR  # noqa
elif PYQT4:
    from PyQt4.QtCore import QT_VERSION_STR  # noqa
else:
    raise RuntimeError('unknown qt version')
try:
    from pyoncat import __version__ as pyoncat_version  # noqa
except ImportError:
    pyoncat_version = 'disabled'


class AboutDialog(object):

    def __init__(self, parent=None):
        self.parent = parent

    def display(self):
        addie_version = self.get_appli_version()
        python_version = self.get_python_version()
        numpy_version = numpy_version_str
        mantid_version = mantid.__version__
        matplotlib_version = matplotlib_version_str
        qt_version = QT_VERSION_STR
        pyqt_version = PYQT_VERSION

        message = ''' Addie

        version %s

        Library versions:
           - Python: %s
           - Numpy: %s
           - Mantid: %s
           - Matplotlib: %s
           - pyoncat: %s
           - Qt: %s
           - PyQt: %s
        ''' % (addie_version,
               python_version,
               numpy_version,
               mantid_version,
               matplotlib_version,
               pyoncat_version,
               qt_version,
               pyqt_version)

        QMessageBox.about(self.parent, "About Addie", message)

    def get_appli_version(self):
        if '+' in addie_version:
            return addie_version.split('+')[0] + ' dev'
        else:
            return addie_version

    def get_python_version(self):
        str_version = sys.version_info
        str_array = []
        for value in str_version:
            str_array.append(str(value))
        return ".".join(str_array[0:3])
