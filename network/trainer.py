import os
import tensorflow as tf
import numpy as np
from data_generator import DataGenerator
from model import Model
from random import randint
from sklearn.model_selection import KFold
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix


classname = []
for _, clsdirs, _ in os.walk('./datasets/nccfaces/train/'):
    for index, clsdir in enumerate(clsdirs):
        classname.append(clsdir)

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

            train_spec = tf.estimator.TrainSpec(
                train_input_fn,
                max_steps=20000
            )    

            eval_spec = tf.estimator.EvalSpec(
                eval_input_fn,
                steps=100,
                name='validation',
                start_delay_secs=150,
                throttle_secs=200
            )
            # Finally, train and evaluate the model after each epoch
            for _ in range(self.config.num_epochs):
                self.classifier.train(input_fn=train_input_fn)
                metrics = self.classifier.evaluate(input_fn=eval_input_fn)
                print(metrics)
            '''tf.estimator.train_and_evaluate(
                self.classifier,
                train_spec,
                eval_spec
            )'''

    def do_predict(self):
        y_pred = []
        y_true = np.argmax(self.data.ytest, 1)
        for best_idx, _, _ in self.predict(self.data.xtest, self.config.batch_size):
            y_pred.append(best_idx)

        assert(len(y_pred) == len(y_true), "diff range error")

        #metrics        
        print("Precision", precision_score(y_true, y_pred, average='macro'))
        print("Recall", recall_score(y_true, y_pred, average='macro'))
        print("f1_score", f1_score(y_true, y_pred, average='macro'))
        print("confusion_matrix")
        print(confusion_matrix(y_true, y_pred))
        #fpr, tpr, tresholds = sk.metrics.roc_curve(y_true, y_pred)
    


    def predict(self, image, batch_size):
        predict_input_fn = tf.estimator.inputs.numpy_input_fn(
            x=image,
            batch_size=batch_size,
            shuffle=False)
        predictions = self.classifier.predict(input_fn=predict_input_fn) #, checkpoint_path=os.path.join(self.config.checkpoint_dir, 'model.ckpt-1932'))

        for p in predictions:
            best_idx = p['predicted_logit']
            clsname = classname[best_idx]
            prob = p['probabilities'][best_idx]

            yield best_idx, clsname, prob                



        
