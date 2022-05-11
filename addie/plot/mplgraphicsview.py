# pylint: disable=invalid-name,too-many-public-methods,too-many-arguments,non-parent-init-called,R0902,too-many-branches,C0302
from __future__ import (absolute_import, division, print_function)
import os
import numpy as np

from qtpy.QtWidgets import QVBoxLayout, QWidget

from addie.plot import IndicatorManager, NavigationToolbar
from addie.plot import FigureCanvas
from addie.plot.constants import BASIC_COLORS, LINE_MARKERS, LINE_STYLES
import addie.utilities.workspaces
import mantid.simpleapi as simpleapi


class MplGraphicsView(QWidget):
    """ A combined graphics view including matplotlib canvas and
    a navigation tool bar

    Note: Merged with HFIR_Powder_Reduction.MplFigureCanvas
    """

    def __init__(self, parent):
        # Initialize parent
        QWidget.__init__(self, parent)

        # set up canvas
        self._myCanvas = FigureCanvas(self)
        self._myToolBar = NavigationToolbar(self, self._myCanvas)

        # state of operation
        self._isZoomed = False
        # X and Y limit with home button
        self._homeXYLimit = None

        # set up layout
        self._vBox = QVBoxLayout(self)
        self._vBox.addWidget(self._myCanvas)
        self._vBox.addWidget(self._myToolBar)

        # auto line's maker+color list
        self._myLineMarkerColorList = []
        self._myLineMarkerColorIndex = 0
        self.setAutoLineMarkerColorCombo()

        # records for all the lines that are plot on the canvas
        self._my1DPlotDict = dict()
        self._my1DPlotMinYDict = dict()
        self._my1DPlotMaxYDict = dict()

        # Declaration of class variables
        self._indicatorKey = None

        # Indicator manager
        self._myIndicatorsManager = IndicatorManager()

        # some statistic recorder for convenient operation
        self._statDict = dict()

    def add_arrow(self, start_x, start_y, stop_x, stop_y):
        self._myCanvas.add_arrow(start_x, start_y, stop_x, stop_y)

    def add_line_set(self, vec_set, color, marker, line_style, line_width):
        """ Add a set of line and manage together
        """
        key_list = list()
        bd_tmp_list = []
        i = 0
        for vec_x, vec_y in vec_set:
            bd_tmp_list.append(simpleapi.CreateWorkspace(DataX=vec_x, DataY=vec_y, NSpec=1))
            temp_key = self._myCanvas.add_plot_1d(wkspname=bd_tmp_list[i], wkspindex=0, color=color, marker=marker,
                                                  line_style=line_style, line_width=line_width)
            assert isinstance(temp_key, int)
            assert temp_key >= 0
            key_list.append(temp_key)
            i += 1

        return key_list

    # TODO change this to pass down the workspace handle
    def add_plot_1d(self, wkspname, wkspindex, color=None, label='', x_label=None, y_label=None,
                    marker=None, line_style=None, line_width=1, alpha=1., show_legend=True, plotError=False):
        """
        Add a 1-D plot to canvas
        """
        line_key = self._myCanvas.add_plot_1d(wkspname, wkspindex, color, label, x_label, y_label, marker, line_style,
                                              line_width, alpha, show_legend)

        xmin, xmax, ymin, ymax = addie.utilities.workspaces.get_xy_range(wkspname, wkspindex)

        # record min/max
        self._statDict[line_key] = xmin, xmax, ymin, ymax
        self._my1DPlotDict[line_key] = label

        self._my1DPlotMinYDict[line_key] = ymin
        self._my1DPlotMaxYDict[line_key] = ymax

        return line_key

    def add_2way_indicator(self, x=None, y=None, color=None, master_line=None):
        """ Add a 2-way indicator following an existing line?
        """
        if master_line is not None:
            raise RuntimeError('Implement how to use master_line ASAP.')

        x_min, x_max = self._myCanvas.getXLimit()
        if x is None:
            x = (x_min + x_max) * 0.5
        else:
            assert isinstance(x, float)

        y_min, y_max = self._myCanvas.getYLimit()
        if y is None:
            y = (y_min + y_max) * 0.5
        else:
            assert isinstance(y, float)

        if color is None:
            color = self._myIndicatorsManager.get_next_color()
        else:
            assert isinstance(color, str)

        my_id = self._myIndicatorsManager.add_2way_indicator(x, x_min, x_max,
                                                             y, y_min, y_max,
                                                             color)
        vec_set = self._myIndicatorsManager.get_2way_data(my_id)

        canvas_line_index = self.add_line_set(vec_set, color=color,
                                              marker=self._myIndicatorsManager.get_marker(),
                                              line_style=self._myIndicatorsManager.get_line_style(),
                                              line_width=1)
        self._myIndicatorsManager.set_canvas_line_index(my_id, canvas_line_index)

        return my_id

    def add_horizontal_indicator(self, y=None, color=None):
        """ Add an indicator line
        """
        # Default
        if y is None:
            y_min, y_max = self._myCanvas.getYLimit()
            y = (y_min + y_max) * 0.5
        else:
            assert isinstance(y, float)

        x_min, x_max = self._myCanvas.getXLimit()

        # For color
        if color is None:
            color = self._myIndicatorsManager.get_next_color()
        else:
            assert isinstance(color, str)

        # Form
        my_id = self._myIndicatorsManager.add_horizontal_indicator(y, x_min, x_max, color)
        vec_x, vec_y = self._myIndicatorsManager.get_data(my_id)

        bd_tmp_h = simpleapi.CreateWorkspace(DataX=vec_x, DataY=vec_y, NSpec=1)

        canvas_line_index = self._myCanvas.add_plot_1d(wkspname=bd_tmp_h, wkspindex=0,
                                                       color=color, marker=self._myIndicatorsManager.get_marker(),
                                                       line_style=self._myIndicatorsManager.get_line_style(),
                                                       line_width=1)

        self._myIndicatorsManager.set_canvas_line_index(my_id, canvas_line_index)

        return my_id

    def add_vertical_indicator(self, x=None, color=None, style=None, line_width=1):
        """
        Add a vertical indicator line
        Guarantees: an indicator is plot and its ID is returned
        :param x: None as the automatic mode using default from middle of canvas
        :param color: None as the automatic mode using default
        :param style:
        :return: indicator ID
        """
        # For indicator line's position
        if x is None:
            x_min, x_max = self._myCanvas.getXLimit()
            x = (x_min + x_max) * 0.5
        else:
            assert isinstance(x, float)

        y_min, y_max = self._myCanvas.getYLimit()

        # For color
        if color is None:
            color = self._myIndicatorsManager.get_next_color()
        else:
            assert isinstance(color, str)

        # style
        if style is None:
            style = self._myIndicatorsManager.get_line_style()

        # Form
        my_id = self._myIndicatorsManager.add_vertical_indicator(x, y_min, y_max, color)
        vec_x, vec_y = self._myIndicatorsManager.get_data(my_id)

        bd_tmp = simpleapi.CreateWorkspace(DataX=vec_x, DataY=vec_y, NSpec=1)

        canvas_line_index = self._myCanvas.add_plot_1d(wkspname=bd_tmp, wkspindex=0,
                                                       color=color, marker=self._myIndicatorsManager.get_marker(),
                                                       line_style=self._myIndicatorsManager.get_line_style(),
                                                       line_width=1)

        self._myIndicatorsManager.set_canvas_line_index(my_id, canvas_line_index)

        return my_id

    def add_plot_2d(self, array2d, x_min, x_max, y_min, y_max, hold_prev_image=True, y_tick_label=None):
        """
        Add a 2D image to canvas
        :param array2d: numpy 2D array
        :param x_min:
        :param x_max:
        :param y_min:
        :param y_max:
        :param hold_prev_image:
        :param y_tick_label:
        :return:
        """
        self._myCanvas.addPlot2D(array2d, x_min, x_max, y_min, y_max, hold_prev_image, y_tick_label)

    def addImage(self, imagefilename):
        """ Add an image by file
        """
        # check
        if os.path.exists(imagefilename) is False:
            raise NotImplementedError("Image file %s does not exist." % (imagefilename))

        self._myCanvas.addImage(imagefilename)

    def auto_scale_y(self, room_percent=0.05, lower_boundary=None, upper_boundary=None):
        """
        auto scale along Y axis by checking all the min/max value of current plotted Y values
        :param room_percent ::  percentage of the room left
        :return:
        """
        # min and max list
        min_y_list = list()
        max_y_list = list()
        for plot_key in self._my1DPlotMinYDict:
            min_y_list.append(self._my1DPlotMinYDict[plot_key])
            max_y_list.append(self._my1DPlotMaxYDict[plot_key])

        # find min and max
        min_y = np.min(np.array(min_y_list))
        max_y = np.max(np.array(max_y_list))
        delta_y = max_y - min_y

        # find out lower and upper boundaries
        low_y_boundary = min_y - room_percent * delta_y
        upp_y_boundary = max_y + room_percent * delta_y
        if lower_boundary is not None and lower_boundary < low_y_boundary:
            low_y_boundary = lower_boundary
        if upper_boundary is not None and upper_boundary:
            upp_y_boundary = upper_boundary

        # scale to set y limits
        self.setXYLimit(ymin=low_y_boundary, ymax=upp_y_boundary)

    def canvas(self):
        """ Get the canvas
        """
        return self._myCanvas

    def clear_all_lines(self):
        self._myCanvas.clear_all_1d_plots()

        self._statDict.clear()
        self._my1DPlotDict.clear()

        self._my1DPlotMinYDict.clear()
        self._my1DPlotMaxYDict.clear()

        # about zoom
        self._isZoomed = False
        self._homeXYLimit = None

    def clear_canvas(self):
        """ Clear canvas: it includes clear_all_lines()
        """
        # clear all the records
        self.clear_all_lines()

        return self._myCanvas.clear_canvas()

    def draw(self):
        """ Draw to commit the change
        """
        return self._myCanvas.draw()

    def evt_toolbar_home(self):
        """ event for homing key of tool bar
        """
        # turn off zoom mode
        self._isZoomed = False

    def evt_view_updated(self):
        """ Event handling as canvas size updated
        :return:
        """
        # update the indicator
        new_x_range = self.getXLimit()
        new_y_range = self.getYLimit()

        self._myIndicatorsManager.update_indicators_range(new_x_range, new_y_range)
        for indicator_key in self._myIndicatorsManager.get_live_indicator_ids():
            canvas_line_id = self._myIndicatorsManager.get_canvas_line_index(indicator_key)
            data_x, data_y = self._myIndicatorsManager.get_data(indicator_key)
            self._myCanvas.updateLine(ikey=canvas_line_id, vecx=data_x, vecy=data_x)

    def evt_zoom_released(self):
        """
        event for zoom is release
        """
        # record home XY limit if it is never zoomed
        if self._isZoomed is False:
            self._homeXYLimit = list(self.getXLimit())
            self._homeXYLimit.extend(list(self.getYLimit()))
        # END-IF

        # set the state of being zoomed
        self._isZoomed = True

    def getPlot(self):
        return self._myCanvas.getPlot()

    def getLastPlotIndexKey(self):
        """ Get ...
        """
        return self._myCanvas.getLastPlotIndexKey()

    def getXLimit(self):
        """ Get limit of Y-axis
        :return: 2-tuple as xmin, xmax
        """
        return self._myCanvas.getXLimit()

    def getYLimit(self):
        """ Get limit of Y-axis
        """
        return self._myCanvas.getYLimit()

    def get_y_min(self):
        """
        Get the minimum Y value of the plots on canvas
        """
        if len(self._statDict) == 0:
            return 1E10

        line_id_list = list(self._statDict.keys())
        min_y = self._statDict[line_id_list[0]][2]
        for i_plot in range(1, len(line_id_list)):
            if self._statDict[line_id_list[i_plot]][2] < min_y:
                min_y = self._statDict[line_id_list[i_plot]][2]

        return min_y

    def get_y_max(self):
        """
        Get the maximum Y value of the plots on canvas
        :return:
        """
        if len(self._statDict) == 0:
            return -1E10

        line_id_list = list(self._statDict.keys())
        max_y = self._statDict[line_id_list[0]][3]
        for i_plot in range(1, len(line_id_list)):
            if self._statDict[line_id_list[i_plot]][3] > max_y:
                max_y = self._statDict[line_id_list[i_plot]][3]

        return max_y

    def move_indicator(self, line_id, dx, dy):
        """
        Move the indicator line in horizontal
        """
        # Shift value
        self._myIndicatorsManager.shift(line_id, dx=dx, dy=dy)

        # apply to plot on canvas
        if self._myIndicatorsManager.get_line_type(line_id) < 2:
            # horizontal or vertical
            canvas_line_index = self._myIndicatorsManager.get_canvas_line_index(line_id)
            vec_x, vec_y = self._myIndicatorsManager.get_data(line_id)
            self._myCanvas.updateLine(ikey=canvas_line_index, vecx=vec_x, vecy=vec_y)
        else:
            # 2-way
            canvas_line_index_h, canvas_line_index_v = self._myIndicatorsManager.get_canvas_line_index(line_id)
            h_vec_set, v_vec_set = self._myIndicatorsManager.get_2way_data(line_id)

            self._myCanvas.updateLine(ikey=canvas_line_index_h, vecx=h_vec_set[0], vecy=h_vec_set[1])
            self._myCanvas.updateLine(ikey=canvas_line_index_v, vecx=v_vec_set[0], vecy=v_vec_set[1])

    def remove_indicator(self, indicator_key):
        """ Remove indicator line
        """
        #
        plot_id = self._myIndicatorsManager.get_canvas_line_index(indicator_key)
        self._myCanvas.remove_plot_1d(plot_id)
        self._myIndicatorsManager.delete(indicator_key)

    def remove_line(self, line_id):
        """ Remove a line
        """
        # remove line
        self._myCanvas.remove_plot_1d(line_id)

        # remove the records
        if line_id in self._statDict:
            del self._statDict[line_id]
            del self._my1DPlotDict[line_id]
            del self._my1DPlotMinYDict[line_id]
            del self._my1DPlotMaxYDict[line_id]

    def set_indicator_position(self, line_id, pos_x, pos_y):
        """ Set the indicator to new position
        """
        # Set value
        self._myIndicatorsManager.set_position(line_id, pos_x, pos_y)

        # apply to plot on canvas
        if self._myIndicatorsManager.get_line_type(line_id) < 2:
            # horizontal or vertical
            canvas_line_index = self._myIndicatorsManager.get_canvas_line_index(line_id)
            vec_x, vec_y = self._myIndicatorsManager.get_data(line_id)
            self._myCanvas.updateLine(ikey=canvas_line_index, vecx=vec_x, vecy=vec_y)
        else:
            # 2-way
            canvas_line_index_h, canvas_line_index_v = self._myIndicatorsManager.get_canvas_line_index(line_id)
            h_vec_set, v_vec_set = self._myIndicatorsManager.get_2way_data(line_id)

            self._myCanvas.updateLine(ikey=canvas_line_index_h, vecx=h_vec_set[0], vecy=h_vec_set[1])
            self._myCanvas.updateLine(ikey=canvas_line_index_v, vecx=v_vec_set[0], vecy=v_vec_set[1])

    def updateLine(self, ikey, wkspname='', wkspindex=0, linestyle=None, linecolor=None, marker=None, markercolor=None):
        """update a line's set up
        """

        # check
        assert isinstance(ikey, int), 'Line key must be an integer.'
        assert ikey in self._my1DPlotDict, 'Line with ID %d is not on canvas. ' % ikey

        # update line
        if wkspname:
            ymin, ymax = addie.utilities.workspaces.get_y_range(wkspname, wkspindex)
            self._my1DPlotMinYDict[ikey] = ymin
            self._my1DPlotMaxYDict[ikey] = ymax
        self._myCanvas.updateLine(ikey=ikey, wkspname=wkspname, wkspindex=wkspindex,
                                  linestyle=linestyle, linecolor=linecolor, marker=marker,
                                  markercolor=markercolor)

    def update_indicator(self, i_key, color):
        """
        Update indicator with new color
        """
        if self._myIndicatorsManager.get_line_type(i_key) < 2:
            # horizontal or vertical
            canvas_line_index = self._myIndicatorsManager.get_canvas_line_index(i_key)
            self._myCanvas.updateLine(ikey=canvas_line_index, vecx=None, vecy=None, linecolor=color)
        else:
            # 2-way
            canvas_line_index_h, canvas_line_index_v = self._myIndicatorsManager.get_canvas_line_index(i_key)
            # h_vec_set, v_vec_set = self._myIndicatorsManager.get_2way_data(i_key)

            self._myCanvas.updateLine(ikey=canvas_line_index_h, vecx=None, vecy=None, linecolor=color)
            self._myCanvas.updateLine(ikey=canvas_line_index_v, vecx=None, vecy=None, linecolor=color)

    def get_canvas(self):
        """
        get canvas
        """
        return self._myCanvas

    def get_current_plots(self):
        """
        Get the current plots on canvas

        Returns
        -------
        list of 2-tuple: integer (plot ID) and string (label)
        """
        tuple_list = list()
        line_id_list = sorted(self._my1DPlotDict.keys())
        for line_id in line_id_list:
            tuple_list.append((line_id, self._my1DPlotDict[line_id]))

        return tuple_list

    def get_indicator_key(self, x, y):
        """ Get the key of the indicator with given position
        :param picker_pos:
        :return:
        """
        return self._myIndicatorsManager.get_indicator_key(x, y)

    def get_indicator_position(self, indicator_key):
        """ Get position (x or y) of the indicator
        :param indicator_key
        :return: a tuple.  (0) horizontal (x, x); (1) vertical (y, y); (2) 2-way (x, y)
        """
        # Get indicator's type
        indicator_type = self._myIndicatorsManager.get_line_type(indicator_key)
        if indicator_type < 2:
            # horizontal or vertical indicator
            x, y = self._myIndicatorsManager.get_data(indicator_key)

            if indicator_type == 0:
                # horizontal
                return y[0], y[0]

            elif indicator_type == 1:
                # vertical
                return x[0], x[0]

        else:
            # 2-way
            raise RuntimeError('Implement 2-way as soon as possible!')

    def getLineStyleList(self):
        return LINE_STYLES

    def getLineMarkerList(self):
        return LINE_MARKERS

    def getLineBasicColorList(self):
        return BASIC_COLORS

    def getDefaultColorMarkerComboList(self):
        """ Get a list of line/marker color and marker style combination
        as default to add more and more line to plot
        """
        return self._myCanvas.getDefaultColorMarkerComboList()

    def getNextLineMarkerColorCombo(self):
        """ As auto line's marker and color combo list is used,
        get the NEXT marker/color combo
        """
        # get from list
        marker, color = self._myLineMarkerColorList[self._myLineMarkerColorIndex]
        # process marker if it has information
        if marker.count(' (') > 0:
            marker = marker.split(' (')[0]

        # update the index
        self._myLineMarkerColorIndex += 1
        if self._myLineMarkerColorIndex == len(self._myLineMarkerColorList):
            self._myLineMarkerColorIndex = 0

        return marker, color

    def reset_line_color_marker_index(self):
        """ Reset the auto index for line's color and style
        """
        self._myLineMarkerColorIndex = 0

    def set_title(self, title, color='black'):
        """
        set title to canvas
        """
        self._myCanvas.set_title(title, color)

    def setXYLimit(self, xmin=None, xmax=None, ymin=None, ymax=None):
        """ Set X-Y limit automatically
        """
        self._myCanvas.axes.set_xlim([xmin, xmax])
        self._myCanvas.axes.set_ylim([ymin, ymax])

        self._myCanvas.draw()

    def setAutoLineMarkerColorCombo(self):
        """ Set the default/auto line marker/color combination list
        """
        self._myLineMarkerColorList = list()
        for marker in LINE_MARKERS:
            for color in BASIC_COLORS:
                self._myLineMarkerColorList.append((marker, color))

    def setLineMarkerColorIndex(self, newindex):
        """
        """
        self._myLineMarkerColorIndex = newindex
