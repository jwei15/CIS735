import tools
import imageio
import numpy as np
from sklearn.decomposition import PCA
np.set_printoptions(threshold = np.inf)


#We will define a function to compare how close two vectors are
def Vector_Distance(vec1, vec2):
    sum = 0
    for i in range(len(vec1)):
        sum += (vec1[i] - vec2[i])**2
    return sum

import ReformTrainingset
import ReformTestingset

trainingset, traininglabel = ReformTrainingset.getTrainingSet()
testingset, testinglabel = ReformTestingset.getTestingSet()


#This part shows the humblest method
import time
start1 = time.clock()

calculated_test_label_0 = []
for i in range(len(testingset)):
    vec1 = testingset[i]
    best_index = 0
    current_closest_distance = np.inf
    for j in range(len(trainingset)):
        vec2 = trainingset[j]
        if Vector_Distance(vec1, vec2) < current_closest_distance:
            current_closest_distance = Vector_Distance(vec1, vec2)
            best_index = j
    calculated_test_label_0.append(traininglabel[best_index])

acc = 0
for i in range(len(testinglabel)):
    if testinglabel[i] == calculated_test_label_0[i]:
        acc += 1
print("Raw Acc (without PCA): ", acc/len(testinglabel), " Time used: ", time.clock() - start1)





'''

This part below shows how PCA works

'''
start2 = time.clock()
pca = PCA(n_components=0.9999)

#Train on testingset, then transform both training and testing set
X_train_pca = pca.fit_transform(trainingset)
X_test_pca = pca.transform(testingset)

#In this step, we compare each transformed testing sample to every transformed training sample
#We use the closest one as our calculated test label
calculated_test_label = []
for i in range(len(X_test_pca)):
    vec1 = X_test_pca[i]
    best_index = 0
    current_closest_distance = np.inf
    for j in range(len(X_train_pca)):
        vec2 = X_train_pca[j]
        if Vector_Distance(vec1, vec2) < current_closest_distance:
            current_closest_distance = Vector_Distance(vec1, vec2)
            best_index = j
    calculated_test_label.append(traininglabel[best_index])

acc = 0
for i in range(len(testinglabel)):
    if testinglabel[i] == calculated_test_label[i]:
        acc += 1
print("PCA Acc: ", acc/len(testinglabel), "  Time Used:", time.clock() - start2)


'''
#This returns the n_component eigvectors with the greatest eigvalue
#This part is currently not useful for this project

def PCA_manual(pic_path, n_component):
    (imageList, labelList) = tools.reorganize_data(pic_path)

    image_mean = sum(imageList)/len(imageList)

    item = imageList[0]
    S = np.dot((item - image_mean), ((item - image_mean).T))
    for i in range(1, len(imageList)):
        item = imageList[i]
        S += np.dot((item - image_mean), ((item - image_mean).T))
    
    eigVals, eigVects = np.linalg.eig(np.mat(S))
    eigValIndice = np.argsort(eigVals)
    n_eigValIndice = eigValIndice[-n_component:]
    n_eigVect = [eigVects[i] for i in n_eigValIndice]

    return n_eigVect
'''
