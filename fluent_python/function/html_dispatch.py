#!/usr/bin/env python
# coding=utf-8

# this part of codes need python3.4 or higher level

import html
import numbers
from singledispatch import singledispatch

from collections import abc
# Can't be used in python2.7

@singledispatch
def htmlsize(obj):
    content = html.escape(repr(obj))
    return '<pre>{}</pre>'.format(content)

@htmlsize.register(str)
def _(text):
    content = html.escape(text).replace('\n', '<br>\n')
    return '<p>{0}</p>'.format(content)

@htmlsize.register(numbers.Integral)
def _(n):
    return '<pre>{0} (0x{0:x})</pre>',format(n)

@htmlsize.register(tuple)
@htmlsize.register(abc.MutableSequence)
def _(seq):
    inner = '</li>\n<li>'.join(htmlsize(item) for item in seq)
    return '<ul>\n<li>' + inner + '<li>\n</ul>'
