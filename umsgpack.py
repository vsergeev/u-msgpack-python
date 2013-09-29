# umsgpack-python v1.0 - vsergeev at gmail
#
# umsgpack-python is a Python 2 and 3 implementation of msgpack,
# fully compliant with the latest msgpack spec as of 09/29/2013.
#

import struct
import collections
import sys

################################################################################

# Extension type for application code
class Ext:
    def __init__(self, ext_type, data):
        self.ext_type = ext_type
        self.data = data
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.ext_type == other.ext_type and
                self.data == other.data)
    def __ne__(self, other):
        return not self.__eq__(other)

################################################################################

# Base Exception classes
class PackException(Exception): pass
class UnpackException(Exception): pass

# Packing error: Object type not supported for packing
class UnsupportedTypeException(PackException): pass

# Unpacking error: Insufficient data to unpack object
class InsufficientDataException(UnpackException): pass
# Unpacking error: Reserved code encountered
class ReservedCodeException(UnpackException): pass
# Unpacking error: Non-hashable key encountered during map unpacking
class KeyNotPrimitiveException(UnpackException): pass
# Unpacking error: Duplicate key encountered during map unpacking
class KeyDuplicateException(UnpackException): pass
# Unpacking error: Invalid string (not UTF-8)
class InvalidStringException(UnpackException): pass

################################################################################

def pack_integer(x):
    if x < 0:
        if x >= -32:
            return struct.pack("b", x)
        elif x >= -2**(8-1):
            return b"\xd0" + struct.pack("b", x)
        elif x >= -2**(16-1):
            return b"\xd1" + struct.pack(">h", x)
        elif x >= -2**(32-1):
            return b"\xd2" + struct.pack(">i", x)
        elif x >= -2**(64-1):
            return b"\xd3" + struct.pack(">q", x)
        else:
            raise UnsupportedTypeException("huge signed int")
    else:
        if x <= 127:
            return struct.pack("B", x)
        elif x <= 2**8-1:
            return b"\xcc" + struct.pack("B", x)
        elif x <= 2**16-1:
            return b"\xcd" + struct.pack(">H", x)
        elif x <= 2**32-1:
            return b"\xce" + struct.pack(">I", x)
        elif x <= 2**64-1:
            return b"\xcf" + struct.pack(">Q", x)
        else:
            raise UnsupportedTypeException("huge unsigned int")

def pack_nil(x):
    return b"\xc0"

def pack_boolean(x):
    return b"\xc3" if x else b"\xc2"

def pack_float(x):
    if float_size == 64:
        return b"\xcb" + struct.pack(">d", x)
    else:
        return b"\xca" + struct.pack(">f", x)

def pack_string(x):
    x = str(x)

    if len(x) <= 31:
        return struct.pack("B", 0xa0 | len(x)) + x.encode('utf-8')
    elif len(x) <= 2**8-1:
        return b"\xd9" + struct.pack("B", len(x)) + x.encode('utf-8')
    elif len(x) <= 2**16-1:
        return b"\xda" + struct.pack(">H", len(x)) + x.encode('utf-8')
    elif len(x) <= 2**32-1:
        return b"\xdb" + struct.pack(">I", len(x)) + x.encode('utf-8')
    else:
        raise UnsupportedTypeException("huge string")

def pack_binary(x):
    if len(x) <= 2**8-1:
        return b"\xc4" + struct.pack("B", len(x)) + x
    elif len(x) <= 2**16-1:
        return b"\xc5" + struct.pack(">H", len(x)) + x
    elif len(x) <= 2**32-1:
        return b"\xc6" + struct.pack(">I", len(x)) + x
    else:
        raise UnsupportedTypeException("huge binary string")

def pack_ext(x):
    if len(x.data) == 1:
        return b"\xd4" + struct.pack("B", x.ext_type & 0xff) + x.data
    elif len(x.data) == 2:
        return b"\xd5" + struct.pack("B", x.ext_type & 0xff) + x.data
    elif len(x.data) == 4:
        return b"\xd6" + struct.pack("B", x.ext_type & 0xff) + x.data
    elif len(x.data) == 8:
        return b"\xd7" + struct.pack("B", x.ext_type & 0xff) + x.data
    elif len(x.data) == 16:
        return b"\xd8" + struct.pack("B", x.ext_type & 0xff) + x.data
    elif len(x.data) <= 2**8-1:
        return b"\xc7" + struct.pack("BB", len(x.data), x.ext_type & 0xff) + x.data
    elif len(x.data) <= 2**16-1:
        return b"\xc8" + struct.pack(">HB", len(x.data), x.ext_type & 0xff) + x.data
    elif len(x.data) <= 2**32-1:
        return b"\xc9" + struct.pack(">IB", len(x.data), x.ext_type & 0xff) + x.data
    else:
        raise UnsupportedTypeException("huge ext data")

def pack_array(x):
    if len(x) <= 15:
        s = struct.pack("B", 0x90 | len(x))
    elif len(x) <= 2**16-1:
        s = b"\xdc" + struct.pack(">H", len(x))
    elif len(x) <= 2**32-1:
        s = b"\xdd" + struct.pack(">I", len(x))
    else:
        raise UnsupportedTypeException("huge array")

    for e in x:
        s += packb(e)

    return s

def pack_map(x):
    if len(x) <= 15:
        s = struct.pack("B", 0x80 | len(x))
    elif len(x) <= 2**16-1:
        s = b"\xde" + struct.pack(">H", len(x))
    elif len(x) <= 2**32-1:
        s = b"\xdf" + struct.pack(">I", len(x))
    else:
        raise UnsupportedTypeException("huge array")

    for k,v in x.items():
        s += packb(k)
        s += packb(v)

    return s

########################################

# Pack for Python 2, with basestring type, and long type
def packb2(x):
    if x is None:
        return pack_nil(x)
    elif isinstance(x, bool):
        return pack_boolean(x)
    elif isinstance(x, int) or isinstance(x, long):
        return pack_integer(x)
    elif isinstance(x, float):
        return pack_float(x)
    elif isinstance(x, basestring):
        try:
            return pack_string(x.decode('utf-8'))
        except UnicodeError:
            return pack_binary(x)
    elif isinstance(x, list) or isinstance(x, tuple):
        return pack_array(x)
    elif isinstance(x, dict):
        return pack_map(x)
    elif isinstance(x, Ext):
        return pack_ext(x)
    else:
        raise UnsupportedTypeException("unsupported type: %s" % str(type(x)))

# Pack for Python 3, with unicode string type, bytes type, and no long type
def packb3(x):
    if x is None:
        return pack_nil(x)
    elif isinstance(x, bool):
        return pack_boolean(x)
    elif isinstance(x, int):
        return pack_integer(x)
    elif isinstance(x, float):
        return pack_float(x)
    elif isinstance(x, str):
        return pack_string(x)
    elif isinstance(x, bytes):
        return pack_binary(x)
    elif isinstance(x, list) or isinstance(x, tuple):
        return pack_array(x)
    elif isinstance(x, dict):
        return pack_map(x)
    elif isinstance(x, Ext):
        return pack_ext(x)
    else:
        raise UnsupportedTypeException("unsupported type: %s" % str(type(x)))

# Note: initialization code below

# Auto-detect system float precision
if sys.float_info.mant_dig == 53:
    float_size = 64
else:
    float_size = 32
# Map packb to the appropriate version
packb = packb3 if sys.version > '3' else packb2

################################################################################

def unpack_integer(code, read_fn):
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
    raise Exception("logic error, not int: %s" % code)

def unpack_reserved(code, read_fn):
    if code == b'\xc1':
        raise ReservedCodeException("reserved code encountered: 0x%02x" % ord(code))
    raise Exception("logic error, not reserved code: 0x%02x" % ord(code))

def unpack_nil(code, read_fn):
    if code == b'\xc0':
        return None
    raise Exception("logic error, not nil: 0x%02x" % ord(code))

def unpack_boolean(code, read_fn):
    if code == b'\xc2':
        return False
    elif code == b'\xc3':
        return True
    raise Exception("logic error, not boolean: 0x%02x" % ord(code))

def unpack_float(code, read_fn):
    if code == b'\xca':
        return struct.unpack(">f", read_fn(4))[0]
    elif code == b'\xcb':
        return struct.unpack(">d", read_fn(8))[0]
    raise Exception("logic error, not float: 0x%02x" % ord(code))

def unpack_string(code, read_fn):
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

    try:
        return bytes.decode(read_fn(length), 'utf-8')
    except UnicodeDecodeError:
        raise InvalidStringException("unpacked string is not utf-8")

def unpack_binary(code, read_fn):
    if code == b'\xc4':
        length = struct.unpack("B", read_fn(1))[0]
    elif code == b'\xc5':
        length = struct.unpack(">H", read_fn(2))[0]
    elif code == b'\xc6':
        length = struct.unpack(">I", read_fn(4))[0]
    else:
        raise Exception("logic error, not binary: 0x%02x" % ord(code))

    return read_fn(length)

def unpack_ext(code, read_fn):
    if code == b'\xd4':
        return Ext(ord(read_fn(1)), read_fn(1))
    elif code == b'\xd5':
        return Ext(ord(read_fn(1)), read_fn(2))
    elif code == b'\xd6':
        return Ext(ord(read_fn(1)), read_fn(4))
    elif code == b'\xd7':
        return Ext(ord(read_fn(1)), read_fn(8))
    elif code == b'\xd8':
        return Ext(ord(read_fn(1)), read_fn(16))
    elif code == b'\xc7':
        length = struct.unpack("B", read_fn(1))[0]
        return Ext(ord(read_fn(1)), read_fn(length))
    elif code == b'\xc8':
        length = struct.unpack(">H", read_fn(2))[0]
        return Ext(ord(read_fn(1)), read_fn(length))
    elif code == b'\xc9':
        length = struct.unpack(">I", read_fn(4))[0]
        return Ext(ord(read_fn(1)), read_fn(length))
    raise Exception("logic error, not ext: 0x%02x" % ord(code))

def unpack_array(code, read_fn):
    if (ord(code) & 0xf0) == 0x90:
        length = (ord(code) & ~0xf0)
    elif code == b'\xdc':
        length = struct.unpack(">H", read_fn(2))[0]
    elif code == b'\xdd':
        length = struct.unpack(">I", read_fn(4))[0]
    else:
        raise Exception("logic error, not array: 0x%02x" % ord(code))

    return [_unpackb(read_fn) for i in range(length)]

def unpack_map(code, read_fn):
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
        k = _unpackb(read_fn)
        if not isinstance(k, collections.Hashable):
            raise KeyNotPrimitiveException("encountered non-primitive key type: %s" % str(type(k)))
        if k in d:
            raise KeyDuplicateException("encountered duplicate key: %s" % str(k))
        v = _unpackb(read_fn)

        d[k] = v
    return d

########################################

def string_reader(s):
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
    return unpack_dispatch_table[code](code, read_fn)

# Wrapper unpack function that builds a read stream function from s
def unpackb(s):
    read_fn = string_reader(s)
    return _unpackb(read_fn)

########################################

# Note: initialization code below

# Build a dispatch table for fast lookup of unpacking function

unpack_dispatch_table = {}
# Fix uint
for code in range(0, 0x7f+1):
    unpack_dispatch_table[struct.pack("B", code)] = unpack_integer
# Fix map
for code in range(0x80, 0x8f+1):
    unpack_dispatch_table[struct.pack("B", code)] = unpack_map
# Fix array
for code in range(0x90, 0x9f+1):
    unpack_dispatch_table[struct.pack("B", code)] = unpack_array
# Fix str
for code in range(0xa0, 0xbf+1):
    unpack_dispatch_table[struct.pack("B", code)] = unpack_string
# Nil
unpack_dispatch_table[b'\xc0'] = unpack_nil
# Reserved
unpack_dispatch_table[b'\xc1'] = unpack_reserved
# Boolean
unpack_dispatch_table[b'\xc2'] = unpack_boolean
unpack_dispatch_table[b'\xc3'] = unpack_boolean
# Bin
for code in range(0xc4, 0xc6+1):
    unpack_dispatch_table[struct.pack("B", code)] = unpack_binary
# Ext
for code in range(0xc7, 0xc9+1):
    unpack_dispatch_table[struct.pack("B", code)] = unpack_ext
# Float
unpack_dispatch_table[b'\xca'] = unpack_float
unpack_dispatch_table[b'\xcb'] = unpack_float
# Uint
for code in range(0xcc, 0xcf+1):
    unpack_dispatch_table[struct.pack("B", code)] = unpack_integer
# Int
for code in range(0xd0, 0xd3+1):
    unpack_dispatch_table[struct.pack("B", code)] = unpack_integer
# Fixext
for code in range(0xd4, 0xd8+1):
    unpack_dispatch_table[struct.pack("B", code)] = unpack_ext
# String
for code in range(0xd9, 0xdb+1):
    unpack_dispatch_table[struct.pack("B", code)] = unpack_string
# Array
unpack_dispatch_table[b'\xdc'] = unpack_array
unpack_dispatch_table[b'\xdd'] = unpack_array
# Map
unpack_dispatch_table[b'\xde'] = unpack_map
unpack_dispatch_table[b'\xdf'] = unpack_map
# Negative fixint
for code in range(0xe0, 0xff+1):
    unpack_dispatch_table[struct.pack("B", code)] = unpack_integer

################################################################################

def validate_integer(code, read_fn):
    if (ord(code) & 0xe0) == 0xe0 or (ord(code) & 0x80) == 0x00:
        pass
    elif code == b'\xd0' or code == b'\xcc':
        read_fn(1)
    elif code == b'\xd1' or code == b'\xcd':
        read_fn(2)
    elif code == b'\xd2' or code == b'\xce':
        read_fn(4)
    elif code == b'\xd3' or code == b'\xcf':
        read_fn(8)
    else:
        raise Exception("logic error, not int: %s" % code)
    return True

def validate_reserved(code, read_fn):
    if code == b'\xc1':
        raise ReservedCodeException("reserved code encountered: 0x%02x" % ord(code))
    raise Exception("logic error, not reserved code: 0x%02x" % ord(code))

def validate_nil(code, read_fn):
    if code == b'\xc0':
        pass
    else:
        raise Exception("logic error, not nil: 0x%02x" % ord(code))
    return True

def validate_boolean(code, read_fn):
    if code == b'\xc2' or code == b'\xc3':
        pass
    else:
        raise Exception("logic error, not boolean: 0x%02x" % ord(code))
    return True

def validate_float(code, read_fn):
    if code == b'\xca':
        read_fn(4)
    elif code == b'\xcb':
        read_fn(8)
    else:
        raise Exception("logic error, not float: 0x%02x" % ord(code))
    return True

def validate_string(code, read_fn):
    if (ord(code) & 0xe0) == 0xa0:
        read_fn(ord(code) & ~0xe0)
    elif code == b'\xd9':
        length = struct.unpack("B", read_fn(1))[0]
        read_fn(length)
    elif code == b'\xda':
        length = struct.unpack(">H", read_fn(2))[0]
        read_fn(length)
    elif code == b'\xdb':
        length = struct.unpack(">I", read_fn(4))[0]
        read_fn(length)
    else:
        raise Exception("logic error, not string: 0x%02x" % ord(code))
    return True

def validate_binary(code, read_fn):
    if code == b'\xc4':
        length = struct.unpack("B", read_fn(1))[0]
        read_fn(length)
    elif code == b'\xc5':
        length = struct.unpack(">H", read_fn(2))[0]
        read_fn(length)
    elif code == b'\xc6':
        length = struct.unpack(">I", read_fn(4))[0]
        read_fn(length)
    else:
        raise Exception("logic error, not binary: 0x%02x" % ord(code))
    return True

def validate_ext(code, read_fn):
    if code == b'\xd4':
        read_fn(1+1)
    elif code == b'\xd5':
        read_fn(1+2)
    elif code == b'\xd6':
        read_fn(1+4)
    elif code == b'\xd7':
        read_fn(1+8)
    elif code == b'\xd8':
        read_fn(1+16)
    elif code == b'\xc7':
        length = struct.unpack("B", read_fn(1))[0]
        read_fn(1+length)
    elif code == b'\xc8':
        length = struct.unpack(">H", read_fn(2))[0]
        read_fn(1+length)
    elif code == b'\xc9':
        length = struct.unpack(">I", read_fn(4))[0]
        read_fn(1+length)
    else:
        raise Exception("logic error, not ext: 0x%02x" % ord(code))
    return True

def validate_array(code, read_fn):
    if (ord(code) & 0xf0) == 0x90:
        length = (ord(code) & ~0xf0)
    elif code == b'\xdc':
        length = struct.unpack(">H", read_fn(2))[0]
    elif code == b'\xdd':
        length = struct.unpack(">I", read_fn(4))[0]
    else:
        raise Exception("logic error, not array: 0x%02x" % ord(code))

    for i in range(length):
        if _validate(read_fn) != True:
            return False

    return True

def validate_map(code, read_fn):
    if (ord(code) & 0xf0) == 0x80:
        length = (ord(code) & ~0xf0)
    elif code == b'\xde':
        length = struct.unpack(">H", read_fn(2))[0]
    elif code == b'\xdf':
        length = struct.unpack(">I", read_fn(4))[0]
    else:
        raise Exception("logic error, not map: 0x%02x" % ord(code))

    for i in range(length):
        if _validate(read_fn) != True:
            return False
        if _validate(read_fn) != True:
            return False

    return True

########################################

def _validate(read_fn):
    try:
        code = read_fn(1)
        return validate_dispatch_table[code](code, read_fn)
    except InsufficientDataException:
        return False

# Wrapper validate function that builds a read stream function with s
def validate(s):
    read_fn = string_reader(s)
    return _validate(read_fn)

########################################

# Note: initialization code below

# Build the validate dispatch table based on the unpack one

validate_dispatch_table = {}
validate_dispatch_substitutions = {
    unpack_integer : validate_integer,
    unpack_reserved : validate_reserved,
    unpack_nil : validate_nil,
    unpack_boolean : validate_boolean,
    unpack_float : validate_float,
    unpack_string : validate_string,
    unpack_binary : validate_binary,
    unpack_ext : validate_ext,
    unpack_array : validate_array,
    unpack_map : validate_map,
}
for k,v in unpack_dispatch_table.items():
    validate_dispatch_table[k] = validate_dispatch_substitutions[v]

################################################################################

