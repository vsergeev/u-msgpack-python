# u-msgpack-python v1.6

u-msgpack-python is a lightweight [MessagePack](http://msgpack.org/) serializer and deserializer module written in pure Python, compatible with both Python 2 and 3, as well CPython and PyPy implementations of Python. u-msgpack-python is fully compliant with the latest [MessagePack specification](https://github.com/msgpack/msgpack/blob/master/spec.md). In particular, it supports the new binary, UTF-8 string, and application ext types.

u-msgpack-python is currently distributed on PyPI: https://pypi.python.org/pypi/u-msgpack-python and as a single file: [umsgpack.py](https://raw.github.com/vsergeev/u-msgpack-python/master/umsgpack.py)

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
'\x82\xa7compact\xc3\xa6schema\x00'
>>> umsgpack.unpackb(_)
{u'compact': True, u'schema': 0}
>>> 
```

A more complicated example:
``` python
>>> umsgpack.packb( \
    [1, True, False, 0xffffffff, {u"foo": b"\x80\x01\x02", \
     u"bar": [1,2,3, {u"a": [1,2,3,{}]}]}, -1, 2.12345] )
'\x97\x01\xc3\xc2\xce\xff\xff\xff\xff\x82\xa3foo\xc4\x03\x80\x01
\x02\xa3bar\x94\x01\x02\x03\x81\xa1a\x94\x01\x02\x03\x80\xff\xcb
@\x00\xfc\xd3Z\x85\x87\x94'
>>> umsgpack.unpackb(_)
[1, True, False, 4294967295, {u'foo': '\x80\x01\x02', \
 u'bar': [1, 2, 3, {u'a': [1, 2, 3, {}]}]}, -1, 2.12345]
>>> 
```

The more complicated example in Python 3:
``` python
>>> umsgpack.packb( \
    [1, True, False, 0xffffffff, {u"foo": b"\x80\x01\x02", \
     u"bar": [1,2,3, {u"a": [1,2,3,{}]}]}, -1, 2.12345] )
b'\x97\x01\xc3\xc2\xce\xff\xff\xff\xff\x82\xa3foo\xc4\x03\x80\x01
\x02\xa3bar\x94\x01\x02\x03\x81\xa1a\x94\x01\x02\x03\x80\xff\xcb@
\x00\xfc\xd3Z\x85\x87\x94'
>>> umsgpack.unpackb(_)
[1, True, False, 4294967295, {'foo': b'\x80\x01\x02', \
 'bar': [1, 2, 3, {'a': [1, 2, 3, {}]}]}, -1, 2.12345]
>>> 
```

An example of encoding and decoding an application ext type:
``` python
# Create an Ext object with type 0x05 and data b"\x01\x02\x03"
>>> foo = umsgpack.Ext(0x05, b"\x01\x02\x03")
>>> umsgpack.packb({u"special stuff": foo, u"awesome": True})
b'\x82\xadspecial stuff\xc7\x03\x05\x01\x02\x03\xa7awesome\xc3'
>>> bar = umsgpack.unpackb(_)
>>> print(bar["special stuff"])
Ext Object (Type: 0x05, Data: 01 02 03)
>>> bar["special stuff"].type
5
>>> bar["special stuff"].data
b'\x01\x02\x03'
>>> 
```

Python standard library style `loads` and `dumps` functions are also available as aliases:

``` python
>>> import umsgpack
>>> umsgpack.dumps({u"compact": True, u"schema": 0})
'\x82\xa7compact\xc3\xa6schema\x00'
>>> umsgpack.loads(_)
{u'compact': True, u'schema': 0}
>>> 
```

## Compatibility Mode

u-msgpack-python offers a compatibility mode for the [old specification](https://github.com/msgpack/msgpack/blob/master/spec-old.md) to handle the old "raw" bytes msgpack type. When the compatibility mode is enabled, u-msgpack-python will serialize both unicode strings and bytes into the old "raw" msgpack type, and deserialize the "raw" msgpack type into bytes. To enable compatibility mode, simply set the `compatibility` boolean of the umsgpack module to `True`.

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

If an error occurs during packing, `umsgpack.packb()` will raise an exception derived from `umsgpack.PackException`. All possible packing exceptions are described below.

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

If a non-byte-string argument is passed to `umsgpack.unpackb()`, it will raise a `TypeError` exception. If an error occurs during unpacking, `umsgpack.unpackb()` will raise an exception derived from `umsgpack.UnpackException`. All possible unpacking exceptions are described below.

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

* `InsufficientDataException`: Insufficient data to unpack the encoded object.

    ``` python
    # Attempt to unpack a cut-off encoded 32-bit unsigned int
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

    String bytes are strictly decoded with UTF-8. This exception is thrown if UTF-8 decoding of string bytes fails.

    ``` python
    # Attempt to unpack the string "\x80\x81"
    >>> umsgpack.unpackb(b"\xa2\x80\x81")
    ...
    umsgpack.InvalidStringException: unpacked string is not utf-8
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

* `UnhashableKeyException`: Unhashable key encountered during map unpacking. The serialized map cannot be deserialized into a Python dictionary.

    Python dictionaries only support keys that are instances of `collections.Hashable`, so while the map `{ { u'abc': True } : 5 }` has a msgpack encoding, it cannot be unpacked into a valid Python dictionary.

    ``` python
    # Attempt to unpack { {} : False }
    >>> umsgpack.unpackb(b"\x82\x80\xc2")
    ...
    umsgpack.UnhashableKeyException: encountered unhashable key type: <type 'dict'>
    >>> 
    ```

* `DuplicateKeyException`: Duplicate key encountered during map unpacking.

    Python dictionaries do not support duplicate keys, but msgpack maps may be encoded with duplicate keys.

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
* The msgpack string format is strictly decoded with UTF-8. An exception is thrown if the string bytes cannot be decoded into a valid UTF-8 string.
* The msgpack array format is unpacked into a Python list, not tuple
* Python float types are packed into the msgpack float32 or float64 format depending on the system's `sys.float_info`

## Testing

u-msgpack-python's included unit tests may be run with `test_umsgpack.py`, under your favorite interpreter.

``` text
$ python2 test_umsgpack.py
$ python3 test_umsgpack.py
$ pypy test_umsgpack.py
```

## License

u-msgpack-python is MIT licensed. See the included `LICENSE` file for more details.

