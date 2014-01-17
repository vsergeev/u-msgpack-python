# u-msgpack-python v1.6

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
>>> # Create an Ext object with type 0x05 and data b"\x01\x02\x03"
... foo = umsgpack.Ext(0x05, b"\x01\x02\x03")
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

## More Information

See the [project page](https://github.com/vsergeev/u-msgpack-python) for more information on old specification compatibility mode, exceptions, behavior, and testing.

## License

u-msgpack-python is MIT licensed. See the included `LICENSE` file for more details.

