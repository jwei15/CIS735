import pandas as pd
import csv
import numpy as np

class_mapping = {'wyc':0, 'zyf':1, 'zl':2, 'xxj':3, 'wq':4, 'zdx':5, 'lsl':6, 'xch':7
        ,'zc':8, 'ml':9, 'syj':10, 'rj':11, 'hy':12, 'lqf':13, 'zjg':14, 'fyc':15,'ljg':16,
        'wl':17}

'''
Read from raw.csv, 
Wash the data in raw.csv
and write washed data to "washed_data.csv"
'''
def WashData(filepath):
    df = pd.read_csv(filepath)
    washed_frame = df.fillna(method='ffill')
    
    washed_frame['-1'] = washed_frame['-1'].map(class_mapping)
    
    for item in washed_frame:
        if item != '-1':
            washed_frame[item] = pd.qcut(washed_frame[item], 30, labels=False, duplicates = 'drop')
    washed_frame.to_csv("washed_data.csv")


'''
Generate train and test set from washed_data.csv
training set will be saved in "train.csv"
testing set will be save in "test.csv"
'''
def GenerateTest(filepath):    
    df = pd.read_csv(filepath)

    df_tmp = pd.DataFrame(columns=(['-1'] + [str(i) for i in range(28)]))
    line = 0
    for index, row in df.iterrows():
        if (index % 8 == 0):
            df_tmp = pd.concat([df_tmp, pd.DataFrame(df[index: index + 2])], sort=False)
            df.drop(index = [index, index + 1], inplace = True)
   
    df.to_csv("train.csv", index = None)
    df_tmp.to_csv("test.csv")

WashData("./raw.csv")
GenerateTest("./washed_data.csv")
