# pylint:
# disable=invalid-name,too-many-public-methods,too-many-arguments,non-parent-init-called,R0902,too-many-branches,C0302
from __future__ import (absolute_import, division, print_function)
import numpy as np

from qtpy.QtWidgets import QSizePolicy
from addie.plot.constants import BASIC_COLORS, LINE_MARKERS, LINE_STYLES
from mantidqt.MPLwidgets import FigureCanvasQTAgg

import matplotlib.image  # noqa
from matplotlib.figure import Figure  # noqa
from addie.addiedriver import AddieDriver  # noqa
import addie.utilities.workspaces # noqa


class FigureCanvas(FigureCanvasQTAgg):
    """  A customized Qt widget for matplotlib figure.
    It can be used to replace GraphicsView of QtGui
    """

    def __init__(self, parent):
        self._driver = AddieDriver()
        # from mpl_toolkits.axes_grid1 import host_subplot
        # import mpl_toolkits.axisartist as AA
        # import matplotlib.pyplot as plt

        # Instantiating matplotlib Figure
        self.fig = Figure()
        self.fig.patch.set_facecolor('white')

        self.axes = self.fig.add_subplot(111, projection='mantid')
        self.fig.subplots_adjust(bottom=0.15)

        # Initialize parent class and set parent
        FigureCanvasQTAgg.__init__(self, self.fig)
        self.setParent(parent)

        # Set size policy to be able to expanding and resizable with frame
        FigureCanvasQTAgg.setSizePolicy(
            self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

        # Variables to manage all lines/subplot
        self._lineDict = {}
        self._lineIndex = 0

        # legend and color bar
        self._colorBar = None
        self._isLegendOn = False
        self._legendFontSize = 10

    @property
    def is_legend_on(self):
        """
        check whether the legend is shown or hide
        """
        return self._isLegendOn

    def add_arrow(self, start_x, start_y, stop_x, stop_y):
        """
        0, 0, 0.5, 0.5, head_width=0.05, head_length=0.1, fc='k', ec='k')
        :return:
        """
        head_width = 0.05
        head_length = 0.1
        fc = 'k'
        ec = 'k'

        self.axes.arrrow(start_x, start_y, stop_x, stop_y, head_width,
                         head_length, fc, ec)

    def add_plot_1d(
            self,
            wkspname,
            wkspindex,
            color=None,
            label="",
            x_label=None,
            y_label=None,
            marker=None,
            line_style=None,
            line_width=1,
            alpha=1.,
            show_legend=True,
            plotError=False):

        # process inputs and defaults
        if color is None:
            color = (0, 1, 0, 1)
        if marker is None:
            marker = 'None'
        if line_style is None:
            line_style = '-'

        # color must be RGBA (4-tuple)
        wksp = addie.utilities.workspaces.get_ws(wkspname)
        if plotError:
            r = self.axes.errorbar(
                wksp,
                wkspIndex=wkspindex,
                color=color,
                marker=marker,
                linestyle=line_style,
                label=label,
                linewidth=line_width,
                alpha=alpha,
                markersize=40)
        else:
            # return: list of matplotlib.lines.Line2D object
            r = self.axes.plot(
                wksp,
                wkspIndex=wkspindex,
                color=color,
                marker=marker,
                markersize=2,
                linestyle=line_style,
                label=label,
                linewidth=line_width,
                alpha=alpha,
                distribution=True)

        self.axes.set_aspect('auto')

        # set x-axis and y-axis label
        if x_label is not None:
            self.axes.set_xlabel(x_label, fontsize=20)
        if y_label is not None:
            self.axes.set_ylabel(y_label, fontsize=20)

        # set/update legend
        if show_legend:
            self._setup_legend()

        # Register
        line_key = self._lineIndex
        if len(r) == 1:
            self._lineDict[line_key] = r[0]
            self._lineIndex += 1
        else:
            msg = 'Return from plot is a %d-tuple: %s.. \n' % (len(r), r)
            for i_r in range(len(r)):
                msg += 'r[%d] = %s\n' % (i_r, str(r[i_r]))
            raise NotImplementedError(msg)

        # Flush/commit
        self.draw()

        return line_key

    def addPlot2D(
            self,
            array2d,
            xmin,
            xmax,
            ymin,
            ymax,
            holdprev,
            yticklabels=None):
        """ Add a 2D plot

        Arguments:
         - yticklabels :: list of string for y ticks
        """
        # Release the current image
        self.axes.hold(holdprev)

        # Do plot
        # y ticks will be shown on line 1, 4, 23, 24 and 30
        # yticks = [1, 4, 23, 24, 30]
        # self.axes.set_yticks(yticks)

        # show image
        imgplot = self.axes.imshow(
            array2d,
            extent=[
                xmin,
                xmax,
                ymin,
                ymax],
            interpolation='none')
        # set y ticks as an option:
        if yticklabels is not None:
            # it will always label the first N ticks even image is zoomed in
            print(
                "--------> [FixMe]: The way to set up the Y-axis ticks is wrong!")
            # self.axes.set_yticklabels(yticklabels)

        # explicitly set aspect ratio of the image
        self.axes.set_aspect('auto')

        # Set color bar.  plt.colorbar() does not work!
        if self._colorBar is None:
            # set color map type
            imgplot.set_cmap('spectral')
            self._colorBar = self.fig.colorbar(imgplot)
        else:
            self._colorBar.update_bruteforce(imgplot)

        # Flush...
        self._flush()

    def add_contour_plot(self, vec_x, vec_y, matrix_z):
        # create mesh grid
        grid_x, grid_y = np.meshgrid(vec_x, vec_y)

        # check size
        assert grid_x.shape == matrix_z.shape, 'Size of X (%d) and Y (%d) must match size of Z (%s).' \
                                               '' % (len(vec_x), len(vec_y), matrix_z.shape)

        # Release the current image
        self.axes.hold(False)

        # Do plot
        contour_plot = self.axes.contourf(grid_x, grid_y, matrix_z, 100)

        labels = [item.get_text() for item in self.axes.get_yticklabels()]
        print(
            '[DB...BAT] Number of Y labels = ',
            len(labels),
            ', Number of Y = ',
            len(vec_y))

        # TODO/ISSUE/55: how to make this part more powerful
        if len(labels) == 2 * len(vec_y) - 1:
            new_labels = [''] * len(labels)
            for i in range(len(vec_y)):
                new_labels[i * 2] = '%d' % int(vec_y[i])
            self.axes.set_yticklabels(new_labels)

        # explicitly set aspect ratio of the image
        self.axes.set_aspect('auto')

        # Set color bar.  plt.colorbar() does not work!
        if self._colorBar is None:
            # set color map type
            contour_plot.set_cmap('spectral')
            self._colorBar = self.fig.colorbar(contour_plot)
        else:
            self._colorBar.update_bruteforce(contour_plot)

        # Flush...
        self._flush()

    def add_plot_postprocess(self, bank, x_list, y_list):
        x_label = 'Q(angstrom^-1)'
        y_label = 'S(Q), F(Q), ...'
        color = None
        marker = None
        line_style = None
        # process inputs and defaults
        if color is None:
            color = (0, 1, 0, 1)
        if marker is None:
            marker = 'None'
        if line_style is None:
            line_style = '-'

        self.axes.plot(x_list, y_list, label=bank)
        self.axes.legend()
        self.axes.set_aspect('auto')

        # set x-axis and y-axis label
        if x_label is not None:
            self.axes.set_xlabel(x_label, fontsize=20)
        if y_label is not None:
            self.axes.set_ylabel(y_label, fontsize=20)

        # Flush/commit
        self.draw()

    def addImage(self, imagefilename):
        """ Add an image by file
        """
        #import matplotlib.image as mpimg

        # set aspect to auto mode
        self.axes.set_aspect('auto')

        img = matplotlib.image.imread(str(imagefilename))
        # lum_img = img[:,:,0]
        # FUTURE : refactor for image size, interpolation and origin
        imgplot = self.axes.imshow(
            img,
            extent=[
                0,
                1000,
                800,
                0],
            interpolation='none',
            origin='lower')

        # Set color bar.  plt.colorbar() does not work!
        if self._colorBar is None:
            # set color map type
            imgplot.set_cmap('spectral')
            self._colorBar = self.fig.colorbar(imgplot)
        else:
            self._colorBar.update_bruteforce(imgplot)

        self._flush()

    def clear_all_1d_plots(self):
        """ Remove all lines from the canvas
        """
        for ikey in list(self._lineDict.keys()):
            plot = self._lineDict[ikey]
            if plot is None:
                continue
            if isinstance(plot, tuple) is False:
                try:
                    self.axes.lines.remove(plot)
                except ValueError as e:
                    print(
                        "[Error] Plot %s is not in axes.lines which has %d lines. Error mesage: %s" %
                        (str(plot), len(
                            self.axes.lines), str(e)))
                del self._lineDict[ikey]
            else:
                # error bar
                plot[0].remove()
                for line in plot[1]:
                    line.remove()
                for line in plot[2]:
                    line.remove()
                del self._lineDict[ikey]
            # ENDIF(plot)
        # ENDFOR

        self._setup_legend()

        self.draw()

    def clear_canvas(self):
        """ Clear data including lines and image from canvas
        """
        # clear the image for next operation
        self.axes.hold(False)

        # Clear all lines
        self.clear_all_1d_plots()

        # clear image
        self.axes.cla()
        # Try to clear the color bar
        if len(self.fig.axes) > 1:
            self.fig.delaxes(self.fig.axes[1])
            self._colorBar = None
            # This clears the space claimed by color bar but destroys sub_plot
            # too.
            self.fig.clear()
            # Re-create subplot
            self.axes = self.fig.add_subplot(111)
            self.fig.subplots_adjust(bottom=0.15)

        # flush/commit
        self._flush()

    def decrease_legend_font_size(self):
        """
        reset the legend with the new font size
        Returns:

        """
        # minimum legend font size is 2! return if it already uses the smallest
        # font size.
        if self._legendFontSize <= 2:
            return

        self._legendFontSize -= 1
        self._setup_legend()

        self.draw()

    def getLastPlotIndexKey(self):
        """ Get the index/key of the last added line
        """
        return self._lineIndex - 1

    def getPlot(self):
        """ reture figure's axes to expose the matplotlib figure to PyQt client
        """
        return self.axes

    def getXLimit(self):
        """ Get limit of Y-axis
        """
        return self.axes.get_xlim()

    def getYLimit(self):
        """ Get limit of Y-axis
        """
        return self.axes.get_ylim()

    def hide_legend(self):
        """
        hide the legend if it is not None
        """
        if self.axes.legend() is not None:
            # set visible to be False and re-draw
            self.axes.legend().set_visible(False)
            self.draw()

        self._isLegendOn = False

    def increase_legend_font_size(self):
        """
        reset the legend with the new font size
        """
        self._legendFontSize += 1

        self._setup_legend()

        self.draw()

    def setXYLimit(self, xmin, xmax, ymin, ymax):
        # for X
        xlims = self.axes.get_xlim()
        xlims = list(xlims)
        if xmin is not None:
            xlims[0] = xmin
        if xmax is not None:
            xlims[1] = xmax
        self.axes.set_xlim(xlims)

        # for Y
        ylims = self.axes.get_ylim()
        ylims = list(ylims)
        if ymin is not None:
            ylims[0] = ymin
        if ymax is not None:
            ylims[1] = ymax
        self.axes.set_ylim(ylims)

        # try draw
        self.draw()

    def set_title(self, title, color):
        # TODO/NOW - doc & etc

        self.axes.set_title(title, loc='center', color=color)

        self.draw()

    def remove_plot_1d(self, plot_key):
        """ Remove the line with its index as key
        """
        if plot_key in self._lineDict:
            try:
                self.axes.lines.remove(self._lineDict[plot_key])
            except ValueError as r_error:
                error_message = 'Unable to remove to 1D line %s (ID=%d) due to %s.' % (
                    str(self._lineDict[plot_key]), plot_key, str(r_error))
                raise RuntimeError(error_message)
            # remove the plot key from dictionary
            del self._lineDict[plot_key]
        else:
            raise RuntimeError('Line with ID %s is not recorded.' % plot_key)

        self._setup_legend()

        # Draw
        self.draw()

    def show_legend(self):
        """
        show the legend if the legend is not None
        Returns:

        """
        if self.axes.legend() is not None:
            # set visible to be True and re-draw
            # self.axes.legend().set_visible(True)
            self._setup_legend()
            self.draw()

            # set flag on
            self._isLegendOn = True

    def updateLine(
            self,
            ikey=-1,
            wkspname=None,
            wkspindex=None,
            vecx=None,
            vecy=None,
            linestyle=None,
            linecolor=None,
            marker=None,
            markercolor=None):
        """
        Update a plot line or a series plot line
        """

        line = self._lineDict[ikey]
        if line is None:
            print('[ERROR] Line (key = %d) is None. Unable to update' % ikey)
            return

        if wkspname or (vecx.all() and vecy.all()):
            if wkspname:
                vecx, vecy, _ = addie.utilities.workspaces.get_ws_data(
                    wkspname, wkspindex)
            line.set_data(vecx, vecy)

        if linecolor is not None:
            line.set_color(linecolor)

        if linestyle is not None:
            line.set_linestyle(linestyle)

        if marker is not None:
            line.set_marker(marker)

        if markercolor is not None:
            line.set_markerfacecolor(markercolor)

        oldlabel = line.get_label()
        line.set_label(oldlabel)

        self._setup_legend()

        # commit
        self.draw()

    def get_data(self, line_id):
        """
        Get vecX and vecY from line object in matplotlib
        :param line_id:
        :return: 2-tuple as vector X and vector Y
        """
        # check
        if line_id not in self._lineDict:
            raise KeyError('Line ID %s does not exist.' % str(line_id))

        # get line
        line = self._lineDict[line_id]
        if line is None:
            raise RuntimeError('Line ID %s has been removed.' % line_id)

        return line.get_xdata(), line.get_ydata()

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
        combo_list = list()
        num_markers = len(LINE_MARKERS)
        num_colors = len(BASIC_COLORS)

        for i in range(num_markers):
            marker = LINE_MARKERS[i]
            for j in range(num_colors):
                color = BASIC_COLORS[j]
                combo_list.append((marker, color))
            # ENDFOR (j)
        # ENDFOR(i)

        return combo_list

    def _flush(self):
        """ A dirty hack to flush the image
        """
        w, h = self.get_width_height()
        self.resize(w + 1, h)
        self.resize(w, h)

    def _setup_legend(self, location='best'):
        """
        Set up legend
        self.axes.legend(): Handler is a Line2D object. Lable maps to the line object
        """
        allowed_location_list = [
            "best",
            "upper right",
            "upper left",
            "lower left",
            "lower right",
            "right",
            "center left",
            "center right",
            "lower center",
            "upper center",
            "center"]

        # Check legend location valid or not
        if location not in allowed_location_list:
            location = 'best'

        handles, labels = self.axes.get_legend_handles_labels()
        self.axes.legend(handles, labels, loc=location,
                         fontsize=self._legendFontSize)

        self._isLegendOn = True
