import os


class RunNDabs(object):
    
    script_to_run = 'python ~zjn/pytest/NDabs.py -f STO.ndsum'
    
    def __init__(self, parent = None, list_sample_files=None):
        self.parent = parent
        if list_sample_files  == []:
            return
        
        self.list_sample_files = list_sample_files
        
    def run(self):
        _str_list_sample_files = " ".join(self.list_sample_files)
        print("[LOG] executing:")
        print("[LOG] " + self.script_to_run + ' ' + _str_list_sample_files)
        os.system(self.script_to_run + ' ' + _str_list_sample_files)