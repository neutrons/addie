import mplgraphicsview as base


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
        self.add_plot_1d(vec_r, vec_g, vec_e)
        print vec_g

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
        self.add_plot_1d(vec_r, vec_s, vec_e)

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
            self.hide_indicator(self._leftIndicator)
            self.hide_indicator(self._rightIndicator)
            self._showBoundary = False
        else:
            self.show_indicator(self._leftIndicator)
            self.show_indicator(self._rightIndicator)
            self.move_indicator_to(self._leftIndicator, q_left)
            self.move_indicator_to(self._rightIndicator, q_right)
        # END-IF-ELSE (show boundary)

        return
