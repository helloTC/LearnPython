#!/usr/bin/env python
# coding=utf-8

import time
import random

class Timer():
    """
    Timing Context Manager Completion
    """
    def __init__(self):
        self.start = time.time()
    
    def __enter__(self):
        return self

    def __exit__(self, *args):
        end = time.time()
        runtime = end - self.start
        msg = 'The function took {time} seconds to complete'
        print(msg.format(time = runtime))

def long_runner():
    for x in range(5):
        sleep_time = random.choice(range(1,5))
        time.sleep(sleep_time)

if __name__ == '__main__':
    with Timer():
        long_runner()

