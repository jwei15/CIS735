
import xyDist
import pandas as pd
import Correlations
import numpy as np

class tan:
    def __init__(self):
        self.dist = xyDist.xyDist("./train.csv")
        self.correlations = Correlations.correlationMeasrues()
        self.testfile = pd.read_csv("./test.csv")
        self.testfile.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis = 1, inplace=True)
        self.testcount = len(self.testfile)
        self.acc = 0
      
        
        self.CMImatrix = self.correlations.generalCMI
        self.Build()

        for it, instance in self.testfile.iterrows():
            self.classify(instance)
        print("TAN acc: ", self.acc/self.testcount)
        

    def normalise(self, posterior):
        tmp = sum(posterior)
        for i in range(len(posterior)):
            posterior[i] = posterior[i]/tmp
    
    #When we do Build, we create a general model
    #We need self.CMImatrix
    def Build(self):
        CMImatrix = self.CMImatrix
        print(np.array(CMImatrix).shape)
        #parent_list[i] holds the parent of ith att
        parent_list = [-1 for i in range(xyDist.ATT_NUM)]
        print("Arranging parent attributes for each attribute: ") 
        for i in range(xyDist.ATT_NUM):
            currentmax = i
            if (i == xyDist.ATT_NUM-1):
                break
            for j in range((int(i/4)*4), (int(i/4)*4+3)):
            #for j in range(i, xyDist.ATT_NUM):
                if i != j:
                    if (CMImatrix[i][j] > CMImatrix[i][currentmax]):
                        currentmax = j
            parent_list[i] = currentmax
        self.parent_list = parent_list
    
    def classify(self, instance):
        posteriorP = [1 for i in range(xyDist.CLS_NUM)]
        
        parents = self.parent_list
        #print(parents)
        for j in range(xyDist.CLS_NUM):
            for k, item in instance.iteritems():
                if k!='-1':
                    if parents[int(k)] != -1:
                        posteriorP[j] = posteriorP[j] * self.dist.condPxxy(int(k),int(item), int(parents[int(k)]), instance[str(parents[int(k)])],j)
                    else:
                        posteriorP[j] = posteriorP[j]*self.dist.condPxy(int(k),int(item),j)
            posteriorP[j] = posteriorP[j]*self.dist.Py(j)
        

        self.normalise(posteriorP)
        #print(posteriorP.index(max(posteriorP)), instance['-1'])

        if (posteriorP.index(max(posteriorP)) == instance['-1']):
            self.acc += 1

classifier = tan()
