
import xyDist
import pandas as pd
import numpy as np

class AODE:
    def __init__(self):
        self.dist = xyDist.xyDist("./train.csv")
        self.testfile = pd.read_csv("./test.csv")
        self.testfile.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis = 1, inplace=True)
        self.testcount = len(self.testfile)
        self.acc = 0
        
        for i, row in self.testfile.iterrows():
            self.classify(row)
        print("AODE acc: ",self.acc/self.testcount)
        
    def normalise(self, posterior):
        tmp = sum(posterior)
        for i in range(len(posterior)):
            posterior[i] = posterior[i]/tmp


    def classify(self, instance):
        posteriorP = [[1e40 for i in range(xyDist.CLS_NUM)] for j in range(xyDist.ATT_NUM)]
        
        for i in range(xyDist.ATT_NUM):
            #Now we deal with the case where i in the parent of every attribute
            for j in range(xyDist.CLS_NUM):
                for k, item in instance.iteritems():
                    if k != '-1':
                        if k != str(i): #Att k is not parent of Att k
                            posteriorP[i][j] = posteriorP[i][j] * self.dist.condPxxy(int(k),int(item) , i, int(instance[str(i)]),j)
                        else:
                            posteriorP[i][j] = posteriorP[i][j]*self.dist.condPxy(i, int(instance[str(i)]),j)
                posteriorP[i][j] = posteriorP[i][j]*self.dist.Py(j)
            self.normalise(posteriorP[i])

        pos_overall = list(np.mean(np.array(posteriorP), axis = 0))

        if (pos_overall.index(max(pos_overall)) == instance['-1']):
            self.acc += 1

classifier = AODE()
