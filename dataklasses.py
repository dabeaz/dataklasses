# dataklasses.py
# 
#     https://github.com/dabeaz/dataklasses
#
# Author: David Beazley (@dabeaz). 
#         http://www.dabeaz.com
#
# Copyright (C) 2021-2022.
#
# Permission is granted to use, copy, and modify this code in any
# manner as long as this copyright message and disclaimer remain in
# the source code.  There is no warranty.  Try to use the code for the
# greater good.

__all__ = ['dataklass']

from functools import lru_cache, reduce

def codegen(func):
    @lru_cache
    def make_func_code(numfields):
        names = [ f'_{n}' for n in range(numfields) ]
        exec(func(names), globals(), d:={})
        return d.popitem()[1]
    return make_func_code

def patch_args_and_attributes(func, fields, start=0):
    return type(func)(func.__code__.replace(
        co_names=(*func.__code__.co_names[:start], *fields),
        co_varnames=('self', *fields),
    ), func.__globals__)

def patch_attributes(func, fields, start=0):
    return type(func)(func.__code__.replace(
        co_names=(*func.__code__.co_names[:start], *fields)
    ), func.__globals__)
    
def all_hints(cls):
    return reduce(lambda x, y: getattr(y, '__annotations__',{}) | x, cls.__mro__, {})

@codegen
def make__init__(fields):
    code = 'def __init__(self, ' + ','.join(fields) + '):\n'
    return code + '\n'.join(f' self.{name} = {name}\n' for name in fields)

@codegen
def make__repr__(fields):
    return 'def __repr__(self):\n' \
           ' return f"{type(self).__name__}(' + \
           ', '.join('{self.' + name + '!r}' for name in fields) + ')"\n'

@codegen
def make__eq__(fields):
    selfvals = ','.join(f'self.{name}' for name in fields)
    othervals = ','.join(f'other.{name}' for name in fields)
    return  'def __eq__(self, other):\n' \
            '  if self.__class__ is other.__class__:\n' \
           f'    return ({selfvals},) == ({othervals},)\n' \
            '  else:\n' \
            '    return NotImplemented\n'

@codegen
def make__iter__(fields):
    return 'def __iter__(self):\n' + '\n'.join(f'   yield self.{name}' for name in fields)

@codegen
def make__hash__(fields):
    self_tuple = '(' + ','.join(f'self.{name}' for name in fields) + ',)'
    return 'def __hash__(self):\n' \
          f'    return hash({self_tuple})\n'

def dataklass(cls):
    fields = all_hints(cls)
    nfields = len(fields)
    clsdict = vars(cls)
    if not '__init__' in clsdict: cls.__init__ = patch_args_and_attributes(make__init__(nfields), fields)
    if not '__repr__' in clsdict: cls.__repr__ = patch_attributes(make__repr__(nfields), fields, 2)
    if not '__eq__' in clsdict: cls.__eq__ = patch_attributes(make__eq__(nfields), fields, 1)
    # if not '__iter__' in clsdict:  cls.__iter__ = patch_attributes(make__iter__(nfields), fields)
    # if not '__hash__' in clsdict:  cls.__hash__ = patch_attributes(make__hash__(nfields), fields, 1)
    cls.__match_args__ = tuple(fields)
    return cls

# Example use
if __name__ == '__main__':
    @dataklass
    class Coordinates:
        x: int
        y: int


