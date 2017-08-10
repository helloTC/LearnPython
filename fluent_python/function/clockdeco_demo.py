#!/usr/bin/env python
# coding=utf-8

import time
from clockdeco import clock

@clock
def snooze(seconds):
    time.sleep(seconds)

@clock
def factorial(n):
    return 1 if n<2 else n*factorial(n-1)

if __name__ == '__main__':
    snooze(3)
    factorial(3)
