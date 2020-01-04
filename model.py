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

