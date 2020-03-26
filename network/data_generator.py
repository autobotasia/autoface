import numpy as np
from keras.utils.np_utils import to_categorical
import pandas as pd
from sklearn.utils import shuffle
from random import randint
import tensorflow as tf
import os

class DataGenerator:
    def __init__(self, config):
        self.config = config
        testdf = pd.read_csv("./data/test1.csv")
        self.testdf = testdf['clsidx'].tolist()
        traindf = pd.read_csv("./data/train.csv")
        self.traindf = traindf['clsidx'].tolist()
        
        #xtrain = np.load('train_data.npy')
        self.xtrain = np.load('./data/train_data.npy')
        self.ytrain = self.get_y_true(self.traindf)
        #self.train_size = len(self.xtrain)
        self.xtest = np.load('./data/test1_data.npy')

        #print("="*10)
        #print(self.xtrain[158])
        #print(self.traindf[158])
        
        self.ytest = self.get_y_true(self.testdf)

    def get_y_true(self, df):
        y_true = []
        for label in df:
            y_true.append(to_categorical(label, num_classes=self.config.number_of_class))
        return np.array(y_true)
            
