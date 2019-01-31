from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import (QDialog)  # noqa
from addie.utilities import load_ui
from . import mplgraphicsview as mplview


class PlotStyleDialog(QDialog):
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

        self.ui = load_ui(__file__, '../designer/ui_colorStyleSetup.ui',
                          baseinstance=self)

        # init widgets
        self._init_widgets()

        # define event handlers
        self.ui.pushButton_apply.clicked.connect(self.do_accept_quit)
        self.ui.pushButton_quit.clicked.connect(self.do_cancel_quit)

        # class variable
        self._acceptSelection = False

        # plot ID list
        self._plotIDList = list()

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

        self.ui.pushButton_quit.setText('Cancel')

        return

    def do_accept_quit(self):
        """

        Returns
        -------

        """
        self._acceptSelection = True
        self.close()

        return

    def do_cancel_quit(self):
        """

        Returns
        -------

        """
        self._acceptSelection = False
        self.close()

        return

    def get_color_marker(self):
        """

        Returns: 3-tuple. Line ID (None for all lines),
                          color (string, None for no change),
                          mark (string, None for no change)

        """
        # plot IDs
        plot_index = self.ui.comboBox_lines.currentIndex()
        plot_id = self._plotIDList[plot_index]
        if plot_id == -1:
            return_list = self._plotIDList[1:]
        else:
            return_list = [plot_id]

        # color
        color = str(self.ui.comboBox_color.currentText())
        if color == 'No Change':
            color = None

        # marker
        mark = str(self.ui.comboBox_style.currentText())
        if mark == 'No Change':
            mark = None
        else:
            mark = mark.split('(')[0].strip()

        return return_list, color, mark

    def is_to_apply(self):
        """
        Check whether the user wants to apply the changes to the canvas or not
        Returns: boolean to apply the change or not.

        """
        return self._acceptSelection

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

        # clear combo box and plot ID list
        self.ui.comboBox_lines.clear()
        self._plotIDList = list()

        # add lines
        plot_labels.insert(0, (-1, 'All'))
        for line_info in plot_labels:
            plot_id, label = line_info
            self.ui.comboBox_lines.addItem(label)
            self._plotIDList.append(plot_id)

        return


def get_plots_color_marker(parent_window, plot_label_list):
    """
    Launch a dialog to get the new color and marker for all or a specific plot.
    Note:
        1. use 2-tuple list for input plot is to avoid 2 lines with same label
    Args:
        parent_window:  parent window (main UI)
        plot_label_list: list of 2-tuples: line ID (integer) and line label (string)

    Returns:
        3-tuples: line ID (None for all lines, -1 for canceling), color (string) and marker (string)

    """
    # check input
    assert isinstance(plot_label_list, list), 'List of plots\' labels must be a list but not a %s.' \
                                              '' % plot_label_list.__class__.__name__

    # Launch window
    child_window = PlotStyleDialog(parent_window)

    # init set up
    child_window.set_plot_labels(plot_labels=plot_label_list)

    # launch window
    r = child_window.exec_()

    # get result
    if child_window.is_to_apply():
        # set the close one
        plot_id_list, color, marker = child_window.get_color_marker()
    else:
        # not accept
        plot_id_list, color, marker = None, None, None

    return plot_id_list, color, marker
