class GuiHandler:

    @staticmethod
    def preview_widget_status(window_ui, enabled_widgets=False):
        """enable or not all the widgets related to the preview tab"""
        window_ui.search_logo_label.setEnabled(enabled_widgets)
        window_ui.name_search.setEnabled(enabled_widgets)
        window_ui.clear_search_button.setEnabled(enabled_widgets)
        window_ui.list_of_runs_label.setEnabled(enabled_widgets)

    @staticmethod
    def filter_widget_status(window_ui, enabled_widgets=False):
        """enable or not all the widgets related to the filter tab"""
        window_ui.tableWidget.setEnabled(enabled_widgets)
        window_ui.add_criteria_button.setEnabled(enabled_widgets)
        window_ui.filter_result_label.setEnabled(enabled_widgets)
        window_ui.tableWidget_filter_result.setEnabled(enabled_widgets)

    @staticmethod
    def check_import_button(parent):
        window_ui = parent.ui
        enable_import = False
        if window_ui.ipts_radio_button.isChecked():
            if str(window_ui.ipts_lineedit.text()).strip() != "":
                if parent.ipts_exist:
                    enable_import = True
            else:
                enable_import = True
        else:
            if str(window_ui.run_number_lineedit.text()).strip() != "":
                enable_import = True

        window_ui.import_button.setEnabled(enable_import)