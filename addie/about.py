from PyQt4 import QtGui, QtCore

from numpy.version import version as numpy_version_str
from matplotlib import __version__ as matplotlib_version_str
from PyQt4.pyqtconfig import Configuration as pyqt_configuration
import mantid
import sys
import addie._version as addie_version


class AboutDialog(object):
    
    def __init__(self, parent=None):
        self.parent = parent
        
    def display(self):
        addie_version = self.get_appli_version()
        python_version = self.get_python_version()
        numpy_version = numpy_version_str
        mantid_version = mantid.__version__
        matplotlib_version = matplotlib_version_str
        qt_version = QtCore.QT_VERSION_STR
        pyqt_version = pyqt_configuration().pyqt_version_str
        
        message = ''' Addie 
        
        version %s
        
        Library versions:
           - Python: %s
           - Numpy: %s
           - Mantid: %s
           - Matplotlib: %s
           - Qt: %s
           - PyQt: %s
        ''' % (addie_version,
               python_version,
               numpy_version,
               mantid_version,
               matplotlib_version,
               qt_version,
               pyqt_version)
        
        QtGui.QMessageBox.about(self.parent, "About Addie", message)
        
    def get_appli_version(self):
        _version = addie_version.get_versions()
        return str(_version['version'][0:5])
        
    def get_python_version(self):
        str_version = sys.version_info
        str_array = []
        for value in str_version:
            str_array.append(str(value))
        return ".".join(str_array[0:3])