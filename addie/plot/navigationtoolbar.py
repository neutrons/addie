# pylint: disable=invalid-name,too-many-public-methods,too-many-arguments,non-parent-init-called,R0902,too-many-branches,C0302
from __future__ import (absolute_import, division, print_function)

from qtpy import PYQT4, PYQT5
from qtpy.QtCore import (Signal)

if PYQT5:
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
elif PYQT4:
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT
else:
    raise ImportError('do not know which matplotlib backend to use')

import matplotlib.image  # noqa
from matplotlib.figure import Figure  # noqa

# constants for modes
NAVIGATION_MODE_NONE = 0
NAVIGATION_MODE_PAN = 1
NAVIGATION_MODE_ZOOM = 2


class NavigationToolbar(NavigationToolbar2QT):
    """ A customized navigation tool bar attached to canvas
    Note:
    * home, left, right: will not disable zoom/pan mode
    * zoom and pan: will turn on/off both's mode

    Other methods
    * drag_pan(self, event): event handling method for dragging canvas in pan-mode
    """
    # This defines a signal called 'home_button_pressed' that takes 1 boolean
    # argument for being in zoomed state or not
    home_button_pressed = Signal()

    # This defines a signal called 'canvas_zoom_released'
    canvas_zoom_released = Signal()

    def __init__(self, parent, canvas):
        """ Initialization
        built-in methods
        - drag_zoom(self, event): triggered during holding the mouse and moving
        """
        NavigationToolbar2QT.__init__(self, canvas, canvas)

        # parent
        self._myParent = parent
        # tool bar mode
        self._myMode = NAVIGATION_MODE_NONE

        # connect the events to parent
        self.home_button_pressed.connect(self._myParent.evt_toolbar_home)
        self.canvas_zoom_released.connect(self._myParent.evt_zoom_released)

    @property
    def is_zoom_mode(self):
        """
        check whether the tool bar is in zoom mode
        """
        return self._myMode == NAVIGATION_MODE_ZOOM

    def get_mode(self):
        """
        :return: integer as none/pan/zoom mode
        """
        return self._myMode

    # Overriding base's methods
    def draw(self):
        """
        Canvas is drawn called by pan(), zoom()
        :return:
        """
        NavigationToolbar2QT.draw(self)

        self._myParent.evt_view_updated()

    def home(self, *args):
        # call super's home() method
        NavigationToolbar2QT.home(self, args)

        # send a signal to parent class for further operation
        self.home_button_pressed.emit()

    def pan(self, *args):
        """

        :param args:
        :return:
        """
        NavigationToolbar2QT.pan(self, args)

        if self._myMode == NAVIGATION_MODE_PAN:
            # out of pan mode
            self._myMode = NAVIGATION_MODE_NONE
        else:
            # into pan mode
            self._myMode = NAVIGATION_MODE_PAN

        print('PANNED')

    def zoom(self, *args):
        """
        Turn on/off zoom (zoom button)
        :param args:
        :return:
        """
        NavigationToolbar2QT.zoom(self, args)

        if self._myMode == NAVIGATION_MODE_ZOOM:
            # out of zoom mode
            self._myMode = NAVIGATION_MODE_NONE
        else:
            # into zoom mode
            self._myMode = NAVIGATION_MODE_ZOOM

    def release_zoom(self, event):
        """
        override zoom released method
        """
        self.canvas_zoom_released.emit()

        NavigationToolbar2QT.release_zoom(self, event)

    def _update_view(self):
        """
        view update called by home(), back() and forward()
        :return:
        """
        NavigationToolbar2QT._update_view(self)

        self._myParent.evt_view_updated()
