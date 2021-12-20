# dataklasses

Dataklasses is a library that allows you to quickly define data
classes using Python type hints. Here's an example of how you use it:

```python
from dataklasses import dataklass

@dataklass
class Coordinates:
    x: int
    y: int
```

The resulting class works in a well civilised way, providing the usual
`__init__()`, `__repr__()`, and `__eq__()` methods that you'd normally
have to type out by hand:

```python
>>> a = Coordinates(2, 3)
>>> a
Coordinates(2, 3)
>>> a.x
2
>>> a.y
3
>>> b = Coordinates(2, 3)
>>> a == b
True
>>>
```

It's easy! Almost too easy.

## Wait, doesn't this already exist?

No, it doesn't.  Yes, certain naysayers will be quick to point out the
existence of `@dataclass` from the standard library. Ok, sure, THAT
exists.  However, it's slow and complicated.  Dataklasses are neither
of those things.  The entire `dataklasses` module is less than 100
lines.  The resulting classes import 15-20 times faster than
dataclasses.  See the `perf.py` file for a benchmark.

## Theory of Operation

While out walking with his puppy, Dave had a certain insight about the nature
of Python byte-code.  Coming back to the house, he had to try it out:

```python
>>> def __init1__(self, x, y):
...     self.x = x
...     self.y = y
...
>>> def __init2__(self, foo, bar):
...     self.foo = foo
...     self.bar = bar
...
>>> __init1__.__code__.co_code == __init2__.__code__.co_code
True
>>>
```

How intriguing!  The underlying byte-code is exactly the same even
though the functions are using different argument and attribute names.
Aha! Now, we're onto something interesting.

The `dataclasses` module in the standard library works by collecting
type hints, generating code strings, and executing them using the
`exec()` function.  This happens for every single class definition
where it's used. If it sounds slow, that's because it is.  In fact, it
defeats any benefit of module caching in Python's import system.

Dataklasses are different.  They start out in the same manner--code is
first generated by collecting type hints and using `exec()`.  However,
the underlying byte-code is cached and reused in subsequent class
definitions whenever possible. 

## Questions and Answers

**Q: What methods does `dataklass` generate?**

A: By default `__init__()`, `__repr__()`, and `__eq__()` methods are generated.
`__match_args__` is also defined to assist with pattern matching.

**Q: Does `dataklass` enforce the specified types?**

A: No. The types are merely clues about what the value might be and
the Python language does not provide any enforcement on its own. 

**Q: Does `dataklass` use any advanced magic such as metaclasses?**

A: No. 

**Q: How do I install `dataklasses`?**

A: There is no `setup.py` file, installer, or an official release. You
install it by copying the code into your own project. `dataklasses.py` is
small. You are encouraged to modify it to your own purposes.

**Q: But what if new features get added?**

A: What new features?  The best new features are no new features. 

**Q: Who maintains dataklasses?**

A: If you're using it, you do. You maintain dataklasses.

**Q: Who wrote this?**

A: `dataklasses` is the work of David Beazley. http://www.dabeaz.com.
