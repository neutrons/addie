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
        Returns
        -------

        """
        self.add_plot_1d(vec_r, vec_g, vec_e)

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