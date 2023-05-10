# Packing

## Example

``` python
>>> umsgpack.packb([1, True, False, 0xffffffff, {'foo': b'\x80\x01\x02', \
...                 'bar': [1,2,3, {'a': [1,2,3,{}]}]}, -1, 2.12345])
b'\x97\x01\xc3\xc2\xce\xff\xff\xff\xff\x82\xa3foo\xc4\x03\x80\x01\
\x02\xa3bar\x94\x01\x02\x03\x81\xa1a\x94\x01\x02\x03\x80\xff\xcb\
@\x00\xfc\xd3Z\x85\x87\x94'
>>> 
```

## API

```{eval-rst}
.. autofunction:: umsgpack.packb
    :noindex:

Also available under the ``umsgpack.dumps()`` alias.
```

## Options

### Ext Handlers

See the [Extension Types](extension.md) section.

### Float Precision

The packing functions provide a `force_float_precision` option to force packing
of floats into the specified precision: `"single"` for IEEE-754
single-precision floats, or `"double"` for IEEE-754 double-precision floats.

``` python
>>> # Force float packing to single-precision floats
... umsgpack.packb(2.5, force_float_precision="single")
b'\xca@ \x00\x00'
>>> # Force float packing to double-precision floats
... umsgpack.packb(2.5, force_float_precision="double")
b'\xcb@\x04\x00\x00\x00\x00\x00\x00'
>>> 
```

### Old Specification Compatibility Mode

The compatibility mode supports the "raw" bytes MessagePack type from the [old
specification](https://github.com/msgpack/msgpack/blob/master/spec-old.md).
When the module-wide `compatibility` attribute is enabled, both unicode strings
and bytes will be serialized into the "raw" MessagePack type, and the "raw"
MessagePack type will be deserialized into bytes.

``` python
>>> umsgpack.compatibility = True
>>>
>>> umsgpack.packb([u"some string", b"some bytes"])
b'\x92\xabsome string\xaasome bytes'
>>> umsgpack.unpackb(_)
[b'some string', b'some bytes']
>>> 
```

## Exceptions

If an error occurs during packing, u-msgpack-python will raise an exception
derived from `umsgpack.PackException`. Possible packing exceptions are
described below.

### UnsupportedTypeException

```{eval-rst}
.. autoexception:: umsgpack.UnsupportedTypeException
    :noindex:
```

``` python
>>> # Attempt to pack set type
... umsgpack.packb(set([1,2,3]))
...
umsgpack.UnsupportedTypeException: unsupported type: <type 'set'>
>>> 

>>> # Attempt to pack > 64-bit unsigned int
... umsgpack.packb(2**64)
...
umsgpack.UnsupportedTypeException: huge unsigned int
>>> 
```

### NotImplementedError

Ext serializable class is missing implementation of `packb()`.

``` python
>>> @umsgpack.ext_serializable(0x50)
... class Point(collections.namedtuple('Point', ['x', 'y'])):
...   pass
... 
>>> umsgpack.packb(Point(1, 2))
...
NotImplementedError: Ext serializable class <class '__main__.Point'> is missing implementation of packb()
>>> 
```
