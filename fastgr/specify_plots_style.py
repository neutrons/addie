from PyQt4 import QtCore, QtGui

import ui_colorStyleSetup


class PlotStyleDialog(QtGui.QDialog):
    """

    """
    def __init__(self, parent=None):
        """

        Parameters
        ----------
        parent
        """
        super(PlotStyleDialog, self).__init__(parent)

        self.ui = ui_colorStyleSetup.Ui_Dialog()
        self.ui.setupUi(self)

        return

    def get_plot_color_marker(self):
        """

        Returns
        -------

        """
        return None, 'red', 'dot'


def get_plot_color_marker(parent_window):
    """

    Returns
    -------

    """
    # Launch window
    child_window = PlotStyleDialog(parent_window)

    # init set up
    pass

    # launch window
    print 'POP!'
    r = child_window.exec_()

    # set the close one
    line_id, color, marker = child_window.get_plot_color_marker()

    return line_id, color, marker

