import sys

import ui_mainWindow

import PyQt4
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

import fastgrdriver as driver

__version__ = "1.0.0"


class MainWindow(PyQt4.QtGui.QMainWindow):
    """ Main FastGR window
    """

    def __init__(self, parent=None):
        """ Initialization
        Parameters
        ----------
        parent :: parent application
        """

        # Base class
        QtGui.QMainWindow.__init__(self, parent)

        self.ui = ui_mainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.dockWidget_ipython.setup()

        # set widgets
        self._init_widgets()

        # define the event handling methods
        # bragg diffraction tab
        self.connect(self.ui.pushButton_loadBraggFile, QtCore.SIGNAL('clicked()'),
                     self.do_load_bragg_file)
        self.connect(self.ui.checkBox_bank1, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.checkBox_bank2, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.checkBox_bank3, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.checkBox_bank4, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.checkBox_bank5, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.checkBox_bank6, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.comboBox_xUnit, QtCore.SIGNAL('stateChanged(int)'),
                     self.evt_plot_bragg_bank)

        # for tab G(R)
        self.connect(self.ui.pushButton_loadSQ, QtCore.SIGNAL('clicked()'),
                     self.do_load_sq)
        self.connect(self.ui.radioButton_sq, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_sq)
        self.connect(self.ui.radioButton_sqm1, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_sq)
        self.connect(self.ui.radioButton_qsqm1, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_sq)
        self.connect(self.ui.pushButton_showQMinMax, QtCore.SIGNAL('clicked()'),
                     self.do_show_sq_bound)
        self.connect(self.ui.pushButton_generateGR, QtCore.SIGNAL('clicked()'),
                     self.do_generate_gr)
        self.connect(self.ui.pushButton_saveGR, QtCore.SIGNAL('clicked()'),
                     self.do_save_GR)
        self.connect(self.ui.pushButton_clearGrCanvas, QtCore.SIGNAL('clicked()'),
                     self.do_clear_gr)

        # interaction with canvas

        self.ui.graphicsView_sq.canvas().mpl_connect('button_press_event',
                                                     self.on_mouse_press_event)
        self.ui.graphicsView_sq.canvas().mpl_connect('button_release_event',
                                                     self.on_mouse_release_event)
        self.ui.graphicsView_sq.canvas().mpl_connect('motion_notify_event',
                                                     self.on_mouse_motion)

        # organize widgets group
        self.braggBankWidgets = {1: self.ui.checkBox_bank1,
                                 2: self.ui.checkBox_bank2,
                                 3: self.ui.checkBox_bank3,
                                 4: self.ui.checkBox_bank4,
                                 5: self.ui.checkBox_bank5,
                                 6: self.ui.checkBox_bank6}

        # define the driver
        self._myController = driver.FastGRDriver()

        self._gssGroupName = None

        # some controlling variables


        return

    def on_mouse_press_event(self, event):
        """

        Returns
        -------

        """
        print 'Pressed @ (%.5f, %.5f)' % (event.xdata, event.ydata)

        if self.ui.graphicsView_sq.is_boundary_shown():
            self.ui.graphicsView_sq.set_mouse_pressed_position(event.xdata, event.ydata)

        return

    def on_mouse_release_event(self, event):
        """

        Parameters
        ----------
        event

        Returns
        -------

        """
        print 'Released'

        if self.ui.graphicsView_sq.is_boundary_shown():
            self.ui.graphicsView_sq.set_mouse_current_position(event.xdata, event.ydata)

        return

    def on_mouse_motion(self, event):
        """

        Returns
        -------

        """
        if self.ui.graphicsView_sq.is_boundary_shown():
            self.ui.graphicsView_sq.set_mouse_current_position(event.xdata, event.ydata)

        return

    def _init_widgets(self):
        """ Initialize widgets
        Returns
        -------

        """
        self.ui.comboBox_xUnit.clear()
        self.ui.comboBox_xUnit.addItems(['TOF', 'dSpacing', 'Q'])

        self.ui.treeWidget_braggWSList.set_parent_window(self)
        self.ui.treeWidget_grWsList.set_main_window(self)

        self.ui.dockWidget_ipython.iPythonWidget.set_main_application(self)

        return

    def do_clear_gr(self):
        """
        Clear G(r) canvas
        Returns
        -------

        """
        self.ui.graphicsView_gr.clear_all_lines()

        return

    def do_generate_gr(self):
        """
        Generate G(r) by the present user-setup
        Returns
        -------

        """
        # get data
        # calculate the G(R)
        min_r = float(self.ui.doubleSpinBoxRmin.value())
        max_r = float(self.ui.doubleSpinBoxRmax.value())
        delta_r = float(self.ui.doubleSpinBoxDelR.value())

        min_q = float(self.ui.doubleSpinBoxQmin.value())
        max_q = float(self.ui.doubleSpinBoxQmax.value())

        gr_ws_name = self._myController.calculate_gr(min_r, delta_r, max_r, min_q, max_q)

        # plot G(R)
        vec_r, vec_g, vec_ge = self._myController.get_gr(min_q, max_q)
        key_plot = gr_ws_name
        self.ui.graphicsView_gr.plot_gr(key_plot, vec_r, vec_g, vec_ge, False)

        # add to tree
        gr_param_str = 'Q: (%.3f, %.3f)' % (min_q, max_q)
        self.ui.treeWidget_grWsList.add_gr(gr_param_str, gr_ws_name)

        return

    def plot_gr(self, gr_ws_name_list):
        """
        Plot G(r) by its name (workspace as protocol)
        Parameters
        ----------
        gr_ws_name

        Returns
        -------

        """
        # TODO/NOW - Docs and check

        # plot G(R)
        for gr_ws_name in gr_ws_name_list:
            vec_r, vec_g, vec_ge = self._myController.get_gr_by_ws(gr_ws_name)
            key_plot = gr_ws_name
            self.ui.graphicsView_gr.plot_gr(key_plot, vec_r, vec_g, vec_ge, False)

        return

    def do_load_bragg_file(self):
        """
        Load Bragg files including GSAS, NeXus, 3-column ASCii.
        Returns
        -------
        """
        # get file
        ext = 'GSAS (*.gsa, *.gss);;DAT (*.dat);;Nexus (*.nxs)'
        bragg_file_name = str(QtGui.QFileDialog.getOpenFileName(self, 'Choose Bragg File', ext))
        if bragg_file_name is None:
            return

        # load file
        gss_ws_name = self._myController.load_bragg_file(bragg_file_name)

        # split
        self._gssGroupName = self._myController.split_to_single_bank(gss_ws_name)

        # clear all lines
        self.ui.graphicsView_bragg.reset()

        # plot and will triggered the graph
        self.ui.checkBox_bank1.setChecked(True)

        # add to tree
        banks_list = ['bank1', 'bank2', 'bank3', 'bank4', 'bank5', 'bank6']
        self.ui.treeWidget_braggWSList.add_bragg_ws_group(self._gssGroupName, banks_list)

        return

    def do_load_sq(self):
        """
        Load S(Q) from file
        Returns
        -------

        """
        # get the file
        ext = 'DAT (*.dat);;All (*.*)'
        sq_file_name = str(QtGui.QFileDialog.getOpenFileName(self, 'Choose S(Q) File', ext))
        if sq_file_name is None:
            return

        # open the file
        q_min, q_max = self._myController.load_sq(sq_file_name)

        # set the UI widgets
        self.ui.doubleSpinBoxQmin.setValue(q_min)
        self.ui.doubleSpinBoxQmax.setValue(q_max)

        # plot the figure
        self.ui.radioButton_sq.setChecked(True)

        # calculate and calculate G(R)
        self.do_generate_gr()

        return

    def do_save_GR(self):
        """

        Returns
        -------

        """
        # TODO/NOW - Implement!
        self.ui.dockWidget_ipython.wild_test()

    def do_show_sq_bound(self):
        """
        Show or hide the left and right boundary of the S(Q)
        Returns
        -------

        """
        q_left = self.ui.doubleSpinBoxQmin.value()
        q_right = self.ui.doubleSpinBoxQmax.value()
        self.ui.graphicsView_sq.toggle_boundary(q_left, q_right)

        return

    def evt_plot_bragg_bank(self):
        """
        Find out which bank will be plot
        Returns
        -------

        """
        # check
        assert self._gssGroupName is not None

        # get current unit
        x_unit = str(self.ui.comboBox_xUnit.currentText())
        if x_unit == 'Q':
            x_unit = 'MomentumTransfer'

        # get bank IDs to plot
        plot_bank_list = list()
        for bank_id in self.braggBankWidgets.keys():
            bank_checkbox = self.braggBankWidgets[bank_id]
            if bank_checkbox.isChecked():
                plot_bank_list.append(bank_id)
            # END-IF
        # END-FOR

        # get the list of banks to plot or remove
        new_bank_list, remove_bank_list = self.ui.graphicsView_bragg.check_banks(plot_bank_list)
        new_data_list = list()
        for bank_id in new_bank_list:
            vec_x, vec_y, vec_e = self._myController.get_bragg_data(bank_id, x_unit)
            new_data_list.append((vec_x, vec_y, vec_e))
        # END-FOR

        # remove unused and plot new
        self.ui.graphicsView_bragg.remove_banks(remove_bank_list)
        self.ui.graphicsView_bragg.plot_banks(new_bank_list, new_data_list, x_unit)

        return

    def evt_plot_sq(self):
        """ Event handling to plot S(Q)
        Returns
        -------

        """
        # get the raw S(Q)
        vec_q, vec_sq, vec_se = self._myController.get_sq()

        # get the unit
        sq_unit = None
        if self.ui.radioButton_sq.isChecked():
            # use the original S(Q)
            sq_unit = 'S(Q)'
            vec_y = vec_sq
        elif self.ui.radioButton_sqm1.isChecked():
            # use S(Q)-1
            sq_unit = 'S(Q)-1'
            vec_y = vec_sq - 1
        elif self.ui.radioButton_qsqm1.isChecked():
            # use Q(S(Q)-1)
            sq_unit = 'Q(S(Q)-1)'
            vec_y = vec_q * (vec_sq - 1)
        else:
            raise RuntimeError('None of S(Q), S(Q)-1 or Q(S(Q)-1) is chosen.')

        # plot
        self.ui.graphicsView_sq.plot_sq(vec_q, vec_y, vec_se, sq_unit)

        return

    def process_workspace_change(self, new_ws_list):
        """

        Returns
        -------

        """
        # TODO/NOW - Check & doc & figure out what to do!
        print 'current tab = ', self.ui.tabWidget.currentIndex(), self.ui.tabWidget.currentWidget(),
        print self.ui.tabWidget.currentWidget().objectName()

        print 'current workspaces: ', self._myController.get_current_workspaces()

        # add to tree
        if len(new_ws_list) > 0:
            if self.ui.tabWidget.currentWidget().objectName() == 'tab_gR':
                self.ui.treeWidget_grWsList.add_main_item('workspaces', append=True)
                for new_ws in new_ws_list:
                    self.ui.treeWidget_grWsList.add_temp_ws(new_ws)

        return

    def set_ipython_script(self, script):
        """

        Parameters
        ----------
        script

        Returns
        -------

        """
        # TODO/NOW - Doc and check
        self.ui.dockWidget_ipython.iPythonWidget.write_command(script)

        return


def main():
    app = PyQt4.QtGui.QApplication(sys.argv)
    app.setOrganizationName("Qtrac Ltd.")
    app.setOrganizationDomain("qtrac.eu")
    app.setApplicationName("Image Changer")
    app.setWindowIcon(PyQt4.QtGui.QIcon(":/icon.png"))
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
