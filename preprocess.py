import os
import pandas as pd
import argparse
import cv2
import sys
import numpy as np
import os
from tqdm import *
from multiprocessing import Pool
import imgaug as ia
from imgaug import augmenters as iaa
from utils.config import process_config
from bunch import Bunch
from utils.insightface_utils import InsightfaceUtils
import tensorflow as tf

config = process_config("./config.json")
gutil = InsightfaceUtils(Bunch(config.pretrained_model))

sometimes = lambda aug: iaa.Sometimes(0.8, aug)
seq = iaa.Sequential([
	iaa.Fliplr(0.5),
	sometimes(
		iaa.OneOf([
			iaa.Grayscale(alpha=(0.0, 1.0)),
			iaa.AddToHueAndSaturation((-20, 20)),
			iaa.Add((-20, 20), per_channel=0.5),
			iaa.Multiply((0.5, 1.5), per_channel=0.5),
			iaa.GaussianBlur((0, 2.0)),
			iaa.ContrastNormalization((0.5, 2.0), per_channel=0.5),
			iaa.Sharpen(alpha=(0, 0.5), lightness=(0.7, 1.3)),
			iaa.Emboss(alpha=(0, 0.5), strength=(0, 1.5))
		])
	)
])

def my_process1(file_name):
    emb_path = './datasets/test/%s'%file_name
    emb, _ = gutil.get_embedding(cv2.imread(emb_path))
    return emb.reshape(512)

def my_process2(file_name):        
    emb_path = './datasets/test/%s'%file_name
    flip_img = cv2.flip(cv2.imread(emb_path), 1)
    flip_img = np.transpose(flip_img, (2,0,1))
    emb, _ = gutil.get_embedding(flip_img)
    return emb.reshape(512)

def my_process3(file_name):
    emb_path = './datasets/train/%s'%file_name
    emb, _ = gutil.get_embedding(cv2.imread(emb_path))
    return emb.reshape(512)

def my_process4(file_name):
    emb_path = './datasets/train/%s'%file_name
    augmentation_arr = np.array([],dtype=np.float32).reshape(0,512)
    for i in range(100):
        img_org = cv2.imread(emb_path)
        img_aug = seq.augment_image(img_org)
        img_aug = np.transpose(img_aug, (2,0,1))
        emb, _ = gutil.get_embedding(img_aug)
        augmentation_arr = np.vstack((augmentation_arr, emb.reshape(1,512)))        
    return augmentation_arr.reshape(100,512)

def process():
    test_df = pd.read_csv('./datasets/test_refined.csv')
    train_df = pd.read_csv('./datasets/train_refined.csv') 

    p = Pool(16)
    test_data = p.map(func=my_process1, iterable = test_df.image.values.tolist())
    p.close()
    test_data = np.array(test_data)
    print(test_data.shape)
    np.save('test_data.npy', test_data)
    test_data = []

    p = Pool(16)
    test_flip_data = p.map(func=my_process2, iterable = test_df.image.values.tolist())
    p.close()
    test_flip_data = np.array(test_flip_data)
    print(test_flip_data.shape)
    np.save('test_flip_data.npy', test_flip_data)
    test_flip_data = []

    p = Pool(16)
    train_data = p.map(func=my_process3, iterable = train_df.image.values.tolist())
    p.close()
    train_data = np.array(train_data)
    print(train_data.shape)
    np.save('./data/train_data_checking.npy', train_data)
    train_data = []

    p = Pool(16)
    train_aug_data = p.map(func=my_process4, iterable = train_df.image.values.tolist())
    p.close()
    train_aug_data = np.array(train_aug_data)
    print(train_aug_data.shape)
    np.save('./data/train_aug_data_checking.npy', train_aug_data)
    train_aug_data = []

         
if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    process()
                                 