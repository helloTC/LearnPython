#!/usr/bin/env python
# coding=utf-8

def validate(value, validator):
    try:
        return validator(value)
    except ValueError:
        raise ValueError('Invalid value: %s' % value)

def validator(value):
    if len(value) > 10:
        raise Exception('Value can''t exceed 10 characters')
    if len(value) < 5:
        raise Exception('values should exceed at least 5 characters')

if __name__ == '__main__':
    validate(range(2), validator)
    # validate(False, validator)
