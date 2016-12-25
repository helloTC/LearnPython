#!/usr/bin/env python
# coding=utf-8

"""
>>> print(list(range(10))) # doctest: +ELLIPSIS
[0, 1, ..., 9]

>>> class Dog: pass
>>> Dog() # doctest: +ELLIPSIS
<__main__.Dog instance at 0x...>
"""

def add(a,b):
    """
    Return the addition of the arguments
    >>> add(1,2)
    3
    >>> add('a','b')
    'ab'
    >>> add(1, '2')
    Traceback (most recent call last):
      File "test.py", line 43, in <module>
        add(1, '2')
    TypeError: unsupported operand type(s) for +: 'int' and 'str'
    """
    return a + b

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    doctest.testfile('/home/hellotc/workingdir/program/LearnPython/testing/add.txt', False)
