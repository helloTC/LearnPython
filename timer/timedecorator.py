#!/usr/bin/env python
# coding=utf-8

import time

def timerfunc(func):
    """
    timer decorator
    """
    def function_timer(*args, **kwargs):
        """
        A nested function for timing other functions
        """
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        runtime = end - start

        msg = "Run time for {func} took {time} seconds to finish"
        print(msg.format(func = func.__name__, time = runtime))
       
        return value
    return function_timer

@timerfunc
def long_runner():
    import random
    for x in range(5):
        sleep_time = random.choice(range(1,5))
        time.sleep(sleep_time)
    a = 1
    b = 2
    return a, b

if __name__ == '__main__':
    a, b = long_runner()

