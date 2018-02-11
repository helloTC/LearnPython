#!/usr/bin/env python
# coding=utf-8

def f(a, b):
    a += b
    return a

if __name__ == "__main__":
    x1 = 1
    x2 = 2
    print("integer number: {}".format(f(x1, x2)))
    print("x1 = {0}, x2 = {1}".format(x1, x2))

    x3 = [1,2]
    x4 = [3,4]
    print("list: {}".format(f(x3, x4)))
    print("x3 = {0}, x4 = {1}".format(x3, x4))

    x5 = (1,2)
    x6 = (3,4)
    print("tuple: {}".format(f(x5, x6)))
    print("x5 = {1}, x6 = {0}".format(x5, x6))

