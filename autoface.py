import tensorflow as tf
from data_generator import DataGenerator
from model import Model
from trainer import Trainer
from utils.config import process_config
from utils.dirs import create_dirs
from utils.logger import Logger
from utils.utils import get_args


def main():
    # capture the config path from the run arguments
    # then process the json configuration file
    try:
        args = get_args()
        config = process_config(args.config)

    except:
        print("missing or invalid arguments")
        exit(0)

    # create the experiments dirs
    create_dirs([config.summary_dir, config.checkpoint_dir])
    # create tensorflow session
    sess = tf.Session()
    # create your data generator
    data = DataGenerator(config)    
    # create an instance of the model you want
    model = Model(config)
    # create tensorboard logger
    logger = Logger(sess, config)

    if config.do_train:
        # create trainer and pass all the previous components to it
        trainer = Trainer(sess, model, data, config, logger)        
        # here you train your model
        trainer.train()

    if config.do_eval:
        #load model if exists
        model.load(sess)
        

if __name__ == '__main__':
    main()
