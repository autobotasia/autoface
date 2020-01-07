import tensorflow as tf

class Model():
    def __init__(self, config):
        self.config = config

    def build_model(self, inputs):
        # network architecture
        weight1 = tf.get_variable("weight1", [2048, self.config.input_dim],
                initializer=tf.truncated_normal_initializer(stddev=0.02))
        bias1 = tf.get_variable("bias1", [2048], initializer=tf.zeros_initializer())

        weight2 = tf.get_variable("weight2", [self.config.number_of_class, 2048],
                initializer=tf.truncated_normal_initializer(stddev=0.02))
        bias2 = tf.get_variable("bias2", [self.config.number_of_class], initializer=tf.zeros_initializer())

        logits1 = tf.matmul(inputs, weight1, transpose_b=True)            
        logits1 = tf.nn.bias_add(logits1, bias1)
        prob_logits1 = tf.nn.relu(logits1)
        prob_logits1 = tf.nn.dropout(prob_logits1, rate=0.25)
        logits = tf.matmul(prob_logits1, weight2, transpose_b=True)
        logits = tf.nn.bias_add(logits, bias2)
        return logits                                                   

    def model_fn(self, features, labels, mode):
        global_step = tf.train.get_global_step()
        
        #images = tf.reshape(features, [-1, self.config.input_dim])
        
        logits = self.build_model(features)
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
                eval_metric_ops={'accuracy': accuracy},
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
                scaffold=None,
                training_hooks=train_hook_list)