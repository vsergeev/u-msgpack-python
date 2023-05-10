# Streaming

The streaming `pack()` and `unpack()` functions allow packing and unpacking
objects directly to and from a stream, respectively. Streaming may be necessary
when unpacking serialized bytes whose size is unknown in advance, or it may be
more convenient and efficient when working directly with stream objects (e.g.
files or stream sockets).

## Packing

`pack(obj, fp)` serializes Python object `obj` to a `.write()` supporting
file-like object `fp`.

``` python
>>> class Foo:
...     def write(self, data):
...         # write 'data' bytes
...         pass
... 
>>> f = Foo()
>>> umsgpack.pack({u"compact": True, u"schema": 0}, f)
>>> 
```

```{eval-rst}
.. autofunction:: umsgpack.pack
    :noindex:

Also available under the ``umsgpack.dump()`` alias.
```

## Unpacking

`unpack(fp)` deserializes a Python object from a `.read()` supporting file-like
object `fp`.

``` python
>>> class Bar:
...     def read(self, n):
...         # read and return 'n' number of bytes
...         return b"\x01"*n
... 
>>> f = Bar()
>>> umsgpack.unpack(f)
1
>>> 
```

```{eval-rst}
.. autofunction:: umsgpack.unpack
    :noindex:

Also available under the ``umsgpack.load()`` alias.
```
