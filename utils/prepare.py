import pandas as pd
import numpy as np
import os
from tqdm import *
from multiprocessing import Pool, cpu_count

def my_process1(file_name):
    print("my_process1", file_name)
    emb = np.load(file_name).reshape(512)    
    return emb

def my_process2(file_name):
    print("my_process2", file_name)
    emb = np.load(file_name).reshape(100,512)
    return emb

if __name__ == '__main__':
    test_df = []
    test_flip_df = []
    for file in os.listdir('./data/embedding/model-r100-ii/test/'):
        if file == '.' or file == '..':
            continue
        if '_augmentation.npy' in file:
            continue
        if '_flip.npy' in file: 
            test_flip_df.append(os.path.join('./data/embedding/model-r100-ii/test/', file))
        else:
            test_df.append(os.path.join('./data/embedding/model-r100-ii/test/', file))    

    testcam_df = []
    testcam_flip_df = []
    for file in os.listdir('./data/embedding/model-r100-ii/testcam/'):
        if file == '.' or file == '..':
            continue
        if '_augmentation.npy' in file:
            continue
        if '_flip.npy' in file: 
            testcam_flip_df.append(os.path.join('./data/embedding/model-r100-ii/testcam/', file))
        else:
            testcam_df.append(os.path.join('./data/embedding/model-r100-ii/testcam/', file))

    train_df = []
    train_augmentation_df = []
    for file in os.listdir('./data/embedding/model-r100-ii/train/'):
        if file == '.' or file == '..':
            continue
        if '_flip.npy' in file:
            continue
        if '_augmentation.npy' in file: 
            train_augmentation_df.append(os.path.join('./data/embedding/model-r100-ii/train/', file))
        else:
            train_df.append(os.path.join('./data/embedding/model-r100-ii/train/', file))         

    p = Pool(16)
    test_data = p.map(func=my_process1, iterable = test_df)
    p.close()
    test_data = np.array(test_data)
    print(test_data.shape)
    np.save('./data/test_data.npy', test_data)
    test_data = []

    p = Pool(16)
    test_flip_data = p.map(func=my_process1, iterable = test_flip_df)
    p.close()
    test_flip_data = np.array(test_flip_data)
    print(test_flip_data.shape)
    np.save('./data/test_flip_data.npy', test_flip_data)
    test_flip_data = []

    p = Pool(16)
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
    testcam_flip_data = []

    p = Pool(16)
    train_data = p.map(func=my_process1, iterable = train_df)
    p.close()
    train_data = np.array(train_data)
    print(train_data.shape)
    np.save('./data/train_data.npy', train_data)
    train_data = []

    p = Pool(16)
    train_aug_data = p.map(func=my_process2, iterable = train_augmentation_df)
    p.close()
    train_aug_data = np.array(train_aug_data)
    print(train_aug_data.shape)
    np.save('./data/train_aug_data.npy', train_aug_data)
    train_aug_data = []