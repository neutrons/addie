from __future__ import (absolute_import, division, print_function)

from qtpy.QtCore import (Signal)
from qtpy.QtGui import (QCursor)
from qtpy.QtWidgets import (QAction, QMenu)

from addie.plot import MplGraphicsView


class SofQView(MplGraphicsView):
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

        MplGraphicsView.__init__(self, parent)

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

    def plot_sq(self, ws_name,
                sq_y_label=None, reset_color_mark=None,
                color=None, marker=None, plotError=False):
        """Plot S(Q)
        :param sq_name:
        :param sq_y_label: label for Y-axis
        :param reset_color_mark:  boolean to reset color marker
        :param color:
        :param color_marker:
        :return:
        """
        # check whether it is a new plot or an update
        if ws_name in self._sqLineDict:
            # exiting S(q) workspace, do update
            sq_key = self._sqLineDict[ws_name]
            self.updateLine(ikey=sq_key, wkspname=ws_name, wkspindex=0)
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
            plot_id = self.add_plot_1d(ws_name, wkspindex=0, color=color, x_label='Q', y_label=sq_y_label,
                                       marker=marker, label=ws_name, plotError=plotError)
            self._sqLineDict[ws_name] = plot_id
            self._sqPlotInfoDict[ws_name] = color, marker
            if ws_name not in self._shownSQNameList:
                self._shownSQNameList.append(ws_name)

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
