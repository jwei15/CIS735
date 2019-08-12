import os
import shutil

import imageio
import numpy as np

cwd_abs = os.getcwd()
dirs = os.listdir(cwd_abs + "/train/")

if os.path.isdir("./pca_data/"):
    shutil.rmtree("./pca_data/")
os.mkdir("./pca_data/")

Total_Img = []
Class = []

def getTrainingSet():
    for dir_ in dirs:
        #I always hate this directory "DS_Store"
        if "DS" in dir_:
            continue
        print("========  " + dir_ + "  ===========")
        for file_ in os.listdir(cwd_abs + "/train/" + dir_):
            if "sum" in file_:
                print(file_)
                img = np.array(imageio.imread(cwd_abs + "/train/" + dir_ + '/'+file_)).reshape(-1).tolist()
                Total_Img.append(img)
                Class.append(dir_)

    imageio.imwrite("./pca_data/Total_Img.png", Total_Img)        
    return Total_Img, Class

'''
files= os.listdir(path) 
s = []
for file in files:
    if not os.path.isdir(file):
        f = open(path+"/"+file)
          iter_f = iter(f)
          str = ""
          for line in iter_f:
              str = str + lines.append(str)
'''
