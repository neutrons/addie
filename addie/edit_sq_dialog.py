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
        self.connect(self.ui.lineEdit_scaleFactor, QtCore.SIGNAL('textChanged(QString)'),
                     self.event_cal_sq)
        self.connect(self.ui.lineEdit_shift, QtCore.SIGNAL('textChanged(QString)'),
                     self.event_cal_sq)

        # connect signals
        self.MyEditSignal.connect(self._myParentWindow.edit_sq)
        self.MySaveSignal.connect(self._myParentWindow.do_save_sq)

        return

    def _init_widgets(self):
        """
        initialize widgets by their default values
        :return:
        """
        self.ui.comboBox_workspaces.clear()
        self.ui.lineEdit_scaleFactor.setText('1.')
        self.ui.lineEdit_shift.setText('0.')

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
            # TODO - Need to make this one work! (ALL)
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
        """
        handling the events such that a new S(Q) will be calculated
        :return:
        """
        print '[DB...BAT] Shift = {0} Scale Factor = {1}'.format(self.ui.lineEdit_shift.text(),
                                                                 self.ui.lineEdit_scaleFactor.text())

        # get the workspace name
        workspace_name = str(self.ui.comboBox_workspaces.currentText())
        if len(workspace_name) == 0:
            print '[INFO] No workspace is selected'
            return

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

        # set out the signal
        self.MyEditSignal.emit(workspace_name, scale_factor, shift)

        return
