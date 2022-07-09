# A managing class (like database) for color and style of lines of all the G(r) and thus S(q) that are loaded and/or
# calculated.
from __future__ import (absolute_import, division, print_function)

LineColorBase = ['black', 'red', 'blue', 'green', 'brown', 'orange']
LineStyleBase = ['-', '--', '-.']
LineMarkerBase = [None, 'o', '.', 'D', 's']

Q_MIN = 10.
Q_MAX = 50.


class PDFPlotManager(object):
    """
    class to manage the color and line styles of G(r) and S(Q)
    """

    def __init__(self):
        """ initialization
        """
        self._currLineColorIndex = 0
        self._currStandaloneGofRColorIndex = 0

        self._sofqInfoDict = dict()  # key: SofQ workspace name, value (tuple): color index, style-marker index
        self._gofrInfoDict = dict()  # key: GofR workspace name

        self._maxLineStyleMarkerIndex = len(LineStyleBase) * len(LineMarkerBase)

        return

    def add_sofq(self, sq_ws_name):
        """ Add a S(Q) workspace to plot
        :param sq_ws_name:
        :return:
        """
        if sq_ws_name not in self._sofqInfoDict:
            # new workspace
            self._sofqInfoDict[sq_ws_name] = self._currLineColorIndex, 0
            self._currLineColorIndex += 1
            if self._currLineColorIndex >= len(LineColorBase):
                self._currLineColorIndex = 0

        # existing workspace
        color = LineColorBase[self._sofqInfoDict[sq_ws_name][0]]

        return color

    @staticmethod
    def retrieve_line_style_marker(style_marker_index):
        """
        convert the combo-index of line style and marker index to line style and marker in string
        Parameters
        ----------
        style_marker_index

        Returns
        -------

        """
        marker_index = style_marker_index // len(LineStyleBase)
        style_index = style_marker_index % len(LineStyleBase)

        return LineStyleBase[style_index], LineMarkerBase[marker_index]

    def add_gofr(self, sq_ws_name, gr_ws_name, curr_q_max):
        """add a G(r) line
        :param sq_ws_name: S(Q) workspace that is associated
        :param gr_ws_name:
        :param curr_q_max:
        :return:
        """
        if sq_ws_name is None:
            # standalone G(r) which might come from a GofR data file
            color = LineColorBase[self._currStandaloneGofRColorIndex]
            line_style = ':'
            alpha = 1.
            line_marker = None

            self._currStandaloneGofRColorIndex %= len(LineColorBase)

        elif sq_ws_name not in self._sofqInfoDict:
            # it is possible that a S(Q) never been plotted???
            raise RuntimeError('S(Q) workspace {0} has not been added. It is not allowed!'.format(sq_ws_name))

        else:
            # G(r) from parent
            assert isinstance(curr_q_max, float), 'Current Q Max {0} must be a float but  not a {1}' \
                                                  ''.format(curr_q_max, type(curr_q_max))

            # get current information
            color_index, style_marker_index = self._sofqInfoDict[sq_ws_name]

            color = LineColorBase[color_index]
            line_style, line_marker = self.retrieve_line_style_marker(style_marker_index)

            # increase index counter for next
            style_marker_index += 1
            if style_marker_index == self._maxLineStyleMarkerIndex:
                style_marker_index = 0

            self._sofqInfoDict[sq_ws_name] = color_index, style_marker_index
            alpha = ((curr_q_max - Q_MIN) / (Q_MAX - Q_MIN) + 1.) * 0.5
            alpha = min(alpha, 1.0)
        # END-IF-ELSE

        self._gofrInfoDict[gr_ws_name] = color, line_style, alpha

        return color, line_style, line_marker, alpha

    def get_gr_line(self, gr_ws_name):
        """
        get color, style and alpha for a G(r) line
        :param gr_ws_name:
        :return:
        """
        return self._gofrInfoDict[gr_ws_name]
