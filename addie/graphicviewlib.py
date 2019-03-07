from __future__ import (absolute_import, division, print_function)
import numpy as np
import time

from qtpy.QtCore import (Signal)
from qtpy.QtGui import (QCursor)
from qtpy.QtWidgets import (QAction, QMenu)

from addie.utilities import mplgraphicsview as base


class GofRView(base.MplGraphicsView):
    """
    Graphics view for G(R)
    """

    def __init__(self, parent):
        """
        Initialization
        """
        base.MplGraphicsView.__init__(self, parent)

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

    def plot_gr(self, plot_key, vec_r, vec_g, vec_e=None, plot_error=False, color='black', style='.', marker=None,
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
        # check
        assert isinstance(plot_key, str), 'Key for the plot must be a string but not %s.' \
                                          '' % str(type(plot_key))
        assert isinstance(vec_r, np.ndarray), 'Vector(r) must be a numpy vector but not %s.' \
                                              '' % str(type(vec_r))
        assert isinstance(vec_g, np.ndarray), 'Vector(G) must be a numpy vector but not %s.' \
                                              '' % str(type(vec_g))

        # plot
        if plot_error:
            self.add_plot_1d(vec_r, vec_g, vec_e)
            raise NotImplementedError('ASAP')
        else:
            # add a plot without error
            # q_min = 10., q_max = 50.
            # alpha = 1. - (q_now - q_min)/(q_max - q_min)
            if label is None:
                label = plot_key

            line_id = self.add_plot_1d(vec_r, vec_g, marker=marker,
                                       color=color, line_style=style, alpha=alpha,
                                       label=label, x_label=r'r ($\AA$)')
            self._colorIndex += 1
            self._grDict[plot_key] = line_id
        # END-IF-ELSE

        # check the low/max
        self.auto_scale_y()

        return

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

    def update_gr(self, plot_key, vec_r, vec_g, vec_ge):
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
        self.updateLine(ikey=line_key, vecx=vec_r, vecy=vec_g)

        # update range
        self.auto_scale_y()

        return


class SofQView(base.MplGraphicsView):
    """
    Graphics view for S(Q)
    """
    # boundary moving signal (1) int for left/right boundary indicator (2)
    boundaryMoveSignal = Signal(int, float)

    # resolution of boundary indicator to be selected
    IndicatorResolution = 0.01

    def __init__(self, parent):
        """
        Initialization
        :param parent:t
        """
        self._myParent = parent

        base.MplGraphicsView.__init__(self, parent)

        # declare event handling to indicators
        self._myCanvas.mpl_connect('button_press_event', self.on_mouse_press_event)
        self._myCanvas.mpl_connect('button_release_event', self.on_mouse_release_event)
        self._myCanvas.mpl_connect('motion_notify_event', self.on_mouse_motion)

        self._mainApp = None

        # dictionary to record all the plots, key: (usually) SofQ's name, value: plot ID
        self._sqLineDict = dict()
        # S(Q) plot's information including color, marker and etc.
        self._sqPlotInfoDict = dict()

        # list of SofQ that are plot on the canvas
        self._shownSQNameList = list()

        # link signal
        # self.boundaryMoveSignal.connect(self._myParent.update_sq_boundary)

        # declare class variables for moving boundary
        self._showBoundary = False
        self._leftID = None
        self._rightID = None

        self._selectedBoundary = 0
        self._prevCursorPos = None

        return

    def get_plot_info(self, sofq_name):
        """
        get the information of a plot including color, marker and etc.
        :param sofq_name:
        :return:
        """
        # check
        assert isinstance(sofq_name, str), 'SofQ {0} must be a string but not a {1}'.format(sofq_name, type(sofq_name))

        if sofq_name not in self._sqPlotInfoDict:
            raise RuntimeError('SofQ-view does not have S(Q) plot {0}'.format(sofq_name))

        # return
        return self._sqPlotInfoDict[sofq_name]

    def get_shown_sq_names(self):
        """
        get the names of S(q) workspaces that are shown on the canvas
        Returns
        -------

        """
        return self._shownSQNameList[:]

    def is_boundary_shown(self):
        """

        Returns
        -------

        """
        return self._showBoundary

    def is_on_canvas(self, sq_name):
        """
        check whether an S(Q) is on canvas now
        Args:
            sq_name:

        Returns: boolean. True if on canvas; Otherwise False

        """
        # check input
        assert isinstance(sq_name, str), 'SofQ name %s must be a string but not of type %s.' \
                                         '' % (str(sq_name), str(type(sq_name)))

        # return
        return sq_name in self._sqLineDict

    def move_left_indicator(self, displacement, relative):
        """

        Args:
            displacement:
            relative:

        Returns:

        """
        # check
        assert isinstance(displacement, float)
        assert isinstance(relative, bool)

        if relative:
            self.move_indicator(self._leftID, displacement)
        else:
            self.set_indicator_position(self._leftID, displacement, 0)

        return

    def move_right_indicator(self, displacement, relative):
        """

        Args:
            displacement:
            relative:

        Returns:

        """
        # check
        assert isinstance(displacement, float)
        assert isinstance(relative, bool)

        if relative:
            self.move_indicator(self._rightID, displacement)
        else:
            self.set_indicator_position(self._rightID, displacement, 0)

        return

    def on_mouse_motion(self, event):
        """

        Returns
        -------

        """
        # ignore if boundary is not shown
        if not self._showBoundary:
            return

        # ignore if no boundary is selected
        if self._selectedBoundary == 0:
            return
        elif self._selectedBoundary > 2:
            raise RuntimeError('Impossible to have selected boundary mode %d' % self._selectedBoundary)

        cursor_pos = event.xdata

        # ignore if the cursor is out of canvas
        if cursor_pos is None:
            return

        cursor_displace = cursor_pos - self._prevCursorPos

        left_bound_pos = self.get_indicator_position(self._leftID)[0]
        right_bound_pos = self.get_indicator_position(self._rightID)[0]

        x_range = self.getXLimit()
        resolution = (x_range[1] - x_range[0]) * self.IndicatorResolution

        if self._selectedBoundary == 1:
            # left boundary
            new_left_bound = left_bound_pos + cursor_displace

            # return if the left boundary is too close to right
            if new_left_bound > right_bound_pos - resolution * 5:
                return

            # move left boundary
            self.move_indicator(self._leftID, cursor_displace, 0)

            # signal main
            self.boundaryMoveSignal.emit(1, new_left_bound)

        else:
            # right boundary
            new_right_bound = right_bound_pos + cursor_displace

            # return if the right boundary is too close or left to the left boundary
            if new_right_bound < left_bound_pos + resolution * 5:
                return

            # move right boundary
            self.move_indicator(self._rightID, cursor_displace, 0)

            # emit signal to the main app
            self.boundaryMoveSignal.emit(2, new_right_bound)

        # update cursor position
        self._prevCursorPos = cursor_pos

        return

    def on_mouse_press_event(self, event):
        """
        Handle mouse pressing event
        (1) left mouse: in show-boundary mode, check the action to select a boundary indicator
        (2) right mouse: pop up the menu
        Returns
        -------

        """
        # get the button
        button = event.button

        if button == 3:
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

            return
        # END-IF

        # ignore if boundary is not shown and the pressed mouse button is left or middle
        if not self._showBoundary:
            return

        # get mouse cursor x position
        mouse_x_pos = event.xdata
        if mouse_x_pos is None:
            return
        else:
            self._prevCursorPos = mouse_x_pos

        # get absolute resolution
        x_range = self.getXLimit()
        resolution = (x_range[1] - x_range[0]) * self.IndicatorResolution

        # see whether it is close enough to any boundary
        left_bound_pos = self.get_indicator_position(self._leftID)[0]
        right_bound_pos = self.get_indicator_position(self._rightID)[0]
        if abs(mouse_x_pos - left_bound_pos) < resolution:
            self._selectedBoundary = 1
        elif abs(mouse_x_pos - right_bound_pos) < resolution:
            self._selectedBoundary = 2
        else:
            self._selectedBoundary = 0
        # END-IF-ELSE

        return

    def on_mouse_release_event(self, event):
        """
        handling the event that mouse is released
        The operations include setting some flags' values
        :param event:
        :return:
        """
        # ignore if boundary is not shown
        if not self._showBoundary:
            return

        # get mouse cursor position
        self._prevCursorPos = event.xdata

        self._prevCursorPos = None
        self._selectedBoundary = 0

        return

    def plot_sq(self, sq_name, vec_q, vec_s, vec_e, sq_y_label, reset_color_mark, color=None, marker=None):
        """Plot S(Q)
        :param sq_name:
        :param vec_q:
        :param vec_s:
        :param vec_e:
        :param sq_y_label: label for Y-axis
        :param reset_color_mark:  boolean to reset color marker
        :param color:
        :param color_marker:
        :return:
        """
        # check
        assert isinstance(vec_q, np.ndarray) and isinstance(vec_s, np.ndarray),\
            'Q-vector ({0}) and S-vector ({1}) must be numpy arrays.'.format(type(vec_q), type(vec_s))

        # check whether it is a new plot or an update
        if sq_name in self._sqLineDict:
            # exiting S(q) workspace, do update
            sq_key = self._sqLineDict[sq_name]
            self.updateLine(ikey=sq_key, vecx=vec_q, vecy=vec_s)
        else:
            # new S(Q) plot on the canvas
            assert isinstance(sq_y_label, str), 'S(Q) label {0} must be a string but not a {1}.' \
                                                ''.format(sq_y_label, type(sq_y_label))

            # define color
            if color is None:
                if reset_color_mark:
                    self.reset_line_color_marker_index()
                marker, color = self.getNextLineMarkerColorCombo()
            else:
                marker = None

            # plot
            plot_id = self.add_plot_1d(vec_q, vec_s, color=color, x_label='Q', y_label=sq_y_label,
                                       marker=marker, label=sq_name)
            self._sqLineDict[sq_name] = plot_id
            self._sqPlotInfoDict[sq_name] = color, marker
            if sq_name not in self._shownSQNameList:
                self._shownSQNameList.append(sq_name)
        # END-IF-ELSE

        # auto scale
        self.auto_scale_y(room_percent=0.05, lower_boundary=0.)

        return

    def set_main(self, main_app):
        """

        Returns
        -------

        """
        self._mainApp = main_app

        # link signal
        self.boundaryMoveSignal.connect(self._mainApp.update_sq_boundary)

        return

    def remove_sq(self, sq_ws_name):
        """
        Remove 1 S(q) line from canvas
        Args:
            sq_ws_name: workspace name as plot key

        Returns:

        """
        # check whether S(Q) does exist
        assert isinstance(sq_ws_name, str), 'S(Q) workspace name {0} must be a string but not a {1}.' \
                                            ''.format(sq_ws_name, type(sq_ws_name))
        if sq_ws_name not in self._sqLineDict:
            raise RuntimeError('key (SofQ name) {0} does not exist on the S(Q) canvas.'.format(sq_ws_name))

        # retrieve the plot and remove it from the dictionary
        plot_id = self._sqLineDict[sq_ws_name]
        sq_color, sq_marker = self._sqPlotInfoDict[sq_ws_name]

        del self._sqLineDict[sq_ws_name]
        del self._sqPlotInfoDict[sq_ws_name]

        # delete from canvas
        self.remove_line(plot_id)

        # delete from on-show S(q) list
        self._shownSQNameList.remove(sq_ws_name)

        return sq_color, sq_marker

    def reset(self):
        """
        Reset the canvas including removing all the 1-D plots and boundary indicators
        Returns:

        """
        # clear the dictionary and on-show Sq list
        self._sqLineDict.clear()
        self._sqPlotInfoDict.clear()
        self._shownSQNameList = list()

        # clear the image and reset the marker/color scheme
        self.clear_all_lines()
        self.reset_line_color_marker_index()

        # clear the boundary flag
        self._showBoundary = False

        return

    def toggle_boundary(self, q_left, q_right):
        """ Turn on or off the left and right boundary to select Q-range
        Parameters
        ----------
        q_left ::
        q_right ::
        Returns
        -------

        """
        # check
        assert isinstance(q_left, float) and isinstance(q_right, float)
        assert q_left < q_right

        if self._showBoundary:
            # Q-boundary indicator is on. turn off
            self.remove_indicator(self._leftID)
            self.remove_indicator(self._rightID)
            self._leftID = None
            self._rightID = None
            self._showBoundary = False
        else:
            self._leftID = self.add_vertical_indicator(q_left, 'red')
            self._rightID = self.add_vertical_indicator(q_right, 'red')
            self._showBoundary = True

            # reset the x-range
            x_range = self.getXLimit()
            if x_range[0] > q_left - 1:
                self.setXYLimit(xmin=q_left-1)

        # END-IF-ELSE (show boundary)

        return
