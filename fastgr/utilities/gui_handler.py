class GuiHandler(object):
    
    def __init__(self, parent=None):
        self.parent = parent
        
    def dropdown_value(self, widget_id = None):
        if not widget_id:
            return "N/A"
        
        return widget_id.currentText()
    
    def radiobutton_state(self, widget_id = None):
        return widget_id.isChecked()