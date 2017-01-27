#!/usr/bin/env python
# coding=utf-8

def multiply_by(factor):
    """
    Return a function that multiplies values by factor
    """
    def multiply(value):
        """
        Multiply given value by the factor already existed
        """
        return value * factor
    
    return multiply

if __name__ == '__main__':
    times3 = multiply_by(3)
    print('Output is {}'.format(times3(6)))
