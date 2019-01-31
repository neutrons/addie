from addie.utilities.general import remove_white_spaces
from addie.master_table.import_from_database.oncat_template_retriever import OncatTemplateRetriever
from addie.utilities.oncat import pyoncatGetIptsList, pyoncatGetNexus, \
    pyoncatGetRunsFromIpts, pyoncatGetTemplate
from addie.master_table.import_from_database import utilities as ImportFromDatabaseUtilities

try:
    from PyQt4.QtGui import QApplication
    from PyQt4 import QtGui, QtCore
except:
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5 import QtGui, QtCore
    except:
        raise ImportError("Requires PyQt4 or PyQt5")


class ImportTableFromOncat:

    def __init__(self, parent=None):
        self.parent = parent

    def from_oncat_template(self):
        """Using ONCat template, this method retrieves the metadata of either the IPTS or
               runs selected"""

        if self.parent.ui.run_radio_button.isChecked():
            # remove white space to string to make ONCat happy
            str_runs = str(self.parent.ui.run_number_lineedit.text())
            str_runs = remove_white_spaces(str_runs)

            projection = OncatTemplateRetriever.create_oncat_projection_from_template(with_location=True,
                                                                                      template=self.parent.oncat_template)

            nexus_json = pyoncatGetNexus(oncat=self.parent.parent.oncat,
                                         instrument=self.parent.parent.instrument['short_name'],
                                         runs=str_runs,
                                         facility=self.parent.parent.facility,
                                         projection=projection,
                                         )

        else:
            ipts = str(self.parent.ui.ipts_combobox.currentText())

            projection = OncatTemplateRetriever.create_oncat_projection_from_template(with_location=False,
                                                                                      template=self.parent.oncat_template)

            nexus_json = pyoncatGetRunsFromIpts(oncat=self.parent.parent.oncat,
                                                instrument=self.parent.parent.instrument['short_name'],
                                                ipts=ipts,
                                                facility=self.parent.parent.facility,
                                                projection=projection,
                                                )

        self.parent.nexus_json_from_template = nexus_json

    def from_oncat_config(self, insert_in_table=True):
        """using only the fields we are looking for (defined in the config.json file,
        this method retrieves the metadata of either the IPTS or the runs selected,
        and populate or not the Master table (if insert_in_table is True)"""

        QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        self.parent.list_of_runs_not_found = []

        if self.parent.ui.run_radio_button.isChecked():

            # remove white space to string to make ONCat happy
            str_runs = str(self.parent.ui.run_number_lineedit.text())
            str_runs = remove_white_spaces(str_runs)

            nexus_json = pyoncatGetNexus(oncat=self.parent.parent.oncat,
                                         instrument=self.parent.parent.instrument['short_name'],
                                         runs=str_runs,
                                         facility=self.parent.parent.facility,
                                         )

            result = ImportFromDatabaseUtilities.get_list_of_runs_found_and_not_found(str_runs=str_runs,
                                                                                      oncat_result=nexus_json)
            list_of_runs_not_found = result['not_found']
            self.parent.list_of_runs_not_found = list_of_runs_not_found
            self.parent.list_of_runs_found = result['found']

        else:
            ipts = str(self.parent.ui.ipts_combobox.currentText())

            nexus_json = pyoncatGetRunsFromIpts(oncat=self.parent.parent.oncat,
                                                instrument=self.parent.parent.instrument['short_name'],
                                                ipts=ipts,
                                                facility=self.parent.parent.facility)

            result = ImportFromDatabaseUtilities.get_list_of_runs_found_and_not_found(oncat_result=nexus_json,
                                                                                      check_not_found=False)

            self.parent.list_of_runs_not_found = result['not_found']
            self.parent.list_of_runs_found = result['found']

        if insert_in_table:
            self.parent.insert_in_master_table(nexus_json=nexus_json)
        else:
            self.parent.nexus_json = nexus_json
            self.parent.isolate_metadata()

        QApplication.restoreOverrideCursor()

        if insert_in_table:
            self.parent.close()