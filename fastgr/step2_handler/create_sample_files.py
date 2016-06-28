from PyQt4.QtCore import Qt
import os

from step2_handler.table_handler import TableHandler


class CreateSampleFiles(object):

    list_selected_row = None
    file_extension = '.ini'
        
    def __init__(self, parent = None):
        self.parent = parent
        self.current_dir = self.parent.current_folder
        
    def run(self):
        self._retrieve_list_of_selected_rows()
        self._create_list_of_sample_properties_files()
                
    def _retrieve_list_of_selected_rows(self):
        o_table_handler = TableHandler(parent = self.parent)
        o_table_handler.retrieve_list_of_selected_rows()
        self.list_selected_row = o_table_handler.list_selected_row
                
    def _create_list_of_sample_properties_files(self):
        _list_selected_row = self.list_selected_row
        nbr_files = len(_list_selected_row)
        for _index_file in range(nbr_files):
            self._export_ini_file(_list_selected_row[_index_file])

    def _export_ini_file(self, row_metadata):
        full_name_of_file = os.path.join(self.current_dir, row_metadata['name'] + self.file_extension)
        _text = []
        _text.append(row_metadata['name'] + ' #sample title\n')
        if row_metadata['sample_formula']:
            _text.append(row_metadata['sample_formula'] + ' #sample formula\n')       

        if row_metadata['mass_density']:
            _text.append(row_metadata['mass_density'] + ' #mass density in g/cc\n')

        if row_metadata['radius']:
            _text.append(row_metadata['radius'] + ' #radius in cm\n')
            
        if row_metadata['packing_fraction']:
            _text.append(row_metadata['packing_fraction'] + ' #packing fraction\n')
            
        _text.append(row_metadata['sample_shape'] + ' #sample shape\n')
        _text.append(row_metadata['do_abs_correction'] + ' #do absorption correction in IDL\n')
        
        f = open(full_name_of_file, 'w')
        for _line in _text:
            f.write(_line)
        f.close()

  