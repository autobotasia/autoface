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
from datetime import  datetime, timedelta, date
from utils.mongodb import AutofacesMongoDB
from utils.email_notification import Notification

os.environ["CUDA_VISIBLE_DEVICES"]="0"

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

    # connect MongoDB database
    db = AutofacesMongoDB(config)
    util = InsightfaceUtils(Bunch(config.pretrained_model))
    trainer = Trainer(config)
    notifier = Notification(Bunch(config.notification))
    
    saved_day = date.today()

    if config.do_train:
        # create the experiments dirs
        create_dirs([config.summary_dir, config.checkpoint_dir])
        trainer.train()
    if config.do_predict:
        trainer.do_predict()


    if config.do_demo:
        start_time = time.time()
        next_time_can_save_img = datetime.now()


        while True:
            for f in os.listdir('./data/capture/'):
                file_name, file_ext = os.path.splitext(f)
                
                if file_ext != '.png' or file_name[:3] == 'tmp':
                    print(file_name)
                    continue
                
                frame = cv2.imread('./data/capture/%s'%f)
                try:
                    predictimg, points = util.get_embedding(frame)
                    predictimg = predictimg.reshape(1, 512)
                    for best_idx, clsname, prob in trainer.predict(predictimg, batch_size=1):
                        face = {'point': points[0], 'name': clsname}
                        print("=====%s: %f=====" % (clsname, prob))
                        #for index, val in enumerate(result_top3):
                        #    print("%d: =====%s: %f=====" % (index + 1, val[0], val[1]))
                                       
                    if prob >= 0.70:
                        if os.path.exists('./data/cls/%s'%clsname) == False:
                            os.makedirs('./data/cls/%s'%clsname)
                        cv2.imwrite('./data/cls/%s/%s'%(clsname,f), frame)

                    # save prediction to database
                    #if max_prob > 0.7 and datetime.now() > next_time_can_save_img:
                    #    db.save_and_noti(frame, face['name'], max_prob, saved_day)
                
                except Exception as e:
                    print("ignore this frame", e)                    
                
                os.remove('./data/capture/%s'%f) 