import re
import os
import imageio
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import csv

import cv2
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
        print(tmp)
        return int(sum(tmp)/len(tmp))
        #return (Counter(tmp).most_common(1))[0][0]


class PortionAndCircle:
    def __init__(self):
        pass

    def concat_up(self, array_list):
        if len(array_list) != 7:
            return 0
        line0 = array_list[0]
        line1 = np.hstack((array_list[1], array_list[2]))
        line2 = np.hstack((array_list[3], array_list[4]))
        line3 = np.hstack((array_list[5], array_list[6]))
        pic = np.vstack((line0, line1))
        pic = np.vstack((pic, line2))
        pic = np.vstack((pic, line3))
        return pic

    def Portion(self, img):
        #We should portion each image into seven ellipses
        #I want this to return a list of seven np array
        array_list = []
        height = len(img)
        length = len(img[0])

        line0 = img[0:int(height/2)]
        arr0 = np.array(line0)

        line1 = img[int(height/2): int(2*height/3)]
        arr1 = np.array([i[:int(length/2)] for i in line1])
        arr2 = np.array([i[int(length/2):length] for i in line1])

        line2 = img[int(2*height/3): int(5*height/6)]
        arr3 = np.array([i[:int(length/2)] for i in line2])
        arr4 = np.array([i[int(length/2):length] for i in line2])

        line3 = img[int(5*height/6): height]
        arr5 = np.array([i[:int(length/2)] for i in line3])
        arr6 = np.array([i[int(length/2):length] for i in line3])
      
        array_list.append(arr0)
        array_list.append(arr1)
        array_list.append(arr2)
        array_list.append(arr3)
        array_list.append(arr4)
        array_list.append(arr5)
        array_list.append(arr6)
        return array_list
        
    def FitEllipse(self, img_file):
        im = cv2.imread(img_file)
        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
       
        #item_list is a list of two-dimensional matrix
        #each of the two-dimensional matrix corresponds to a part of the person, head, arms, legs, etc
        #item_list should be of length 7
        #this is because the function Portion had divided the picture into 7 parts
        item_list = self.Portion(imgray)
        
        print("In FitEllipse: ", img_file)
        #label is the name of the person
        label = img_file.split('/')[2].split('_')[0]
        
        #probe_data will contain all the features we extracted from the picture
        probe_data = []
        for item in item_list:
            ret, thresh = cv2.threshold(item, 180, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            
            if len(contours) != 0:
                for i in range(len(contours)):
                    if (len(contours[i]) >= 5):
                        ellipse = cv2.fitEllipse(contours[i])
            #ellipse returns the centroid, major axis and minor axis lengths and angle
                        probe_data.append(str(ellipse[0][0]))
                        probe_data.append(str(ellipse[0][1]))
                        probe_data.append(str(ellipse[1][1]/(ellipse[1][0] + 1e-99)))
                        probe_data.append(str(ellipse[2]))
                        break

        #Then we write the probe_data to our csv file
        with open("raw.csv", "a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([label] + probe_data)

#test stub
PC = PortionAndCircle()

#Write the head of the csv file
#This will write the first row of the csv file: -1, 0, 1, 2, ..., 27
with open("raw.csv", "a") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['-1'] + [str(i) for i in range(28)])

#Traverse each directory of the training set
#Traverse each of the pictures in each directory
#Fit them with ellipses, and write the data in our csv file
for dirs in os.listdir("./train/"):
    if not os.path.isdir('./train/' + dirs + '/'):
        continue
    else:
        for item in os.listdir("./train/" + dirs + '/'):
            if ("cut" in item):
                PC.FitEllipse("./train/" + dirs +'/'+ item)



#The part below is currently useless
'''
CD = Cycle_Detector("./train/fyc_00_1/")
CD.get_pixel_sum_list()
CD.get_bottems_in_list()
print(CD.get_cycle())
'''
