#!/usr/bin/env python
# coding=utf-8

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# parameters
learning_rate = 0.01
trainint_epochs = 2000
display_step = 50

# Training Data
train_X = np.array([3.3, 4.4, 5.5, 6.7, 7.0, 4.2, 9.8, 6.2, 7.6, 2.2, 7.0, 10.8, 5.3, 8.0, 5.7, 9.3, 3.1])
train_Y = np.array([1.7, 2.8, 2.1, 3.2, 1.7, 1.6, 3.4, 2.6, 2.5, 1.2, 2.8, 3.4, 1.6, 2.9, 2.4, 2.9, 1.3])
n_samples = train_X.shape[0]

# tf Graph Input
X = tf.placeholder('float')
Y = tf.placeholder('float')

# Create Model

# Set model weights
W = tf.Variable(np.random.randn(), name = 'weights')
b = tf.Variable(np.random.randn(), name = 'b')

# Construct a linear Model
activation = tf.add(tf.multiply(X, W), b)

# Minimize the squared errors
cost = tf.reduce_sum(tf.pow(activation - Y, 2))/(2*n_samples)
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

# Initializating the variables
init = tf.global_variables_initializer()

# Launch the Graph
with tf.Session() as sess:
    sess.run(init)

    # Fit all training Data
    for epoch in range(trainint_epochs):
        for (x, y) in zip(train_X, train_Y):
            sess.run(optimizer, feed_dict={X: x, Y: y})

        # Display logs per epoch step
        if epoch % display_step == 0:
            print('Epoch: {}'.format(epoch+1))
            print('Cost={:.9f}'.format(sess.run(cost, feed_dict={X:train_X, Y:train_Y})))
            print('W={}'.format(sess.run(W)))
            print('b={}'.format(sess.run(b)))

    print('Optimization finished!')
    print('cost = {}'.format(cost, feed_dict={X:train_X, Y:train_Y}))
    print('W = {}'.format(sess.run(W)))
    print('b = {}'.format(sess.run(b)))

    # Graphic display
    plt.plot(train_X, train_Y, 'ro', label = 'Original data')
    plt.plot(train_X, sess.run(W)*train_X + sess.run(b), label = 'Fitted line')
    plt.legend()
    plt.show()



