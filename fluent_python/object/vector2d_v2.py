#!/usr/bin/env python
# encoding=utf-8

class vector2d(object):
    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)
    
    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)
