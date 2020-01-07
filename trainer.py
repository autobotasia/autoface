import os
import tensorflow as tf
import numpy as np
from data_generator import DataGenerator
from model import Model
from random import randint
from sklearn.model_selection import KFold

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
        #eval_data, eval_labels = next(self.data.next_batch(self.config.batch_size))        
 
        n_split=3
        train_data = self.data.xtrain_aug[:,randint(0, 99),:]
        train_labels = self.data.ytrain
        for train_index,test_index in KFold(n_split).split(train_data):            
            x_train,x_test=train_data[train_index],train_data[test_index]
            y_train,y_test=train_labels[train_index],train_labels[test_index]            

            # Create a input function to train
            train_input_fn = tf.estimator.inputs.numpy_input_fn(
                x=x_train,
                y=y_train,
                batch_size=self.config.batch_size,
                num_epochs=self.config.num_epochs,
                shuffle=True)
        
            # Create a input function to eval
            eval_input_fn = tf.estimator.inputs.numpy_input_fn(
                x=x_test,
                y=y_test,
                batch_size=self.config.batch_size,
                num_epochs=self.config.num_epochs,
                shuffle=False)    

            # Finally, train and evaluate the model after each epoch
            for _ in range(self.config.num_epochs):
                self.classifier.train(input_fn=train_input_fn)
                metrics = self.classifier.evaluate(input_fn=eval_input_fn)
                for metric in metrics:
                    print(metric)

    def predict(self, image):
        predict_input_fn = tf.estimator.inputs.numpy_input_fn(
            x=image,
            batch_size=1,
            shuffle=False)
        predictions = self.classifier.predict(input_fn=predict_input_fn, 
            checkpoint_path=os.path.join(self.config.checkpoint_dir, 'avg/avg-0')) 
        return predictions                



        
