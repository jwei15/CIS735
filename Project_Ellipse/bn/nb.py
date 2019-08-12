
import xyDist
import pandas as pd

class nb:
    def __init__(self):
        self.dist = xyDist.xyDist("./train.csv")
        self.testfile = pd.read_csv("./test.csv")
        self.testfile.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis = 1, inplace=True)
        self.testcount = len(self.testfile)
        self.acc = 0
        
        for i, row in self.testfile.iterrows():
            self.classify(row)
        print("nb acc: ",self.acc/self.testcount)
        
    def normalise(self, posterior):
        tmp = sum(posterior)
        for i in range(len(posterior)):
            posterior[i] = posterior[i]/tmp


    def classify(self, instance):
        posteriorP = [1e40 for i in range(xyDist.CLS_NUM)]
        for j in range(xyDist.CLS_NUM):
            for k, item in instance.iteritems():
                if k!='-1':
                    posteriorP[j] = posteriorP[j] * self.dist.condPxy(int(k),int(item),j)
            posteriorP[j] = posteriorP[j]*self.dist.Py(j)
        
        self.normalise(posteriorP)
        if (posteriorP.index(max(posteriorP)) == instance['-1']):
            self.acc += 1

classifier = nb()
