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
from datetime import  datetime, timedelta
from save2DB import AutofacesMongoDB
import pjconfig
import re
import emailNotification


def createData(frame, pred_clsname, max_prob):

    if not os.path.exists('./datasets/new-frame'):
        os.makedirs('./datasets/new-frame')

    created_time = datetime.now()
    time_str = str(created_time)
    time_str = re.sub('[:-]', '', time_str.split('.')[0])
    time_str = re.sub(' ', '_', time_str)
    image_link = './datasets/new-frame/' + pred_clsname + '_' + time_str + '.jpg'
    try:
        cv2.imwrite(image_link, frame)
    except:
        print("Imwrite error in autoface.createData function.")
    predict_data = {
        "time": created_time,
        'face_class': pred_clsname,
        'prob': max_prob,
        'image_link': image_link
    }
    # wait 1 seconds to save next image
    next_time_can_save_img = datetime.now() + timedelta(seconds=1)
    return next_time_can_save_img, predict_data


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

    # MongoDB info
    username = pjconfig.DBUSERNAME
    password = pjconfig.DBPASSWORD
    host = pjconfig.DBHOST
    port = pjconfig.DBPORT
    database_name = pjconfig.DBNAME
    collection_name = pjconfig.COLNAME

    # connect MongoDB database
    autofaces_db = AutofacesMongoDB(username, password, host, port, database_name, collection_name)

    # variable for email notification
    # checkin dict save member checkin status, saved_day for check isNewDay
    checkin = emailNotification.createCheckinDict()
    saved_day = datetime.now().date
    serverMail = emailNotification.loginEmail()
    sender_email = pjconfig.SENDER_EMAIL
    receiver_email_list = emailNotification.getReceiverEmailList()


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
        next_time_can_save_img = datetime.now()

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
                    max_prob = 0
                    pred_clsname = ''
                    for best_idx, clsname, prob in trainer.predict(predictimg, batch_size=1):
                        face = {'point': points[0], 'name': clsname}
                        print("=====%s: %f=====" % (clsname, prob))
                        if max_prob < prob:
                            max_prob = prob
                            pred_clsname = clsname


                    # save prediction to database
                    if max_prob > 0.7 and datetime.now() > next_time_can_save_img:
                        next_time_can_save_img, predict_data = createData(frame, pred_clsname, max_prob)
                        autofaces_db.save2db(predict_data)

                        # send-email code block
                        if emailNotification.isNewDay(saved_day):
                            # reset dict values
                            for key in checkin:
                                checkin[key] = False
                            # renew saved_day
                            saved_day = datetime.now().date

                        if checkin[pred_clsname] is False:
                            checkin[pred_clsname] = True

                            for receiver_email in receiver_email_list:
                                message = emailNotification.createMess(pred_clsname, sender_email, receiver_email)
                                emailNotification.sendMail(serverMail, sender_email, receiver_email, message)
                        # end of send-email code block
                    # end of save-prediction-to-database code block

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

        # logout Email
        emailNotification.logoutEmail(serverMail)
