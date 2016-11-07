import numpy as np

from PyQt4 import QtCore, QtGui

import mplgraphicsview as base


class BraggView(base.MplGraphicsView):
    """ Graphics view for Bragg diffraction
    """
    def __init__(self, parent):
        """
        Initialization
        Parameters
        ----------
        parent
        """
        base.MplGraphicsView.__init__(self, parent)

        # control class
        # key: bank ID, value: list of workspace names
        self._bankPlotDict = dict()
        for bank_id in range(1, 7):
            self._bankPlotDict[bank_id] = list()
        # key: workspace name. value: line ID
        self._gssDict = dict()
        # dictionary for on-canvas plot Y size
        self._plotScaleDict = dict()

        self._singleGSSMode = True
        self._bankColorDict = {1: 'black',
                               2: 'red',
                               3: 'blue',
                               4: 'green',
                               5: 'brown',
                               6: 'yellow'}

        self._gssColorList = ["black", "red", "blue", "green",
                              "cyan", "magenta", "yellow"]
        self._currColorIndex = 0

        # records of the plots on canvas
        # workspaces' names (not bank, but original workspace) on canvas
        self._workspaceSet = set()

        return

    def check_banks(self, bank_to_plot_list):
        """ Check the to-plot bank list against the current being-plot bank list,
        to find out the banks which are to plot and to be removed from plot.
        Args:
            bank_to_plot_list:
        Returns:
            2-tuple.  (1) list of banks' IDs to be plot and (2) list of
            banks' IDs to be removed from current canvas.
        """
        # check
        assert isinstance(bank_to_plot_list, list)

        new_plot_banks = bank_to_plot_list[:]
        to_remove_banks = list()

        for bank_id in self._bankPlotDict.keys():
            if len(self._bankPlotDict[bank_id]) == 0:
                # previously-not-being plot. either in new_plot_banks already or no-op
                continue
            elif bank_id in bank_to_plot_list:
                # previously-being plot, then to be removed from new-plot-list
                new_plot_banks.remove(bank_id)
            else:
                # previously-being plot, then to be removed from canvas
                to_remove_banks.append(bank_id)
        # END-FOR (bank_id)

        return new_plot_banks, to_remove_banks

    def get_ws_name_on_canvas(self, bank_id):
        """
        Get workspace' names on canvas according to its bank ID
        Args:
            bank_id: bank ID, integer between 1 and 6

        Returns: a list of workspace' names

        """
        # check input requirements
        assert isinstance(bank_id, int), 'Bank ID %s must be an integer but not %s.' \
                                         '' % (str(bank_id), str(type(bank_id)))
        assert 1 <= bank_id <= 6, 'Bank ID %d must be in [1, 6].' % bank_id

        # return
        return self._bankPlotDict[bank_id]

    def get_multi_gss_color(self):
        """
        Get the present color in multiple-GSS mode
        Returns:

        """
        color = self._gssColorList[self._currColorIndex]
        self._currColorIndex += 1
        if self._currColorIndex == len(self._gssColorList):
            self._currColorIndex = 0

        return color

    def get_workspaces(self):
        """
        Get the names of workspaces on the canvas
        Returns
        -------

        """
        return list(self._workspaceSet)

    @staticmethod
    def _generate_plot_key(ws_group_name, bank_id):
        """
        Generate a standard key for a plot from GSAS Workspace group name and bank ID
        Args:
            ws_group_name:
            bank_id:

        Returns:

        """
        # check
        assert isinstance(ws_group_name, str), 'Workspace group\'s name must be a string, but not %s.' \
                                               '' % str(type(ws_group_name))
        assert isinstance(bank_id, int), 'Bank ID %s must be an integer but not %s.' \
                                         '' % (str(bank_id), str(type(bank_id)))

        plot_key = '%s_bank%d' % (ws_group_name, bank_id)

        return plot_key

    def plot_banks(self, plot_bank_dict, unit):
        """
        Plot a few banks to canvas.  If the bank has been plot on canvas already,
        then remove the previous data
        Args:
            plot_bank_dict: dictionary: key = ws group name, value = dictionary (key = bank ID, value = (x, y, e)
            unit: string for X-range unit.  can be TOF, dSpacing or Q (momentum transfer)

        Returns:

        """
        # check
        assert isinstance(plot_bank_dict, dict)

        # plot
        for ws_group in plot_bank_dict.keys():
            # get workspace name
            ws_name = ws_group.split('_group')[0]
            self._workspaceSet.add(ws_name)

            for bank_id in plot_bank_dict[ws_group]:
                # add the new plot
                if self._singleGSSMode:
                    bank_color = self._bankColorDict[bank_id]
                else:
                    bank_color = self.get_multi_gss_color()
                vec_x, vec_y, vec_e = plot_bank_dict[ws_group][bank_id]
                print '[DB...BAT] Plot ', ws_group, bank_id
                plot_id = self.add_plot_1d(vec_x, vec_y, marker=None, color=bank_color,
                                           x_label=unit, y_label='I(%s)' % unit,
                                           label='%s Bank %d' % (ws_group, bank_id))

                # plot key
                plot_key = self._generate_plot_key(ws_group, bank_id)
                self._bankPlotDict[bank_id].append(plot_key)
                self._gssDict[plot_key] = plot_id
                self._plotScaleDict[plot_id] = (min(vec_y), max(vec_y))
            # END-FOR (bank id)
        # END-FOR (ws_group)

        #  self.scale_auto()

        return

    def plot_general_ws(self, bragg_ws_name, vec_x, vec_y, vec_e):
        """
        Plot a workspace that does not belong to any workspace group
        Parameters
        ----------
        bragg_ws_name
        vec_x
        vec_y
        vec_e

        Returns
        -------

        """
        # register
        self._workspaceSet.add(bragg_ws_name)

        # plot
        plot_id = self.add_plot_1d(vec_x, vec_y, marker=None, color='black',
                                   label=bragg_ws_name)
        self._plotScaleDict[plot_id] = (min(vec_y), max(vec_y))

        # scale the plot automatically
        self.scale_auto()

        return

    def remove_gss_banks(self, ws_group_name, bank_id_list):
        """
        Remove a few bank ID from Bragg plot
        Args:
            ws_group_name: workspace group name as bank ID
            bank_id_list:

        Returns: error message (empty string for non-error)

        """
        # check
        assert isinstance(bank_id_list, list)

        # remove line from canvas
        error_message = ''
        for bank_id in bank_id_list:
            # check bank ID type
            assert isinstance(bank_id, int), 'Bank ID %s must be an integer but not a %s.' % (str(bank_id),
                                                                                              str(type(bank_id)))
            # from bank ID key
            plot_key = self._generate_plot_key(ws_group_name, bank_id)

            # line is not plot
            if plot_key not in self._gssDict:
                error_message += 'Workspace %s Bank %d is not on canvas to delete.\n' % (ws_group_name, bank_id)
                continue

            bank_line_id = self._gssDict[plot_key]
            # remove from canvas
            try:
                self.remove_line(bank_line_id)
            except ValueError as val_error:
                error_message = 'Unable to remove bank %d plot (ID = %d) due to %s.' % (bank_id,
                                                                                        bank_line_id,
                                                                                        str(val_error))
                raise ValueError(error_message)
            # remove from data structure
            del self._gssDict[plot_key]
            del self._plotScaleDict[bank_line_id]
            self._bankPlotDict[bank_id].remove(plot_key)
        # END-FOR

        # scale automatically
        # self.scale_auto()

        # debug output
        db_buf = ''
        for bank_id in self._bankPlotDict:
            db_buf += '%d: %s \t' % (bank_id, str(self._bankPlotDict[bank_id]))
        print 'After removing %s, Buffer: %s.' % (str(bank_id_list), db_buf)

        return error_message

    def reset(self):
        """
        Reset the canvas for new Bragg data
        Returns:
        None
        """
        # clean the dictionaries
        for bank_id in self._bankPlotDict.keys():
            self._bankPlotDict[bank_id] = list()
        self._gssDict.clear()
        self._plotScaleDict.clear()

        # clear the workspace record
        self._workspaceSet.clear()

        # clear all lines and reset color/marker counter
        self.clear_all_lines()
        self.reset_line_color_marker_index()
        self._currColorIndex = 0

        return

    def reset_color(self):
        """
        Reset color index
        Returns
        -------

        """
        self._currColorIndex = 0

    def scale_auto(self):
        """ Scale automatically for the plots on the canvas
        Args:

        Returns: None

        """
        # get Y min and Y max
        y_min = 0
        y_max = 0
        for plot_id in self._plotScaleDict.keys():
            if self._plotScaleDict[plot_id][1] > y_max:
                y_max = self._plotScaleDict[plot_id][1]

        # determine the canvas Y list
        upper_y = y_max * 1.05

        # set limit
        self.setXYLimit(ymin=y_min, ymax=upper_y)

        return

    def set_to_single_gss(self, mode_on):
        """
        Set to single-GSAS/multiple-bank model
        Args:
            mode_on:

        Returns:

        """
        assert isinstance(mode_on, bool)

        self._singleGSSMode = mode_on

        return


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

        # define the dynamic menu
        self._myCanvas.mpl_connect('button_press_event', self.on_mouse_press_event)
        self._myCanvas.mpl_connect('button_release_event', self.on_mouse_release_event)
        self._myCanvas.mpl_connect('motion_notify_event', self.on_mouse_motion)

        # variable
        self._isLegendOn = False

        return

    # TODO/FIXME/NOW - Make it complete!
    def on_mouse_press_event(self, event):
        """
        blabla
        Args:
            event:

        Returns:

        """
        button = event.button

        curr_x = event.xdata
        curr_y = event.ydata
        if curr_x is None or curr_y is None:
            # outside of canvas
            return

        if button == 1:
            # left button: no operation
            pass

        elif button == 3:
            # right button:
            # Pop-out menu
            self.menu = QtGui.QMenu(self)

            action1 = QtGui.QAction('Remove legend', self)
            action1.triggered.connect(self.menu_remove_legend)
            self.menu.addAction(action1)

            # add other required actions
            self.menu.popup(QtGui.QCursor.pos())
        # END-IF-ELSE

        return

    def menu_remove_legend(self):
        """
        blabla
        Returns:

        """
        return

    def on_mouse_release_event(self, event):
        """
        blabla
        Args:
            event:

        Returns:

        """
        return

    def on_mouse_motion(self, event):
        """
        blabla
        Args:
            event:

        Returns:

        """

    def plot_gr(self, plot_key, vec_r, vec_g, vec_e=None, plot_error=False):
        """
        Plot G(r)
        Parameters
        -------
        plot_key: a key to the current plot
        vec_r: numpy array for R
        vec_g: numpy array for G(r)
        vec_e: numpy array for G(r) error
        Returns
        -------

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
            line_id = self.add_plot_1d(vec_r, vec_g, marker=None,
                                       color=self._colorList[self._colorIndex % len(self._colorList)],
                                       label=plot_key,
                                       x_label=r'r ($\AA$)')
            self._colorIndex += 1
            self._grDict[plot_key] = line_id

        return

    def remove_gr(self, plot_key):
        """

        Parameters
        ----------
        plot_key :: key to locate the 1-D plot on canvas

        Returns :: boolean, string (as error message)
        -------

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

        return

    def reset_color(self):
        """
        Reset color scheme
        Returns
        -------

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


class SofQView(base.MplGraphicsView):
    """
    Graphics view for S(Q)
    """
    # boundary moving signal (1) int for left/right boundary indicator (2)
    boundaryMoveSignal = QtCore.pyqtSignal(int, float)

    # resolution of boundary indicator to be selected
    IndicatorResolution = 0.01

    def __init__(self, parent):
        """
        Initialization
        Parameters
        ----------
        parent
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

        # link signal
        # self.boundaryMoveSignal.connect(self._myParent.update_sq_boundary)

        # declare class variables for moving boundary
        self._showBoundary = False
        self._leftID = None
        self._rightID = None

        self._selectedBoundary = 0
        self._prevCursorPos = None

        return

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
        print event.xdata

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

        Returns
        -------

        """
        # ignore if boundary is not shown
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

        Returns
        -------

        """
        # ignore if boundary is not shown
        if not self._showBoundary:
            return

        # get mouse cursor position
        self._prevCursorPos = event.xdata

        self._prevCursorPos = None
        self._selectedBoundary = 0

        return

    def plot_sq(self, sq_name, vec_q, vec_s, vec_e, sq_y_label, reset_color_mark):
        """
        Plot S(Q)
        Parameters
        ----------
        sq_name:
        vec_q
        vec_s
        vec_e
        sq_y_label :: label for Y-axis
        reset_color_mark : boolean to reset color marker

        Returns
        -------

        """
        # check
        assert isinstance(vec_q, np.ndarray) and isinstance(vec_s, np.ndarray)
        assert isinstance(sq_y_label, str)

        # define color
        if reset_color_mark:
            self.reset_line_color_marker_index()
        marker, color = self.getNextLineMarkerColorCombo()

        # plot
        plot_id = self.add_plot_1d(vec_q, vec_s, color=color, x_label='Q', y_label=sq_y_label,
                                   marker=None, label=sq_name)
        self._sqLineDict[sq_name] = plot_id

        return

    def remove_sq(self, plot_key):
        """
        Remove 1 S(q) line from canvas
        Args:
            plot_key:

        Returns:

        """
        # check whether S(Q) does exist
        assert isinstance(plot_key, str)
        assert plot_key in self._sqLineDict, 'Plot key (SofQ name) %s does not exist on the S(Q) canvas.' % plot_key

        # retrieve the plot and remove it from the dictionary
        plot_id = self._sqLineDict[plot_key]
        del self._sqLineDict[plot_key]

        # delete from canvas
        self.remove_line(plot_id)

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

    def reset(self):
        """
        Reset the canvas including removing all the 1-D plots and boundary indicators
        Returns:

        """
        # clear the dictionary
        self._sqLineDict.clear()

        # clear the image and reset the marker/color scheme
        self.clear_all_lines()
        self.reset_line_color_marker_index()

        return

