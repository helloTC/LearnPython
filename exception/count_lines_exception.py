#!/usr/bin/env python
# coding=utf-8

import logging

def count_lines_exception(filename):
    """
    Count the number of lines in a file.
    If file can't be opened, treated the same as if it was empty
    """
    try:
        return len(open(filename, 'r').readlines())
    except (EnvironmentError, TypeError):
        print('Exception error')
        return 0

def count_lines_logging(filename):
    """
    
    """
    try:
        return len(open(filename, 'r').readlines())
    except EnvironmentError as e:
        logging.error(e)
    except TypeError as e:
        logging.error(e.args[1])
        return 0

if __name__ == '__main__':
    count_lines_exception('pattenr.txt')
    count_lines_logging('pattenr.txt')
