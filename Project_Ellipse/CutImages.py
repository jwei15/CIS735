'''
CutImage is mainly responsible for:
    Read from the pictures and cut them to pictures of size 240x100

The first version of this file intent to cut images to size 240x80
but a width of 80 will lose some useful pixels, So I modified it to width 100

Author: Jinhao Wei
'''
import dirloader
import tools
#import gadget

import os
import imageio
import numpy as np


DEFAULT_WIDTH = 100 

np.set_printoptions(threshold = np.inf)

class CutImage:
    def __init__(self):
        pass

    #Given an image, return the white part and resize it to width 80
    #img_path is absolute path
    def cut_single_image(self, img_path):
        #print("Cutting image: ", img_path)
        image = imageio.imread(img_path)
        tmp = (image.T)/255
        new_tmp = []
        for rows in tmp:
            if not (1 in rows):
                continue
            new_tmp.append(list(rows))
        
        height = len(new_tmp[0])
        PADDING_ROW_COUNT = int((DEFAULT_WIDTH - len(new_tmp))/2)
        
        #Pad from front and rear
        #This could give us 80 or 81, we need to figure it out, so we use two if statements
        if (len(new_tmp) > DEFAULT_WIDTH):
            for i in range( int((len(new_tmp) - DEFAULT_WIDTH) /2)):
                new_tmp.pop(0)
            for i in range((len(new_tmp) - DEFAULT_WIDTH)):
                del new_tmp[-1]
        
        if (len(new_tmp) < DEFAULT_WIDTH):
            for i in range(PADDING_ROW_COUNT):
                new_tmp.append([0.0 for j in range(height)])
            for i in range(DEFAULT_WIDTH - len(new_tmp)):
                new_tmp.insert(0, [0 for j in range(height)])
        #print("Writing cut file: ", os.path.splitext(img_path)[0] + "_cut.png")
        imageio.imwrite(os.path.splitext(img_path)[0] + "_cut.png", (np.array(new_tmp).T))    
    #To cut all the images under a directory
    def cut_images(self, dir_path):
        print("Processing ", dir_path)
        if not os.path.isdir(dir_path):
            return 0
        for images in os.listdir(dir_path):
            if (os.path.splitext(images)[1] == '.png') and (not "cut" in images):
                self.cut_single_image(dir_path + images)
   
CI = CutImage()

for dirs in os.listdir("./train/"):
    CI.cut_images("./train/" + dirs + "/")    

for dirs in os.listdir("./test/"):
    CI.cut_images("./test/" + dirs + "/")    



#The part below is currently useless, just consider this to be a test stub
'''
for dirs in os.listdir("./train/"):
    print(dirs)
    picList = []
    if (os.path.isdir("./train/" + dirs + "/")):
        for images in os.listdir("./train/" + dirs + "/"):
            images_abs_path = "./train/" + dirs + "/" + images
            if ("cut" in images):
                picList.append(images_abs_path)
        picList.sort()

        image_List = []
        for item in picList:
            image_List.append(imageio.imread(item))
 
        CD = gadget.Cycle_Detector("./train/" + dirs + "/")
        CD.get_pixel_sum_list()
        CD.get_bottems_in_list()
        cycle = CD.get_cycle()

        print(cycle)
'''
