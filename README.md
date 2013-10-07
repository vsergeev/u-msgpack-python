# u-msgpack-python v1.0

u-msgpack-python is a lightweight [MessagePack](https://github.com/msgpack/msgpack) serializer and deserializer module, compatible with both Python 2 and Python 3. u-msgpack-python is fully compliant with the latest [MessagePack specification](https://github.com/msgpack/msgpack/blob/master/spec.md), as of 09/29/2013. In particular, it supports the new binary, UTF-8 string, and application ext types.

u-msgpack-python is written in pure Python and is currently distributed as a single file: [umsgpack.py](umsgpack.py)

Future releases may also provide a Python .egg package.

## Examples

Basic Example:
```
>>> import umsgpack
>>> umsgpack.packb({u"compact": True, u"schema": 0})
'\x82\xa7compact\xc3\xa6schema\x00'
>>> umsgpack.unpackb(_)
{u'compact': True, u'schema': 0}
>>> 
```
A more complicated example:
```
>>> umsgpack.packb([1, True, False, 0xffffffff, {u"foo": b"\x80\x01\x02", u"bar": [1,2,3, {u"a": [1,2,3,{}]}]}, -1, 2.12345])
'\x97\x01\xc3\xc2\xce\xff\xff\xff\xff\x82\xa3foo\xc4\x03\x80\x01\x02\xa3bar\x94\x01\x02\x03\x81\xa1a\x94\x01\x02\x03\x80\xff\xcb@\x00\xfc\xd3Z\x85\x87\x94'
>>> umsgpack.unpackb(_)
[1, True, False, 4294967295, {u'foo': '\x80\x01\x02', u'bar': [1, 2, 3, {u'a': [1, 2, 3, {}]}]}, -1, 2.12345]
>>> 
```

The more complicated example in Python 3:
```
>>> umsgpack.packb([1, True, False, 0xffffffff, {u"foo": b"\x80\x01\x02", u"bar": [1,2,3, {u"a": [1,2,3,{}]}]}, -1, 2.12345])
b'\x97\x01\xc3\xc2\xce\xff\xff\xff\xff\x82\xa3foo\xc4\x03\x80\x01\x02\xa3bar\x94\x01\x02\x03\x81\xa1a\x94\x01\x02\x03\x80\xff\xcb@\x00\xfc\xd3Z\x85\x87\x94'
>>> umsgpack.unpackb(_)
[1, True, False, 4294967295, {'foo': b'\x80\x01\x02', 'bar': [1, 2, 3, {'a': [1, 2, 3, {}]}]}, -1, 2.12345]
>>> 
```

An example of encoding and decoding an application ext type:
```
>>> # Create foo, an Ext object with type 0x05 and data b"\x01\x02\x03"
... foo = umsgpack.Ext(0x05, b"\x01\x02\x03")
>>> umsgpack.packb({u"special stuff": foo, u"awesome": True})
b'\x82\xadspecial stuff\xc7\x03\x05\x01\x02\x03\xa7awesome\xc3'
>>> bar = umsgpack.unpackb(_)

>>> print(bar["special stuff"])
Ext Object
   Type: 05
   Data: 01 02 03 
>>> bar["special stuff"].type
5
>>> bar["special stuff"].data
b'\x01\x02\x03'
>>> 
```

## Exceptions

### Packing Exceptions

If an error occurs during packing, `umsgpack.packb()` will raise an exception derived from `umsgpack.PackException`. All possible packing exceptions are described below.

* `UnsupportedTypeException`: Object type not supported for packing.

    ```
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

    ```
    >>> # Attempt to unpack non-str type data in Python 2
    ... umsgpack.unpackb(u"no good")
    ...
    TypeError: expected packed data as type 'str'
    >>> 

    >>> # Attempt to unpack non-bytes type data in Python 3
    ... umsgpack.unpackb("no good")
    ...
    TypeError: expected packed data as type 'bytes'
    >>> 
    ```

* `InsufficientDataException`: Insufficient data to unpack encoded object.

    ```
    >>> # Attempt to unpack a cut-off encoded 32-bit unsigned int
    ... umsgpack.unpackb(b"\xce\xff\xff\xff")
    ...
    umsgpack.InsufficientDataException
    >>> 

    >>> # Attempt to unpack an array of length 2 missing the second item
    ... umsgpack.unpackb(b"\x92\xc2")
    ...
    umsgpack.InsufficientDataException
    >>> 

    ```
* `InvalidStringException`: Invalid string (not UTF-8) encountered.

    String bytes are strictly decoded with UTF-8. This exception is thrown if UTF-8 decoding of string bytes fails.

    ```
    >>> # Attempt to unpack the string "\x80\x81"
    ... umsgpack.unpackb(b"\xa2\x80\x81")
    ...
    umsgpack.InvalidStringException: unpacked string is not utf-8
    >>> 
    ```

* `ReservedCodeException`: msgpack reserved code encountered.

    ```
    >>> # Attempt to unpack reserved code 0xc1
    ... umsgpack.unpackb(b"\xc1")
    ...
    umsgpack.ReservedCodeException: reserved code encountered: 0xc1
    >>> 
    ```

* `KeyNotPrimitiveException`: Unhashable key encountered during map unpacking.

    Python dictionaries only support keys that are instances of `collections.Hashable`, so while the map `{ { u'abc': True } : 5 }` has a msgpack encoding, it cannot be unpacked into a valid Python dictionary.

    ```
    >>> # Attempt to unpack { {} : False }
    ... umsgpack.unpackb(b"\x82\x80\xc2")
    ...
    umsgpack.KeyNotPrimitiveException: encountered non-primitive key type: <type 'dict'>
    >>> 
    ```

* `KeyDuplicateException`: Duplicate key encountered during map unpacking.

    Python dictionaries do not support duplicate keys, but msgpack maps may be encoded with duplicate keys.

    ```
    >>> # Attempt to unpack { 1: True, 1: False }
    ... umsgpack.unpackb(b"\x82\x01\xc3\x01\xc2")
    ...
    umsgpack.KeyDuplicateException: encountered duplicate key: 1, <type 'int'>
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

u-msgpack-python's included unit tests may be run with [pytest](http://pytest.org). Simply invoke `py.test` or `py.test2` to test in either Python 3 or Python 2.

## License

u-msgpack-python is MIT licensed. See the included `LICENSE` file for more details.

