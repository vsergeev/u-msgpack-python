# Unpacking

## Example

``` python
>>> umsgpack.unpackb(b'\x97\x01\xc3\xc2\xce\xff\xff\xff\xff\x82\xa3\
foo\xc4\x03\x80\x01\x02\xa3bar\x94\x01\x02\x03\x81\xa1a\x94\x01\x02\
\x03\x80\xff\xcb@\x00\xfc\xd3Z\x85\x87\x94')
[1, True, False, 4294967295, {'foo': b'\x80\x01\x02', \
 'bar': [1, 2, 3, {u'a': [1, 2, 3, {}]}]}, -1, 2.12345]
>>> 
```

## API

```{eval-rst}
.. autofunction:: umsgpack.unpackb
    :noindex:

Also available under the ``umsgpack.loads()`` alias.
```

## Options

### Ext Handlers

See the [Extension Types](extension.md) section.

### Ordered Dictionaries

The unpacking functions provide a `use_ordered_dict` option to unpack
MessagePack maps into the `collections.OrderedDict` type, rather than the
unordered `dict` type, to preserve the order of deserialized MessagePack maps.
Note that as of Python 3.6, dictionaries are insertion ordered by default.

``` python
>>> umsgpack.unpackb(b'\x82\xa7compact\xc3\xa6schema\x00')
{'compact': True, 'schema': 0}
>>> umsgpack.unpackb(b'\x82\xa7compact\xc3\xa6schema\x00', use_ordered_dict=True)
OrderedDict([('compact', True), ('schema', 0)])
>>> 
```

### Tuples

The unpacking functions provide a `use_tuple` option to unpack MessagePack
arrays into tuples, rather than lists.

``` python
>>> umsgpack.unpackb(b'\x93\xa1a\xc3\x92\x01\x92\x02\x03')
['a', True, [1, [2, 3]]]
>>> umsgpack.unpackb(b'\x93\xa1a\xc3\x92\x01\x92\x02\x03', use_tuple=True)
('a', True, (1, (2, 3)))
>>> 
```

### Invalid UTF-8 Strings

The unpacking functions provide an `allow_invalid_utf8` option to unpack
MessagePack strings with invalid UTF-8 into the `umsgpack.InvalidString` type,
instead of throwing an exception. The `umsgpack.InvalidString` type is a
subclass of `bytes`, and can be used like any other `bytes` object.

``` python
>>> # Attempt to unpack invalid UTF-8 string
... umsgpack.unpackb(b'\xa4\x80\x01\x02\x03')
...
umsgpack.InvalidStringException: unpacked string is invalid utf-8
>>> umsgpack.unpackb(b'\xa4\x80\x01\x02\x03', allow_invalid_utf8=True)
b'\x80\x01\x02\x03'
>>> 
```

## Exceptions

If a non-byte-string argument is passed to `umsgpack.unpackb()`, it will raise
a `TypeError` exception. If an error occurs during unpacking, u-msgpack-python
will raise an exception derived from `umsgpack.UnpackException`. Possible
unpacking exceptions are described below.


### TypeError

Packed data is not type `str` (Python 2), or not type `bytes` (Python 3).

``` python
# Attempt to unpack non-str type data in Python 2
>>> umsgpack.unpackb(u"no good")
...
TypeError: expected packed data as type 'str'
>>> 

# Attempt to unpack non-bytes type data in Python 3
>>> umsgpack.unpackb("no good")
...
TypeError: expected packed data as type 'bytes'
>>> 
```

### InsufficientDataException

```{eval-rst}
.. autoexception:: umsgpack.InsufficientDataException
    :noindex:
```

``` python
# Attempt to unpack a cut-off serialized 32-bit unsigned int
>>> umsgpack.unpackb(b"\xce\xff\xff\xff")
...
umsgpack.InsufficientDataException
>>> 

# Attempt to unpack an array of length 2 missing the second item
>>> umsgpack.unpackb(b"\x92\xc2")
...
umsgpack.InsufficientDataException
>>> 
```

### InvalidStringException

```{eval-rst}
.. autoexception:: umsgpack.InvalidStringException
    :noindex:
```

String bytes are strictly decoded with UTF-8. This exception is thrown if UTF-8
decoding of string bytes fails. Use the `allow_invalid_utf8` option to unpack
invalid MessagePack strings into byte strings.

``` python
# Attempt to unpack invalid UTF-8 string
>>> umsgpack.unpackb(b"\xa2\x80\x81")
...
umsgpack.InvalidStringException: unpacked string is invalid utf-8
>>> 
```

### UnsupportedTimestampException

```{eval-rst}
.. autoexception:: umsgpack.UnsupportedTimestampException
    :noindex:
```

The official timestamp extension type supports 32-bit, 64-bit and 96-bit
formats. This exception is thrown if a timestamp extension type with an
unsupported format is encountered.

``` python
# Attempt to unpack invalid timestamp
>>> umsgpack.unpackb(b"\xd5\xff\x01\x02")
...
umsgpack.UnsupportedTimestampException: unsupported timestamp with data length 2
>>> 
```

### ReservedCodeException

```{eval-rst}
.. autoexception:: umsgpack.ReservedCodeException
    :noindex:
```

``` python
# Attempt to unpack reserved code 0xc1
>>> umsgpack.unpackb(b"\xc1")
...
umsgpack.ReservedCodeException: reserved code encountered: 0xc1
>>> 
```

### UnhashableKeyException

```{eval-rst}
.. autoexception:: umsgpack.UnhashableKeyException
    :noindex:
```

Python dictionaries only support keys that are instances of
`collections.Hashable`, so while the map `{ { u'abc': True } : 5 }` has a
MessagePack serialization, it cannot be unpacked into a valid Python
dictionary.

``` python
# Attempt to unpack { {} : False }
>>> umsgpack.unpackb(b"\x82\x80\xc2")
...
umsgpack.UnhashableKeyException: encountered unhashable key type: {}, <type 'dict'>
>>> 
```

### DuplicateKeyException

```{eval-rst}
.. autoexception:: umsgpack.DuplicateKeyException
    :noindex:
```

Python dictionaries do not support duplicate keys, but MessagePack maps may be
serialized with duplicate keys.

``` python
# Attempt to unpack { 1: True, 1: False }
>>> umsgpack.unpackb(b"\x82\x01\xc3\x01\xc2")
...
umsgpack.DuplicateKeyException: encountered duplicate key: 1, <type 'int'>
>>> 
```

### NotImplementedError

Ext serializable class is missing implementation of `unpackb()`.

``` python
>>> @umsgpack.ext_serializable(0x50)
... class Point(collections.namedtuple('Point', ['x', 'y'])):
...   pass
... 
>>> umsgpack.unpackb(b'\xd7\x50\x00\x00\x00\x01\x00\x00\x00\x02')
...
NotImplementedError: Ext serializable class <class '__main__.Point'> is missing implementation of unpackb()
>>> 
```
