#!/usr/bin/env python
# coding=utf-8

def test_value_raw(value):
    if value < 100:
        return 'The value is just right.'
    else:
        return 'The value is too big!'

def test_value_new(value):
    return 'The value is ' + ('just right.' if value < 100 else 'too big!')
