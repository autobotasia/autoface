import cv2 as cv
import time
import os

#vcap = cv.VideoCapture("rtsp://admin:12345678a@@172.16.110.2:554/Streamming/channels/101")
vcap = cv.VideoCapture(0)
while(1):
    ret, frame = vcap.read()
    cv.imshow('VIDEO', frame)
    strtime = round(time.time())
    tmpfilename = './data/images/tmp-%d.png'%strtime
    filename = './data/images/%d.png'%strtime
    cv.imwrite(tmpfilename, frame)
    os.rename(tmpfilename, filename)
    cv.waitKey(1)
