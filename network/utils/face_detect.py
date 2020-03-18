from mtcnn import MTCNN
import numpy as np
import cv2
import os
import time

os.environ["CUDA_VISIBLE_DEVICES"]="1" 
detector = MTCNN()

vcap = cv2.VideoCapture("rtsp://admin:12345678a@@172.16.110.2:554/Streamming/channels/101")
#vcap = cv.VideoCapture(0)

while True:
    ret, frame = vcap.read()
    #cv.imshow('VIDEO', frame)

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    bounding_boxes = detector.detect_faces(img)

    for box in bounding_boxes:
        if box['confidence'] < 0.9:
            continue

        det = np.squeeze(box['box'])
        x1, y1, x2, y2 = det
        cropped = img[y1: y1 + y2, x1: x1 + y2, :]            
        strtime = round(time.time())
        cv2.imwrite('./data/capture/tmp-%d.png'%strtime, cropped)
        os.rename('./data/capture/tmp-%d.png'%strtime, './data/capture/%d.png'%strtime)   