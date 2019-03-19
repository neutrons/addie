from __future__ import (absolute_import, division, print_function)
import numpy as np
from addie.plot.constants import BASIC_COLORS


class IndicatorManager(object):
    """ Manager for all indicator lines

    Indicator's Type =
    - 0: horizontal.  moving along Y-direction. [x_min, x_max], [y, y];
    - 1: vertical. moving along X-direction. [x, x], [y_min, y_max];
    - 2: 2-way. moving in any direction. [x_min, x_max], [y, y], [x, x], [y_min, y_max].
    """

    def __init__(self):
        # Auto color index
        self._colorIndex = 0
        # Auto line ID
        self._autoLineID = 1

        self._lineManager = dict()
        self._canvasLineKeyDict = dict()
        self._indicatorTypeDict = dict()  # value: 0 (horizontal), 1 (vertical), 2 (2-way)

    def add_2way_indicator(self, x, x_min, x_max, y, y_min, y_max, color):
        # Set up indicator ID
        this_id = str(self._autoLineID)
        self._autoLineID += 1

        # Set up vectors
        vec_x_horizontal = np.array([x_min, x_max])
        vec_y_horizontal = np.array([y, y])

        vec_x_vertical = np.array([x, x])
        vec_y_vertical = np.array([y_min, y_max])

        #
        self._lineManager[this_id] = [vec_x_horizontal, vec_y_horizontal, vec_x_vertical, vec_y_vertical, color]
        self._indicatorTypeDict[this_id] = 2

        return this_id

    def add_horizontal_indicator(self, y, x_min, x_max, color):
        """
        Add a horizontal indicator moving vertically
        """
        # Get ID
        this_id = str(self._autoLineID)
        self._autoLineID += 1

        #
        vec_x = np.array([x_min, x_max])
        vec_y = np.array([y, y])

        #
        self._lineManager[this_id] = [vec_x, vec_y, color]
        self._indicatorTypeDict[this_id] = 0

        return this_id

    def add_vertical_indicator(self, x, y_min, y_max, color):
        """
        Add a vertical indicator to data structure moving horizontally
        :return: indicator ID as an integer
        """
        # Get ID
        this_id = self._autoLineID
        self._autoLineID += 1

        # form vec x and vec y
        vec_x = np.array([x, x])
        vec_y = np.array([y_min, y_max])

        #
        self._lineManager[this_id] = [vec_x, vec_y, color]
        self._indicatorTypeDict[this_id] = 1

        return this_id

    def delete(self, indicator_id):
        """
        Delete indicator
        """
        del self._lineManager[indicator_id]
        del self._canvasLineKeyDict[indicator_id]
        del self._indicatorTypeDict[indicator_id]

    def get_canvas_line_index(self, indicator_id):
        """
        Get a line's ID (on canvas) from an indicator ID
        """
        assert isinstance(indicator_id, int)

        if indicator_id not in self._canvasLineKeyDict:
            raise RuntimeError('Indicator ID %s cannot be found. Current keys are %s.' % (
                indicator_id, str(sorted(self._canvasLineKeyDict.keys()))
            ))
        return self._canvasLineKeyDict[indicator_id]

    def get_line_type(self, my_id):
        return self._indicatorTypeDict[my_id]

    def get_2way_data(self, line_id):
        assert line_id in self._indicatorTypeDict, 'blabla'
        assert self._indicatorTypeDict[line_id] == 2, 'blabla'

        vec_set = [self._lineManager[line_id][0:2], self._lineManager[line_id][2:4]]

        return vec_set

    def get_data(self, line_id):
        """
        Get line's vector x and vector y
        :return: 2-tuple of numpy arrays
        """
        return self._lineManager[line_id][0], self._lineManager[line_id][1]

    def get_indicator_key(self, x, y):
        """ Get indicator's key with position
        """
        if x is None and y is None:
            raise RuntimeError('It is not allowed to have both X and Y are none to get indicator key.')

        ret_key = None

        for line_key in self._lineManager:

            if x is not None and y is not None:
                # 2 way
                raise NotImplementedError('ASAP')
            elif x is not None and self._indicatorTypeDict[line_key] == 1:
                # vertical indicator moving along X
                if abs(self._lineManager[line_key][0][0] - x) < 1.0E-2:
                    return line_key
            elif y is not None and self._indicatorTypeDict[line_key] == 0:
                # horizontal indicator moving along Y
                if abs(self._lineManager[line_key][1][0] - y) < 1.0E-2:
                    return line_key
        # END-FOR

        return ret_key

    @staticmethod
    def get_line_style(line_id=None):
        if line_id is not None:
            style = '--'
        else:
            style = '--'

        return style

    def get_live_indicator_ids(self):
        return sorted(self._lineManager.keys())

    @staticmethod
    def get_marker():
        """
        Get the marker a line
        """
        return '.'

    def get_next_color(self):
        """
        Get next color by auto color index
        :return: string as color
        """
        next_color = BASIC_COLORS[self._colorIndex]

        # Advance and possibly reset color scheme
        self._colorIndex += 1
        if self._colorIndex == len(BASIC_COLORS):
            self._colorIndex = 0

        return next_color

    def set_canvas_line_index(self, my_id, canvas_line_index):
        self._canvasLineKeyDict[my_id] = canvas_line_index

    def set_position(self, my_id, pos_x, pos_y):
        """ Set the indicator to a new position
        """
        if self._indicatorTypeDict[my_id] == 0:
            # horizontal
            self._lineManager[my_id][1][0] = pos_y
            self._lineManager[my_id][1][1] = pos_y

        elif self._indicatorTypeDict[my_id] == 1:
            # vertical
            self._lineManager[my_id][0][0] = pos_x
            self._lineManager[my_id][0][1] = pos_x

        elif self._indicatorTypeDict[my_id] == 2:
            # 2-way
            self._lineManager[my_id][0] = pos_x
            self._lineManager[my_id][1] = pos_y

        else:
            raise RuntimeError('Unsupported indicator of type %d' % self._indicatorTypeDict[my_id])

        self._lineManager[my_id][2] = 'black'

    def shift(self, my_id, dx, dy):
        if self._indicatorTypeDict[my_id] == 0:
            # horizontal
            self._lineManager[my_id][1] += dy

        elif self._indicatorTypeDict[my_id] == 1:
            # vertical
            self._lineManager[my_id][0] += dx

        elif self._indicatorTypeDict[my_id] == 2:
            # 2-way
            self._lineManager[my_id][2] += dx
            self._lineManager[my_id][1] += dy

        else:
            raise RuntimeError('Unsupported indicator of type %d' % self._indicatorTypeDict[my_id])

    def update_indicators_range(self, x_range, y_range):
        """
        Update indicator's range
        """
        for i_id in self._lineManager:
            # NEXT - Need a new flag for direction of the indicating line, vertical or horizontal
            if True:
                self._lineManager[i_id][1][0] = y_range[0]
                self._lineManager[i_id][1][-1] = y_range[1]
            else:
                self._lineManager[i_id][0][0] = x_range[0]
                self._lineManager[i_id][0][-1] = x_range[1]
