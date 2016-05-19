#!/usr/bin/env python
import os
import tempfile
from PyQt4 import QtCore, QtGui
import matplotlib.cm
import matplotlib.colors
import matplotlib.pyplot
#from . import icons_rc #@UnusedImport

# set the default backend to be compatible with Qt in case someone uses pylab from IPython console

def _set_default_rc():
  #matplotlib.pyplot.xkcd()
  matplotlib.rc('font', **{'family' : 'serif',
                         #  'weight' : 'normal',
                         #  'variant': 'DejaVuSerif',
                         'size': 7,
                 })
  matplotlib.rc('savefig', **{'dpi': 600})

_set_default_rc()

cmap=matplotlib.colors.LinearSegmentedColormap.from_list('default',
                  ['#0000ff', '#00ff00', '#ffff00', '#ff0000', '#bd7efc', '#000000'], N=256)
matplotlib.cm.register_cmap('default', cmap=cmap)

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT
from matplotlib.cbook import Stack
from matplotlib.colors import LogNorm, Normalize
from matplotlib.figure import Figure
try:
    import matplotlib.backends.qt4_editor.figureoptions as figureoptions
except ImportError:
    figureoptions=None

class NavigationToolbar(NavigationToolbar2QT):
  '''
    A small change to the original navigation toolbar.
  '''
  _auto_toggle=False
  logtog = QtCore.pyqtSignal(str)
  homeClicked = QtCore.pyqtSignal()
  exportClicked = QtCore.pyqtSignal()

  isPanActivated = False
  isZoomActivated = False

  home_settings = None

  def __init__(self, canvas, parent, coordinates=False):
    NavigationToolbar2QT.__init__(self, canvas, parent, coordinates)
    self.setIconSize(QtCore.QSize(20, 20))

  def _init_toolbar(self):
    if not hasattr(self, '_actions'):
      self._actions={}
    self.basedir=os.path.join(matplotlib.rcParams[ 'datapath' ], 'images')

    icon=QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/MPL Toolbar/go-home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    a=self.addAction(icon, 'Home', self.home)
    a.setToolTip('Reset original view')
    icon=QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/MPL Toolbar/zoom-previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    a=self.addAction(icon, 'Back', self.back)
    a.setToolTip('Back to previous view')
    icon=QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/MPL Toolbar/zoom-next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    a=self.addAction(icon, 'Forward', self.forward)
    a.setToolTip('Forward to next view')
    self.addSeparator()
    icon=QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/MPL Toolbar/transform-move.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    a=self.addAction(icon, 'Pan', self.pan)
    a.setToolTip('Pan axes with left mouse, zoom with right')
    a.setCheckable(True)
    self._actions['pan']=a
    icon=QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/MPL Toolbar/zoom-select.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    a=self.addAction(icon, 'Zoom', self.zoom)
    a.setToolTip('Zoom to rectangle')
    a.setCheckable(True)
    self._actions['zoom']=a
    self.addSeparator()
    icon=QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/MPL Toolbar/edit-guides.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    a=self.addAction(icon, 'Subplots', self.configure_subplots)
    a.setToolTip('Configure plot boundaries')

    icon=QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/MPL Toolbar/document-save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    a=self.addAction(icon, 'Save', self.save_figure)
    a.setToolTip('Save the figure')

    icon=QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/MPL Toolbar/document-print.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    a=self.addAction(icon, 'Print', self.print_figure)
    a.setToolTip('Print the figure with the default printer')

    self.buttons={}

    # Add the x,y location widget at the right side of the toolbar
    # The stretch factor is 1 which means any resizing of the toolbar
    # will resize this label instead of the buttons.
    self.locLabel=QtGui.QLabel("", self)
    self.locLabel.setAlignment(
            QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
    self.locLabel.setSizePolicy(
        QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                          QtGui.QSizePolicy.Ignored))
    self.labelAction=self.addWidget(self.locLabel)
    if self.coordinates:
      self.labelAction.setVisible(True)
    else:
      self.labelAction.setVisible(False)

    # reference holder for subplots_adjust window
    self.adj_window=None

  def activate_widget(self, widget_name, activateIt):

    if widget_name == 'pan':
      if activateIt:
        self.isPanActivated = True
        self.isZoomActivated = False
      else:
        self.isPanActivated = False
    elif widget_name == 'zoom':
      if activateIt:
        self.isZoomActivated = True
        self.isPanActivated = False
      else:
        self.isZoomActivated = False

  def home(self, *args):
    NavigationToolbar2QT.home(self,*args)
    self.homeClicked.emit()

  def pan(self, *args):
    NavigationToolbar2QT.pan(self, *args)
    self.activate_widget('pan', not self.isPanActivated)

  def zoom(self, *args):
    NavigationToolbar2QT.zoom(self, *args)
    self.activate_widget('zoom', not self.isZoomActivated)

  if matplotlib.__version__<'1.2':
    def pan(self, *args):
      'Activate the pan/zoom tool. pan with left button, zoom with right'
      # set the pointer icon and button press funcs to the
      # appropriate callbacks
      if self._auto_toggle:
        return
      if self._active=='ZOOM':
        self._auto_toggle=True
        self._actions['zoom'].setChecked(False)
        self._auto_toggle=False

      if self._active=='PAN':
        self._active=None
      else:
        self._active='PAN'
      if self._idPress is not None:
        self._idPress=self.canvas.mpl_disconnect(self._idPress)
        self.mode=''

      if self._idRelease is not None:
        self._idRelease=self.canvas.mpl_disconnect(self._idRelease)
        self.mode=''

      if self._active:
        self._idPress=self.canvas.mpl_connect(
            'button_press_event', self.press_pan)
        self._idRelease=self.canvas.mpl_connect(
            'button_release_event', self.release_pan)
        self.mode='pan/zoom'
        self.canvas.widgetlock(self)
      else:
        self.canvas.widgetlock.release(self)

      for a in self.canvas.figure.get_axes():
        a.set_navigate_mode(self._active)

      self.set_message(self.mode)

    def zoom(self, *args):
      'activate zoom to rect mode'
      if self._auto_toggle:
        return
      if self._active=='PAN':
        self._auto_toggle=True
        self._actions['pan'].setChecked(False)
        self._auto_toggle=False

      if self._active=='ZOOM':
        self._active=None
      else:
        self._active='ZOOM'

      if self._idPress is not None:
        self._idPress=self.canvas.mpl_disconnect(self._idPress)
        self.mode=''

      if self._idRelease is not None:
        self._idRelease=self.canvas.mpl_disconnect(self._idRelease)
        self.mode=''

      if  self._active:
        self._idPress=self.canvas.mpl_connect('button_press_event', self.press_zoom)
        self._idRelease=self.canvas.mpl_connect('button_release_event', self.release_zoom)
        self.mode='zoom rect'
        self.canvas.widgetlock(self)
      else:
        self.canvas.widgetlock.release(self)

      for a in self.canvas.figure.get_axes():
        a.set_navigate_mode(self._active)

      self.set_message(self.mode)

  def export_ascii(self):
    self.exportClicked.emit()

  def print_figure(self):
    '''
      Save the plot to a temporary png file and show a preview dialog also used for printing.
    '''
    filetypes=self.canvas.get_supported_filetypes_grouped()
    sorted_filetypes=filetypes.items()
    sorted_filetypes.sort()

    filename=os.path.join(tempfile.gettempdir(), u"quicknxs_print.png")
    self.canvas.print_figure(filename, dpi=600)
    imgpix=QtGui.QPixmap(filename)
    os.remove(filename)

    imgobj=QtGui.QLabel()
    imgobj.setPixmap(imgpix)
    imgobj.setMask(imgpix.mask())
    imgobj.setGeometry(0, 0, imgpix.width(), imgpix.height())

    def getPrintData(printer):
      imgobj.render(printer)


    printer=QtGui.QPrinter()
    printer.setPrinterName('mrac4a_printer')
    printer.setPageSize(QtGui.QPrinter.Letter)
    printer.setResolution(600)
    printer.setOrientation(QtGui.QPrinter.Landscape)

    pd=QtGui.QPrintPreviewDialog(printer)
    pd.paintRequested.connect(getPrintData)
    pd.exec_()

  def save_figure(self, *args):
      filetypes=self.canvas.get_supported_filetypes_grouped()
      sorted_filetypes=filetypes.items()
      sorted_filetypes.sort()
      default_filetype=self.canvas.get_default_filetype()

      start="image."+default_filetype
      filters=[]
      for name, exts in sorted_filetypes:
          exts_list=" ".join(['*.%s'%ext for ext in exts])
          filter_='%s (%s)'%(name, exts_list)
          if default_filetype in exts:
            filters.insert(0, filter_)
          else:
            filters.append(filter_)
      filters=';;'.join(filters)

      fname=QtGui.QFileDialog.getSaveFileName(self, u"Choose a filename to save to", start, filters)
      if fname:
          try:
              self.canvas.print_figure(unicode(fname))
          except Exception, e:
              QtGui.QMessageBox.critical(
                  self, "Error saving file", str(e),
                  QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton)

  def toggle_log(self, *args):
    ax=self.canvas.ax
    if len(ax.images)==0 and all([c.__class__.__name__!='QuadMesh' for c in ax.collections]):
      logstate=ax.get_yscale()
      if logstate=='linear':
        ax.set_yscale('log')
      else:
        ax.set_yscale('linear')
      self.canvas.draw()
      self.logtog.emit(ax.get_yscale())
    else:
      imgs=ax.images+[c for c in ax.collections if c.__class__.__name__=='QuadMesh']
      norm=imgs[0].norm
      if norm.__class__ is LogNorm:
        for img in imgs:
          img.set_norm(Normalize(norm.vmin, norm.vmax))
      else:
        for img in imgs:
          img.set_norm(LogNorm(norm.vmin, norm.vmax))
    self.canvas.draw()

class MplCanvas(FigureCanvas):

  trigger_click = QtCore.pyqtSignal()
  trigger_figure_left = QtCore.pyqtSignal()

  def __init__(self, parent=None, width=3, height=3, dpi=100, sharex=None, sharey=None, adjust={}):
    self.fig=Figure(figsize=(width, height), dpi=dpi, facecolor='#FFFFFF')
    self.ax=self.fig.add_subplot(111, sharex=sharex, sharey=sharey)
    self.fig.subplots_adjust(left=0.15, bottom=0.1, right=0.95, top=0.95)
    self.xtitle=""
    self.ytitle=""
    self.PlotTitle=""
    self.grid_status=True
    self.xaxis_style='linear'
    self.yaxis_style='linear'
    self.format_labels()
    self.ax.hold(True)
    FigureCanvas.__init__(self, self.fig)
    #self.fc = FigureCanvas(self.fig)
    FigureCanvas.setSizePolicy(self,
                              QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Expanding)
    FigureCanvas.updateGeometry(self)

    self.fig.canvas.mpl_connect('button_press_event', self.button_pressed)
    self.fig.canvas.mpl_connect('figure_leave_event', self.figure_leave)

  def button_pressed(self, event):
    self.trigger_click.emit()

  def figure_leave(self, event):
    self.trigger_figure_left.emit()

  def format_labels(self):
    self.ax.set_title(self.PlotTitle)
#    self.ax.title.set_fontsize(10)
#    self.ax.set_xlabel(self.xtitle, fontsize=9)
#    self.ax.set_ylabel(self.ytitle, fontsize=9)
#    labels_x=self.ax.get_xticklabels()
#    labels_y=self.ax.get_yticklabels()
#
#    for xlabel in labels_x:
#      xlabel.set_fontsize(8)
#    for ylabel in labels_y:
#      ylabel.set_fontsize(8)

  def sizeHint(self):
    w, h=self.get_width_height()
    w=max(w, self.height())
    h=max(h, self.width())
    return QtCore.QSize(w, h)

  def minimumSizeHint(self):
    return QtCore.QSize(40, 40)

  def get_default_filetype(self):
      return 'png'


class MPLWidget(QtGui.QWidget):
  cplot=None
  cbar=None

  logtogy = QtCore.pyqtSignal(str)
  singleClick = QtCore.pyqtSignal(bool)
  leaveFigure = QtCore.pyqtSignal()

  def __init__(self, parent=None, with_toolbar=True, coordinates=False):
    QtGui.QWidget.__init__(self, parent)
    self.canvas=MplCanvas()
    self.canvas.ax2=None
    self.vbox=QtGui.QVBoxLayout()
    self.vbox.setMargin(1)
    self.vbox.addWidget(self.canvas)
    if with_toolbar:
      self.toolbar=NavigationToolbar(self.canvas, self)
      self.toolbar.coordinates=coordinates
      self.vbox.addWidget(self.toolbar)
      self.toolbar.logtog.connect(self.logtoggleylog)
    else:
      self.toolbar=None
    self.setLayout(self.vbox)
    self.canvas.trigger_click.connect(self._singleClick)
    self.canvas.trigger_figure_left.connect(self._leaveFigure)

  def _singleClick(self):
    status = self.toolbar.isPanActivated or self.toolbar.isZoomActivated
    self.singleClick.emit(status)

  def _leaveFigure(self):
    self.leaveFigure.emit()

  def logtoggleylog(self, status):
    self.logtogy.emit(status)

  def leaveEvent(self, event):
    '''
    Make sure the cursor is reset to it's default when leaving the widget.
    In some cases the zoom cursor does not reset when leaving the plot.
    '''
    if self.toolbar:
      QtGui.QApplication.restoreOverrideCursor()
      self.toolbar._lastCursor=None
    return QtGui.QWidget.leaveEvent(self, event)

  def set_config(self, config):
    self.canvas.fig.subplots_adjust(**config)

  def get_config(self):
    spp=self.canvas.fig.subplotpars
    config=dict(left=spp.left,
                right=spp.right,
                bottom=spp.bottom,
                top=spp.top)
    return config


  def draw(self):
    '''
      Convenience to redraw the graph.
    '''
    self.canvas.draw()

  def plot(self, *args, **opts):
    '''
      Convenience wrapper for self.canvas.ax.plot
    '''
    return self.canvas.ax.plot(*args, **opts)

  def semilogy(self, *args, **opts):
    '''
      Convenience wrapper for self.canvas.ax.semilogy
    '''
    return self.canvas.ax.semilogy(*args, **opts)

  def errorbar(self, *args, **opts):
    '''
      Convenience wrapper for self.canvas.ax.semilogy
    '''
    return self.canvas.ax.errorbar(*args, **opts)

  def pcolormesh(self, datax, datay, dataz, log=False, imin=None, imax=None, update=False, **opts):
    '''
      Convenience wrapper for self.canvas.ax.plot
    '''
    if self.cplot is None or not update:
      if log:
        self.cplot=self.canvas.ax.pcolormesh(datax, datay, dataz, norm=LogNorm(imin, imax), **opts)
      else:
        self.cplot=self.canvas.ax.pcolormesh(datax, datay, dataz, **opts)
    else:
      self.update(datax, datay, dataz)
    return self.cplot

  def imshow(self, data, log=False, imin=None, imax=None, update=True, **opts):
    '''
      Convenience wrapper for self.canvas.ax.plot
    '''
    if self.cplot is None or not update:
      if log:
        self.cplot=self.canvas.ax.imshow(data, norm=LogNorm(imin, imax), **opts)
      else:
        self.cplot=self.canvas.ax.imshow(data, **opts)
    else:
      self.update(data, **opts)
    return self.cplot

  def set_title(self, new_title):
    return self.canvas.ax.title.set_text(new_title)

  def set_xlabel(self, label):
    return self.canvas.ax.set_xlabel(label)

  def set_ylabel(self, label):
    return self.canvas.ax.set_ylabel(label)

  def set_xscale(self, scale):
    try:
      return self.canvas.ax.set_xscale(scale)
    except ValueError:
      pass

  def set_yscale(self, scale):
    try:
      return self.canvas.ax.set_yscale(scale)
    except ValueError:
      pass

  def clear_fig(self):
    self.cplot=None
    self.cbar=None
    self.canvas.fig.clear()
    self.canvas.ax=self.canvas.fig.add_subplot(111, sharex=None, sharey=None)

  def clear(self):
    self.cplot=None
    self.toolbar._views.clear()
    self.toolbar._positions.clear()
    self.canvas.ax.clear()
    if self.canvas.ax2 is not None:
      self.canvas.ax2.clear()

  def update(self, *data, **opts):
    self.cplot.set_data(*data)
    if 'extent' in opts:
      self.cplot.set_extent(opts['extent'])
      oldviews=self.toolbar._views
      if self.toolbar._views:
        # set the new extent as home for the new data
        newviews=Stack()
        newviews.push([tuple(opts['extent'])])
        for item in oldviews[1:]:
          newviews.push(item)
        self.toolbar._views=newviews
      if not oldviews or oldviews[oldviews._pos]==oldviews[0]:
        self.canvas.ax.set_xlim(opts['extent'][0], opts['extent'][1])
        self.canvas.ax.set_ylim(opts['extent'][2], opts['extent'][3])

  def legend(self, *args, **opts):
    return self.canvas.ax.legend(*args, **opts)

  def adjust(self, **adjustment):
    return self.canvas.fig.subplots_adjust(**adjustment)
