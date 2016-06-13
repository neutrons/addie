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
            # remove previous plot
            if self._bankPlotDict[bank_id]:
                plot_id = self._bankPlotDict[bank_id]
                assert isinstance(plot_id, int) and plot_id >= 0
                self.remove_line(plot_id)

            # add the new plot
            bank_color = self._bankColorDict[bank_id]
            vec_x, vec_y, vec_e = bank_data_list[index]
            plot_id = self.add_plot_1d(vec_x, vec_y, line_style='.', color=bank_color,
                                       x_label=unit, y_label='I(%s)' % unit)
            self._bankPlotDict[bank_id] = plot_id
            print '[DB...BAT] add line with ID = %d to bank %d.' % (plot_id, bank_id)
        # END-FOR (bank id)

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
            self.remove_line(bank_line_id)
            # remove from daa structure
        # END-FOR

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

        return

    def plot_gr(self, vec_r, vec_g, vec_e):
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
        line_id = self.add_plot_1d(vec_r, vec_g)
        self._grList.append(line_id)

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

    def plot_sq(self, vec_r, vec_s, vec_e):
        """
        Plot S(Q)
        Parameters
        ----------
        vec_r
        vec_s
        vec_e

        Returns
        -------

        """
        self.add_plot_1d(vec_r, vec_s, vec_e, color='blue', x_label='Q', y_label='S(Q)',
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
