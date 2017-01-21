#!/usr/bin/env python
# coding=utf-8

import sys

def validate(data):
    if 'username' in data and data['username'].startswith('_'):
        raise ValueError('Username must not start with underscore')

if __name__ == '__main__':
    username = sys.argv[0]
    # username = '_name'
    try:
        validate({'username': username})
    except (TypeError, ValueError) as errors:
        print errors
