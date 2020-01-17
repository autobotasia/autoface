import os
import cv2
import time
import numpy as np
import tensorflow as tf
from trainer import Trainer
from utils.config import process_config
from utils.dirs import create_dirs
from utils.logger import Logger
from utils.utils import get_args 
from utils.insightface_utils import InsightfaceUtils
from bunch import Bunch
import imutils

def add_overlays(frame, faces, frame_rate):
    if faces is not None:
        for face in faces:
            face_bb = face["point"]
            #cv2.rectangle(frame,
            #              (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]),
            #              (0, 255, 0), 2)
            if face["name"] is not None:
                cv2.putText(frame, face["name"], (face_bb[0], face_bb[1]),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                            thickness=2, lineType=2)

    cv2.putText(frame, str(frame_rate) + " fps", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                thickness=2, lineType=2)

if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    # capture the config path from the run arguments
    # then process the json configuration file
    try:
        args = get_args()
        config = process_config(args.config)

    except:
        print("missing or invalid arguments")
        exit(0)
    if not config.pretrained_model:
        raise Exception('model path is required')

    util = InsightfaceUtils(Bunch(config.pretrained_model))
    trainer = Trainer(config)

    if config.do_train:
        # create the experiments dirs
        create_dirs([config.summary_dir, config.checkpoint_dir])
        trainer.train()
    if config.do_predict:
        trainer.do_predict()

    if config.do_demo:
        frame_interval = 3  # Number of frames after which to run face detection
        fps_display_interval = 5  # seconds
        frame_rate = 0
        frame_count = 0

        #video_capture = cv2.VideoCapture(0)
        video_capture = cv2.VideoCapture("rtsp://admin:12345678a@@172.16.12.111:554/Streamming/channels/101")

        start_time = time.time()
        
        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()
            if not ret:
                continue

            frame = imutils.resize(frame, width=512)

            if (frame_count % frame_interval) == 0:
                try:
                    predictimg, points = util.get_embedding(frame)
                    predictimg = predictimg.reshape(1, 512)
                    for best_idx, clsname, prob in trainer.predict(predictimg, batch_size=1):
                        face = {'point': points[0], 'name': clsname}
                        print("=====%s: %f=====" % (clsname, prob))
                        
                except Exception as e:
                    print("ignore this frame", e)
                    continue

                # Check our current fps
                end_time = time.time()
                if (end_time - start_time) > fps_display_interval:
                    frame_rate = int(frame_count / (end_time - start_time))
                    start_time = time.time()
                    frame_count = 0
            
            add_overlays(frame, [face], frame_rate)
            frame_count += 1            
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything is done, release the capture
        video_capture.release()
        cv2.destroyAllWindows()
