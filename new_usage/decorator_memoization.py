#!/usr/bin/env python
# coding=utf-8

import functools
# Cache execution
# Pay attention do not use this decorator into functions with multiple argments which may cause large variability.
def memoize(func):
    """
    Cache the results of the function
    """
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args):
        if args in cache:
            return cache[args]
        
        print('Calling {}()'.format(func.__name__))

        result = func(*args)
        cache[args] = result
        return result
    return wrapper

@memoize
def addvalues(x,y):
    return x+y

if __name__ == '__main__':
    print('First calling...')
    print('{}'.format(addvalues(4,5)))
    print('Second calling...')
    print('{}'.format(addvalues(4,5)))
    print('Third calling...')
    print('{}'.format(addvalues(2,5)))

