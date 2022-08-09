from addie.plot import MplGraphicsView


class PPMView(MplGraphicsView):

    def __init__(self, parent):
        MplGraphicsView.__init__(self, parent)

        self._bankPlotDict = dict()
        self._bankColorDict = {
            1: 'black',
            2: 'red',
            3: 'blue',
            4: 'green',
            5: 'brown',
            6: 'orange'}

        self._myCanvas.mpl_connect(
            'button_press_event',
            self.on_mouse_press_event)

    def on_mouse_press_event(self, e):
        pass

    def plot(self, bank, x_list, y_list):
        self._myCanvas.add_plot_postprocess(bank, x_list, y_list)

    def canvas_reset(self):
        self._myCanvas.axes.cla()
        self._myCanvas.draw()

        self._myCanvas._flush()
