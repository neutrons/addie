import os
import ConfigParser


class FileHandler(object):
    
    file_contain = []
    
    def __init__(self, filename=None):
        self.filename = filename
        
    def retrieve_contain(self):
        file_contain = []
        with open(self.filename, 'r') as f:
            file_contain = f.read()
            
        self.file_contain = file_contain
        
    def check_file_extension( self, ext_requested = 'txt'):
        file_parsed = self.filename.split(".")
        if len(file_parsed) > 1:
            _ext = file_parsed[-1]
            if _ext != ext_requested:
                self.filename = self.filename + "." + ext_requested
        else:
            self.filename = self.filename + "." + ext_requested

    def create_ascii(self, contain=None, carriage_return=True):
        _filename = self.filename
        f = open(_filename, 'w')
        for _line in contain:
            if carriage_return:
                f.write(_line + "\n")
            else:
                f.write(_line)
                
        f.close()
        
    def create_config_parser(self, dictionary=None):
        config = ConfigParser.ConfigParser()
        cfgfile = open(self.filename, 'w')
        
        config.add_section("Configuration")
        for key, value in dictionary.iteritems():
            config.set('Configuration', key, value)
            
        config.write(cfgfile)
        cfgfile.close()
        
