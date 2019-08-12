import numpy as np
import csv
import pandas as pd

ATT_NUM = 28    #28 attributes and 1 class label
CAT_NUM = 30    #each Attribute is categorized to 30 values
CLS_NUM = 18

class xyDist:
    def __init__(self, filepath):
        self.filepath = filepath
        self.instancecount = 0

        self.xDist = {} #Return the count (X = x)
        self.xyDist = []    #Return the count (X = x, Y = y), we will find it at xyDist[X][x][y]
        self.xxyDist = []   #Return count(X1=x1, X2=x2,Y=y), use xxyDist[X1][x1][X2][x2][y]
 
        self.condxyDist = []    #Return P(X=x|Y=y)
        self.condxxyDist = []   #Return P(X1=x1|X2=x2,Y=y)

        self.getxDist()
        self.getxyDist()
        self.getxxyDist()
        self.getcondxyDist()
        self.getcondxxyDist()   
    
    def getcondxyDist(self):
        tmp = []
        for i in range(ATT_NUM):
            tmp1 = []
            for j in range(CAT_NUM):
                tmp1.append([1 for k in range(CLS_NUM)])
            tmp.append(tmp1)
        #Remember, P(X = x|Y =y) = P(X = x, Y =y)/P(Y = y)
        #The reason I dare to divide is that, I had controlled the index perfectly so P(Y = y) will never be 0
        for i in range(ATT_NUM):
            for j in range(CAT_NUM):
                for k in range(CLS_NUM):
                    tmp[i][j][k] = self.xyDist[i][j][k]/self.xDist['-1'][k]
        self.condxyDist = tmp

    #Remember, P(X1 = x1 | X2 = x2, Y=y ) = P(X1 = x1, X2 = x2, Y =y) / P(X2 = x2, Y = y)
    #The reason I dare to divide here is that, 
    #if P(X1 = x1, X2 = x2, Y =y) != 0, then P(X2 = x2, Y=y) will not be zero
    #Five-dimensional list, this real gonna be hurt
    def getcondxxyDist(self):
        tmp = []
        for i in range(ATT_NUM):
            tmp1 = []
            for j in range(CAT_NUM):
                tmp2 = []
                for k in range(ATT_NUM):
                    tmp3 = []
                    for m in range(CAT_NUM):
                        tmp3.append([1 for n in range(CLS_NUM)])
                    tmp2.append(tmp3)
                tmp1.append(tmp2)
            tmp.append(tmp1)
    
        for i in range(ATT_NUM):
            for j in range(CAT_NUM):
                for k in range(ATT_NUM):
                    for m in range(CAT_NUM):
                        for n in range(CLS_NUM):
                            denominator = self.xyDist[k][m][n]
                            numerator = self.xxyDist[i][j][k][m][n]
                            if numerator != 0:
                                tmp[i][j][k][m][n] = numerator/denominator
        self.condxxyDist = tmp
        
    #This returns the count
    def getxDist(self):
        df = pd.read_csv(self.filepath)
        df.drop(['Unnamed: 0'], axis = 1, inplace=True)
   
        for index, column in df.iteritems():
            self.instancecount = df[index].size
            tmp = [1 for i in range(CAT_NUM)]
            #for i, content in (df[index].value_counts()/df[index].size).iteritems():
            for i, content in (df[index].value_counts()).iteritems():
                tmp[i] = content
                self.xDist[index] = tmp

    def getxyDist(self):
        tmp = []
        for i in range(ATT_NUM):
            tmp1 = []
            for j in range(CAT_NUM):
                tmp1.append([1 for k in range(CLS_NUM)])
            tmp.append(tmp1)

        df = pd.read_csv(self.filepath)
        df.drop(['Unnamed: 0'], axis = 1, inplace = True)
        for i, row in df.iterrows():
            for att, value in row.iteritems():
                if att == '-1':
                    continue
                else:
                    tmp[int(att)][row[att]][row['-1']] += 1       
        self.xyDist = tmp

    def getxxyDist(self):
        tmp = []
        for i in range(ATT_NUM):
            tmp1 = []
            for j in range(CAT_NUM):
                tmp2 = []
                for k in range(ATT_NUM):
                    tmp3 = []
                    for l in range(CAT_NUM):
                        tmp4 = [1 for m in range(CLS_NUM)]
                        tmp3.append(tmp4)
                    tmp2.append(tmp3)
                tmp1.append(tmp2)
            tmp.append(tmp1)
        
        df = pd.read_csv(self.filepath)
        df.drop(['Unnamed: 0'], axis = 1, inplace = True)
        for i, row in df.iterrows():
            for j, column1 in row.iteritems():
                for k, column2 in row.iteritems():
                    if j == '-1' or k == '-1':
                        continue
                    if j == k:
                        continue
                    else:
                        tmp[int(j)][row[j]][int(k)][row[k]][row['-1']] += 1
        self.xxyDist = tmp


    #returns P(X1 = v1|X2 = v2, Y = y)
    def condPxxy(self,X1, v1, X2, v2, y):
        return self.condxxyDist[X1][v1][X2][v2][y]

    def condPxy(self,X1, v1, y):
        return self.condxyDist[X1][v1][y]

    def jointPxxy(self,X1, v1, X2, v2, y):
        return self.xxyDist[X1][v1][X2][v2][y]/self.instancecount

    def jointPxy(self,X1, v1, y):
        return self.xyDist[X1][v1][y]/self.instancecount

    def Px(self, X1, v1):
        return self.xDist[X1][v1]/self.instancecount

    def Py(self,y):
        return self.xDist['-1'][y]/self.instancecount

#xydist = xyDist("./train.csv")
#xydist.getxDist()
#xydist.getxyDist()
#xydist.getcondxxyDist()
