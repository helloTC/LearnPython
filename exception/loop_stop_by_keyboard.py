#!/usr/bin/env python
# coding=utf-8

def print_key():
    """
    Return everything you type until press Ctrl+c
    """
    while True:
        try:
            print(input('Type Something: '))
        except KeyboardInterrupt:
            print()
            break
