import mantid_ipython_widget
import PyQt4.QtGui


class IPythonDockWidget(PyQt4.QtGui.QDockWidget):
    """
    """
    def __init__(self, parent):
        """
        """
        PyQt4.QtGui.QDockWidget.__init__(self, parent)

        self.iPythonWidget = None

        return

    def setup(self):
        """
        """
        # set ipython
        self.iPythonWidget = mantid_ipython_widget.MantidIPythonWidget()
        self.setWidget(self.iPythonWidget)

        return

    def wild_test(self):
        """
        WILD TEST
        Returns
        -------

        """
        # append output to the output stream but not input console
        self.iPythonWidget.append_stream('bababa')