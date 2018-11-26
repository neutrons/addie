import mantid_ipython_widget
from qtpy.QtWidgets import QDockWidget


class IPythonDockWidget(QDockWidget):
    """
    """

    def __init__(self, parent):
        """
        """
        QDockWidget.__init__(self, parent)

        self.iPythonWidget = None

        return

    def setup(self):
        """
        """
        # set ipython
        self.iPythonWidget = mantid_ipython_widget.MantidIPythonWidget()
        self.setWidget(self.iPythonWidget)

        return
