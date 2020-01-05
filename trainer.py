import tensorflow as tf
import numpy as np
from data_generator import DataGenerator
from model import Model
from random import randint

class Trainer():
    def __init__(self, config):
        self.config = config
        self.data = DataGenerator(config)
        self.model = Model(config)

        # Create a estimator with model_fn
        self.classifier = tf.estimator.Estimator(model_fn=self.model.model_fn, 
                        model_dir=self.config.checkpoint_dir)

    def train(self):
        # Load training and eval data 
        eval_data, eval_labels = next(self.data.next_batch(self.config.batch_size))
        train_data = self.data.xtrain_aug[:,randint(0, 99),:]
        train_labels = self.data.ytrain

        # Create a input function to train
        train_input_fn = tf.estimator.inputs.numpy_input_fn(
            x=train_data,
            y=train_labels,
            batch_size=self.config.batch_size,
            num_epochs=self.config.num_epochs,
            shuffle=True)

    
        # Create a input function to eval
        eval_input_fn = tf.estimator.inputs.numpy_input_fn(
            x=eval_data,
            y=eval_labels,
            batch_size=self.config.batch_size,
            num_epochs=self.config.num_epochs,
            shuffle=False)    

        # Finally, train and evaluate the model after each epoch
        for _ in range(self.config.num_epochs):
            self.classifier.train(input_fn=train_input_fn)
            metrics = self.classifier.evaluate(input_fn=eval_input_fn)

    def predict(self, image):
        predict_input_fn = tf.estimator.inputs.numpy_input_fn(
            x=image,
            batch_size=1,
            shuffle=False)
        predictions = self.classifier.predict(input_fn=predict_input_fn) 
        return predictions                



        
