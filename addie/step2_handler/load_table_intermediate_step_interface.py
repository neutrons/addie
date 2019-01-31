from __future__ import (absolute_import, division, print_function)
from qtpy.QtWidgets import (QDialog)
from addie.utilities import load_ui
from addie.utilities.gui_handler import GuiHandler


class loadTableIntermediateStepInterface(QDialog):

    def __init__(self, parent=None):
        self.parent = parent

        QDialog.__init__(self, parent=parent)
        self.ui = load_ui('ui_loadTableIntermediateStep.ui', baseinstance=self)
        self.parent.load_intermediate_step_ok = False

    def closeEvent(self, event=None):
        pass

    def ok_clicked(self):
        o_gui = GuiHandler(parent=self)
        _state_button = o_gui.radiobutton_get_state(widget_id=self.ui.remove_temperature_checkbox)
        self.parent.remove_dynamic_temperature_flag = _state_button
        self.parent.load_intermediate_step_ok = True
        self.close()
        self.parent.move_to_folder_step2()

    def cancel_clicked(self):
        self.close()
