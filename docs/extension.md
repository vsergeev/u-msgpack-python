# Extension Types

u-msgpack-python supports two mechanisms for packing and unpacking MessagePack
Ext types: the `ext_handlers` keyword option, and the `ext_serializable()`
decorator.

## Ext Handlers

The packing functions accept an optional `ext_handlers` dictionary that maps
custom types to callables that pack the type into an Ext object. The callable
should accept the custom type object as an argument and return a packed
`umsgpack.Ext` object.

Example for packing `set`, `complex`, and `decimal.Decimal` types into Ext
objects with type codes 0x20, 0x30, and 0x40, respectively:

``` python
>>> umsgpack.packb([1, True, {"foo", 2}, complex(3, 4), decimal.Decimal("0.31")],
...  ext_handlers = {
...   set: lambda obj: umsgpack.Ext(0x20, umsgpack.packb(list(obj))),
...   complex: lambda obj: umsgpack.Ext(0x30, struct.pack("ff", obj.real, obj.imag)),
...   decimal.Decimal: lambda obj: umsgpack.Ext(0x40, str(obj).encode()),
... })
b'\x95\x01\xc3\xc7\x06 \x92\xa3foo\x02\xd70\x00\x00@@\x00\x00\x80@\xd6@0.31'
>>> 
```
Similarly, the unpacking functions accept an optional `ext_handlers` dictionary
that maps Ext type codes to callables that unpack the Ext into a custom object.
The callable should accept a `umsgpack.Ext` object as an argument and return an
unpacked custom type object.

Example for unpacking Ext objects with type codes 0x20, 0x30, and 0x40, into
`set`, `complex`, and `decimal.Decimal` typed objects, respectively:

``` python
>>> umsgpack.unpackb(b'\x95\x01\xc3\xc7\x06 \x92\xa3foo\x02\xd70\x00\x00@@\x00\x00\x80@\xd6@0.31',
...  ext_handlers = {
...   0x20: lambda ext: set(umsgpack.unpackb(ext.data)),
...   0x30: lambda ext: complex(*struct.unpack("ff", ext.data)),
...   0x40: lambda ext: decimal.Decimal(ext.data.decode()),
... })
[1, True, {'foo', 2}, (3+4j), Decimal('0.31')]
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

## Ext Serializable

The `ext_serializable()` decorator registers application classes for automatic
packing and unpacking with the specified Ext type.  The decorator accepts the
Ext type code as an argument. The application class should implement a
`packb()` method that returns serialized bytes, and an `unpackb()` class method
or static method that accepts serialized bytes and returns an instance of the
application class.

Example for registering, packing, and unpacking a custom class with Ext type
code 0x10:

``` python
@umsgpack.ext_serializable(0x10)
class Point(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "Point({}, {}, {})".format(self.x, self.y, self.z)

    def packb(self):
        return struct.pack(">iii", self.x, self.y, self.z)

    @staticmethod
    def unpackb(data):
        return Point(*struct.unpack(">iii", data))

# Pack
obj = Point(1,2,3)
data = umsgpack.packb(obj)

# Unpack
obj = umsgpack.unpackb(data)
print(obj) # -> Point(1, 2, 3)
```
