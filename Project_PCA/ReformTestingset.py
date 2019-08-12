import os
import shutil
import imageio
import numpy as np

cwd_abs = os.getcwd()
dirs = os.listdir(cwd_abs + "/test/")

Total_test_Img = []
Class = []

if os.path.isdir("./pca_test/"):
    shutil.rmtree("./pca_test/")
os.mkdir("./pca_test/")

def getTestingSet():
    for dir_ in dirs:
        if "DS" in dir_:
            continue
        print("========  " + dir_ + "  ===========")
        for file_ in os.listdir(cwd_abs + "/test/" + dir_):
            if "sum" in file_:
                print(file_)
                img = np.array(imageio.imread(cwd_abs + "/test/" + dir_ + '/' + file_)).reshape(-1).tolist()
                Total_test_Img.append(img)
                Class.append(dir_)
    print(Class)
    imageio.imwrite("./pca_data/Total_test_Img.png", Total_test_Img)
    return Total_test_Img, Class


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
