# u-msgpack-python [![Build Status](https://travis-ci.org/vsergeev/u-msgpack-python.svg?branch=master)](https://travis-ci.org/vsergeev/u-msgpack-python) [![GitHub release](https://img.shields.io/github/release/vsergeev/u-msgpack-python.svg?maxAge=7200)](https://github.com/vsergeev/u-msgpack-python) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/vsergeev/u-msgpack-python/blob/master/LICENSE)

u-msgpack-python is a lightweight [MessagePack](http://msgpack.org/) serializer and deserializer module written in pure Python, compatible with both Python 2 and 3, as well CPython and PyPy implementations of Python. u-msgpack-python is fully compliant with the latest [MessagePack specification](https://github.com/msgpack/msgpack/blob/master/spec.md).

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
b'\x82\xa7compact\xc3\xa6schema\x00'
>>> umsgpack.unpackb(_)
{u'compact': True, u'schema': 0}
>>> 
```

A more complicated example:
``` python
>>> umsgpack.packb(
...     [1, True, False, 0xffffffff, {u"foo": b"\x80\x01\x02",
...      u"bar": [1,2,3, {u"a": [1,2,3,{}]}]}, -1, 2.12345] )
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
>>> umsgpack.packb([complex(1,2), decimal.Decimal("0.31")],
...  ext_handlers = {
...   complex: lambda obj:
...     umsgpack.Ext(0x30, struct.pack("ff", obj.real, obj.imag)),
...   decimal.Decimal: lambda obj:
...     umsgpack.Ext(0x40, str(obj).encode()),
... })
b'\x92\xd70\x00\x00\x80?\x00\x00\x00@\xd6@0.31'
>>> umsgpack.unpackb(_,
...  ext_handlers = {
...   0x30: lambda ext:
...     complex(*struct.unpack("ff", ext.data)),
...   0x40: lambda ext:
...     decimal.Decimal(ext.data.decode()),
... })
[(1+2j), Decimal('0.31')]
>>> 
```

Python standard library style names `dump`, `dumps`, `load`, `loads` are also
available:
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

## More Information

See the [project page](https://github.com/vsergeev/u-msgpack-python) for more information on options, exceptions, behavior, and testing.

## License

u-msgpack-python is MIT licensed. See the included `LICENSE` file for more details.
