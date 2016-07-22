import sys
import os
from ipythondockwidget import IPythonDockWidget

import ui_mainWindow
import step1
import step2

from initialization.init_step1 import InitStep1
from step1_handler.step1_gui_handler import Step1GuiHandler
from step1_handler.run_step1 import RunStep1

from initialization.init_step2 import InitStep2
from step2_handler.populate_master_table import PopulateMasterTable
from step2_handler.populate_background_widgets import PopulateBackgroundWidgets
from step2_handler.step2_gui_handler import Step2GuiHandler
from step2_handler.table_handler import TableHandler
from step2_handler.create_sample_files import CreateSampleFiles
from step2_handler.create_ndsum_file import CreateNdsumFile
from step2_handler.run_ndabs import RunNDabs
from step2_handler.run_sum_scans import RunSumScans
from step3_handler.step3_gui_handler import Step3GuiHandler

import PyQt4
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

import fastgrdriver as driver

__version__ = "1.0.0"


class MainWindow(PyQt4.QtGui.QMainWindow, ui_mainWindow.Ui_MainWindow):
    """ Main FastGR window
    """
    debugging = False
    current_folder = os.getcwd()

    def __init__(self):
        """ Initialization
        Parameters
        ----------
        parent :: parent application
        """

        # Base class
        QtGui.QMainWindow.__init__(self)

        # Initialize the UI widgets
        self.ui = ui_mainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.graphicsView_sq.set_main(self)
 
        self.ui.dockWidget_ipython.setup()

        # set widgets
        self._init_widgets()
        init_step1 = InitStep1(parent=self)
        init_step2 = InitStep2(parent=self)

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
        self.connect(self.ui.comboBox_xUnit, QtCore.SIGNAL('currentIndexChanged(int)'),
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
        self.connect(self.ui.pushButton_clearSofQ, QtCore.SIGNAL('clicked()'),
                     self.do_clear_sq)
        self.connect(self.ui.pushButton_showQMinMax, QtCore.SIGNAL('clicked()'),
                     self.do_show_sq_bound)
        self.connect(self.ui.pushButton_generateGR, QtCore.SIGNAL('clicked()'),
                     self.do_generate_gr)
        self.connect(self.ui.pushButton_saveGR, QtCore.SIGNAL('clicked()'),
                     self.do_save_gr)
        self.connect(self.ui.pushButton_clearGrCanvas, QtCore.SIGNAL('clicked()'),
                     self.do_clear_gr)

        self.connect(self.ui.doubleSpinBoxQmin, QtCore.SIGNAL('valueChanged(double)'),
                     self.evt_qmin_changed)
        self.connect(self.ui.doubleSpinBoxQmax, QtCore.SIGNAL('valueChanged(double)'),
                     self.evt_qmax_changed)

        # organize widgets group
        self._braggBankWidgets = {1: self.ui.checkBox_bank1,
                                  2: self.ui.checkBox_bank2,
                                  3: self.ui.checkBox_bank3,
                                  4: self.ui.checkBox_bank4,
                                  5: self.ui.checkBox_bank5,
                                  6: self.ui.checkBox_bank6}
        self._braggBankWidgetRecords = dict()
        for bank_id in self._braggBankWidgets.keys():
            checked = self._braggBankWidgets[bank_id].isChecked()
            self._braggBankWidgetRecords[bank_id] = checked

        # define the driver
        self._myController = driver.FastGRDriver()

        self._gssGroupName = None

        # some controlling variables
        self._currBraggXUnit = str(self.ui.comboBox_xUnit.currentText())

        # mutex-like variables
        self._noEventBankWidgets = False

        return

    def evt_qmin_changed(self):
        """

        Returns:

        """
        q_min = self.ui.doubleSpinBoxQmin.value()
        q_max = self.ui.doubleSpinBoxQmax.value()

        if q_min < q_max and self.ui.graphicsView_sq.is_boundary_shown():
            self.ui.graphicsView_sq.move_left_indicator(q_min, relative=False)

        return

    def evt_qmax_changed(self):
        """
        Handle if the user change the value of Qmax of S(Q) including
        1. moving the right boundary in S(q) figure
        Returns:

        """
        q_min = self.ui.doubleSpinBoxQmin.value()
        q_max = self.ui.doubleSpinBoxQmax.value()

        if q_min < q_max and self.ui.graphicsView_sq.is_boundary_shown():
            self.ui.graphicsView_sq.move_right_indicator(q_max, relative=False)

        return

    def _init_widgets(self):
        """ Initialize widgets
        Returns
        -------

        """
        self.ui.comboBox_xUnit.clear()
        self.ui.comboBox_xUnit.addItems(['TOF', 'dSpacing', 'Q'])

        self.ui.treeWidget_braggWSList.set_main_window(self)
        self.ui.treeWidget_braggWSList.add_main_item('workspaces', append=True, as_current_index=False)

        self.ui.treeWidget_grWsList.set_main_window(self)
        self.ui.treeWidget_grWsList.add_main_item('workspaces', append=True, as_current_index=False)
        self.ui.treeWidget_grWsList.add_main_item('SofQ', append=True, as_current_index=False)

        self.ui.dockWidget_ipython.iPythonWidget.set_main_application(self)

        self.ui.radioButton_sq.setChecked(True)
        self.ui.radioButton_multiBank.setChecked(True)

        # add the combo box for PDF type
        self.ui.comboBox_pdfType.addItems(['G(r)', 'g(r)', 'RDF(r)'])

        # some starting value
        self.ui.doubleSpinBoxDelR.setValue(0.01)

        return

    def do_clear_gr(self):
        """
        Clear G(r) canvas
        Returns
        -------

        """
        self.ui.graphicsView_gr.clear_all_lines()

        return

    def do_clear_sq(self):
        """
        Clear S(Q) canvas
        Returns
        -------

        """
        self.ui.graphicsView_sq.clear_all_lines()

        return

    def do_generate_gr(self):
        """
        Generate G(r) by the present user-setup
        Returns
        -------

        """
        # get S(Q) workspace
        sq_ws_name = str(self.ui.comboBox_SofQ.currentText())

        # get r-range and q-range
        min_r = float(self.ui.doubleSpinBoxRmin.value())
        max_r = float(self.ui.doubleSpinBoxRmax.value())
        delta_r = float(self.ui.doubleSpinBoxDelR.value())

        min_q = float(self.ui.doubleSpinBoxQmin.value())
        max_q = float(self.ui.doubleSpinBoxQmax.value())

        # PDF type
        pdf_type = str(self.ui.comboBox_pdfType.currentText())

        # calculate the G(R)
        gr_ws_name = self._myController.calculate_gr(sq_ws_name, pdf_type, min_r, delta_r, max_r,
                                                     min_q, max_q)

        # plot G(R)
        vec_r, vec_g, vec_ge = self._myController.get_gr(min_q, max_q)
        key_plot = gr_ws_name
        self.ui.graphicsView_gr.plot_gr(key_plot, vec_r, vec_g, vec_ge, False)

        # add to tree
        gr_param_str = 'Q: (%.3f, %.3f)' % (min_q, max_q)
        self.ui.treeWidget_grWsList.add_gr(gr_param_str, gr_ws_name)

        return

    def plot_bragg(self, bragg_ws_list):
        """

        Parameters
        ----------
        bragg_ws_list

        Returns
        -------

        """
        for bragg_ws_name in bragg_ws_list:
            if bragg_ws_name.startswith('bank') and 0 <= int(bragg_ws_name.split('bank')[1]) < 6:
                bank_id = int(bragg_ws_name.split('bank')[1])
                self._braggBankWidgets[bank_id].setChecked(True)
            else:
                vec_x, vec_y, vec_e = self._myController.get_ws_data(bragg_ws_name)
                self.ui.graphicsView_bragg.plot_general_ws(bragg_ws_name, vec_x, vec_y, vec_e)

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

    def plot_sq(self, sq_ws_name, clear_prev):
        """
        Plot S(Q)
        Parameters
        ----------
        sq_ws_name
        clear_prev

        Returns
        -------

        """
        # clear previous lines
        if clear_prev:
            self.ui.graphicsView_sq.clear_all_lines()

        # get data
        vec_q, vec_sq, vec_se = self._myController.get_sq(sq_ws_name)

        # get the unit & do conversion if necessary
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
        if clear_prev:
            reset = True
        else:
            reset = False
        self.ui.graphicsView_sq.plot_sq(sq_ws_name, vec_q, vec_y, vec_se, sq_unit, reset)

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
        self._gssGroupName, banks_list, bank_angles = self._myController.split_to_single_bank(gss_ws_name)

        # add to tree
        # banks_list = ['bank1', 'bank2', 'bank3', 'bank4', 'bank5', 'bank6']
        self.ui.treeWidget_braggWSList.add_bragg_ws_group(self._gssGroupName, banks_list)

        # rename bank
        for bank_id in self._braggBankWidgets.keys():
            bank_check_box = self._braggBankWidgets[bank_id]
            if bank_angles[bank_id-1] is None:
                bank_check_box.setText('Bank %d' % bank_id)
            else:
                bank_check_box.setText('Bank %.1f' % bank_angles[bank_id-1])

        # clear all lines
        self.ui.graphicsView_bragg.reset()

        # un-check all the check boxes with mutex on and off
        self._noEventBankWidgets = True
        for check_box in self._braggBankWidgets.values():
            check_box.setChecked(False)
        self._noEventBankWidgets = False

        # plot and will triggered the grap
        self.ui.checkBox_bank1.setChecked(True)

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

        # load S(q)
        sq_ws_name, q_min, q_max = self._myController.load_sq(sq_file_name)

        # set to the tree and combo box
        self.ui.treeWidget_grWsList.add_child_main_item('SofQ', sq_ws_name)
        self.ui.comboBox_SofQ.addItem(sq_ws_name)
        self.ui.comboBox_SofQ.setCurrentIndex(self.ui.comboBox_SofQ.count()-1)

        # set the UI widgets
        self.ui.doubleSpinBoxQmin.setValue(q_min)
        self.ui.doubleSpinBoxQmax.setValue(q_max)

        # plot the figure
        self.evt_plot_sq()

        # calculate and calculate G(R)
        self.do_generate_gr()

        return

    def do_save_gr(self):
        """
        Save the selected the G(r) from menu to ASCII file
        Returns
        -------

        """
        # read the selected item from the tree
        gr_name_list = self.ui.treeWidget_grWsList.get_selected_items_of_level(2, excluded_parent='SofQ',
                                                                               return_item_text=True)
        if len(gr_name_list) != 1:
            self.pop_message('Error! Only 1 workspace of G(r) that can be selected.  So far %d'
                             ' is selected.' % len(gr_name_list))
            return
        else:
            gr_ws_name = gr_name_list[0]

        print '[DB...BAT] G(r) workspace: %s' % gr_ws_name

        # pop-up a dialog for the file to save
        default_dir = os.getcwd()
        file_ext = 'Data (*.dat)'
        gr_file_name = str(QtGui.QFileDialog.getSaveFileName(self, caption='Save G(r)',
                                                             directory=default_dir, filter=file_ext))

        # save!
        self._myController.save_ascii(gr_ws_name, gr_file_name)

        return

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
        # check mutex
        if self._noEventBankWidgets:
            return

        # check
        assert self._gssGroupName is not None

        # get current unit and check whether re-plot all banks is not a choice
        x_unit = str(self.ui.comboBox_xUnit.currentText())
        if x_unit != self._currBraggXUnit:
            re_plot = True
        else:
            re_plot = False
        print 'unit: %s vs. %s' % (x_unit, self._currBraggXUnit)
        self._currBraggXUnit = x_unit

        if x_unit == 'Q':
            x_unit = 'MomentumTransfer'

        # get bank IDs to plot
        plot_all_gss = self.ui.radioButton_multiGSS.isChecked()

        plot_bank_list = list()
        print '[DB...BAT] braggBankWidget: ', self._braggBankWidgets.keys()
        for bank_id in self._braggBankWidgets.keys():
            bank_checkbox = self._braggBankWidgets[bank_id]

            if not bank_checkbox.isChecked():
                # no-operation for not checked
                self._braggBankWidgetRecords[bank_id] = False
                continue

            if plot_all_gss:
                # only allow 1 check box newly checked
                print '[DB...BAT] Bank %d is previously %s.' % (bank_id, str(self._braggBankWidgetRecords[bank_id]))
                if self._braggBankWidgetRecords[bank_id]:
                    # create a mutex on bank widget check box
                    self._noEventBankWidgets = True
                    bank_checkbox.setChecked(False)
                    self._noEventBankWidgets = False

                    self._braggBankWidgetRecords[bank_id] = False
                else:
                    plot_bank_list.append(bank_id)
                    self._braggBankWidgetRecords[bank_id] = True
            else:
                # there is no limitation to plot multiple banks for 1-GSS mode
                plot_bank_list.append(bank_id)
                self._braggBankWidgetRecords[bank_id] = True
            # END-IF
        # END-FOR

        print '[DB...BAT] BraggBankWidgetRecord: ', str(self._braggBankWidgetRecords)

        # deal with the situation that there is no line to plot
        if len(plot_bank_list) == 0:
            # self.ui.graphicsView_bragg.clear_all_lines()
            self.ui.graphicsView_bragg.reset()
            return

        # check
        if plot_all_gss:
            assert len(plot_bank_list) == 1, 'Current number of banks selected is equal to %d. ' \
                                             'Must be 1.' % len(plot_bank_list)

        # determine the GSS workspace to plot
        if plot_all_gss:
            ws_group_list = self.ui.treeWidget_braggWSList.get_main_nodes()
            ws_group_list.remove('workspaces')
            print '[DB...BAT] workspace groups list:', ws_group_list
        else:
            status, ret_obj = self.ui.treeWidget_braggWSList.get_current_main_nodes()
            print '[DB...BAT] workspace group:', status, ret_obj
            if status:
                ws_group_list = ret_obj
            else:
                ws_group_list = [self._gssGroupName]
        # END-IF-ELSE

        # get the list of banks to plot or remove
        self.ui.graphicsView_bragg.clear_all_lines()

        # get new bank date
        plot_data_dict = dict()
        for ws_group in ws_group_list:
            ws_data_dict = dict()
            for bank_id in plot_bank_list:
                vec_x, vec_y, vec_e = self._myController.get_bragg_data(ws_group, bank_id, x_unit)
                ws_data_dict[bank_id] = (vec_x, vec_y, vec_e)
            # END-FOR
            plot_data_dict[ws_group] = ws_data_dict
        # END-FOR

        # remove unused and plot new
        if re_plot:
            self.ui.graphicsView_bragg.clear_all_lines()
            if x_unit == 'TOF':
                self.ui.graphicsView_bragg.setXYLimit(xmin=0, xmax=20000, ymin=None, ymax=None)
            elif x_unit == 'MomentumTransfer':
                self.ui.graphicsView_bragg.setXYLimit(xmin=0, xmax=20, ymin=None, ymax=None)
            elif x_unit == 'dSpacing':
                self.ui.graphicsView_bragg.setXYLimit(xmin=0, xmax=7, ymin=None, ymax=None)

        if plot_all_gss:
            self.ui.graphicsView_bragg.set_to_single_gss(False)
        else:
            self.ui.graphicsView_bragg.set_to_single_gss(True)

        self.ui.graphicsView_bragg.plot_banks(plot_data_dict, x_unit)

        return

    def evt_plot_sq(self):
        """ Event handling to plot S(Q)
        Returns
        -------

        """
        # get the raw S(Q)
        sq_name = self._myController.get_current_sq_name()

        # plot S(Q)
        self.plot_sq(sq_name, clear_prev=True)

        return

    def process_workspace_change(self, new_ws_list):
        """

        Returns
        -------

        """
        # TODO/NOW - Check & doc & figure out what to do!
        print 'current tab = ', self.ui.tabWidget_2.currentIndex(), self.ui.tabWidget_2.currentWidget(),
        print self.ui.tabWidget_2.currentWidget().objectName()

        print 'current workspaces: ', self._myController.get_current_workspaces()

        # add to tree
        if len(new_ws_list) > 0:
            if self.ui.tabWidget_2.currentWidget().objectName() == 'tab_gR':
                for new_ws in new_ws_list:
                    self.ui.treeWidget_grWsList.add_temp_ws(new_ws)
            elif self.ui.tabWidget_2.currentWidget().objectName() == 'tab_bragg':
                for new_ws in new_ws_list:
                    self.ui.treeWidget_braggWSList.add_temp_ws(new_ws)


        return

    def set_ipython_script(self, script):
        """
        Write a command (python script) to ipython console
        Parameters
        ----------
        script

        Returns
        -------

        """
        # check
        assert isinstance(script, str)

        #
        if len(script) == 0:
            # ignore
            return
        else:
            # write to the console
            self.ui.dockWidget_ipython.iPythonWidget.write_command(script)

        return

    def update_sq_boundary(self, boundary_index, new_position):
        """
        Update the S(Q) range at the main app inputs
        Returns
        -------

        """
        # check
        assert isinstance(boundary_index, int)
        assert isinstance(new_position, float)

        # set value
        if boundary_index == 1:
            # left boundary
            self.ui.doubleSpinBoxQmin.setValue(new_position)
        elif boundary_index == 2:
            # right boundary
            self.ui.doubleSpinBoxQmax.setValue(new_position)
        else:
            # exception
            raise RuntimeError('Boundary index %f in method update_sq_boundary() is not '
                               'supported.' % new_position)

        return

# step1
    def select_current_folder_clicked(self):
        o_gui = Step1GuiHandler(parent = self)
        o_gui.select_working_folder()

    def diamond_edited(self):
        self.check_step1_gui()
        
    def diamond_background_edited(self):
        self.check_step1_gui()
        
    def vanadium_edited(self):
        self.check_step1_gui()
        
    def vanadium_background_edited(self):
        self.check_step1_gui()
        
    def sample_background_edited(self):
        self.check_step1_gui()
        
    def output_folder_radio_buttons(self):
        o_gui_handler = Step1GuiHandler(parent=self)
        o_gui_handler.manual_output_folder_button_handler()
        o_gui_handler.check_go_button()

    def manual_output_folder_field_edited(self):
        self.check_step1_gui()
        
    def check_step1_gui(self):
        '''check the status of the step1 GUI in order to enable or not the GO BUTTON at the bottom'''
        o_gui_handler = Step1GuiHandler(parent=self)
        o_gui_handler.check_go_button()
        
    def run_autonom(self):
        """Will first create the output folder, then create the exp.ini file"""
        _run_autonom = RunStep1(parent = self)
        _run_autonom.create_folder()
        _run_autonom.create_exp_ini_file()

# step2
    def move_to_folder_clicked(self):
        o_gui = Step2GuiHandler(parent = self)
        o_gui.move_to_folder()
        self.populate_table_clicked()
        
    def populate_table_clicked(self):
        
        if self.debugging:
            self.current_folder = os.getcwd()  + '/autoNOM_01/'
        else:
            self.current_folder = os.getcwd()

        _pop_table = PopulateMasterTable(parent = self)
        _pop_table.run()
        _error_reported = _pop_table.error_reported
        
        if _error_reported:
            return
        
        _pop_back_wdg = PopulateBackgroundWidgets(parent = self)
        _pop_back_wdg.run()
        
        _o_gui = Step2GuiHandler(parent = self)
        _o_gui.check_gui()

    def table_select_state_changed(self, state, row):
        _o_gui = Step2GuiHandler(parent = self)
        _o_gui.check_gui()

    def check_q_range(self):
        _o_gui = Step2GuiHandler(parent = self)
        _o_gui.check_gui()

    def check_step2_gui(self, row, column):
        _o_gui = Step2GuiHandler(parent = self)
        _o_gui.check_gui()
            
    def hidrogen_clicked(self):
        o_gui = Step2GuiHandler(parent = self)
        o_gui.hidrogen_clicked()
    
    def no_hidrogen_clicked(self):
        o_gui = Step2GuiHandler(parent = self)
        o_gui.no_hidrogen_clicked()
    
    def yes_background_clicked(self):
        o_gui = Step2GuiHandler(parent = self)
        o_gui.yes_background_clicked()
    
    def no_background_clicked(self):
        o_gui = Step2GuiHandler(parent = self)
        o_gui.no_background_clicked()
        
    def background_combobox_changed(self, index):
        o_gui = Step2GuiHandler(parent = self)
        o_gui.background_index_changed(row_index = index)

    def reset_q_range(self):
        o_gui = Step2GuiHandler(parent = self)
        o_gui.reset_q_range()

    def run_ndabs_clicked(self):
        o_create_sample_files = CreateSampleFiles(parent = self)
        o_create_sample_files.run()
        
        list_sample_files = o_create_sample_files.list_sample_files
        
        o_create_ndsum_file = CreateNdsumFile(parent = self)
        o_create_ndsum_file.run()

        o_run_ndsum = RunNDabs(parent = self, list_sample_files = list_sample_files)
        o_run_ndsum.run()
        
    def check_fourier_filter_widgets(self):
        o_gui = Step2GuiHandler(parent = self)
        o_gui.check_gui()

    def check_plazcek_widgets(self):
        o_gui = Step2GuiHandler(parent = self)
        o_gui.check_gui()
        
    def table_right_click(self, position):
        _o_table = TableHandler(parent = self)
        _o_table.right_click(position = position)

    def run_sum_scans_clicked(self):
        o_run_sum_scans = RunSumScans(parent = self)
        o_run_sum_scans.run()

    # tab3 - ascii display
    def browse_ascii_file_clicked(self):
        o_gui = Step3GuiHandler(parent = self)
        o_gui.browse_file()


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
