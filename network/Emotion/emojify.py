import tensorflow as tf 
import numpy as np 
from kt_utils import * 

train_x, train_y, test_x, test_y, classes = load_dataset()

# Normalize image vectors
X_train = train_x/255.
X_test = test_x/255.

# Reshape
Y_train = train_y.T
Y_test = test_y.T


def modelHappy(input_shape):

    