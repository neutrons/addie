# Dialog to edit S(Q)


from PyQt4 import QtGui, QtCore

import ui_editSq

class EditSofQDialog(QtGui.QDialog):
    """
    Extended dialog class to edit S(Q)
    """
    MyEditSignal = QtCore.SIGNAL(float, float, str)
    MySaveSignal = QtCore.SIGNAL(str)

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
        self.connect(self.ui.lineEdit_scaleFactor, QtCore.SIGNAL('blabla'),
                     self.event_cal_sq)
        self.connect(self.ui.lineEdit_shift, QtCore.SIGNAL('blabla'),
                     self.event_cal_sq)

        # connect signals
        self.MyEditSignal.connect(self._myParentWindow.blabla)
        self.MySaveSignal.connect()

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
        # get the workspace name
        workspace_name = str(self.ui.comboBox_workspaces.currentText())
        if len(workspace_name) == 0:
            return

        try:
            shift = float(self.ui.lineEdit_shift.text())
            scaler = float(self.ui.lineEdit_scaleFactor.text())
        except ValueError as val_error:
            print '[ERROR] Shift or Scaler cannot be converted to float.'
            return

        self.MyEditSignal.emit(workspace_name, shift, scaler)

        return