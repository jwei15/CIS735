import os
import shutil

cwd_abs = os.getcwd()
dirs = os.listdir(cwd_abs + "/test/")

if os.path.isdir("./cnn_data_test/"):
    shutil.rmtree("./cnn_data_test/")
os.mkdir("./cnn_data_test/")

for dir_ in dirs:
    if "DS" in dir_:
        continue
    print("========  " + dir_ + "  ===========")
    for file_ in os.listdir(cwd_abs + "/test/" + dir_):
        print(file_)
        if ("sum" in file_):
            shutil.copy(cwd_abs + "/test/" + dir_ + "/" + file_ , "./cnn_data_test/" + dir_ +"_"+ file_ )




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
