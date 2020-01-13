import pandas as pd
import numpy as np
import os
from tqdm import *
from multiprocessing import Pool, cpu_count

def my_process1(file_name):
    emb_path = './data/embedding/model-r100-ii/test/%s'%file_name.replace('.png', '.npy')
    emb_path = emb_path.replace('.jpg', '.npy')
    emb_path = emb_path.replace('.JPG', '.npy')
    emb = np.load(emb_path).reshape(512)
    return emb

def my_process2(file_name):
    emb_path = './data/embedding/model-r100-ii/test/%s'%file_name.replace('.png', '_flip.npy')
    emb_path = emb_path.replace('.jpg', '_flip.npy')
    emb_path = emb_path.replace('.JPG', '_flip.npy')
    emb = np.load(emb_path).reshape(512)
    return emb

def my_process3(file_name):
    emb_path = './data/embedding/model-r100-ii/train/%s'%file_name.replace('.png', '.npy')
    emb_path = emb_path.replace('.PNG', '.npy')
    emb_path = emb_path.replace('.jpg', '.npy')
    emb_path = emb_path.replace('.JPG', '.npy')
    emb_path = emb_path.replace('.jpeg', '.npy')
    emb_path = emb_path.replace('.JPEG', '.npy')
    emb = np.load(emb_path).reshape(512)
    return emb

def my_process4(file_name):
    emb_path = './data/embedding/model-r100-ii/train/%s'%file_name.replace('.png', '_augmentation.npy')
    emb_path = emb_path.replace('.jpg', '_augmentation.npy')
    emb_path = emb_path.replace('.JPG', '_augmentation.npy')
    emb_path = emb_path.replace('.jpeg', '_augmentation.npy')
    emb_path = emb_path.replace('.JPEG', '_augmentation.npy')
    emb_path = emb_path.replace('.PNG', '_augmentation.npy')
    emb = np.load(emb_path).reshape(100,512)
    return emb

if __name__ == '__main__':
    # load data here        
    test_df = pd.read_csv('./datasets/test.csv')
    train_df = pd.read_csv('./datasets/train.csv') 

    test = []
    for i in test_df.image.values.tolist():
        if os.path.exists('./datasets/aligned/test/112x112/%s'%i):
            test.append(i)

    train = []
    for i in train_df.image.values.tolist():
        if os.path.exists('./datasets/aligned/train/112x112/%s'%i):
            train.append(i)

    p = Pool(16)
    test_data = p.map(func=my_process1, iterable = test)
    p.close()
    test_data = np.array(test_data)
    print(test_data.shape)
    np.save('./data/test_data.npy', test_data)
    test_data = []

    p = Pool(16)
    test_flip_data = p.map(func=my_process2, iterable = test)
    p.close()
    test_flip_data = np.array(test_flip_data)
    print(test_flip_data.shape)
    np.save('./data/test_flip_data.npy', test_flip_data)
    test_flip_data = []

    '''p = Pool(16)
    testcam_data = p.map(func=my_process1, iterable = testcam_df)
    p.close()
    testcam_data = np.array(testcam_data)
    print(testcam_data.shape)
    np.save('./data/testcam_data.npy', testcam_data)
    testcam_data = []

    p = Pool(16)
    testcam_flip_data = p.map(func=my_process1, iterable = testcam_flip_df)
    p.close()
    testcam_flip_data = np.array(testcam_flip_data)
    print(testcam_flip_data.shape)
    np.save('./data/testcam_flip_data.npy', testcam_flip_data)
    testcam_flip_data = []'''

    p = Pool(16)
    train_data = p.map(func=my_process3, iterable = train)
    p.close()
    train_data = np.array(train_data)
    print(train_data.shape)
    np.save('./data/train_data.npy', train_data)
    train_data = []

    p = Pool(16)
    train_aug_data = p.map(func=my_process4, iterable = train)
    p.close()
    train_aug_data = np.array(train_aug_data)
    print(train_aug_data.shape)
    np.save('./data/train_aug_data.npy', train_aug_data)
    train_aug_data = []