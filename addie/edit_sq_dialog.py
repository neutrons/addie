# Dialog to edit S(Q)
from PyQt4 import QtGui, QtCore

import ui_editSq


class EditSofQDialog(QtGui.QDialog):
    """
    Extended dialog class to edit S(Q)
    """
    MyEditSignal = QtCore.pyqtSignal(str, float, float)
    MySaveSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent_window):
        """
        initialization
        """
        super(EditSofQDialog, self).__init__()

        # check inputs
        assert parent_window is not None, 'Parent window cannot be None.'

        self._myParentWindow = parent_window

        # set up UI
        self.ui = ui_editSq.Ui_Dialog()
        self.ui.setupUi(self)

        # set up default value
        self._init_widgets()

        # set up event handlers
        self.connect(self.ui.pushButton_quit, QtCore.SIGNAL('clicked()'),
                     self.do_quit)

        self.connect(self.ui.pushButton_saveNewSq, QtCore.SIGNAL('clicked()'),
                     self.do_save)

        # connect widgets' events with methods
        self.connect(self.ui.pushButton_editSQ, QtCore.SIGNAL('clicked()'),
                     self.do_edit_sq)

        # TODO/NOW - replace by 'set' button
        # self.connect(self.ui.lineEdit_scaleFactor, QtCore.SIGNAL('textChanged(QString)'),
        #              self.event_cal_sq)
        # self.connect(self.ui.lineEdit_shift, QtCore.SIGNAL('textChanged(QString)'),
        #              self.event_cal_sq)

        self.connect(self.ui.pushButton_setScaleRange, QtCore.SIGNAL('clicked()'),
                     self.do_set_scale_range)
        self.connect(self.ui.pushButton_setShiftRange, QtCore.SIGNAL('clicked()'),
                     self.do_set_shift_range)

        # connect q-slide
        self.connect(self.ui.horizontalSlider_scale, QtCore.SIGNAL('valueChanged()'),
                     self.event_cal_sq)
        self.connect(self.ui.horizontalSlider_shift, QtCore.SIGNAL('valueChanged()'),
                     self.event_cal_sq)

        # connect signals
        self.MyEditSignal.connect(self._myParentWindow.edit_sq)
        self.MySaveSignal.connect(self._myParentWindow.do_save_sq)

        # initialize class variables
        self._scaleMin = None
        self._scaleMax = None
        self._shiftMin = None
        self._shiftMax = None

        self._shiftSlideMutex = False
        self._scaleSlideMutex = True

        return

    def _init_widgets(self):
        """
        initialize widgets by their default values
        :return:
        """
        self.ui.comboBox_workspaces.clear()
        self.ui.lineEdit_scaleFactor.setText('1.')
        self.ui.lineEdit_shift.setText('0.')

        # slider limit
        self.ui.lineEdit_scaleMin.setText('0')
        self.ui.lineEdit_scaleMax.setText('5')
        self.ui.lineEdit_shiftMin.setText('-5')
        self.ui.lineEdit_shiftMax.setText('5')

        # set up class variable
        self._scaleMin = 0
        self._scaleMax = 5
        self._shiftMin = -5
        self._shiftMax = 5

        # set up the sliders
        self._shiftSlideMutex = True
        self.ui.horizontalSlider_shift.setMinimum(0)
        self.ui.horizontalSlider_shift.setMaximum(100)
        self.ui.horizontalSlider_shift.setValue(49)
        self._shiftSlideMutex = False

        return

    def do_edit_sq(self):
        """handling for push button 'edit S(Q)' by reading the scale factor and shift
        :return:
        """
        # read the scale and shift value
        print '[DB...BAT] Shift = {0} Scale Factor = {1}'.format(self.ui.lineEdit_shift.text(),
                                                                 self.ui.lineEdit_scaleFactor.text())

        shift_str = str(self.ui.lineEdit_shift.text())
        scale_str = str(self.ui.lineEdit_scaleFactor.text())
        try:
            # parse shift
            if len(shift_str) == 0:
                shift = 0
                self.ui.lineEdit_shift.setText('0.')
            else:
                shift = float(self.ui.lineEdit_shift.text())

            # parse scaling factor
            if len(scale_str) == 0:
                scale_factor = 1.
                self.ui.lineEdit_scaleFactor.setText('1.')
            else:
                scale_factor = float(scale_str)
        except ValueError as val_error:
            print '[ERROR] Shift {0} or scale factor {1} cannot be converted to float due to {2}.' \
                  ''.format(shift_str, scale_str, val_error)
            return

        # call edit_sq()
        self.edit_sq(shift, scale_factor)

        # enable mutex
        self._scaleSlideMutex = True
        self._shiftSlideMutex = True

        # set sliders
        self.set_scale_value(scale_factor)
        self.set_shift_value(shift)

        # disable mutex
        self._scaleSlideMutex = False
        self._shiftSlideMutex = False

        return

    def do_quit(self):
        """
        close the window and quit
        :return:
        """
        self.close()

        return

    def do_save(self):
        """
        save SofQ
        :return:
        """
        # get the selected S(Q)
        sq_ws_name = str(self.ui.comboBox_workspaces.currentText())

        self.MyEditSignal.emit(sq_ws_name)

        return

    def add_sq_by_name(self, sq_name_list):
        """
        add a list of S(Q) by workspace name
        :param sq_name_list:
        :return:
        """
        # check
        assert isinstance(sq_name_list, list), 'S(Q) workspace names {0} must be given by list but not {1}' \
                                               ''.format(sq_name_list, type(sq_name_list))

        # add
        for sq_ws_name in sq_name_list:
            # TODO/FUTURE - Need to make this one work! (ALL)
            if sq_ws_name != 'All':
                self.add_workspace(sq_ws_name)

        return

    def add_workspace(self, ws_name):
        """
        add workspace name
        :return:
        """
        # check input
        assert isinstance(ws_name, str), 'Input workspace name {0} must be a string but not a {1}.'.\
            format(ws_name, type(ws_name))

        self.ui.comboBox_workspaces.addItem(ws_name)

        return

    def event_cal_sq(self):
        """handling the events from a moving sliding bar such that a new S(Q) will be calculated
        :return:
        """
        # check whether mutex is on or off
        if self._shiftSlideMutex or self._scaleSlideMutex:
            # return if either mutex is on: it is not a time to do calculation
            return

        # read the value of sliders
        shift_int = self.ui.horizontalSlider_shift.value()
        scale_int = self.ui.horizontalSlider_scale.value()

        # convert to double
        shift = shift_int * ((self._shiftMax - self._shiftMin)/(self.ui.horizontalSlider_shift.maximum() -
                                                                self.ui.horizontalSlider_shift.minimum()))
        scale = scale_int * ((self._scaleMax - self._scaleMin)/(self.ui.horizontalSlider_scale.maximum() -
                                                                self.ui.horizontalSlider_scale.minimum()))

        # call edit_sq()
        self.edit_sq(shift, scale)

        # enable mutex
        self._shiftSlideMutex = True
        self._scaleSlideMutex = True

        # edit line edits for shift and scale
        self.ui.lineEdit_scaleFactor.setText('{0}'.format(scale))
        self.ui.lineEdit_shift.setText('{0}'.format(shift))

        # disable mutex
        self._shiftSlideMutex = False
        self._scaleSlideMutex = False

        return

    def edit_sq(self, shift, scale_factor):
        """ edit S(Q)
        :param shift:
        :param scale_factor:
        :return:
        """
        # check
        assert isinstance(shift, float), 'Shift {0} must be a float but not a {1}.' \
                                         ''.format(shift, type(shift))
        assert isinstance(scale_factor, float), 'Scale factor {0} must be a float but not a {1}.' \
                                                ''.format(scale_factor, type(scale_factor))

        # get the workspace name
        workspace_name = str(self.ui.comboBox_workspaces.currentText())
        if len(workspace_name) == 0:
            print '[INFO] No workspace is selected'
            return

        # set out the signal
        # TODO/NOW - parent class shall edit S(Q) and calculate G(r) again!
        self.MyEditSignal.emit(workspace_name, scale_factor, shift)

        return

    def do_set_scale_range(self):
        """set the range of scale factor slider bar
        :return:
        """
        # get new scale range
        min_scale = float(self.ui.lineEdit_scaleMin.text())
        max_scale = float(self.ui.lineEdit_scaleMax.text())

        # check valid or not!
        if min_scale >= max_scale:
            # if not valid: set the values back to stored original
            print '[ERROR] Minimum scale factor value {0} cannot exceed maximum scale factor value {1}.' \
                  ''.format(min_scale, max_scale)
            return
        else:
            # re-set the class variable as the new min/max is accepted
            self._scaleMin = min_scale
            self._scaleMax = max_scale

        # otherwise, re-set the slider
        current_scale_factor = float(self.ui.lineEdit_scaleFactor.text())
        if current_scale_factor < min_scale:
            current_scale_factor = min_scale
        elif current_scale_factor > max_scale:
            current_scale_factor = max_scale

        scale_factor_int = int(current_scale_factor/(max_scale - min_scale)*(self.ui.horizontalSlider_scale.maximum() - self.ui.horizontalSlider_scale.minimum()))
        self.ui.horizontalSlider_scale.setValue(scale_factor_int)

        return

    def do_set_shift_range(self):
        """set the new range of shift slider
        :return:
        """
        # get new scale range
        min_shift = float(self.ui.lineEdit_shiftMin.text())
        max_shift = float(self.ui.lineEdit_shiftMax.text())

        # check valid or not!
        if min_shift >= max_shift:
            # if not valid: set the values back to stored original
            print '[ERROR] Minimum scale factor value {0} cannot exceed maximum scale factor value {1}.' \
                  ''.format(min_shift, max_shift)
            return
        else:
            # re-set the class variable as the new min/max is accepted
            self._shiftMin = min_shift
            self._shiftMax = max_shift

        # otherwise, re-set the slider
        curr_shift = float(self.ui.lineEdit_shift.text())
        if curr_shift < min_shift:
            curr_shift = min_shift
        elif curr_shift > max_shift:
            curr_shift = max_shift

        shift_int = int(curr_shift/(max_shift - min_shift)*(self.ui.horizontalSlider_shift.maximum() - self.ui.horizontalSlider_shift.minimum()))
        self.ui.horizontalSlider_shift.setValue(shift_int)

        return