import sys


import ui_mainWindow

import PyQt4.QtCore as QtCore
import PyQt4.QtGui

__version__ = "1.0.0"


class MainWindow(PyQt4.QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(PyQt4.QtGui.QMainWindow, self).__init__(parent)

        self.ui = ui_mainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        # set widgets
        self._init_widgets()

        # define the event handling methods
        # bragg diffraction tab
        self.connect(self.ui.pushButton_loadBraggFile, QtCore.SIGNAL('clicked()'),
                     self.do_load_bragg_file)
        self.connect(self.ui.radioButton_b1, QtCore.SIGNAL('toggled(int)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.radioButton_b2, QtCore.SIGNAL('toggled(int)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.radioButton_b3, QtCore.SIGNAL('toggled(int)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.radioButton_b4, QtCore.SIGNAL('toggled(int)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.radioButton_b5, QtCore.SIGNAL('toggled(int)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.radioButton_b6, QtCore.SIGNAL('toggled(int)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.comboBox_xUnit, QtCore.SIGNAL('stateChanged(int)'),
                     self.evt_plot_bragg_bank)

        # for tab G(R)
        self.connect(self.ui.pushButton_loadSQ, QtCore.SIGNAL('clicked()'),
                     self.do_load_sq)
        self.connect(self.ui.radioButton_sq, QtCore.SIGNAL('toggled(int)'),
                     self.evt_plot_sq)
        self.connect(self.ui.radioButton_sq, QtCore.SIGNAL('toggled(int)'),
                     self.evt_plot_sqm1)
        self.connect(self.ui.radioButton_sq, QtCore.SIGNAL('toggled(int)'),
                     self.evt_plot_qsqm1)
        self.connect(self.ui.pushButton_showQMinMax, QtCore.SIGNAL('clicked()'),
                     self.do_show_sq_bound)
        self.connect(self.ui.pushButton_generateGR, QtCore.SIGNAL('clicked()'),
                     self.do_generateGR)
        self.connect(self.ui.pushButton_saveGR, QtCore.SIGNAL('clicked()'),
                     self.do_save_GR)

        return

    def _init_widgets(self):
        """ Initialize widgets
        Returns
        -------

        """
        self.ui.comboBox_xUnit.clear()
        self.ui.comboBox_xUnit.addItems(['TOF', ])

    def do_load_bragg_file(self):
        """
        Load Bragg files including GSAS, NeXus, 3-column ASCii.
        Returns
        -------
        """

        return

    def do_load_sq(self):
        """
        Load S(Q) from file
        Returns
        -------

        """
        return

    def evt_plot_bragg_bank(self):
        """

        Returns
        -------

        """


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Qtrac Ltd.")
    app.setOrganizationDomain("qtrac.eu")
    app.setApplicationName("Image Changer")
    app.setWindowIcon(QIcon(":/icon.png"))
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
