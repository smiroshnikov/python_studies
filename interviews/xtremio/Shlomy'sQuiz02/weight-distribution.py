import sys

weight_list = [11, 22, 3, 14, 5, 6]


def divide_list(anylist):
    pass


weight_dictionary = {}

for _, k in enumerate(sorted(weight_list)):
    weight_dictionary[_] = k

print (weight_dictionary)
"""
print (None)
print type(None)
print (True.__doc__)
"""
# we can see one or more base classes
print (True.__class__)
print (True.__class__.__bases__)  # bool is subclass of int
print (True.__class__.__bases__[0].__bases__[0])  # int is a subclass of object

print (bool.__mro__)  # method resolution order - same info as above

import inspect

# inspect.getmro(False) # expects a class , not an instance

inspect.getmro(bool)

print id('a string')
print id(234234)
print (id(id(id(id(id(3))))))
print id(True)

a = ' cool long string !'
print a.__len__()  # same as calling len(a)

print dict(pi=3.14, e=2.17)

size = sys.getsizeof

print 'Size of w is {} bytes'.format(size('w'))
print size('walk')
