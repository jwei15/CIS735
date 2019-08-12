import tools
import imageio
import numpy as np
from sklearn.decomposition import PCA
from sklearn import svm

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


'''

This part below shows how PCA works

'''
pca = PCA(n_components=90)

#Train on testingset, then transform both training and testing set
X_train_pca = pca.fit_transform(trainingset)
X_test_pca = pca.transform(testingset)

eigengaits = pca.components_.reshape((90, 240, 100))
#print(eigengaits[0])
for i in range(90):
    imageio.imwrite("./SampleEigenGaits/Sample_Eigen_Gait_" + str(i) +".png", eigengaits[i])


clf = svm.LinearSVC()
clf.fit(X_train_pca, traininglabel)
result = clf.predict(X_test_pca)

sum = 0
for i in range(len(result)):
    if result[i] == testinglabel[i]:
        sum += 1
print("Acc: ", sum/len(result))

