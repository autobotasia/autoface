import tensorflow as tf
import face_model
import face_alignment
import cv2
import imutils
import numpy as np
import argparse
import os
import time
from skimage import transform as trans

os.environ["CUDA_VISIBLE_DEVICES"]="1" 

parser = argparse.ArgumentParser()
#parser.add_argument("--imgpath", type = str, required=True)
args = parser.parse_args()
sess = tf.Session()

fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, flip_input=False, device='cuda:0')

def alignment(cv_img, dst, dst_w, dst_h):
        if dst_w == 112 and dst_h == 112:
            src = np.array([
                [38.2946, 51.6963],
                [73.5318, 51.5014],
                [56.0252, 71.7366],
                [41.5493, 92.3655],
                [70.7299, 92.2041] ], dtype=np.float32)        
        else:
            return None
        tform = trans.SimilarityTransform()
        tform.estimate(dst, src)
        M = tform.params[0:2,:]
        face_img = cv2.warpAffine(cv_img,M,(dst_w,dst_h), borderValue = 0.0)
        return face_img

def getFace(img):
    landmarks = fa.get_landmarks(img)
    if landmarks is not None:
        points = landmarks[0]
        p1 = np.mean(points[36:42,:], axis=0)
        p2 = np.mean(points[42:48,:], axis=0)
        p3 = points[33,:]
        p4 = points[48,:]
        p5 = points[54,:]

        dst = np.array([p1,p2,p3,p4,p5],dtype=np.float32)
        cv_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        face_112x112 = alignment(cv_img, dst, 112, 112)
    
    return face_112x112
    
while True:
    for f in os.listdir('./data/images/'):
        file_name, file_ext = os.path.splitext(f)
        
        if file_ext != '.png' or file_name[:3] == 'tmp':
            print(file_name)
            continue
        
        img = cv2.imread('./data/images/%s'%f)
        #img = imutils.resize(img, width=256)        
        os.remove('./data/images/%s'%f)

        try:
            face = getFace(img)            
            strtime = round(time.time())
            cv2.imwrite('./data/capture/tmp-%d.png'%strtime, face)
            os.rename('./data/capture/tmp-%d.png'%strtime, './data/capture/%d.png'%strtime)
        except Exception as e:
            print(e)
            pass
