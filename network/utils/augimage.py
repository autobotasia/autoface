import os
from tqdm import *
import imgaug as ia
from imgaug import augmenters as iaa
import cv2
import numpy as np

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

for mset in ['train']:
    datalist = []
    for dirname in os.listdir('./datasets/%s/'%mset):
        for file in os.listdir('./datasets/%s/%s/'%(mset,dirname)):
            if file == '.' or file == '..':
                continue
            img_path = os.path.join('./datasets/%s/%s/'%(mset,dirname), file)
            img_org = cv2.imread(img_path)
            img_org = cv2.cvtColor(img_org, cv2.COLOR_BGR2RGB)
            for i in range(10):
                img_aug = seq.augment_image(img_org)
                #img_aug = np.transpose(img_aug, (2,0,1))
                cv2.imwrite('./datasets/%s/%s/%d_%s'%(mset,dirname,i,file), img_aug)
                
