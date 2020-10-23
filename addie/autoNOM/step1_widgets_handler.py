from __future__ import (absolute_import, division, print_function)


class Step1WidgetsHandler(object):

    def __init__(self, parent=None):
        self.parent = parent.autonom_ui
        self.parent_no_ui = parent

    def set_recalibration(self, status):
        self.parent.recalibration_yes.setChecked(status)
        self.parent.recalibration_no.setChecked(not status)

    def set_renormalization(self, status):
        self.parent.renormalization_yes.setChecked(status)
        self.parent.renormalization_no.setChecked(not status)

    def set_autotemplate(self, status):
        self.parent.autotemplate_yes.setChecked(status)
        self.parent.autotemplate_no.setChecked(not status)
