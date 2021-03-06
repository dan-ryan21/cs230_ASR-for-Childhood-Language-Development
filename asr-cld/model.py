#####################################################################################################
#  Dan Ryan
#
#  Stanford University - CS230 Deep Learning
#
#  06/05/2020
#
#  dryan2@stanford.edu
#  dan_ryan21@hotmail.com
#
#  Definition of the model used to detect keywords.  The model takes as input a spectrogram and
#  outputs a time series of labels corresponding to the words, if any, detected.  The labels for
#  this implementation are one-hot encoded according to the following schema:
#
#  0 - No word or unrecognized word detected
#  1 - 'bird'
#  2 - 'cat'
#  3 - 'dog'
#  4 - 'one'
#  5 - 'two'
#  6 - 'three'
#
#  NOTE:  Much of the code contained here is taken from the Coursera Trigger Word Detection
#  programming assignment.  It has been modified to accomodate multiple labels.
#
#####################################################################################################

from keras.layers import Dense, Activation, Dropout, Input, TimeDistributed, Conv1D
from keras.layers import GRU, BatchNormalization
from keras.models import Model
from asr_cld_constants import *


#  Build the Keras Model
def getModel(input_shape):
    X_input = Input(shape=input_shape)

    # CONV layer
    X = Conv1D(filters=196, kernel_size=15, strides=4)(X_input)
    X = BatchNormalization()(X)
    X = Activation("relu")(X)
    X = Dropout(rate=0.2)(X)

    # GRU Layer
    X = GRU(units=128, return_sequences=True)(X)
    X = Dropout(rate=0.2)(X)
    X = BatchNormalization()(X)

    # GRU Layer
    X = GRU(units=128, return_sequences=True)(X)
    X = Dropout(rate=0.2)(X)
    X = BatchNormalization()(X)
    X = Dropout(rate=0.2)(X)

    # Time-distributed dense layer
    #X = TimeDistributed(Dense(getNumOfClasses(), activation="softmax"))(X)
    X = TimeDistributed(Dense(getNumOfClasses(), activation="sigmoid"))(X)

    # Softmax output layer
    X = Activation('softmax')(X)

    model = Model(inputs=X_input, outputs=X)

    return model
