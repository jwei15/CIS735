import os
import shutil

cwd_abs = os.getcwd()
dirs = os.listdir(cwd_abs + "/train/")

if os.path.isdir("./cnn_data/"):
    shutil.rmtree("./cnn_data/")
os.mkdir("./cnn_data/")

for dir_ in dirs:
    if "DS" in dir_:
        continue
    print("========  " + dir_ + "  ===========")
    for file_ in os.listdir(cwd_abs + "/train/" + dir_):
        print(file_)
        if ("sum" in file_):
            shutil.copy(cwd_abs + "/train/" + dir_ + "/" + file_ , "./cnn_data/" + dir_ +"_"+ file_ )




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
