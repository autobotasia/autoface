import tensorflow as tf

class Model():
    def __init__(self, config):
        self.config = config
        # init the global step
        self.init_global_step()
        # init the epoch counter
        self.init_cur_epoch()

        self.build_model()
        self.init_saver()

    # save function that saves the checkpoint in the path defined in the config file
    def save(self, sess):
        print("Saving model at %s...", self.config.checkpoint_dir)
        self.saver.save(sess, '%smodel'%self.config.checkpoint_dir, self.global_step_tensor)
        print("Model saved")

    # load latest checkpoint from the experiment path defined in the config file
    def load(self, sess):
        latest_checkpoint = tf.train.latest_checkpoint(self.config.checkpoint_dir)
        if latest_checkpoint:
            print("Loading model checkpoint {} ...\n".format(latest_checkpoint))
            self.saver.restore(sess, latest_checkpoint)
            print("Model loaded")

    # just initialize a tensorflow variable to use it as epoch counter
    def init_cur_epoch(self):
        with tf.variable_scope('cur_epoch'):
            self.cur_epoch_tensor = tf.Variable(0, trainable=False, name='cur_epoch')
            self.increment_cur_epoch_tensor = tf.assign(self.cur_epoch_tensor, self.cur_epoch_tensor + 1)

    # just initialize a tensorflow variable to use it as global step counter
    def init_global_step(self):
        # DON'T forget to add the global step tensor to the tensorflow trainer
        with tf.variable_scope('global_step'):
            self.global_step_tensor = tf.Variable(0, trainable=False, name='global_step')

    def build_model(self):
        self.is_training = tf.placeholder(tf.bool)

        self.inputs = tf.placeholder(tf.float32, shape=[self.config.batch_size, self.config.input_dim])
        self.labels = tf.placeholder(tf.float32, shape=[self.config.batch_size, self.config.number_of_class])

        # network architecture
        weight1 = tf.get_variable("weight1", [2048, self.config.input_dim],
                initializer=tf.truncated_normal_initializer(stddev=0.02))
        bias1 = tf.get_variable("bias1", [2048], initializer=tf.zeros_initializer())

        weight2 = tf.get_variable("weight2", [self.config.number_of_class, 2048],
                initializer=tf.truncated_normal_initializer(stddev=0.02))
        bias2 = tf.get_variable("bias2", [self.config.number_of_class], initializer=tf.zeros_initializer())

        with tf.variable_scope("loss"):
            logits1 = tf.matmul(self.inputs, weight1, transpose_b=True)            
            logits1 = tf.nn.bias_add(logits1, bias1)
            prob_logits1 = tf.nn.relu(logits1)
            prob_logits1 = tf.nn.dropout(prob_logits1, rate=0.25)
            logits = tf.matmul(prob_logits1, weight2, transpose_b=True)
            logits = tf.nn.bias_add(logits, bias2)

            self.probabilities = tf.nn.softmax(logits, axis=-1)
            #log_probs = tf.nn.log_softmax(logits, axis=-1)
            #one_hot_labels = tf.one_hot(self.labels, depth=NUMBER_OF_CLASSES, dtype=tf.float32)
            #per_example_loss = -tf.reduce_sum(self.labels * log_probs, axis=-1)
            self.loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.labels, logits=logits)) 
            update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
            with tf.control_dependencies(update_ops):
                self.train_step = tf.train.AdamOptimizer(self.config.learning_rate).minimize(self.loss,
                                                            global_step=self.global_step_tensor)


    def init_saver(self):
        # here you initialize the tensorflow saver that will be used in saving the checkpoints.
        self.saver = tf.train.Saver(max_to_keep=self.config.max_to_keep, filename='checkpoint')

