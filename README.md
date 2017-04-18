# u-msgpack-python [![Build Status](https://travis-ci.org/vsergeev/u-msgpack-python.svg?branch=master)](https://travis-ci.org/vsergeev/u-msgpack-python) [![GitHub release](https://img.shields.io/github/release/vsergeev/u-msgpack-python.svg?maxAge=7200)](https://github.com/vsergeev/u-msgpack-python) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/vsergeev/u-msgpack-python/blob/master/LICENSE)

u-msgpack-python is a lightweight [MessagePack](http://msgpack.org/) serializer and deserializer module written in pure Python, compatible with both Python 2 and 3, as well CPython and PyPy implementations of Python. u-msgpack-python is fully compliant with the latest [MessagePack specification](https://github.com/msgpack/msgpack/blob/master/spec.md). In particular, it supports the new binary, UTF-8 string, and application-defined ext types.

u-msgpack-python is currently distributed on [PyPI](https://pypi.python.org/pypi/u-msgpack-python) and as a single file: [umsgpack.py](https://raw.github.com/vsergeev/u-msgpack-python/master/umsgpack.py).

## Installation

With pip:
``` text
$ pip install u-msgpack-python
```

With easy_install:
``` text
$ easy_install u-msgpack-python
```

or simply drop [umsgpack.py](https://raw.github.com/vsergeev/u-msgpack-python/master/umsgpack.py) into your project!
``` text
$ wget https://raw.github.com/vsergeev/u-msgpack-python/master/umsgpack.py
```

## Examples

Basic Example:
``` python
>>> import umsgpack
>>> umsgpack.packb({u"compact": True, u"schema": 0})
b'\x82\xa7compact\xc3\xa6schema\x00'
>>> umsgpack.unpackb(_)
{u'compact': True, u'schema': 0}
>>>
```

A more complicated example:
``` python
>>> umsgpack.packb([1, True, False, 0xffffffff, {u"foo": b"\x80\x01\x02", \
...                 u"bar": [1,2,3, {u"a": [1,2,3,{}]}]}, -1, 2.12345])
b'\x97\x01\xc3\xc2\xce\xff\xff\xff\xff\x82\xa3foo\xc4\x03\x80\x01\
\x02\xa3bar\x94\x01\x02\x03\x81\xa1a\x94\x01\x02\x03\x80\xff\xcb\
@\x00\xfc\xd3Z\x85\x87\x94'
>>> umsgpack.unpackb(_)
[1, True, False, 4294967295, {u'foo': b'\x80\x01\x02', \
 u'bar': [1, 2, 3, {u'a': [1, 2, 3, {}]}]}, -1, 2.12345]
>>>
```

Streaming serialization with file-like objects:
``` python
>>> f = open('test.bin', 'wb')
>>> umsgpack.pack({u"compact": True, u"schema": 0}, f)
>>> umsgpack.pack([1,2,3], f)
>>> f.close()
>>>
>>> f = open('test.bin', 'rb')
>>> umsgpack.unpack(f)
{u'compact': True, u'schema': 0}
>>> umsgpack.unpack(f)
[1, 2, 3]
>>> f.close()
>>>
```

Serializing and deserializing a raw Ext type:
``` python
>>> # Create an Ext object with type 0x05 and data b"\x01\x02\x03"
... foo = umsgpack.Ext(0x05, b"\x01\x02\x03")
>>> umsgpack.packb({u"stuff": foo, u"awesome": True})
b'\x82\xa5stuff\xc7\x03\x05\x01\x02\x03\xa7awesome\xc3'
>>>
>>> bar = umsgpack.unpackb(_)
>>> print(bar['stuff'])
Ext Object (Type: 0x05, Data: 0x01 0x02 0x03)
>>> bar['stuff'].type
5
>>> bar['stuff'].data
b'\x01\x02\x03'
>>>
```

Serializing and deserializing application-defined types with Ext handlers:
``` python
>>> umsgpack.packb([complex(1,2), datetime.datetime.now()],
...  ext_handlers = {
...   complex: lambda obj: umsgpack.Ext(0x30, struct.pack("ff", obj.real, obj.imag)),
...   datetime.datetime: lambda obj: umsgpack.Ext(0x40, obj.strftime("%Y%m%dT%H:%M:%S.%f").encode()),
...  })
b'\x92\xd70\x00\x00\x80?\x00\x00\x00@\xc7\x18@20161017T00:12:53.719377'
>>> umsgpack.unpackb(_,
...  ext_handlers = {
...   0x30: lambda ext: complex(*struct.unpack("ff", ext.data)),
...   0x40: lambda ext: datetime.datetime.strptime(ext.data.decode(), "%Y%m%dT%H:%M:%S.%f"),
...  })
[(1+2j), datetime.datetime(2016, 10, 17, 0, 12, 53, 719377)]
>>>
```

Python standard library style names `dump`, `dumps`, `load`, `loads` are also available:
``` python
>>> umsgpack.dumps({u"compact": True, u"schema": 0})
b'\x82\xa7compact\xc3\xa6schema\x00'
>>> umsgpack.loads(_)
{u'compact': True, u'schema': 0}
>>>
>>> f = open('test.bin', 'wb')
>>> umsgpack.dump({u"compact": True, u"schema": 0}, f)
>>> f.close()
>>>
>>> f = open('test.bin', 'rb')
>>> umsgpack.load(f)
{u'compact': True, u'schema': 0}
>>>
```

## Ext Handlers

The packing functions accept an optional `ext_handlers` dictionary that maps
custom types to callables that pack the type into an Ext object. The callable
should accept the custom type object as an argument and return a packed
`umsgpack.Ext` object.

Example for packing `set`, `complex`, and `datetime.datetime` types into Ext
objects with type codes 0x20, 0x30, and 0x40, respectively:

``` python
>>> umsgpack.packb([1, True, {"foo", 2}, complex(3, 4), datetime.datetime.now()],
...  ext_handlers = {
...   set: lambda obj: umsgpack.Ext(0x20, umsgpack.packb(list(obj))),
...   complex: lambda obj: umsgpack.Ext(0x30, struct.pack("ff", obj.real, obj.imag)),
...   datetime.datetime: lambda obj: umsgpack.Ext(0x40, obj.strftime("%Y%m%dT%H:%M:%S.%f").encode()),
...  })
b'\x95\x01\xc3\xc7\x06 \x92\xa3foo\x02\xd70\x00\x00@@\x00\x00\x80@\xc7\x18@20161015T02:28:35.666425'
>>>
```

Similarly, the unpacking functions accept an optional `ext_handlers` dictionary
that maps Ext type codes to callables that unpack the Ext into a custom object.
The callable should accept a `umsgpack.Ext` object as an argument and return an
unpacked custom type object.

Example for unpacking Ext objects with type codes 0x20, 0x30, and 0x40, into
`set`, `complex`, and `datetime.datetime` typed objects, respectively:

``` python
>>> umsgpack.unpackb(b'\x95\x01\xc3\xc7\x06 \x92\xa3foo\x02\xd70\x00\x00@@\x00\x00\x80@' \
...                  b'\xc7\x18@20161015T02:28:35.666425',
...  ext_handlers = {
...   0x20: lambda ext: set(umsgpack.unpackb(ext.data)),
...   0x30: lambda ext: complex(*struct.unpack("ff", ext.data)),
...   0x40: lambda ext: datetime.datetime.strptime(ext.data.decode(), "%Y%m%dT%H:%M:%S.%f"),
...  })
[1, True, {'foo', 2}, (3+4j), datetime.datetime(2016, 10, 15, 2, 28, 35, 666425)]
>>>
```

Example for packing and unpacking a custom class:

``` python
class Point(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "Point({}, {}, {})".format(self.x, self.y, self.z)

    def pack(self):
        return struct.pack(">iii", self.x, self.y, self.z)

    @staticmethod
    def unpack(data):
        return Point(*struct.unpack(">iii", data))

# Pack
obj = Point(1,2,3)
data = umsgpack.packb(obj, ext_handlers = {Point: lambda obj: umsgpack.Ext(0x10, obj.pack())})

# Unpack
obj = umsgpack.unpackb(data, ext_handlers = {0x10: lambda ext: Point.unpack(ext.data)})
print(obj) # -> Point(1, 2, 3)
```

## Streaming Serialization and Deserialization

The streaming `pack()`/`dump()` and `unpack()`/`load()` functions allow packing and unpacking objects directly to and from a stream, respectively. Streaming may be necessary when unpacking serialized bytes whose size is unknown in advance, or it may be more convenient and efficient when working directly with stream objects (e.g. files or stream sockets).

`pack(obj, fp)` / `dump(obj, fp)` serialize Python object `obj` to a `.write()` supporting file-like object `fp`.

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

`unpack(fp)` / `load(fp)` deserialize a Python object from a `.read()` supporting file-like object `fp`.

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

## Options

### Ordered Dictionaries

The unpacking functions provide a `use_ordered_dict` option to unpack MessagePack maps into the `collections.OrderedDict` type, rather than the unordered `dict` type, to preserve the order of deserialized MessagePack maps.

``` python
>>> umsgpack.unpackb(b'\x82\xa7compact\xc3\xa6schema\x00')
{'compact': True, 'schema': 0}
>>> umsgpack.unpackb(b'\x82\xa7compact\xc3\xa6schema\x00', use_ordered_dict=True)
OrderedDict([('compact', True), ('schema', 0)])
>>>
```

### Invalid UTF-8 Strings

The unpacking functions provide an `allow_invalid_utf8` option to unpack MessagePack strings with invalid UTF-8 into the `umsgpack.InvalidString` type, instead of throwing an exception. The `umsgpack.InvalidString` type is a subclass of `bytes`, and can be used like any other `bytes` object.

``` python
>>> # Attempt to unpack invalid UTF-8 string
... umsgpack.unpackb(b'\xa4\x80\x01\x02\x03')
...
umsgpack.InvalidStringException: unpacked string is invalid utf-8
>>> umsgpack.unpackb(b'\xa4\x80\x01\x02\x03', allow_invalid_utf8=True)
b'\x80\x01\x02\x03'
>>>
```

### Compatibility Mode

The compatibility mode supports the "raw" bytes MessagePack type from the [old specification](https://github.com/msgpack/msgpack/blob/master/spec-old.md). When the module-wide `compatibility` option is enabled, both unicode strings and bytes will be serialized into the "raw" MessagePack type, and the "raw" MessagePack type will be deserialized into bytes.

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

### Packing Exceptions

If an error occurs during packing, umsgpack will raise an exception derived from `umsgpack.PackException`. All possible packing exceptions are described below.

* `UnsupportedTypeException`: Object type not supported for packing.

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

### Unpacking Exceptions

If a non-byte-string argument is passed to `umsgpack.unpackb()`, it will raise a `TypeError` exception. If an error occurs during unpacking, umsgpack will raise an exception derived from `umsgpack.UnpackException`. All possible unpacking exceptions are described below.

* `TypeError`: Packed data is not type `str` (Python 2), or not type `bytes` (Python 3).

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

* `InsufficientDataException`: Insufficient data to unpack the serialized object.

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
* `InvalidStringException`: Invalid UTF-8 string encountered during unpacking.

	String bytes are strictly decoded with UTF-8. This exception is thrown if
	UTF-8 decoding of string bytes fails. Use the `allow_invalid_utf8` option
	to unpack invalid MessagePack strings into byte strings.

    ``` python
    # Attempt to unpack invalid UTF-8 string
    >>> umsgpack.unpackb(b"\xa2\x80\x81")
    ...
    umsgpack.InvalidStringException: unpacked string is invalid utf-8
    >>>
    ```

* `ReservedCodeException`: Reserved code encountered during unpacking.

    ``` python
    # Attempt to unpack reserved code 0xc1
    >>> umsgpack.unpackb(b"\xc1")
    ...
    umsgpack.ReservedCodeException: reserved code encountered: 0xc1
    >>>
    ```

* `UnhashableKeyException`: Unhashable key encountered during map unpacking. The packed map cannot be unpacked into a Python dictionary.

    Python dictionaries only support keys that are instances of `collections.Hashable`, so while the map `{ { u'abc': True } : 5 }` has a MessagePack serialization, it cannot be unpacked into a valid Python dictionary.

    ``` python
    # Attempt to unpack { {} : False }
    >>> umsgpack.unpackb(b"\x82\x80\xc2")
    ...
    umsgpack.UnhashableKeyException: encountered unhashable key type: {}, <type 'dict'>
    >>>
    ```

* `DuplicateKeyException`: Duplicate key encountered during map unpacking.

    Python dictionaries do not support duplicate keys, but MessagePack maps may be serialized with duplicate keys.

    ``` python
    # Attempt to unpack { 1: True, 1: False }
    >>> umsgpack.unpackb(b"\x82\x01\xc3\x01\xc2")
    ...
    umsgpack.DuplicateKeyException: encountered duplicate key: 1, <type 'int'>
    >>>
    ```

## Behavior Notes

* Python 2
  * `unicode` type objects are packed into, and unpacked from, the msgpack `string` format
  * `str` type objects are packed into, and unpacked from, the msgpack `binary` format
* Python 3
  * `str` type objects are packed into, and unpacked from, the msgpack `string` format
  * `bytes` type objects are packed into, and unpacked from, the msgpack `binary` format
* The msgpack string format is strictly decoded with UTF-8 — an exception is thrown if the string bytes cannot be decoded into a valid UTF-8 string, unless the `allow_invalid_utf8` option is enabled
* The msgpack array format is unpacked into a Python list, unless it is the key of a map, in which case it is unpacked into a Python tuple
* Python tuples and lists are both packed into the msgpack array format
* Python float types are packed into the msgpack float32 or float64 format depending on the system's `sys.float_info`

## Testing

The included unit tests may be run with `test_umsgpack.py`, under your favorite interpreter.

``` text
$ python2 test_umsgpack.py
$ python3 test_umsgpack.py
$ pypy test_umsgpack.py
$ pypy3 test_umsgpack.py
```

Alternatively you can use `tox` or `detox` to test multiple Python versions at once.

``` text
$ pip install -U detox
$ detox
```

## License

u-msgpack-python is MIT licensed. See the included `LICENSE` file for more details.
