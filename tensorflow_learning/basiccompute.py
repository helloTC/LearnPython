#!/usr/bin/env python
# coding=utf-8
import tensorflow as tf
a = tf.constant(2)
b = tf.constant(3)

with tf.Session() as sess:
    print('a = 2, b = 3')
    print('Addition with constants: {}'.format(sess.run(a+b)))
    print('Multiplication with constants: {}'.format(sess.run(a*b)))

add_unit = tf.add(a, b)
mul_unit = tf.multiply(a, b)
with tf.Session() as sess:
    print('Calling node for addition and multiplication:')
    print('Addition with constants: {}'.format(sess.run(add_unit)))
    print('Multiplication with constants: {}'.format(sess.run(mul_unit)))
