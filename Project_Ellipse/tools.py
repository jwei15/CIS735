import os
import numpy as np
import imageio

'''
To add matrix [M1, M2 ... Mn] together, as long as they have the same shape
ImageList is an list of two-dimensional np array
'''
def AddImgsUp(ImageList):
    if (len(ImageList) == 0):
        return 0
    else:
        tmp = np.zeros((len(ImageList[0]), len(ImageList[0][1])))
        print(tmp.shape)
        for img in ImageList:
            tmp = tmp + img
    return tmp


'''        
Two return the sum of the elements in a two-dimensional matrix
But I guess this also work for an numpy array
'''
def SumOfTwoDim(mat):
    res = 0
    for row in mat:
        for item in row:
            res += item
    return res

'''
To return how many non-zero elements are there in a two-dimensional list
But I believe that this work for an numpy array
'''
def NonzeroCount(mat):
    count = 0
    for rows in mat:
        for e in rows:
            if e:
                count += 1
    return count

'''
Given a list, return the indexs that are the local smallest values in the list
a local smallest element is the element a[i] such that a[i-1] <= a[i] <= a[i+1]
'''
def local_minimum_indexs(List):
    tmp = []
    for i in range(1, len(List) - 1):
        if (List[i] <= List[i+1] and List[i] <= List[i-1]):
            tmp.append(i)
    return tmp


'''
hstack a list of numpy array
'''
def hstack_list(np_array_list):
    if len(np_array_list) == 0:
        return 0
    tmp = np_array_list[0]
    for i in range(1, len(np_array_list)):
        tmp = np.hstack((tmp,np_array_list[i]))

    return tmp

'''
hstack up the sum_up pics, and return the corresponding label list
'''
def reorganize_data(data_dir):
    label_list = []
    imgList= []
    for dirs in os.listdir(data_dir):
        label = dirs
        dirs = data_dir + dirs + "/"
        if not os.path.isdir(dirs):
            continue
        picList = []
        for images in os.listdir(dirs):
            if "sum" in images:
                images = dirs + images
                picList.append(images)

        picList.sort()

        for pic_name in picList:
            imgList.append(imageio.imread(pic_name))
            label_list.append(label)
    #print(len(imgList))
    #imageio.imwrite("test.png", hstack_list(imgList))
    return imgList, label_list

#This is currently useless for this project, this was meant for GEI and PCA approach
reorganize_data("./train/")
