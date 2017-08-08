outdata1 = divmod(20,8)


# prefix an argument with a star when calling a function to unpack tuple
t = (20,8)
outdata2 = divmod(*t)

import os
# Note that filename = hh.grad
_, filename = os.path.split('/nfs/j3/hh.grad')

# Using * to grab excess items
# Can be used in python3, but not in python2

# a, b, *rest = range(5)
# a, b, *rest = range(3)
# a, b, *rest = range(2)
# a, *body, c, d = range(5)
# *head, b, c, d = range(5)

# Nested tuple unpacking
a = [('good', (334,213)),
     ('bad', (231,234))]
for cond, (x, y) in a:
    print('x = {0}, y = {1}'.format(x, y))


# Namedtuple
from collections import namedtuple
place = namedtuple('place', 'condition coordinate')
tokyo = place('good', (334,213))
print(tokyo)

# _fields class attribute, _make(iterable) class method, _asdict() instance method
print(place._fields)
LatLong = namedtuple('LatLong', 'lat long')
delhi_data = ('Delhi NCR', LatLong(28.61, 77.21))
delhi = place._make(delhi_data)
for key, value in delhi._asdict().items():
    print(key + ':', value)


