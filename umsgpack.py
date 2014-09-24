# u-msgpack-python v1.8 - vsergeev at gmail
# https://github.com/vsergeev/u-msgpack-python
#
# u-msgpack-python is a lightweight MessagePack serializer and deserializer
# module, compatible with both Python 2 and 3, as well CPython and PyPy
# implementations of Python. u-msgpack-python is fully compliant with the
# latest MessagePack specification.com/msgpack/msgpack/blob/master/spec.md). In
# particular, it supports the new binary, UTF-8 string, and application ext
# types.
#
# MIT License
#
# Copyright (c) 2013-2014 Ivan A. Sergeev
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
"""
u-msgpack-python v1.8 - vsergeev at gmail
https://github.com/vsergeev/u-msgpack-python

u-msgpack-python is a lightweight MessagePack serializer and deserializer
module, compatible with both Python 2 and 3, as well CPython and PyPy
implementations of Python. u-msgpack-python is fully compliant with the
latest MessagePack specification.com/msgpack/msgpack/blob/master/spec.md). In
particular, it supports the new binary, UTF-8 string, and application ext
types.

License: MIT
"""

version = (1,8)
"Module version tuple"

import struct
import collections
import sys

################################################################################
### Ext Class
################################################################################

# Extension type for application-defined types and data
class Ext:
    """
    The Ext class facilitates creating a serializable extension object to store
    an application-defined type and data byte array.
    """

    def __init__(self, type, data):
        """
        Construct a new Ext object.

        Args:
            type: application-defined type integer from 0 to 127
            data: application-defined data byte array

        Raises:
            TypeError:
                Specified ext type is outside of 0 to 127 range.

        Example:
        >>> foo = umsgpack.Ext(0x05, b"\x01\x02\x03")
        >>> umsgpack.packb({u"special stuff": foo, u"awesome": True})
        '\x82\xa7awesome\xc3\xadspecial stuff\xc7\x03\x05\x01\x02\x03'
        >>> bar = umsgpack.unpackb(_)
        >>> print(bar["special stuff"])
        Ext Object (Type: 0x05, Data: 01 02 03)
        >>>
        """
        # Application ext type should be 0 <= type <= 127
        if not isinstance(type, int) or not (type >= 0 and type <= 127):
            raise TypeError("ext type out of range")
        # Check data is type bytes
        elif sys.version_info[0] == 3 and not isinstance(data, bytes):
            raise TypeError("ext data is not type \'bytes\'")
        elif sys.version_info[0] == 2 and not isinstance(data, str):
            raise TypeError("ext data is not type \'str\'")
        self.type = type
        self.data = data

    def __eq__(self, other):
        """
        Compare this Ext object with another for equality.
        """
        return (isinstance(other, self.__class__) and
                self.type == other.type and
                self.data == other.data)

    def __ne__(self, other):
        """
        Compare this Ext object with another for inequality.
        """
        return not self.__eq__(other)

    def __str__(self):
        """
        String representation of this Ext object.
        """
        s = "Ext Object (Type: 0x%02x, Data: " % self.type
        for i in range(min(len(self.data), 8)):
            if i > 0:
                s += " "
            if isinstance(self.data[i], int):
                s += "%02x" % (self.data[i])
            else:
                s += "%02x" % ord(self.data[i])
        if len(self.data) > 8:
            s += " ..."
        s += ")"
        return s

################################################################################
### Exceptions
################################################################################

# Base Exception classes
class PackException(Exception):
    "Base class for exceptions encountered during packing."
    pass
class UnpackException(Exception):
    "Base class for exceptions encountered during unpacking."
    pass

# Packing error
class UnsupportedTypeException(PackException):
    "Object type not supported for packing."
    pass

# Unpacking error
class InsufficientDataException(UnpackException):
    "Insufficient data to unpack the encoded object."
    pass
class InvalidStringException(UnpackException):
    "Invalid UTF-8 string encountered during unpacking."
    pass
class ReservedCodeException(UnpackException):
    "Reserved code encountered during unpacking."
    pass
class UnhashableKeyException(UnpackException):
    """
    Unhashable key encountered during map unpacking.
    The serialized map cannot be deserialized into a Python dictionary.
    """
    pass
class DuplicateKeyException(UnpackException):
    "Duplicate key encountered during map unpacking."
    pass

# Backwards compatibility
KeyNotPrimitiveException = UnhashableKeyException
KeyDuplicateException = DuplicateKeyException

################################################################################
### Exported Functions and Globals
################################################################################

# Exported functions and variables set in __init()
packb = None
unpackb = None
dumps = None
loads = None

compatibility = False
"""
Compatibility mode boolean.

When compatibility mode is enabled, u-msgpack-python will serialize both
unicode strings and bytes into the old "raw" msgpack type, and deserialize the
"raw" msgpack type into bytes. This provides backwards compatibility with the
old MessagePack specification.

Example:
>>> umsgpack.compatibility = True
>>>
>>> umsgpack.packb([u"some string", b"some bytes"])
b'\x92\xabsome string\xaasome bytes'
>>> umsgpack.unpackb(_)
[b'some string', b'some bytes']
>>>
"""

################################################################################
### Packing
################################################################################

# You may notice struct.pack("B", x) instead of the simpler chr(x) in the code
# below. This is to allow for seamless Python 2 and 3 compatibility, as chr(x)
# has a str return type instead of bytes in Python 3, and struct.pack(...) has
# the right return type in both versions.

def _pack_integer(x, write_fn):
    if x < 0:
        if x >= -32:
            write_fn(struct.pack("b", x))
        elif x >= -2**(8-1):
            write_fn(b"\xd0" + struct.pack("b", x))
        elif x >= -2**(16-1):
            write_fn(b"\xd1" + struct.pack(">h", x))
        elif x >= -2**(32-1):
            write_fn(b"\xd2" + struct.pack(">i", x))
        elif x >= -2**(64-1):
            write_fn(b"\xd3" + struct.pack(">q", x))
        else:
            raise UnsupportedTypeException("huge signed int")
    else:
        if x <= 127:
            write_fn(struct.pack("B", x))
        elif x <= 2**8-1:
            write_fn(b"\xcc" + struct.pack("B", x))
        elif x <= 2**16-1:
            write_fn(b"\xcd" + struct.pack(">H", x))
        elif x <= 2**32-1:
            write_fn(b"\xce" + struct.pack(">I", x))
        elif x <= 2**64-1:
            write_fn(b"\xcf" + struct.pack(">Q", x))
        else:
            raise UnsupportedTypeException("huge unsigned int")

def _pack_nil(x, write_fn):
    write_fn(b"\xc0")

def _pack_boolean(x, write_fn):
    write_fn(b"\xc3" if x else b"\xc2")

def _pack_float(x, write_fn):
    if _float_size == 64:
        write_fn(b"\xcb" + struct.pack(">d", x))
    else:
        write_fn(b"\xca" + struct.pack(">f", x))

def _pack_string(x, write_fn):
    x = x.encode('utf-8')
    if len(x) <= 31:
        write_fn(struct.pack("B", 0xa0 | len(x)) + x)
    elif len(x) <= 2**8-1:
        write_fn(b"\xd9" + struct.pack("B", len(x)) + x)
    elif len(x) <= 2**16-1:
        write_fn(b"\xda" + struct.pack(">H", len(x)) + x)
    elif len(x) <= 2**32-1:
        write_fn(b"\xdb" + struct.pack(">I", len(x)) + x)
    else:
        raise UnsupportedTypeException("huge string")

def _pack_binary(x, write_fn):
    if len(x) <= 2**8-1:
        write_fn(b"\xc4" + struct.pack("B", len(x)) + x)
    elif len(x) <= 2**16-1:
        write_fn(b"\xc5" + struct.pack(">H", len(x)) + x)
    elif len(x) <= 2**32-1:
        write_fn(b"\xc6" + struct.pack(">I", len(x)) + x)
    else:
        raise UnsupportedTypeException("huge binary string")

def _pack_oldspec_raw(x, write_fn):
    if len(x) <= 31:
        write_fn(struct.pack("B", 0xa0 | len(x)) + x)
    elif len(x) <= 2**16-1:
        write_fn(b"\xda" + struct.pack(">H", len(x)) + x)
    elif len(x) <= 2**32-1:
        write_fn(b"\xdb" + struct.pack(">I", len(x)) + x)
    else:
        raise UnsupportedTypeException("huge raw string")

def _pack_ext(x, write_fn):
    if len(x.data) == 1:
        write_fn(b"\xd4" + struct.pack("B", x.type & 0xff) + x.data)
    elif len(x.data) == 2:
        write_fn(b"\xd5" + struct.pack("B", x.type & 0xff) + x.data)
    elif len(x.data) == 4:
        write_fn(b"\xd6" + struct.pack("B", x.type & 0xff) + x.data)
    elif len(x.data) == 8:
        write_fn(b"\xd7" + struct.pack("B", x.type & 0xff) + x.data)
    elif len(x.data) == 16:
        write_fn(b"\xd8" + struct.pack("B", x.type & 0xff) + x.data)
    elif len(x.data) <= 2**8-1:
        write_fn(b"\xc7" + struct.pack("BB", len(x.data), x.type & 0xff) + x.data)
    elif len(x.data) <= 2**16-1:
        write_fn(b"\xc8" + struct.pack(">HB", len(x.data), x.type & 0xff) + x.data)
    elif len(x.data) <= 2**32-1:
        write_fn(b"\xc9" + struct.pack(">IB", len(x.data), x.type & 0xff) + x.data)
    else:
        raise UnsupportedTypeException("huge ext data")

def _pack_array(x, write_fn):
    if len(x) <= 15:
        write_fn(struct.pack("B", 0x90 | len(x)))
    elif len(x) <= 2**16-1:
        write_fn(b"\xdc" + struct.pack(">H", len(x)))
    elif len(x) <= 2**32-1:
        write_fn(b"\xdd" + struct.pack(">I", len(x)))
    else:
        raise UnsupportedTypeException("huge array")

    for e in x:
        _pack(e, write_fn)

def _pack_map(x, write_fn):
    if len(x) <= 15:
        write_fn(struct.pack("B", 0x80 | len(x)))
    elif len(x) <= 2**16-1:
        write_fn(b"\xde" + struct.pack(">H", len(x)))
    elif len(x) <= 2**32-1:
        write_fn(b"\xdf" + struct.pack(">I", len(x)))
    else:
        raise UnsupportedTypeException("huge array")

    for k,v in x.items():
        _pack(k, write_fn)
        _pack(v, write_fn)

# Pack for Python 2, with 'unicode' type, 'str' type, and 'long' type
def _pack2(x, write_fn):
    global compatibility

    if x is None:
        _pack_nil(x, write_fn)
    elif isinstance(x, bool):
        _pack_boolean(x, write_fn)
    elif isinstance(x, int) or isinstance(x, long):
        _pack_integer(x, write_fn)
    elif isinstance(x, float):
        _pack_float(x, write_fn)
    elif compatibility and isinstance(x, unicode):
        _pack_oldspec_raw(bytes(x), write_fn)
    elif compatibility and isinstance(x, bytes):
        _pack_oldspec_raw(x, write_fn)
    elif isinstance(x, unicode):
        _pack_string(x, write_fn)
    elif isinstance(x, str):
        _pack_binary(x, write_fn)
    elif isinstance(x, list) or isinstance(x, tuple):
        _pack_array(x, write_fn)
    elif isinstance(x, dict):
        _pack_map(x, write_fn)
    elif isinstance(x, Ext):
        _pack_ext(x, write_fn)
    else:
        raise UnsupportedTypeException("unsupported type: %s" % str(type(x)))

# Pack for Python 3, with unicode 'str' type, 'bytes' type, and no 'long' type
def _pack3(x, write_fn):
    global compatibility

    if x is None:
        _pack_nil(x, write_fn)
    elif isinstance(x, bool):
        _pack_boolean(x, write_fn)
    elif isinstance(x, int):
        _pack_integer(x, write_fn)
    elif isinstance(x, float):
        _pack_float(x, write_fn)
    elif compatibility and isinstance(x, str):
        _pack_oldspec_raw(x.encode('utf-8'), write_fn)
    elif compatibility and isinstance(x, bytes):
        _pack_oldspec_raw(x, write_fn)
    elif isinstance(x, str):
        _pack_string(x, write_fn)
    elif isinstance(x, bytes):
        _pack_binary(x, write_fn)
    elif isinstance(x, list) or isinstance(x, tuple):
        _pack_array(x, write_fn)
    elif isinstance(x, dict):
        _pack_map(x, write_fn)
    elif isinstance(x, Ext):
        _pack_ext(x, write_fn)
    else:
        raise UnsupportedTypeException("unsupported type: %s" % str(type(x)))

def _packb2(x):
    """
    Serialize a Python object into MessagePack bytes.

    Args:
        x: Python object

    Returns:
        A 'str' containing the serialized bytes.

    Raises:
        UnsupportedType(PackException):
            Object type not supported for packing.

    Example:
    >>> umsgpack.packb({u"compact": True, u"schema": 0})
    '\x82\xa7compact\xc3\xa6schema\x00'
    >>>
    """
    l = []
    def write_fn(s):
        l.append(s)
    _pack2(x, write_fn)
    return "".join(l)

def _packb3(x):
    """
    Serialize a Python object into MessagePack bytes.

    Args:
        x: Python object

    Returns:
        A 'bytes' containing the serialized bytes.

    Raises:
        UnsupportedType(PackException):
            Object type not supported for packing.

    Example:
    >>> umsgpack.packb({u"compact": True, u"schema": 0})
    b'\x82\xa7compact\xc3\xa6schema\x00'
    >>>
    """
    l = []
    def write_fn(s):
        l.append(s)
    _pack3(x, write_fn)
    return b"".join(l)

################################################################################
### Unpacking
################################################################################

def _unpack_integer(code, read_fn):
    if (ord(code) & 0xe0) == 0xe0:
        return struct.unpack("b", code)[0]
    elif code == b'\xd0':
        return struct.unpack("b", read_fn(1))[0]
    elif code == b'\xd1':
        return struct.unpack(">h", read_fn(2))[0]
    elif code == b'\xd2':
        return struct.unpack(">i", read_fn(4))[0]
    elif code == b'\xd3':
        return struct.unpack(">q", read_fn(8))[0]
    elif (ord(code) & 0x80) == 0x00:
        return struct.unpack("B", code)[0]
    elif code == b'\xcc':
        return struct.unpack("B", read_fn(1))[0]
    elif code == b'\xcd':
        return struct.unpack(">H", read_fn(2))[0]
    elif code == b'\xce':
        return struct.unpack(">I", read_fn(4))[0]
    elif code == b'\xcf':
        return struct.unpack(">Q", read_fn(8))[0]
    raise Exception("logic error, not int: 0x%02x" % ord(code))

def _unpack_reserved(code, read_fn):
    if code == b'\xc1':
        raise ReservedCodeException("encountered reserved code: 0x%02x" % ord(code))
    raise Exception("logic error, not reserved code: 0x%02x" % ord(code))

def _unpack_nil(code, read_fn):
    if code == b'\xc0':
        return None
    raise Exception("logic error, not nil: 0x%02x" % ord(code))

def _unpack_boolean(code, read_fn):
    if code == b'\xc2':
        return False
    elif code == b'\xc3':
        return True
    raise Exception("logic error, not boolean: 0x%02x" % ord(code))

def _unpack_float(code, read_fn):
    if code == b'\xca':
        return struct.unpack(">f", read_fn(4))[0]
    elif code == b'\xcb':
        return struct.unpack(">d", read_fn(8))[0]
    raise Exception("logic error, not float: 0x%02x" % ord(code))

def _unpack_string(code, read_fn):
    if (ord(code) & 0xe0) == 0xa0:
        length = ord(code) & ~0xe0
    elif code == b'\xd9':
        length = struct.unpack("B", read_fn(1))[0]
    elif code == b'\xda':
        length = struct.unpack(">H", read_fn(2))[0]
    elif code == b'\xdb':
        length = struct.unpack(">I", read_fn(4))[0]
    else:
        raise Exception("logic error, not string: 0x%02x" % ord(code))

    # Always return raw bytes in compatibility mode
    global compatibility
    if compatibility:
        return read_fn(length)

    try:
        return bytes.decode(read_fn(length), 'utf-8')
    except UnicodeDecodeError:
        raise InvalidStringException("unpacked string is not utf-8")

def _unpack_binary(code, read_fn):
    if code == b'\xc4':
        length = struct.unpack("B", read_fn(1))[0]
    elif code == b'\xc5':
        length = struct.unpack(">H", read_fn(2))[0]
    elif code == b'\xc6':
        length = struct.unpack(">I", read_fn(4))[0]
    else:
        raise Exception("logic error, not binary: 0x%02x" % ord(code))

    return read_fn(length)

def _unpack_ext(code, read_fn):
    if code == b'\xd4':
        length = 1
    elif code == b'\xd5':
        length = 2
    elif code == b'\xd6':
        length = 4
    elif code == b'\xd7':
        length = 8
    elif code == b'\xd8':
        length = 16
    elif code == b'\xc7':
        length = struct.unpack("B", read_fn(1))[0]
    elif code == b'\xc8':
        length = struct.unpack(">H", read_fn(2))[0]
    elif code == b'\xc9':
        length = struct.unpack(">I", read_fn(4))[0]
    else:
        raise Exception("logic error, not ext: 0x%02x" % ord(code))

    return Ext(ord(read_fn(1)), read_fn(length))

def _unpack_array(code, read_fn):
    if (ord(code) & 0xf0) == 0x90:
        length = (ord(code) & ~0xf0)
    elif code == b'\xdc':
        length = struct.unpack(">H", read_fn(2))[0]
    elif code == b'\xdd':
        length = struct.unpack(">I", read_fn(4))[0]
    else:
        raise Exception("logic error, not array: 0x%02x" % ord(code))

    return [_unpackb(read_fn) for i in range(length)]

def _deep_list_to_tuple(x):
    if isinstance(x, list):
        return tuple([_deep_list_to_tuple(e) for e in x])
    return x

def _unpack_map(code, read_fn):
    if (ord(code) & 0xf0) == 0x80:
        length = (ord(code) & ~0xf0)
    elif code == b'\xde':
        length = struct.unpack(">H", read_fn(2))[0]
    elif code == b'\xdf':
        length = struct.unpack(">I", read_fn(4))[0]
    else:
        raise Exception("logic error, not map: 0x%02x" % ord(code))

    d = {}
    for i in range(length):
        # Unpack key
        k = _unpackb(read_fn)

        if isinstance(k, list):
            # Attempt to convert list into a hashable tuple
            k = _deep_list_to_tuple(k)
        elif not isinstance(k, collections.Hashable):
            raise UnhashableKeyException("encountered unhashable key: %s, %s" % (str(k), str(type(k))))
        elif k in d:
            raise DuplicateKeyException("encountered duplicate key: %s, %s" % (str(k), str(type(k))))

        # Unpack value
        v = _unpackb(read_fn)

        try:
            d[k] = v
        except TypeError:
            raise UnhashableKeyException("encountered unhashable key: %s" % str(k))
    return d

########################################

def _byte_reader(s):
    i = [0]
    def read_fn(n):
        if (i[0]+n > len(s)):
            raise InsufficientDataException()
        substring = s[i[0]:i[0]+n]
        i[0] += n
        return substring
    return read_fn

def _unpackb(read_fn):
    code = read_fn(1)
    return _unpack_dispatch_table[code](code, read_fn)

# For Python 2, expects a str object
def _unpackb2(s):
    """
    Deserialize MessagePack bytes into a Python object.

    Args:
        s: a 'str' containing the MessagePack serialized bytes.

    Returns:
        A deserialized Python object.

    Raises:
        TypeError:
            Packed data is not type 'str'.
        InsufficientDataException(UnpackException):
            Insufficient data to unpack the encoded object.
        InvalidStringException(UnpackException):
            Invalid UTF-8 string encountered during unpacking.
        ReservedCodeException(UnpackException):
            Reserved code encountered during unpacking.
        UnhashableKeyException(UnpackException):
            Unhashable key encountered during map unpacking.
            The serialized map cannot be deserialized into a Python dictionary.
        DuplicateKeyException(UnpackException):
            Duplicate key encountered during map unpacking.

    Example:
    >>> umsgpack.unpackb(b'\x82\xa7compact\xc3\xa6schema\x00')
    {u'compact': True, u'schema': 0}
    >>>
    """
    if not isinstance(s, str):
        raise TypeError("packed data is not type 'str'")
    read_fn = _byte_reader(s)
    return _unpackb(read_fn)

# For Python 3, expects a bytes object
def _unpackb3(s):
    """
    Deserialize MessagePack bytes into a Python object.

    Args:
        s: a 'bytes' containing the MessagePack serialized bytes.

    Returns:
        A deserialized Python object.

    Raises:
        TypeError:
            Packed data is not type 'bytes'.
        InsufficientDataException(UnpackException):
            Insufficient data to unpack the encoded object.
        InvalidStringException(UnpackException):
            Invalid UTF-8 string encountered during unpacking.
        ReservedCodeException(UnpackException):
            Reserved code encountered during unpacking.
        UnhashableKeyException(UnpackException):
            Unhashable key encountered during map unpacking.
            The serialized map cannot be deserialized into a Python dictionary.
        DuplicateKeyException(UnpackException):
            Duplicate key encountered during map unpacking.

    Example:
    >>> umsgpack.unpackb(b'\x82\xa7compact\xc3\xa6schema\x00')
    {'compact': True, 'schema': 0}
    >>>
    """
    if not isinstance(s, bytes):
        raise TypeError("packed data is not type 'bytes'")
    read_fn = _byte_reader(s)
    return _unpackb(read_fn)

################################################################################
### Module Initialization
################################################################################

def __init():
    global packb
    global unpackb
    global dumps
    global loads
    global compatibility
    global _pack
    global _float_size
    global _unpack_dispatch_table

    # Compatibility mode for handling strings/bytes with the old specification
    compatibility = False

    # Auto-detect system float precision
    if sys.float_info.mant_dig == 53:
        _float_size = 64
    else:
        _float_size = 32

    # Map packb and unpackb to the appropriate version
    if sys.version_info[0] == 3:
        _pack = _pack3
        packb = _packb3
        dumps = _packb3
        unpackb = _unpackb3
        loads = _unpackb3
    else:
        _pack = _pack2
        packb = _packb2
        dumps = _packb2
        unpackb = _unpackb2
        loads = _unpackb2

    # Build a dispatch table for fast lookup of unpacking function

    _unpack_dispatch_table = {}
    # Fix uint
    for code in range(0, 0x7f+1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_integer
    # Fix map
    for code in range(0x80, 0x8f+1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_map
    # Fix array
    for code in range(0x90, 0x9f+1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_array
    # Fix str
    for code in range(0xa0, 0xbf+1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_string
    # Nil
    _unpack_dispatch_table[b'\xc0'] = _unpack_nil
    # Reserved
    _unpack_dispatch_table[b'\xc1'] = _unpack_reserved
    # Boolean
    _unpack_dispatch_table[b'\xc2'] = _unpack_boolean
    _unpack_dispatch_table[b'\xc3'] = _unpack_boolean
    # Bin
    for code in range(0xc4, 0xc6+1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_binary
    # Ext
    for code in range(0xc7, 0xc9+1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_ext
    # Float
    _unpack_dispatch_table[b'\xca'] = _unpack_float
    _unpack_dispatch_table[b'\xcb'] = _unpack_float
    # Uint
    for code in range(0xcc, 0xcf+1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_integer
    # Int
    for code in range(0xd0, 0xd3+1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_integer
    # Fixext
    for code in range(0xd4, 0xd8+1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_ext
    # String
    for code in range(0xd9, 0xdb+1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_string
    # Array
    _unpack_dispatch_table[b'\xdc'] = _unpack_array
    _unpack_dispatch_table[b'\xdd'] = _unpack_array
    # Map
    _unpack_dispatch_table[b'\xde'] = _unpack_map
    _unpack_dispatch_table[b'\xdf'] = _unpack_map
    # Negative fixint
    for code in range(0xe0, 0xff+1):
        _unpack_dispatch_table[struct.pack("B", code)] = _unpack_integer

__init()
