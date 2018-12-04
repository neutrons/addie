import json


try:
    from PyQt4.QtGui import QDialog, QFileDialog
    from PyQt4 import QtCore, QtGui
except ImportError:
    try:
        from PyQt5.QtWidgets import QDialog, QFileDialog
        from PyQt5 import QtCore, QtGui
    except ImportError:
        raise ImportError("Requires PyQt4 or PyQt5")

from addie.ui_reduction_configuration_dialog import Ui_Dialog as UiDialog

from addie.make_calibration_handler.make_calibration import MakeCalibrationLauncher


class ReductionConfigurationHandler:

    def __init__(self, parent=None):

        if parent.reduction_configuration_ui == None:
            parent.reduction_configuration_ui = ReductionConfiguration(parent=parent)
            parent.reduction_configuration_ui.show()
            if parent.reduction_configuration_ui_position:
                parent.reduction_configuration_ui.move(parent.reduction_configuration_ui_position)
            else:
                parent.reduction_configuration_ui.activateWindow()
                parent.reduction_configuration_ui.setFocus()


class ReductionConfiguration(QDialog):

    def __init__(self, parent=None):
        self.parent = parent
        QDialog.__init__(self, parent=parent)
        self.ui = UiDialog()
        self.ui.setupUi(self)
        self.init_widgets()

    def init_widgets(self):
        '''init all widgets with values in case we already openned that window, or populated with
        default values'''
        self.ui.reset_pdf_q_range_button.setIcon(QtGui.QIcon(":/MPL Toolbar/reset_logo.png"))
        self.ui.reset_pdf_r_range_button.setIcon(QtGui.QIcon(":/MPL Toolbar/reset_logo.png"))

        # list of sample environment
        config_file = self.parent.addie_config_file
        with open(config_file) as f:
            data = json.load(f)
        pdf_q_range = data['pdf_q_range']

        self.ui.pdf_q_range_min.setText(str(pdf_q_range["min"]))
        self.ui.pdf_q_range_max.setText(str(pdf_q_range["max"]))
        self.ui.pdf_q_range_delta.setText(str(pdf_q_range["delta"]))

        pdf_r_range = data['pdf_r_range']
        self.ui.pdf_r_range_min.setText(str(pdf_r_range["min"]))
        self.ui.pdf_r_range_max.setText(str(pdf_r_range["max"]))
        self.ui.pdf_r_range_delta.setText(str(pdf_r_range["delta"]))

    def pdf_reset_q_range_button(self):
        pass

    def pdf_reset_r_range_button(self):
        pass

    def make_calibration_clicked(self):
        MakeCalibrationLauncher(parent=self, grand_parent=self.parent)

    def close_button(self):
        # save state of buttons

        # close
        self.closeEvent(event=None)

    def closeEvent(self, event=None):
        self.parent.reduction_configuration_ui = None
        self.parent.reduction_configuration_ui_position = self.pos()



