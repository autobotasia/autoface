import face_model
import argparse
import cv2
import sys
import numpy as np
import pandas as pd
import os
from tqdm import *
import imgaug as ia
from imgaug import augmenters as iaa
from bunch import Bunch
from config import process_config

config = process_config("./config.json")
args = Bunch(config.pretrained_model)
model = face_model.FaceModel(args)


for mset in ['train', 'test1', 'test2']:
    datalist = []
    for index, dirname in enumerate(os.listdir('./datasets/aligned/%s/112x112/'%mset)):
        for file in os.listdir('./datasets/aligned/%s/112x112/%s/'%(mset,dirname)):
            if file == '.' or file == '..':
                continue

            datalist.append({
                'clsname': dirname, 
                'clsidx': index,
                'path':os.path.join('./datasets/aligned/%s/112x112/%s/'%(mset,dirname), file)
            })

    df = pd.DataFrame.from_dict(datalist)
    df.to_csv(path_or_buf="./data/%s.csv"%mset, index=False)
    pathlist = df['path'].tolist()
    emb = np.array([],dtype = np.float32).reshape(0,512)
    for file in tqdm(pathlist):
        img_org = cv2.imread(file)
        img_org = cv2.cvtColor(img_org, cv2.COLOR_BGR2RGB)

        img = np.transpose(img_org, (2,0,1))
        emb = np.vstack((emb, model.get_feature(img).reshape(1,512)))    

    np.save('./data/%s_data.npy'%mset, emb)
    print(emb.shape)
