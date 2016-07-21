class FileHandler(object):
    
    file_contain = []
    
    def __init__(self, filename=None):
        self.filename = filename
        
    def retrieve_contain(self):
        file_contain = []
        with open(self.filename, 'r') as f:
            file_contain = f.read()
            
        self.file_contain = file_contain
