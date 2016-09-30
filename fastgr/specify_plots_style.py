from PyQt4 import QtCore, QtGui

import ui_colorStyleSetup
import mplgraphicsview as mplview


class PlotStyleDialog(QtGui.QDialog):
    """
    Dialog class for user to specify the color and marker of a certain line
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

        # init widgets
        self._init_widgets()

        return

    def _init_widgets(self):
        """
        Init the color and marker
        Returns:

        """
        color_list = mplview.MplBasicColors[:]
        color_list.insert(0, 'No Change')
        marker_list = mplview.MplLineMarkers[:]
        marker_list.insert(9, 'No Change')

        for color in color_list:
            self.ui.comboBox_color.addItem(color)
        for marker in marker_list:
            self.ui.comboBox_style.addItem(marker)

        return

    def get_plot_color_marker(self):
        """
        Read from the combo boxes and return
        Returns
        -------

        """
        # plot lines
        plot_label = str(self.ui.comboBox_lines.currentText())
        if plot_label == 'All':
            plot_label = None

        # color
        color = str(self.ui.comboBox_color.currentText())
        if color == 'No Change':
            color = None

        # marker
        marker = str(self.ui.comboBox_style.currentText())
        if marker == 'No Change':
            marker = None

        return plot_label, color, marker

    def set_plot_labels(self, plot_labels):
        """
        Add the plots
        Args:
            plot_labels:

        Returns:

        """
        # check
        assert isinstance(plot_labels, list), 'Plot lines\' labels must be list but not %s.' % type(plot_labels)
        assert len(plot_labels) > 0, 'Input plot lines cannot be an empty list.'

        # clear combo box
        self.ui.comboBox_lines.clear()

        # add lines
        plot_labels.insert(0, 'All')
        for label in plot_labels:
            self.ui.comboBox_lines.addItem(plot_labels)

        return


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

