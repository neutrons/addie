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
