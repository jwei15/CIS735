import re
import os
import imageio
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

import tools
import dirloader

np.set_printoptions(threshold = np.inf)

#The class that detects the cycle of each person's gait
class Cycle_Detector:    
    def __init__(self, image_dir):
        self.path = image_dir
        self.tuple_list = []
        self.local_minimum_indexs = []
    
    #The sum of the count of pixels in each picture
    #If ( not pixel == 0 ) sum += 1
    #We use the sum of the count of pixel to help us determine the walking cycle
    def get_pixel_sum_list(self):
        image_list = [] #This is used to store the absolute path of the images
        pixel_count_list = []
        for image_path in os.listdir(self.path):
            if "cut" in image_path:
                abs_path = self.path + image_path
                image_list.append(abs_path)
            
        image_list.sort()
        tuple_list = []
        for image in image_list:
            img = imageio.imread(image)
            pixel_count = tools.NonzeroCount(img)
            pixel_count_list.append(pixel_count)
            self.tuple_list.append((image, pixel_count))
        return self.tuple_list
    
    #This function gives us all the indexes of bottem values in a list
    #In a list x, a bottom value is a value x[i] such that x[i-1] <= x[i] <= x [i+1]
    def get_bottems_in_list(self):
        List = []
        for item in self.tuple_list:
            List.append(item[1])
        self.local_minimum_indexs = tools.local_minimum_indexs(List)

    #return the cycle for this person's gait
    def get_cycle(self):
        print(self.local_minimum_indexs)
        indexs = self.local_minimum_indexs
        print(indexs)
        tmp = []
        for i in range(2, len(indexs) - 1):
            tmp.append(indexs[i] - indexs[i-2])
        if len(tmp) == 0:
            return 0
        return int(sum(tmp)/len(tmp))
        #return (Counter(tmp).most_common(1))[0][0]
#test stub

'''
CD = Cycle_Detector("./train/fyc_00_1/")
CD.get_pixel_sum_list()
CD.get_bottems_in_list()
print(CD.get_cycle())
'''
