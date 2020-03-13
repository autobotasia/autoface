import pandas as pd
import numpy as np
import os
from tqdm import *
from multiprocessing import Pool, cpu_count

def my_process1(file_name):
    if 'nonexistent flip' in file_name:
        emb = np.load(file_name).reshape(512)
        return emb

def my_process2(file_name):
    emb = np.load(file_name)
    if 'augmentation' in file_name:
        emb = emb.reshape(100,512)
        return emb
    
if __name__ == '__main__':
    fdict = {}
    for mset in ['train', 'test1', 'test2']:
        if "nonexistent %s"%mset in fdict.keys(): 
            fdict[mset] = []
        for dirname in os.listdir('./data/embedding/model-r100-ii/%s'%mset):
            for file in os.listdir('./data/embedding/model-r100-ii/%s/%s'%(mset,dirname)):
                if file == '.' or file == '..':
                    continue
                fdict[mset].append(os.path.join('./data/embedding/model-r100-ii/%s/%s'%(mset,dirname), file))


    p = Pool(16)
    test_data = p.map(func=my_process1, iterable = fdict['test1'])
    p.close()
    test_data = np.array(test_data)
    print(test_data.shape)
    np.save('./data/test_data.npy', test_data)
    test_data = []

    p = Pool(16)
    train_aug_data = p.map(func=my_process2, iterable = fdict['train'])
    p.close()
    train_aug_data = np.array(train_aug_data)
    print(train_aug_data.shape)
    np.save('./data/saved_aug_data.npy', train_aug_data)
    train_aug_data = []