import mantid_ipython_widget
import PyQt4.QtGui

# self.dockWidget_ipython = QtGui.QDockWidget(MainWindow)
class IPythonDockWidget(PyQt4.QtGui.QDockWidget):
    """
    """
    def __init__(self, parent):
        """
        """
        PyQt4.QtGui.QDockWidget.__init__(self, parent)

        return

    def setup(self):
        """
        """
        # set ipython
        self.setWidget(mantid_ipython_widget.MantidIPythonWidget())

        return

