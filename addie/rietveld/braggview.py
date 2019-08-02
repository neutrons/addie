from __future__ import (absolute_import, division, print_function)
import time

from qtpy.QtGui import (QCursor)
from qtpy.QtWidgets import (QAction, QMenu)

from addie.plot import MplGraphicsView
from addie.addiedriver import AddieDriver
import addie.utilities.workspaces


class BraggView(MplGraphicsView):
    """ Graphics view for Bragg diffraction
    """

    def __init__(self, parent):
        """
        Initialization
        Parameters
        ----------
        parent
        """
        MplGraphicsView.__init__(self, parent)
        self._driver = AddieDriver()

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
                               6: 'orange'}

        # color sequence for multiple GSAS mode
        self._gssColorList = ["black", "red", "blue", "green",
                              "cyan", "magenta", "yellow"]
        self._gssLineStyleList = ['-', '--', '-.']
        self._gssLineMarkers = ['.', 'D', 'o', 's', 'x']

        # a dictionary to manage the GSAS plot's color and marker
        self._gssLineDict = dict()  # key: GSAS workspace name. value:
        self._gssLineColorMarkerDict = dict()

        self._currColorStyleMarkerIndex = 0

        # define the dynamic menu
        self._myCanvas.mpl_connect(
            'button_press_event',
            self.on_mouse_press_event)

        # records of the plots on canvas
        # workspaces' names (not bank, but original workspace) on canvas
        self._workspaceSet = set()

        # unit
        self._unitX = None

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

        for bank_id in list(self._bankPlotDict.keys()):
            if len(self._bankPlotDict[bank_id]) == 0:
                # previously-not-being plot. either in new_plot_banks already
                # or no-op
                continue
            elif bank_id in bank_to_plot_list:
                # previously-being plot, then to be removed from new-plot-list
                new_plot_banks.remove(bank_id)
            else:
                # previously-being plot, then to be removed from canvas
                to_remove_banks.append(bank_id)

        return new_plot_banks, to_remove_banks

    def set_unit(self, x_unit):
        """
        set the unit of the powder diffraction pattern
        Parameters
        ----------
        x_unit

        Returns
        -------

        """
        assert isinstance(x_unit, str), 'Unit of X-axis {0} must be a string but not a {1}.' \
                                        ''.format(x_unit, type(x_unit))
        if x_unit not in ['TOF', 'MomentumTransfer', 'dSpacing']:
            raise RuntimeError(
                'Unit {0} of X-axis is not recognized.'.format(x_unit))

        self._unitX = x_unit

        return

    def evt_toolbar_home(self):
        """
        override the behavior if a tool bar's HOME button is pressed
        Returns
        -------

        """
        time.sleep(0.1)

        # call the super
        super(BraggView, self).evt_toolbar_home()

        # if it is first time in this region
        if self._homeXYLimit is None:
            if self._unitX == 'TOF':
                self.setXYLimit(xmin=0, xmax=20000, ymin=None, ymax=None)
            elif self._unitX == 'MomentumTransfer':
                self.setXYLimit(xmin=0, xmax=20, ymin=None, ymax=None)
            elif self._unitX == 'dSpacing':
                self.setXYLimit(xmin=0, xmax=7, ymin=None, ymax=None)
            else:
                raise RuntimeError('Unit %s unknown' % self._unitX)

        return

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
        Get the present color and line style in multiple-GSS mode
        Returns:
        """
        # get basic statistic
        num_marker = len(self._gssLineMarkers)
        num_style = len(self._gssLineStyleList)
        num_color = len(self._gssColorList)

        print('[DB] Index = ', self._currColorStyleMarkerIndex)

        # get color with current color index
        value = num_style * num_color
        marker_value = self._currColorStyleMarkerIndex / value
        marker_index = int(marker_value)

        style_value = self._currColorStyleMarkerIndex % value / num_color
        style_index = int(style_value)

        color_value = self._currColorStyleMarkerIndex % value % num_color
        color_index = int(color_value)

        color = self._gssColorList[color_index]
        style = self._gssLineStyleList[style_index]
        marker = self._gssLineMarkers[marker_index]

        # advance to next index but reset if reaches limit
        self._currColorStyleMarkerIndex += 1
        # reset
        if self._currColorStyleMarkerIndex == num_color * num_style * num_marker:
            self._currColorStyleMarkerIndex = 0

        return color, style, marker

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

    def on_mouse_press_event(self, event):
        """
        handle mouse pressing event
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
                action2.triggered.connect(
                    self._myCanvas.increase_legend_font_size)

                action3 = QAction('Legend font smaller', self)
                action3.triggered.connect(
                    self._myCanvas.decrease_legend_font_size)

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

    def plot_banks(self, plot_bank_dict, unit):
        """
        Plot a few banks to canvas.  If the bank has been plot on canvas already,
        then remove the previous data
        Args:
            plot_bank_dict: dictionary: key = ws group name, value = banks to show
            unit: string for X-range unit.  can be TOF, dSpacing or Q (momentum transfer)
        """
        # check
        assert isinstance(plot_bank_dict, dict)

        # plot
        for ws_name in list(plot_bank_dict.keys()):
            self._driver.convert_bragg_data(ws_name, unit)

            # get workspace name
            self._workspaceSet.add(ws_name)

            for bank_id in plot_bank_dict[ws_name]:
                # determine the color/marker/style of the line - shouldn't be
                # special
                if self._singleGSSMode:
                    # single bank mode
                    bank_color = self._bankColorDict[bank_id]
                    marker = None
                    style = None
                else:
                    # multiple bank mode
                    bank_color, style, marker = self.get_multi_gss_color()

                print(
                    '[DB...BAT] Plot Mode (single bank) = {0}, group = {1}, bank = {2}, color = {3}, marker = {4},'
                    'style = {5}'
                    ''.format(
                        self._singleGSSMode,
                        ws_name,
                        bank_id,
                        bank_color,
                        marker,
                        style))

                # plot
                plot_id = self.add_plot_1d(
                    ws_name,
                    wkspindex=bank_id - 1,
                    marker=marker,
                    color=bank_color,
                    line_style=style,
                    x_label=unit,
                    y_label='I({0})'.format(unit),
                    label='%s Bank %d' % (ws_name, bank_id)
                )

                # plot key
                plot_key = self._generate_plot_key(ws_name, bank_id)
                self._bankPlotDict[bank_id].append(plot_key)
                self._gssDict[plot_key] = plot_id
                self._plotScaleDict[plot_id] = addie.utilities.workspaces.get_y_range(
                    ws_name, bank_id - 1)  # is this needed?

        # self.scale_auto()

    def plot_general_ws(self, ws_name):
        """
        Plot a workspace that does not belong to any workspace group
        Parameters
        """
        # register
        self._workspaceSet.add(ws_name)

        # plot
        plot_id = self.add_plot_1d(
            ws_name,
            wkspindex=0,
            marker=None,
            color='black',
            label=ws_name)
        self._plotScaleDict[plot_id] = addie.utilities.workspaces.get_y_range(
            ws_name, 0)

        # scale the plot automatically
        self.scale_auto()

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
            bank_id = int(bank_id)

            # from bank ID key
            plot_key = self._generate_plot_key(ws_group_name, bank_id)

            # line is not plot
            if plot_key not in self._gssDict:
                error_message += 'Workspace %s Bank %d is not on canvas to delete.\n' % (
                    ws_group_name, bank_id)
                continue

            bank_line_id = self._gssDict[plot_key]
            # remove from canvas
            try:
                self.remove_line(bank_line_id)
            except ValueError as val_error:
                error_message = 'Unable to remove bank %d plot (ID = %d) due to %s.' % (
                    bank_id, bank_line_id, str(val_error))
                raise ValueError(error_message)
            # remove from data structure
            del self._gssDict[plot_key]
            del self._plotScaleDict[bank_line_id]
            self._bankPlotDict[bank_id].remove(plot_key)

        # scale automatically
        # self.scale_auto()

        # debug output
        db_buf = ''
        for bank_id in self._bankPlotDict:
            db_buf += '%d: %s \t' % (bank_id, str(self._bankPlotDict[bank_id]))
        print('After removing %s, Buffer: %s.' % (str(bank_id_list), db_buf))

        return error_message

    def reset(self):
        """
        Reset the canvas for new Bragg data
        Returns:
        None
        """
        # clean the dictionaries
        for bank_id in list(self._bankPlotDict.keys()):
            self._bankPlotDict[bank_id] = list()
        self._gssDict.clear()
        self._plotScaleDict.clear()

        # clear the workspace record
        self._workspaceSet.clear()

        # clear all lines and reset color/marker counter
        self.clear_all_lines()
        self.reset_line_color_marker_index()
        self._currColorIndex = 0

    def reset_color(self):
        """
        Reset color, line style and marker index
        Returns
        -------

        """
        self._currColorStyleMarkerIndex = 0

    def scale_auto(self):
        """Scale automatically for the plots on the canvas
        """
        # get Y min and Y max
        y_min = min(0., self._plotScaleDict.values()
                    [0][0])  # always include zero
        y_max = self._plotScaleDict.values()[0][1]
        for temp_min, temp_max in self._plotScaleDict.values():
            y_min = min(y_min, temp_min)
            y_max = max(y_max, temp_max)

        # determine the canvas Y list
        upper_y = y_max * 1.05

        # set limit
        self.setXYLimit(ymin=y_min, ymax=upper_y)

    def set_to_single_gss(self, mode_on):
        """
        Set to single-GSAS/multiple-bank model
        Args:
            mode_on:

        Returns:

        """
        assert isinstance(mode_on, bool), 'Single GSAS mode {0} must be a boolean but not a {1}.' \
                                          ''.format(mode_on, type(mode_on))

        self._singleGSSMode = mode_on

        if mode_on is False:
            # set to multiple GSAS mode
            self._currColorStyleMarkerIndex = 0
