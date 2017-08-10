#!/usr/bin/env python
# coding=utf-8

import time
import functools

def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elasped = time.time() - t0
        name = func.__name__
        arg_str = []
        if args:
            arg_str.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_str.append(', '.join(pairs))
        print('[%.8fs] %s(%s) -> %r' % (elasped, name, arg_str, result))
        return result
    return clocked



