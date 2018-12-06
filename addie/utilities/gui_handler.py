from __future__ import (absolute_import, division, print_function)
class GuiHandler(object):

    def __init__(self, parent=None):
        self.parent = parent

    def dropdown_get_value(self, widget_id=None):
        if not widget_id:
            return "N/A"

        return widget_id.currentText()

    def dropdown_get_index(self, widget_id=None):
        if not widget_id:
            return -1

        return widget_id.currentIndex()

    def dropdown_set_index(self, widget_id=None, index=-1):
        if not widget_id:
            return

        widget_id.setCurrentIndex(index)

    def radiobutton_get_state(self, widget_id=None):
        return widget_id.isChecked()

    def radiobutton_set_state(self, widget_id=None, state=True):
        widget_id.setChecked(state)
