import os

class loader:
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.dirlist = []
        
        self.load_dirs()
    
    def load_dirs(self):
        train_dir = self.path + "\\train\\"
        test_dir = self.path + "\\test\\" 
        
        for dir in os.listdir(train_dir):
            if os.path.isdir(test_dir + dir + "\\"):
                self.dirlist.append([train_dir + dir + "\\", test_dir + dir + "\\"])
        return self.dirlist
         
    def show_dirlist(self):
        print(self.dirlist)
    
'''   
ld = loader("./GaitDatasetA-silh/")
ld.show_dirlist()
'''
