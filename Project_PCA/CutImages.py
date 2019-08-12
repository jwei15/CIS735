#import dirloader
import tools
import gadget

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
        tmp = (image.T)
        new_tmp = []
        for rows in tmp:
            if not (sum(rows) > 0):
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
        imageio.imwrite(os.path.splitext(img_path)[0] + "_cut.png", (np.array(new_tmp).T))  #/255
    
    #To cut all the images under a directory
    def cut_images(self, dir_path):
        print("Processing ", dir_path)
        if not os.path.isdir(dir_path):
            return 0
        for images in os.listdir(dir_path):
            #if the image has not been cut, then we will cut it
            if (os.path.splitext(images)[1] == '.png') and (not "cut" in images):
                self.cut_single_image(dir_path + images)
   

# --------------    Should pass in "./train/" or "./test/"    -----------------------
def processPath(path_):
    CI = CutImage()

    
    for dirs in os.listdir(path_):
        CI.cut_images(path_ + dirs + "/")    
    

    for dirs in os.listdir(path_):
        print(dirs)
        picList = []
        if (os.path.isdir(path_ + dirs + "/")):
            for images in os.listdir(path_ + dirs + "/"):
                images_abs_path = path_ + dirs + "/" + images
                if ("cut" in images):
                    picList.append(images_abs_path)
            #We need to sort them, because python wont read file at ramdom orders
            picList.sort()

            image_List = []
            for item in picList:
                image_List.append(imageio.imread(item))
 
            CD = gadget.Cycle_Detector(path_ + dirs + "/")
            CD.get_pixel_sum_list()
            CD.get_bottems_in_list()
            cycle = CD.get_cycle()

            for i in range(int(len(picList) / cycle)):
                imageio.imwrite(path_ + dirs + "/sum" + str(i) + ".png", tools.AddImgsUp(image_List[i*cycle:(i+1)*cycle]))
                #print(imageio.imread(path_ + dirs + "/sum" +str(i) + ".png"))

processPath("./train/")
processPath("./test/")
