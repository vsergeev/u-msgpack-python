import struct
import sys

# Auto-detect system float precision

if sys.float_info.mant_dig == 53:
    float_size = 64
else:
    float_size = 32

################################################################################

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

# Exceptions

class PackException(Exception): pass
class UnpackException(Exception): pass

# Object type not supported for packing
class UnsupportedTypeException(PackException): pass

# Insufficient data to unpack object
class InsufficientDataException(UnpackException): pass
# Non-hashable key encountered during unpacking a map
class KeyNotPrimitiveException(UnpackException): pass
# Duplicate key encountered during unpacking a map
class KeyDuplicateException(UnpackException): pass

################################################################################

def pack_int(x):
    if x < 0:
        if x >= -32:
            return chr(x & 0xff)
        elif x >= -2**(8-1):
            return "\xd0" + chr(x & 0xff)
        elif x >= -2**(16-1):
            return "\xd1" + struct.pack(">h", x)
        elif x >= -2**(32-1):
            return "\xd2" + struct.pack(">i", x)
        elif x >= -2**(64-1):
            return "\xd3" + struct.pack(">q", x)
        else:
            raise UnsupportedTypeException("huge signed int")
    else:
        if x <= 127:
            return chr(x)
        elif x <= 2**8-1:
            return "\xcc" + chr(x)
        elif x <= 2**16-1:
            return "\xcd" + struct.pack(">H", x)
        elif x <= 2**32-1:
            return "\xce" + struct.pack(">I", x)
        elif x <= 2**64-1:
            return "\xcf" + struct.pack(">Q", x)
        else:
            raise UnsupportedTypeException("huge unsigned int")

def pack_nil(x):
    return "\xc0"

def pack_boolean(x):
    return "\xc3" if x else "\xc2"

def pack_float(x):
    if float_size == 64:
        return "\xcb" + struct.pack(">d", x)
    else:
        return "\xca" + struct.pack(">f", x)

def pack_string(x):
    x = str(x)

    if len(x) <= 31:
        return chr(0xa0 | len(x)) + x
    elif len(x) <= 2**8-1:
        return "\xd9" + chr(len(x)) + x
    elif len(x) <= 2**16-1:
        return "\xda" + struct.pack(">H", len(x)) + x
    elif len(x) <= 2**32-1:
        return "\xdb" + struct.pack(">I", len(x)) + x
    else:
        raise UnsupportedTypeException("huge string")

def pack_binary(x):
    if len(x) <= 2**8-1:
        return "\xc4" + chr(len(x)) + x
    elif len(x) <= 2**16-1:
        return "\xc5" + struct.pack(">H", len(x)) + x
    elif len(x) <= 2**32-1:
        return "\xc6" + struct.pack(">I", len(x)) + x
    else:
        raise UnsupportedTypeException("huge binary string")

def pack_ext(x):
    if len(x.data) == 1:
        return "\xd4" + chr(x.ext_type & 0xff) + x.data
    elif len(x.data) == 2:
        return "\xd5" + chr(x.ext_type & 0xff) + x.data
    elif len(x.data) == 4:
        return "\xd6" + chr(x.ext_type & 0xff) + x.data
    elif len(x.data) == 8:
        return "\xd7" + chr(x.ext_type & 0xff) + x.data
    elif len(x.data) == 16:
        return "\xd8" + chr(x.ext_type & 0xff) + x.data
    elif len(x.data) <= 2**8-1:
        return "\xc7" + chr(len(x.data)) + chr(x.ext_type & 0xff) + x.data
    elif len(x.data) <= 2**16-1:
        return "\xc8" + struct.pack(">H", len(x.data)) + chr(x.ext_type & 0xff) + x.data
    elif len(x.data) <= 2**32-1:
        return "\xc9" + struct.pack(">I", len(x.data)) + chr(x.ext_type & 0xff) + x.data
    else:
        raise UnsupportedTypeException("huge ext data")

def pack_array(x):
    if len(x) <= 15:
        s = chr(0x90 | len(x))
    elif len(x) <= 2**16-1:
        s = "\xdc" + struct.pack(">H", len(x))
    elif len(x) <= 2**32-1:
        s = "\xdd" + struct.pack(">I", len(x))
    else:
        raise UnsupportedTypeException("huge array")

    for e in x:
        s += packb(e)

    return s

def pack_map(x):
    if len(x) <= 15:
        s = chr(0x80 | len(x))
    elif len(x) <= 2**16-1:
        s = "\xde" + struct.pack(">H", len(x))
    elif len(x) <= 2**32-1:
        s = "\xdf" + struct.pack(">I", len(x))
    else:
        raise UnsupportedTypeException("huge array")

    for k,v in x.iteritems():
        s += packb(k)
        s += packb(v)

    return s

def packb(x):
    if x is None:
        return pack_nil(x)
    elif isinstance(x, bool):
        return pack_boolean(x)
    elif isinstance(x, int) or isinstance(x, long):
        return pack_int(x)
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
        raise UnsupportedTypeException("type %s not supported by msgpack" % str(type(x)))

################################################################################


