# A import performance test of standard classes, dataclasses, attrs, and dataklasses

import sys
import time

standard_template = '''
class C{n}:
    def __init__(self, a, b, c, d, e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e

    def __repr__(self):
        return f'C{n}({{self.a!r}}, {{self.b!r}}, {{self.c!r}}, {{self.d!r}}, {{self.e!r}})'

    def __eq__(self, other):
        if self.__class__ is other.__class:
            return (self.a, self.b, self.c, self.d, self.e) == (other.a, other.b, other.c, other.d, other.e)
        else:
            return NotImplemented
'''

namedtuple_template = '''
class C{n}(NamedTuple):
    a : int
    b : int
    c : int
    d : int
    e : int
'''

dataclass_template = '''
@dataclass
class C{n}:
    a : int
    b : int
    c : int
    d : int
    e : int
'''

attr_template = '''
@attr.s
class C{n}:
    a = attr.ib()
    b = attr.ib()
    c = attr.ib()
    d = attr.ib()
    e = attr.ib()
'''

dataklass_template = '''
@dataklass
class C{n}:
    a : int
    b : int
    c : int
    d : int
    e : int
'''

def run_test(name, n):
    start = time.time()
    while n > 0:
        import perftemp
        del sys.modules['perftemp']
        n -= 1
    end = time.time()
    print(name, (end-start))

def write_perftemp(count, template, setup):
    with open('perftemp.py', 'w') as f:
        f.write(setup)
        for n in range(count):
            f.write(template.format(n=n))
    
def main(reps):
    write_perftemp(100, standard_template, '')
    run_test('standard classes', reps)

    write_perftemp(100, namedtuple_template, 'from collections import namedtuple\n')
    write_perftemp(100, namedtuple_template, 'from typing import NamedTuple\n')
    run_test('namedtuple', reps)

    write_perftemp(100, dataclass_template, 'from dataclasses import dataclass\n')
    run_test('dataclasses', reps)
    try:
        write_perftemp(100, attr_template, 'import attr\n')
        run_test('attrs', reps)
    except ImportError:
        print("attrs not installed")

    write_perftemp(100, dataklass_template, 'from dataklasses import dataklass\n')
    run_test('dataklasses', reps)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        reps = int(sys.argv[1])
    else:
        reps = 100
    main(reps)
