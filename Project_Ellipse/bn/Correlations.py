import os
import xyDist
import math
import numpy as np
import pandas as pd

class correlationMeasrues:
    def __init__(self):
        self.dist = xyDist.xyDist("./train.csv")

        self.testfile = pd.read_csv("./test.csv")
        self.testfile.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis = 1, inplace=True) 
        
        if (not os.path.exists("CMI.csv")):
            print("Calculating general CMI: ")
            self.generalCMI = self.getgeneralCMI()
            tmp = pd.DataFrame(columns = [str(i) for i in range(xyDist.ATT_NUM)], data = self.generalCMI)
            tmp.to_csv("CMI.csv")
        else:
            df = pd.read_csv("CMI.csv")
            df.drop("Unnamed: 0", axis = 1, inplace=True)
            self.generalCMI = df.values.tolist()
            #print(self.generalCMI[4][23], self.generalCMI[4][27])
        #self.localCMI = self.getlocalcondCMI(self.instance)
#
#                                                  p(x1, x2  y) p(y)
#CMI(X1;X2|Y) = \sum_{x1,x2,y} p(x1, x2, y) log --------------- 
#                                              p(x1,y) p(x2,y)

    def getgeneralCMI(self):
        tmp = [[0 for i in range(xyDist.ATT_NUM)] for j in range(xyDist.ATT_NUM) ]
        for i in range(xyDist.ATT_NUM):
            for j in range(xyDist.CAT_NUM):
                for k in range(xyDist.ATT_NUM):
                    for m in range(xyDist.CAT_NUM):
                        for n in range(xyDist.CLS_NUM):
                            if self.dist.xxyDist[i][j][k][m][n] != 0 and i!=k:
                                tmp[i][k] += self.dist.jointPxxy(int(i),int(j),int(k),int(m),int(n))*math.log(self.dist.jointPxxy(int(i), int(j), int(k), int(m), int(n)) * self.dist.Py(n)/self.dist.jointPxy(int(i), int(j), int(n)) / self.dist.jointPxy(int(k),int(m),int(n)) )
                                #tmp[i][k] += (self.dist.xxyDist[i][j][k][m][n]/self.dist.instancecount)*math.log( (self.dist.xDist['-1'][n]) *(self.dist.xxyDist[i][j][k][m][n]) /((self.dist.xyDist[i][j][n])*(self.dist.xyDist[k][m][n])))
        return tmp

#                                                               p(x1,x2|y)
#Frankly speaking, I was hoping this to be \sum P (y)* log -----------------
#                                                           p(x1|y)p(x2|y)
    def getlocalcondCMI(self, instance):
        tmp = [[0 for i in range(xyDist.ATT_NUM)] for j in range(xyDist.ATT_NUM)]
        #for i, row in self.testfile.iterrows():
        for i, item1 in instance.iteritems():
            for j, item2 in instance.iteritems():
                if i!= '-1' and j!= '-1':
                    if i!=j:
                        for k in range(xyDist.CLS_NUM):
                            if self.dist.jointPxxy(int(i), int(item1), int(j), int(item2), k) != 0:
                                tmp[int(i)][int(j)] += self.dist.Py(k)* math.log( self.dist.jointPxxy(int(i), int(item1), int(j), int(item2), int(k)) * self.dist.Py(k) / ((self.dist.jointPxy(int(i), int(item1), k))*(self.dist.jointPxy(int(j), int(item2), k))))
        #print(tmp)
        return tmp

#cm = correlationMeasrues()
