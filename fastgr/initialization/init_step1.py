from PyQt4 import QtGui


class InitStep1(object):
    
    def __init__(self, parent=None):
        self.parent = parent
        
        self.parent.ui.diamond.setFocus(True)
        self.set_statusBar()
        
    def set_statusBar(self):
        
        status_bar_label = QtGui.QLabel()
        self.parent.ui.statusbar.addPermanentWidget(status_bar_label)