#!/usr/bin/env python
# coding=utf-8

import functools

def suppress_errors_raw(func):
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

def suppress_errors_arguments(func = None, log_func = None):
    """
    With arguments
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_func is not None:
                    log_func(str(e))
        return wrapper
    if func is None:
        return decorator
    else:
        return decorator(func)

def print_logger(message):
    print(message)


# @suppress_errors_raw
@suppress_errors_arguments(log_func = print_logger)
def divide_zeros():
    print('Running function...')
    return 1.0/0

if __name__ == '__main__':
    divide_zeros()
