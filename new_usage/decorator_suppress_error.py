#!/usr/bin/env python
# coding=utf-8

import functools

def suppress_errors(func):
    """
    Automatically silence errors that occur within a function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            pass
    return wrapper

@suppress_errors
def divide_zeros():
    print('Running function...')
    return 1.0/0

if __name__ == '__main__':
    divide_zeros()
