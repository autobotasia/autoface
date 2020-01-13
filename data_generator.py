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
        # load data here        
        test_df = pd.read_csv('./datasets/test.csv')
        train_df = pd.read_csv('./datasets/train.csv')
        self.testdf = []
        for _, row in test_df.iterrows():
            if os.path.exists('./datasets/aligned/test/112x112/%s'%row['image']):
                self.testdf.append(row['label'])

        self.traindf = []
        for _, row in train_df.iterrows():
            if os.path.exists('./datasets/aligned/train/112x112/%s'%row['image']):
                self.traindf.append(row['label'])
        
        #xtrain = np.load('train_data.npy')
        self.xtrain_aug = np.load('./data/train_aug_data.npy')
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
                x_batch = np.vstack((x_batch, self.xtrain_aug[i, randint(0, 99), :].reshape(1,self.config.input_dim)))
            y_batch = self.ytrain[start:end, :]
            yield x_batch, y_batch
          