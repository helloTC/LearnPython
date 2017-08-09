#!/usr/bin/env python
# coding=utf-8

def make_averager():
    series = []
    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total/len(series)
    return averager

if __name__ == '__main__':
    avg = make_averager()
    print avg(13)
    print avg(15)
    print avg(14)
