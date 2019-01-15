from xml.dom import minidom
import numpy as np


class Utilities:
    '''utilities related to work in master table'''

    def __init__(self, parent=None):
        self.parent = parent
        self.table_ui = parent.ui.h3_table

    def get_row_index_from_row_key(self, row_key=None):
        '''this methods returns the row for the given row key'''

        if row_key == None:
            return -1

        master_table_row_ui = self.parent.master_table_list_ui
        nbr_row = self.parent.ui.h3_table.rowCount()

        checkbox_ui_of_row_key = master_table_row_ui[row_key]['active']

        for _row in np.arange(nbr_row):

            _ui_checkbox = self.parent.ui.h3_table.cellWidget(_row, 0).children()[1]
            if _ui_checkbox == checkbox_ui_of_row_key:
                return _row

        return -1

    def get_row_key_from_row_index(self, row=-1):
        '''this method returns the key (random key) of the given row in master table.
        An example of its use is if we want to retrieve the placzek settings for this row
        as they are saved in the master_table_row_ui using random key as the key
        '''

        if row == -1:
            return None

        master_table_row_ui = self.parent.master_table_list_ui

        for _key in master_table_row_ui.keys():

            _activate_ui = master_table_row_ui[_key]["active"]

            _activate_ui_of_given_row = self.table_ui.cellWidget(row, 0).children()[1]

            if _activate_ui == _activate_ui_of_given_row:
                return _key


class LoadGroupingFile:
    '''This class reads the XML file and will return the number of groups <group ID=""> found in that file'''

    def __init__(self, filename=''):
        self.filename = filename

    def get_number_of_groups(self):
        try:
            xmldoc = minidom.parse(self.filename)
            itemlist = xmldoc.getElementsByTagName('group')
            return len(itemlist)
        except:
            return 'N/A'

