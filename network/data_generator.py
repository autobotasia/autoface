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
        self.testdf = []        
        dirindex = 0
        for dirname in os.listdir('./data/embedding/model-r100-ii/test1'):
            for file in os.listdir('./data/embedding/model-r100-ii/test1/%s'%(dirname)):
                if file == '.' or file == '..':
                    continue
                self.testdf.append(dirindex)
            dirindex += 1    
        
        
        self.traindf = []
        dirindex = 0
        for dirname in os.listdir('./data/embedding/model-r100-ii/train'):
            for file in os.listdir('./data/embedding/model-r100-ii/train/%s'%(dirname)):
                if file == '.' or file == '..':
                    continue
                self.traindf.append(dirindex)
            dirindex += 1    
        
        
        #xtrain = np.load('train_data.npy')
        self.xtrain_aug = np.load('./data/saved_aug_data.npy')
        self.ytrain = self.get_y_true(self.traindf)
        self.train_size = len(self.xtrain_aug)
        
        self.xtest = np.load('./data/test_data.npy')
        self.ytest = self.get_y_true(self.testdf)

    def get_y_true(self, df):
        y_true = []
        for label in df:
            y_true.append(to_categorical(label, num_classes=self.config.number_of_class))
        return np.array(y_true)

    def next_batch(self, batch_size):
        self.xtrain_aug, self.ytrain = shuffle(self.xtrain_aug, self.ytrain)
        for start in range(0, self.train_size, batch_size):
            end = min(start + batch_size, self.train_size)
            x_batch = np.array([],dtype = np.float32).reshape(0,self.config.input_dim)
            for i in range(start,end,1):
                y_batch = self.ytrain[start:end, :]
                for j in range (0,99):
                    x_batch = np.vstack((x_batch, self.xtrain_aug[i, j, :].reshape(1,self.config.input_dim)))                    
                    yield x_batch, y_batch
            