import os
import pandas as pd
import argparse
import cv2
import sys
import numpy as np
import os
from tqdm import *
import imgaug as ia
from imgaug import augmenters as iaa

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

def prepare_data(model):
    dataset_arr = {}
    augmentation_arr = {}
    for mset in ['train', 'test']:
        dataset_arr[mset] = np.array([],dtype=np.float32).reshape(0,512)
        augmentation_arr[mset] = np.array([],dtype=np.float32).reshape(0,512)
        for rdir, sdir, files in os.walk('../datasets/aligned/%s/112x112/'%mset):
            for file in tqdm(files):
                if '.png' not in file:
                    continue
                fn, fe = os.path.splitext(file)
                img_path = os.path.join(rdir, file)
                img_org = cv2.imread(img_path)
                img_org = cv2.cvtColor(img_org, cv2.COLOR_BGR2RGB)

                img = np.transpose(img_org, (2,0,1))
                emb = model.get_feature(img)
                #np.save(output_dir + '/%s.npy'%fn, emb)
                dataset_arr[mset] = np.vstack((dataset_arr[mset], emb.reshape(1,512)))

                if mset == 'test':
                    flip_img = cv2.flip(img_org, 1)
                    flip_img = np.transpose(flip_img, (2,0,1))
                    emb = model.get_feature(flip_img)
                    #np.save(output_dir + '/%s_flip.npy'%fn, emb)
                    dataset_arr[mset] = np.vstack((dataset_arr[mset], emb.reshape(1,512)))

                augmentation_arr = np.array([],dtype=np.float32).reshape(0,512)
                for i in range(100):
                    img_aug = seq.augment_image(img_org)
                    img_aug = np.transpose(img_aug, (2,0,1))
                    emb = model.get_feature(img_aug)
                    augmentation_arr = np.vstack((augmentation_arr, emb.reshape(1,512)))
        print(dataset_arr[mset].shape, augmentation_arr[mset].shape)
        np.save('./data/%s_dataset_arr.npy'%mset, dataset_arr[mset])        
        np.save('./data/%s_augmentation_arr.npy'%mset, augmentation_arr[mset])                                            