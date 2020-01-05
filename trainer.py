import tensorflow as tf
import numpy as np
from data_generator import DataGenerator
from model import Model
from random import randint


class Trainer():
    def __init__(self, config):
        self.config = config
        self.data = DataGenerator(config)

    def model_fn(self, features, labels, mode):
        model = Model(self.config)
        global_step = tf.train.get_global_step()
        
        #images = tf.reshape(features, [-1, self.config.input_dim])
        
        logits = model.build_model(features)
        predicted_logit = tf.argmax(input=logits, axis=1)
        probabilities = tf.nn.softmax(logits)
        
        #PREDICT
        predictions = {
            "predicted_logit": predicted_logit,
            "probabilities": probabilities
        }
        if mode == tf.estimator.ModeKeys.PREDICT:
            return tf.estimator.EstimatorSpec(mode=mode,  
                                            predictions=predictions)
        with tf.name_scope('loss'):
            cross_entropy = tf.nn.softmax_cross_entropy_with_logits_v2(labels=labels, logits=logits)
            loss = tf.reduce_mean(cross_entropy)
        
        with tf.name_scope('accuracy'):
            accuracy = tf.metrics.accuracy(
                labels=tf.argmax(input=labels, axis=1), predictions=predicted_logit, name='acc')   
            tf.summary.scalar('accuracy', accuracy[1])

        #EVAL
        if mode == tf.estimator.ModeKeys.EVAL:
            return tf.estimator.EstimatorSpec(
                mode=mode,
                loss=loss,
                eval_metric_ops={'accuracy/accuracy': accuracy},
                evaluation_hooks=None)
        
        
        # Create a SGR optimizer 
        optimizer = tf.train.AdamOptimizer()
        train_op = optimizer.minimize( 
                    loss, global_step=global_step)
        
        # Create a hook to print acc, loss & global step every 100 iter.   
        train_hook_list = []
        train_tensors_log = {'accuracy': accuracy[1],
                            'loss': loss,
                            'global_step': global_step}
        train_hook_list.append(tf.train.LoggingTensorHook(
            tensors=train_tensors_log, every_n_iter=10))
        
        if mode == tf.estimator.ModeKeys.TRAIN:
            return tf.estimator.EstimatorSpec(
                mode=mode,
                loss=loss,
                train_op=train_op,
                training_hooks=train_hook_list)

    def train(self):
        # Load training and eval data 
        eval_data, eval_labels = next(self.data.next_batch(self.config.batch_size))
        train_data = self.data.xtrain_aug[:,randint(0, 99),:]
        train_labels = self.data.ytrain #self.data.get_aug_data()

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

        # Create a estimator with model_fn
        classifier = tf.estimator.Estimator(model_fn=self.model_fn, 
                        model_dir=self.config.checkpoint_dir)
        # Finally, train and evaluate the model after each epoch
        for _ in range(self.config.num_epochs):
            classifier.train(input_fn=train_input_fn)
            metrics = classifier.evaluate(input_fn=eval_input_fn)

    def predict(self, image):
        # Create a estimator with model_fn
        classifier = tf.estimator.Estimator(model_fn=self.model_fn, 
                        model_dir=self.config.checkpoint_dir)

        # Create a input function to eval
        predict_input_fn = tf.estimator.inputs.numpy_input_fn(
            x=image,
            batch_size=1,
            shuffle=False)
        predictions = classifier.predict(input_fn=predict_input_fn) 
        return predictions                



        
