import os
import shutil
import sys

DataPath = "E:/735/Project/GaitDatasetA-silh/"

paths = os.listdir(DataPath) #To get all the directories in DataPath

#Create test folder to contain testing data
if not (os.path.isdir("test")):
    os.mkdir("test")

#Create train folder to contain training data
if not (os.path.isdir("train")):
    os.mkdir("train")
    
for path in paths:
    if os.path.isdir(path):
        for dirs in os.listdir(path):
            if dirs == "00_1":
                TEST_PATH = DataPath + "test/" + path + '_' + dirs + '/'
                TRAIN_PATH = DataPath + "train/" + path + '_' + dirs + '/'
                CURRENT_PATH = DataPath + path+ '/' + dirs + '/'
            
                if not os.path.isdir(TEST_PATH):
                    os.mkdir(TEST_PATH)
                if not os.path.isdir(TRAIN_PATH):
                    os.mkdir(TRAIN_PATH)
                
                if not (len(os.listdir(TEST_PATH)) == 0):
                    if not (len(os.listdir(TRAIN_PATH)) == 0):
                        print("Dataset already splited up before, no further action required")
                        sys.exit()
                
                i = 0
                for images in os.listdir(CURRENT_PATH):
                    FULL_IMAGE_PATH = CURRENT_PATH + images
                    if i < 12:
                        shutil.copy(FULL_IMAGE_PATH, TEST_PATH)
                    else:
                        shutil.copy(FULL_IMAGE_PATH, TRAIN_PATH)
                    i = i+1
            
    

