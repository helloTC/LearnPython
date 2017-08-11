#!/usr/bin/env python
# coding=utf-8

"""
An example to compare classmethod and staticmethod
"""
class demo(object):
    @classmethod
    def klassmeth(*args):
        return args
    
    @staticmethod
    def statmeth(*args):
        return args
