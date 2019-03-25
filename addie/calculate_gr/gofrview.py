from __future__ import (absolute_import, division, print_function)

from qtpy.QtGui import QCursor
from qtpy.QtWidgets import (QAction, QMenu)

from addie.plot import MplGraphicsView


class GofRView(MplGraphicsView):
    """
    Graphics view for G(R)
    """

    def __init__(self, parent):
        """
        Initialization
        """
        MplGraphicsView.__init__(self, parent)

        # class variable containers
        self._grDict = dict()

        self._colorList = ['black', 'red', 'blue', 'green', 'brown', 'orange']
        self._colorIndex = 0

        # define the event handlers to the mouse actions
        self._myCanvas.mpl_connect('button_press_event', self.on_mouse_press_event)
        # self._myCanvas.mpl_connect('button_release_event', self.on_mouse_release_event)
        # self._myCanvas.mpl_connect('motion_notify_event', self.on_mouse_motion)

        # class variable
        self._minY = None
        self._maxY = None

        # variable
        self._isLegendOn = False

        return

    def on_mouse_press_event(self, event):
        """
        Event handling for mouse press action
        Args:
            event:

        Returns:

        """
        # get the button and position information.
        curr_x = event.xdata
        curr_y = event.ydata
        if curr_x is None or curr_y is None:
            # outside of canvas
            return

        button = event.button
        if button == 1:
            # left button: no operation
            pass

        elif button == 3:
            # right button:
            # Pop-out menu
            self.menu = QMenu(self)

            if self.get_canvas().is_legend_on:
                # figure has legend: remove legend
                action1 = QAction('Hide legend', self)
                action1.triggered.connect(self._myCanvas.hide_legend)

                action2 = QAction('Legend font larger', self)
                action2.triggered.connect(self._myCanvas.increase_legend_font_size)

                action3 = QAction('Legend font smaller', self)
                action3.triggered.connect(self._myCanvas.decrease_legend_font_size)

                self.menu.addAction(action2)
                self.menu.addAction(action3)

            else:
                # figure does not have legend: add legend
                action1 = QAction('Show legend', self)
                action1.triggered.connect(self._myCanvas.show_legend)

            self.menu.addAction(action1)

            # pop up menu
            self.menu.popup(QCursor.pos())
        # END-IF-ELSE

        return

    def plot_gr(self, plot_key, ws_name, plotError=False, color='black', style='.', marker=None,
                alpha=1., label=None):
        """
        Plot G(r)
        :param plot_key: a key to the current plot
        :param vec_r: numpy array for R
        :param vec_g: numpy array for G(r)
        :param vec_e: numpy array for G(r) error
        :param plot_error:
        :param color:
        :param style:
        :param marker:
        :param alpha:
        :param label: label for the line to plot
        :return:
        """
        # q_min = 10., q_max = 50.
        # alpha = 1. - (q_now - q_min)/(q_max - q_min)
        if not label:
            label = str(plot_key)

        line_id = self.add_plot_1d(ws_name, wkspindex=0, marker=marker,
                                   color=color, line_style=style, alpha=alpha,
                                   label=label, x_label=r'r ($\AA$)', plotError=plotError)
        self._colorIndex += 1
        self._grDict[str(plot_key)] = line_id

        # check the low/max
        self.auto_scale_y()

    def _reset_y_range(self, vec_gr):
        """
        reset the Y range
        :param vec_gr:
        :return:
        """
        this_min = min(vec_gr)
        this_max = max(vec_gr)

        if self._minY is None or this_min < self._minY:
            self._minY = this_min

        if self._maxY is None or this_max > self._maxY:
            self._maxY = this_max

        return

    def _auto_rescale_y(self):
        """

        :return:
        """
        if self._minY is None or self._maxY is None:
            return

        delta_y = self._maxY - self._minY

        lower_boundary = self._minY - delta_y * 0.05
        upper_boundary = self._maxY + delta_y * 0.05

        self.setXYLimit(ymin=lower_boundary, ymax=upper_boundary)

        return

    def has_gr(self, gr_ws_name):
        """Check whether a plot of G(r) exists on the canvas
        :param gr_ws_name:
        :return:
        """
        return gr_ws_name in self._grDict

    def get_current_grs(self):
        """
        list all the G(r) plotted on the figure now
        :return:
        """
        return list(self._grDict.keys())

    def remove_gr(self, plot_key):
        """Remove a plotted G(r) from canvas
        :param plot_key: key to locate the 1-D plot on canvas
        :return: boolean, string (as error message)
        """
        # check
        assert isinstance(plot_key, str), 'Key for the plot must be a string but not %s.' % str(type(plot_key))
        if plot_key not in self._grDict:
            return False, 'Workspace %s cannot be found in GofR dictionary of canvas' % plot_key

        # get line ID
        line_id = self._grDict[plot_key]

        # remove from plot
        self.remove_line(line_id)

        # clean G(r) plot
        del self._grDict[plot_key]

        # reset min and max
        self._minY = None
        self._maxY = None

        return

    def reset_color(self):
        """Reset color scheme
        :return:
        """
        self._colorIndex = 0

    def reset(self):
        """
        Reset the canvas by deleting all lines and clean the dictionary
        Returns:
        """
        # remove all lines and reset marker/color default sequence
        self.clear_all_lines()
        self.reset_line_color_marker_index()
        self._colorIndex = 0

        # clean dictionary
        self._grDict.clear()

        return

    def update_gr(self, plot_key, ws_name, plotError=False):
        """update the value of an existing G(r)
        :param plot_key:
        :param vec_r:
        :param vec_g:
        :param vec_ge:
        :return:
        """
        # check existence
        if plot_key not in self._grDict:
            raise RuntimeError('Plot with key/workspace name {0} does not exist on plot.  Current plots are '
                               '{1}'.format(plot_key, list(self._grDict.keys())))

        # update
        line_key = self._grDict[plot_key]
        self.updateLine(ikey=line_key, wkspname=ws_name)

        # update range
        self.auto_scale_y()

        return
