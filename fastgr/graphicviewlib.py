import numpy as np
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
        self._bankPlotDict = dict()
        for bank_id in range(1, 7):
            self._bankPlotDict[bank_id] = False

        self._bankColorDict = {1: 'black',
                               2: 'red',
                               3: 'blue',
                               4: 'green',
                               5: 'brown',
                               6: 'yellow'}
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
            if self._bankPlotDict[bank_id] is False:
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

    def plot_banks(self, bank_id_list, bank_data_list, unit):
        """
        Plot a few banks to canvas.  If the bank has been plot on canvas already,
        then remove the previous data
        Args:
            bank_id_list:
            bank_data_list:
            unit: string for X-range unit.  can be TOF, dSpacing or Q (momentum transfer)

        Returns:

        """
        # check
        assert isinstance(bank_id_list, list)
        assert isinstance(bank_data_list, list)
        assert len(bank_id_list) == len(bank_data_list)

        for index, bank_id in enumerate(bank_id_list):
            # remove previous plot for update
            if self._bankPlotDict[bank_id]:
                plot_id = self._bankPlotDict[bank_id]
                assert isinstance(plot_id, int) and plot_id >= 0
                self.remove_line(plot_id)

            # add the new plot
            bank_color = self._bankColorDict[bank_id]
            vec_x, vec_y, vec_e = bank_data_list[index]
            plot_id = self.add_plot_1d(vec_x, vec_y, marker='.', color=bank_color,
                                       x_label=unit, y_label='I(%s)' % unit,
                                       label='Bank %d' % bank_id)
            self._bankPlotDict[bank_id] = plot_id
        # END-FOR (bank id)

        return

    def plot_general_ws(self, bragg_ws_name, vec_x, vec_y, vec_e):
        plot_id = self.add_plot_1d(vec_x, vec_y, marker='.', color='black',
                                   label=bragg_ws_name)

        return

    def remove_banks(self, bank_id_list):
        """
        Remove a few bank ID fro Bragg plot
        Args:
            bank_id_list:

        Returns:

        """
        # check
        assert isinstance(bank_id_list, list)

        # remove
        for bank_id in bank_id_list:
            bank_line_id = self._bankPlotDict[bank_id]
            # remove from canvas
            try:
                self.remove_line(bank_line_id)
            except ValueError as val_error:
                error_message = 'Unable to remove bank %d plot (ID = %d) due to %s.' % (bank_id,
                                                                                        bank_line_id,
                                                                                        str(val_error))
                raise ValueError(error_message)
            # remove from data structure
            self._bankPlotDict[bank_id] = False
        # END-FOR

        # debug output
        db_buf = ''
        for bank_id in self._bankPlotDict:
            db_buf += '%d: %s \t' % (bank_id, str(self._bankPlotDict[bank_id]))
        print 'After removing %s, Buffer: %s.' % (str(bank_id_list), db_buf)

        return

    def reset(self):
        """
        Reset the canvas for new Bragg data
        Returns:
        None
        """
        # clear the control-dictionary
        for bank_id in self._bankPlotDict.keys():
            self._bankPlotDict[bank_id] = False

        # clear all lines
        self.clear_all_lines()

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

        return

    def plot_gr(self, key_plot, vec_r, vec_g, vec_e=None, plot_error=False):
        """
        Plot G(r)
        Parameters
        -------
        vec_r: numpy array for R
        vec_g: numpy array for G(r)
        vec_e: numpy array for G(r) error
        Returns
        -------

        """
        # TODO/NOW - Doc and check
        if plot_error:
            self.add_plot_1d(vec_r, vec_g, vec_e)
            raise NotImplementedError('ASAP')
        else:
            line_id = self.add_plot_1d(vec_r, vec_g, marker='.',
                                       color=self._colorList[self._colorIndex % len(self._colorList)])
            self._colorIndex += 1
            self._grDict[key_plot] = line_id

        return

    def remove_gr(self, key_plot):
        """

        Parameters
        ----------
        key_plot

        Returns
        -------

        """
        # TODO/NOW - Doc and check
        line_id = self._grDict[key_plot]

        self.remove_line(line_id)

        del self._grDict[line_id]

        return


class SofQView(base.MplGraphicsView):
    """
    Graphics view for S(Q)
    """
    def __init__(self, parent):
        """
        Initialization
        Parameters
        ----------
        parent
        """
        base.MplGraphicsView.__init__(self, parent)

        self._showBoundary = False
        self._leftID = None
        self._rightID = None

        return

    def is_boundary_shown(self):
        """

        Returns
        -------

        """
        return self._showBoundary

    def plot_sq(self, vec_r, vec_s, vec_e, sq_y_label):
        """
        Plot S(Q)
        Parameters
        ----------
        vec_r
        vec_s
        vec_e
        sq_y_label :: label for Y-axis

        Returns
        -------

        """
        # check
        assert isinstance(vec_r, np.ndarray) and isinstance(vec_s, np.ndarray)
        assert isinstance(sq_y_label, str)

        self.clear_all_lines()
        self.add_plot_1d(vec_r, vec_s, color='blue', x_label='Q', y_label=sq_y_label,
                         marker='.')

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
        # END-IF-ELSE (show boundary)

        return
