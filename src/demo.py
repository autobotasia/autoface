import pandas as pd
import numpy as np

import keras
from keras.optimizers import Adam, RMSprop
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger
from keras import *
from keras.models import *
from keras.layers import Input, concatenate, Conv2D, Activation, BatchNormalization, Dense, Dropout, Flatten, add, Lambda
import tensorflow as tf
from keras import backend as K
from keras.utils.np_utils import to_categorical
from sklearn.utils import shuffle
import face_alignment
import numpy as np 
import imgaug as ia
from imgaug import augmenters as iaa
from skimage import transform as trans
import face_model
import os
import cv2
import sys
import time
import argparse

BATCH_SIZE = 1
EPOCHS = 300
NUMBER_OF_FOLDS = 5
NUMBER_OF_PARTS = 4
INPUT_DIM = 512
NUMBER_OF_CLASSES = 1000

fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, flip_input=False, device='cuda:1')

def alignment(cv_img, dst, dst_w, dst_h):
    if dst_w == 96 and dst_h == 112:
        src = np.array([
            [30.2946, 51.6963],
            [65.5318, 51.5014],
            [48.0252, 71.7366],
            [33.5493, 92.3655],
            [62.7299, 92.2041] ], dtype=np.float32)
    elif dst_w == 112 and dst_h == 112:
        src = np.array([
            [38.2946, 51.6963],
            [73.5318, 51.5014],
            [56.0252, 71.7366],
            [41.5493, 92.3655],
            [70.7299, 92.2041] ], dtype=np.float32)
    elif dst_w == 150 and dst_h == 150:
        src = np.array([
            [51.287415, 69.23612],
            [98.48009, 68.97509],
            [75.03375, 96.075806],
            [55.646385, 123.7038],
            [94.72754, 123.48763]], dtype=np.float32)
    elif dst_w == 160 and dst_h == 160:
        src = np.array([
            [54.706573, 73.85186],
            [105.045425, 73.573425],
            [80.036, 102.48086],
            [59.356144, 131.95071],
            [101.04271, 131.72014]], dtype=np.float32)
    elif dst_w == 224 and dst_h == 224:
        src = np.array([
            [76.589195, 103.3926],
            [147.0636, 103.0028],
            [112.0504, 143.4732],
            [83.098595, 184.731],
            [141.4598, 184.4082]], dtype=np.float32)
    else:
        return None
    tform = trans.SimilarityTransform()
    tform.estimate(dst, src)
    M = tform.params[0:2,:]
    face_img = cv2.warpAffine(cv_img,M,(dst_w,dst_h), borderValue = 0.0)
    return face_img

def Model():
    model = Sequential()
    model.add(Dense(2048, input_dim=INPUT_DIM, init='uniform'))
    model.add(Activation('relu'))
    model.add(Dropout(0.25))
    model.add(Dense(NUMBER_OF_CLASSES, init='uniform'))
    model.add(Activation('softmax'))
    return model

def add_overlays(frame, faces, frame_rate):
    if faces is not None:
        for face in faces:
            face_bb = face["bounding_box"]
            #cv2.rectangle(frame,
            #              (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]),
            #              (0, 255, 0), 2)
            if face["name"] is not None:
                cv2.putText(frame, face["name"], (face_bb[0], face_bb[3]),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                            thickness=2, lineType=2)

    cv2.putText(frame, str(frame_rate) + " fps", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                thickness=2, lineType=2)

def get_embedding(image, model):
    
    face_112x112 = image
    landmarks = fa.get_landmarks(image)
    if landmarks is None:
        for sigma in np.linspace(0.0, 3.0, num=11).tolist():
            seq = iaa.GaussianBlur(sigma)
            image_aug = seq.augment_image(image)
            landmarks = fa.get_landmarks(image_aug)
            if landmarks is not None:
                print('sigma:',sigma)
                points = landmarks[0]
                p1 = np.mean(points[36:42,:], axis=0)
                p2 = np.mean(points[42:48,:], axis=0)
                p3 = points[33,:]
                p4 = points[48,:]
                p5 = points[54,:]
                
                if np.mean([p1[1],p2[1]]) < p3[1] \
                    and p3[1] < np.mean([p4[1],p5[1]]) \
                    and np.min([p4[1], p5[1]]) > np.max([p1[1], p2[1]]) \
                    and np.min([p1[1], p2[1]]) < p3[1] \
                    and p3[1] < np.max([p4[1], p5[1]]):

                    dst = np.array([p1,p2,p3,p4,p5],dtype=np.float32)
                    cv_img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    
                    face_112x112 = alignment(cv_img, dst, 112, 112)                    
                    break
    else:
        points = landmarks[0]
        p1 = np.mean(points[36:42,:], axis=0)
        p2 = np.mean(points[42:48,:], axis=0)
        p3 = points[33,:]
        p4 = points[48,:]
        p5 = points[54,:]

        dst = np.array([p1,p2,p3,p4,p5],dtype=np.float32)
        cv_img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        face_112x112 = alignment(cv_img, dst, 112, 112)

    img_org = cv2.cvtColor(face_112x112, cv2.COLOR_BGR2RGB)
    img = np.transpose(img_org, (2,0,1))
    return model.get_feature(img), img


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='face model test')
    # general
    parser.add_argument('--image-size', default='112,112', help='')
    parser.add_argument('--model', default='', help='path to load model.')
    parser.add_argument('--ga-model', default='', help='path to load model.')
    parser.add_argument('--gpu', default=0, type=int, help='gpu id')
    parser.add_argument('--det', default=0, type=int, help='mtcnn option, 1 means using R+O, 0 means detect from begining')
    parser.add_argument('--flip', default=0, type=int, help='whether do lr flip aug')
    parser.add_argument('--threshold', default=1.24, type=float, help='ver dist threshold')
    args = parser.parse_args()

    print(args.model)
    model = face_model.FaceModel(args)

    frame_interval = 3  # Number of frames after which to run face detection
    fps_display_interval = 5  # seconds
    frame_rate = 0
    frame_count = 0

    video_capture = cv2.VideoCapture(0)
    start_time = time.time()

    WEIGHTS_BEST = './weights/best_weight_part6_fold2.hdf5'

    clsmodel = Model()
    clsmodel.summary()
    clsmodel.compile(loss='categorical_crossentropy', optimizer=Adam(lr=1e-3), metrics=['accuracy'])
    clsmodel.load_weights(WEIGHTS_BEST)

    classname = []
    for _, clsdirs, _ in os.walk('/home/autobot/projects/autobot/facenet/datasets/nccfaces/'):
        for index, clsdir in enumerate(clsdirs):
            classname.append(clsdir)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        #frame = cv2.imread('/home/autobot/projects/autobot/dnb-facerecognition-aivivn/datasets/aligned/test/112x112/Nguyen_Dai_Duong_1_IMG_4988(1).png')

        if True or (frame_count % frame_interval) == 0:
            #faces = face_recognition.identify(frame)
            try:
                xtest, alignedimg = get_embedding(frame, model)
            except:
                continue

            tedata = xtest.reshape(1, 512)            
            ptest = clsmodel.predict(tedata, batch_size=None, verbose=0)
            #ptest += clsmodel.predict(xtest_flip, batch_size=BATCH_SIZE, verbose=1)
            #best_n = np.argsort(-p_test, axis=1)[:,0:5]
            
            best_idx = np.argmax(ptest, axis=1)
                                      
            clsname = classname[best_idx[0]]
            prob = ptest[0,best_idx[0]]

            bounding_box = []
            bounding_box.append(alignedimg[:,0,0].min())
            bounding_box.append(alignedimg[:,0,0].max())
            bounding_box.append(alignedimg[:,0,1].min())
            bounding_box.append(alignedimg[:,0,1].max())

            face = {'bounding_box': bounding_box, 'name': clsname}
            print("="*10)
            print(clsname, prob)

            # Check our current fps
            end_time = time.time()
            if (end_time - start_time) > fps_display_interval:
                frame_rate = int(frame_count / (end_time - start_time))
                start_time = time.time()
                frame_count = 0

        #add_overlays(frame, [face], frame_rate)
        frame_count += 1
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

    

    

    
