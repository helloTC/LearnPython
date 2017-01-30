#!/usr/bin/env python
# coding=utf-8

import functools
def decorator(declared_decorator):
    """
    Create a decorator out of a function, used as a wrapper
    """

    @functools.wraps(declared_decorator)
    def final_decorator(func = None, **kwargs):
        
        def decorated(func):
            @functools.wraps(func)
            def wrapper(*a, **kw):
                return declared_decorator(func, a, kw, **kwargs)
            return wrapper
        
        if func is None:
            return decorated
        else:
            return decorated(func)
    return final_decorator

@decorator
def suppress_errors(func, args, kwargs, log_func=None):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if log_func is not None:
            log_func(str(e))

def print_logger(message):
    print(message)

@suppress_errors(log_func = print_logger)
def divided_zero():
    return 1.0/0

if __name__ == '__main__':
    divided_zero()

