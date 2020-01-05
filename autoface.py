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
from utils import insightface_utils
import face_model
from bunch import Bunch

def add_overlays(frame, faces, frame_rate):
    if faces is not None:
        for face in faces:
            face_bb = face["bounding_box"]
            cv2.rectangle(frame,
                          (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]),
                          (0, 255, 0), 2)
            if face["name"] is not None:
                cv2.putText(frame, face["name"], (face_bb[0], face_bb[3]),
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

    trainer = Trainer(config)
    if config.do_train:
        # create the experiments dirs
        create_dirs([config.summary_dir, config.checkpoint_dir])
        trainer.train()

    if config.do_demo:
        if not config.pretrained_model:
            raise Exception('model path is required')

        model = face_model.FaceModel(Bunch(config.pretrained_model))

        frame_interval = 3  # Number of frames after which to run face detection
        fps_display_interval = 5  # seconds
        frame_rate = 0
        frame_count = 0

        video_capture = cv2.VideoCapture(0)
        start_time = time.time()

        classname = []
        for _, clsdirs, _ in os.walk('/home/autobot/projects/autobot/facenet/datasets/nccfaces/'):
            for index, clsdir in enumerate(clsdirs):
                classname.append(clsdir)
        
        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()
            if (frame_count % frame_interval) == 0:
                try:
                    predictimg, alignedimg = insightface_utils.get_embedding(frame, model)
                except:
                    continue

                predictimg = predictimg.reshape(1, 512) 
                predictions = trainer.predict(predictimg)
                for p in predictions:
                    best_idx = p['predicted_logit']
                    clsname = classname[best_idx]
                    prob = p['probabilities'][best_idx]
                    bounding_box = []
                    bounding_box.append(alignedimg[:,0,0].min())
                    bounding_box.append(alignedimg[:,0,0].max())
                    bounding_box.append(alignedimg[:,0,1].min())
                    bounding_box.append(alignedimg[:,0,1].max())

                    face = {'bounding_box': bounding_box, 'name': clsname}
                    print("=====%s: %f=====" % (clsname, prob))

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
