from __future__ import (absolute_import, division, print_function)

from qtpy.QtWidgets import QApplication
from qtpy import QtCore

import copy

from addie.utilities.general import remove_white_spaces
from addie.processing.mantid.master_table.import_from_database.oncat_template_retriever import OncatTemplateRetriever
from addie.databases.oncat.oncat import pyoncatGetNexus, pyoncatGetRunsFromIpts
from addie.utilities.general import json_extractor
import addie.processing.mantid.master_table.import_from_database.utilities as  database_utilities


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

            if str_runs == "":
                "no runs provided. nothing to do"
                self.parent.nexus_json_from_template = {}
                return

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
        nexus_json = self.parent.nexus_json_from_template

        if self.parent.ui.run_radio_button.isChecked():

            # remove white space to string to make ONCat happy
            str_runs = str(self.parent.ui.run_number_lineedit.text())
            str_runs = remove_white_spaces(str_runs)
            #
            # nexus_json = pyoncatGetNexus(oncat=self.parent.parent.oncat,
            #                              instrument=self.parent.parent.instrument['short_name'],
            #                              runs=str_runs,
            #                              facility=self.parent.parent.facility,
            #                              )

            result = database_utilities.get_list_of_runs_found_and_not_found(str_runs=str_runs,
                                                                             oncat_result=nexus_json)
            list_of_runs_not_found = result['not_found']
            self.parent.list_of_runs_not_found = list_of_runs_not_found
            self.parent.list_of_runs_found = result['found']

        else:
            # ipts = str(self.parent.ui.ipts_combobox.currentText())
            #
            # nexus_json = pyoncatGetRunsFromIpts(oncat=self.parent.parent.oncat,
            #                                     instrument=self.parent.parent.instrument['short_name'],
            #                                     ipts=ipts,
            #                                     facility=self.parent.parent.facility)

            result = database_utilities.get_list_of_runs_found_and_not_found(oncat_result=nexus_json,
                                                                             check_not_found=False)

            self.parent.list_of_runs_not_found = result['not_found']
            self.parent.list_of_runs_found = result['found']

        if insert_in_table:
            self.parent.insert_in_master_table(nexus_json=nexus_json)
        else:
            self.isolate_metadata(nexus_json)
            self.parent.nexus_json = nexus_json

        QApplication.restoreOverrideCursor()

        if insert_in_table:
            self.parent.close()

    def isolate_metadata(self, nexus_json):
        '''retrieve the metadata of interest from the json returns by ONCat'''

        # def _format_proton_charge(raw_proton_charge):
        #     _proton_charge = raw_proton_charge/1e12
        #     return "{:.3}".format(_proton_charge)

        oncat_metadata_filters = self.parent.parent.oncat_metadata_filters

        # initialization of metadata dictionary
        metadata = {}
        for _entry in oncat_metadata_filters:
            metadata[_entry["title"]] = []

        for _json in nexus_json:

            for _entry in oncat_metadata_filters:
                _value = json_extractor(json=copy.deepcopy(_json),
                                        list_args=copy.deepcopy(_entry['path']))
                metadata[_entry["title"]].append(_value)

        # make sure we only have the unique element in each arrays
        for _item in metadata.keys():
            metadata[_item] = set(metadata[_item])

        self.parent.metadata = metadata
