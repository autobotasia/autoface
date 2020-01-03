import numpy as np
from keras.utils.np_utils import to_categorical
import pandas as pd
from sklearn.utils import shuffle
from random import randint

class DataGenerator:
    def __init__(self, config):
        self.config = config
        # load data here        
        self.train_df = pd.read_csv('./datasets/train_refined.csv')
        #xtrain = np.load('train_data.npy')
        self.xtrain_aug = np.load('./train_aug_data.npy')
        self.ytrain = self.get_y_true()
        self.train_size = len(self.xtrain_aug)

    def get_y_true(self):
        y_true = []
        for _, row in self.train_df.iterrows():
            y_true.append(to_categorical(row['label'], num_classes=self.config.number_of_class))
        return np.array(y_true)    

    def next_batch(self, batch_size):        

        self.xtrain_aug, self.ytrain = shuffle(self.xtrain_aug, self.ytrain)
        for start in range(0, self.train_size, batch_size):
            end = min(start + batch_size, self.train_size)
            x_batch = np.array([],dtype = np.float32).reshape(0,512)
            for i in range(start,end,1):
                x_batch = np.vstack((x_batch, self.xtrain_aug[i, randint(0, 99), :].reshape(1,512)))
            y_batch = self.ytrain[start:end, :]
            yield x_batch, y_batch